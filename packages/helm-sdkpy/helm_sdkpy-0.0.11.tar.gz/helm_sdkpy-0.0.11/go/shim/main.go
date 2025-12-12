// Copyright 2025 Vantage Compute
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

/*
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned long long helm_sdkpy_handle;
*/
import "C"

import (
	"encoding/json"
	"fmt"
	"os"
	"sync"
	"sync/atomic"
	"unsafe"

	"time"

	"helm.sh/helm/v4/pkg/action"
	"helm.sh/helm/v4/pkg/chart/v2/loader"
	"helm.sh/helm/v4/pkg/cli"
	"helm.sh/helm/v4/pkg/getter"
	"helm.sh/helm/v4/pkg/kube"
	"helm.sh/helm/v4/pkg/registry"
	"helm.sh/helm/v4/pkg/repo/v1"
)

// Configuration state
type configState struct {
	cfg  *action.Configuration
	envs *cli.EnvSettings
	mu   sync.Mutex
}

var (
	handleSeq atomic.Uint64
	configs   sync.Map

	errMu          sync.Mutex
	lastErr        string
	versionCString *C.char
)

func init() {
	versionCString = C.CString("helm-sdkpy-v0.0.1")
}

func setError(err error) C.int {
	errMu.Lock()
	defer errMu.Unlock()
	if err != nil {
		lastErr = err.Error()
		return -1
	}
	lastErr = ""
	return 0
}

func recordErrorf(format string, args ...any) C.int {
	return setError(fmt.Errorf(format, args...))
}

func nextHandle() C.helm_sdkpy_handle {
	return C.helm_sdkpy_handle(handleSeq.Add(1))
}

//export helm_sdkpy_last_error
func helm_sdkpy_last_error() *C.char {
	errMu.Lock()
	defer errMu.Unlock()
	if lastErr == "" {
		return nil
	}
	return C.CString(lastErr)
}

//export helm_sdkpy_free
func helm_sdkpy_free(ptr unsafe.Pointer) {
	C.free(ptr)
}

//export helm_sdkpy_version_string
func helm_sdkpy_version_string() *C.char {
	return versionCString
}

//export helm_sdkpy_version_number
func helm_sdkpy_version_number() C.int {
	return 1 // Version 0.0.1
}

// Configuration management

//export helm_sdkpy_config_create
func helm_sdkpy_config_create(namespace *C.char, kubeconfig *C.char, kubecontext *C.char, handle_out *C.helm_sdkpy_handle) C.int {
	ns := C.GoString(namespace)
	kc := C.GoString(kubeconfig)
	kctx := C.GoString(kubecontext)

	// Create environment settings
	envs := cli.New()
	if ns != "" {
		envs.SetNamespace(ns)
	}
	if kc != "" {
		envs.KubeConfig = kc
	}
	if kctx != "" {
		envs.KubeContext = kctx
	}

	// Create action configuration
	cfg := new(action.Configuration)

	// Initialize the configuration with Kubernetes settings
	err := cfg.Init(envs.RESTClientGetter(), envs.Namespace(), os.Getenv("HELM_DRIVER"))
	if err != nil {
		return setError(fmt.Errorf("failed to initialize helm config: %w", err))
	}
	
	// Configure the Kubernetes client to use Ignore field validation
	// This allows charts with managedFields in templates (like rook-ceph v1.18.x)
	// to install successfully without strict Kubernetes API validation errors
	if cfg.KubeClient != nil {
		// Note: In Helm v4, field validation is handled via client options during Create/Update
		// We'll configure this in the Install action instead
	}

	// Initialize registry client for OCI operations
	registryClient, err := registry.NewClient(
		registry.ClientOptDebug(false),
		registry.ClientOptEnableCache(true),
		registry.ClientOptWriter(os.Stdout),
		registry.ClientOptCredentialsFile(envs.RegistryConfig),
	)
	if err != nil {
		return setError(fmt.Errorf("failed to initialize registry client: %w", err))
	}
	cfg.RegistryClient = registryClient

	state := &configState{
		cfg:  cfg,
		envs: envs,
	}

	handle := nextHandle()
	configs.Store(handle, state)
	*handle_out = handle

	return 0
}

//export helm_sdkpy_config_destroy
func helm_sdkpy_config_destroy(handle C.helm_sdkpy_handle) {
	configs.Delete(handle)
}

func getConfig(handle C.helm_sdkpy_handle) (*configState, error) {
	val, ok := configs.Load(handle)
	if !ok {
		return nil, fmt.Errorf("invalid configuration handle")
	}
	return val.(*configState), nil
}

// Install action

//export helm_sdkpy_install
func helm_sdkpy_install(handle C.helm_sdkpy_handle, release_name *C.char, chart_path *C.char, values_json *C.char, version *C.char, create_namespace C.int, wait C.int, timeout_seconds C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)
	chartPath := C.GoString(chart_path)
	valuesJSON := C.GoString(values_json)
	chartVersion := C.GoString(version)

	// Create install action
	client := action.NewInstall(state.cfg)
	client.ReleaseName = releaseName
	client.Namespace = state.envs.Namespace()
	client.CreateNamespace = create_namespace != 0
	
	// Use client-side apply instead of server-side to avoid strict field validation
	// Server-side apply (default in Helm v4) enforces strict field validation which
	// rejects charts with managedFields in templates (like rook-ceph v1.18.x)
	client.ServerSideApply = false
	
	// Disable OpenAPI validation as well
	client.DisableOpenAPIValidation = true
	
	// Set version if provided
	if chartVersion != "" {
		client.Version = chartVersion
	}
	
	// Configure wait behavior
	if wait != 0 {
		client.WaitStrategy = kube.StatusWatcherStrategy // Use the status watcher strategy
		if timeout_seconds > 0 {
			client.Timeout = time.Duration(timeout_seconds) * time.Second
		} else {
			client.Timeout = 5 * time.Minute // Default timeout
		}
	} else {
		client.WaitStrategy = kube.HookOnlyStrategy // Only wait for hooks by default
	}

	// Locate and load the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Load the chart from the located path
	chart, err := loader.Load(cp)
	if err != nil {
		return setError(fmt.Errorf("failed to load chart: %w", err))
	}

	// Parse values
	var values map[string]interface{}
	if valuesJSON != "" {
		if err := json.Unmarshal([]byte(valuesJSON), &values); err != nil {
			return setError(fmt.Errorf("failed to parse values JSON: %w", err))
		}
	}

	// Run the install
	rel, err := client.Run(chart, values)
	if err != nil {
		return setError(fmt.Errorf("install failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Upgrade action

//export helm_sdkpy_upgrade
func helm_sdkpy_upgrade(handle C.helm_sdkpy_handle, release_name *C.char, chart_path *C.char, values_json *C.char, version *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)
	chartPath := C.GoString(chart_path)
	valuesJSON := C.GoString(values_json)
	chartVersion := C.GoString(version)

	// Create upgrade action
	client := action.NewUpgrade(state.cfg)
	client.Namespace = state.envs.Namespace()
	
	// Set version if provided
	if chartVersion != "" {
		client.Version = chartVersion
	}

	// Locate and load the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Load the chart from the located path
	chart, err := loader.Load(cp)
	if err != nil {
		return setError(fmt.Errorf("failed to load chart: %w", err))
	}

	// Parse values
	var values map[string]interface{}
	if valuesJSON != "" {
		if err := json.Unmarshal([]byte(valuesJSON), &values); err != nil {
			return setError(fmt.Errorf("failed to parse values JSON: %w", err))
		}
	}

	// Run the upgrade
	rel, err := client.Run(releaseName, chart, values)
	if err != nil {
		return setError(fmt.Errorf("upgrade failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Uninstall action

//export helm_sdkpy_uninstall
func helm_sdkpy_uninstall(handle C.helm_sdkpy_handle, release_name *C.char, wait C.int, timeout_seconds C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create uninstall action
	client := action.NewUninstall(state.cfg)
	
	// Configure wait behavior
	if wait != 0 {
		client.WaitStrategy = kube.StatusWatcherStrategy // Use the status watcher strategy
		if timeout_seconds > 0 {
			client.Timeout = time.Duration(timeout_seconds) * time.Second
		} else {
			client.Timeout = 5 * time.Minute // Default timeout
		}
	} else {
		client.WaitStrategy = kube.HookOnlyStrategy // Only wait for hooks by default
	}

	// Run the uninstall
	resp, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("uninstall failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(resp)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// List action

//export helm_sdkpy_list
func helm_sdkpy_list(handle C.helm_sdkpy_handle, all C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	// Create list action
	client := action.NewList(state.cfg)
	if all != 0 {
		client.All = true
	}

	// Run the list
	releases, err := client.Run()
	if err != nil {
		return setError(fmt.Errorf("list failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(releases)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Get/Status action

//export helm_sdkpy_status
func helm_sdkpy_status(handle C.helm_sdkpy_handle, release_name *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create status action
	client := action.NewStatus(state.cfg)

	// Run the status
	rel, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("status failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Rollback action

//export helm_sdkpy_rollback
func helm_sdkpy_rollback(handle C.helm_sdkpy_handle, release_name *C.char, revision C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create rollback action
	client := action.NewRollback(state.cfg)
	client.Version = int(revision)

	// Run the rollback
	err = client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("rollback failed: %w", err))
	}

	// Return success message
	result := map[string]string{"status": "success"}
	resultData, err := json.Marshal(result)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Get values action

//export helm_sdkpy_get_values
func helm_sdkpy_get_values(handle C.helm_sdkpy_handle, release_name *C.char, all_values C.int, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create get values action
	client := action.NewGetValues(state.cfg)
	if all_values != 0 {
		client.AllValues = true
	}

	// Run the get values
	values, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("get values failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(values)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// History action

//export helm_sdkpy_history
func helm_sdkpy_history(handle C.helm_sdkpy_handle, release_name *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create history action
	client := action.NewHistory(state.cfg)

	// Run the history
	releases, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("history failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(releases)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Pull action

//export helm_sdkpy_pull
func helm_sdkpy_pull(handle C.helm_sdkpy_handle, chart_ref *C.char, dest_dir *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartRef := C.GoString(chart_ref)
	destDir := C.GoString(dest_dir)

	// Create pull action
	client := action.NewPull()
	client.Settings = state.envs
	if destDir != "" {
		client.DestDir = destDir
	}

	// Run the pull
	_, err = client.Run(chartRef)
	if err != nil {
		return setError(fmt.Errorf("pull failed: %w", err))
	}

	return 0
}

// Show chart action

//export helm_sdkpy_show_chart
func helm_sdkpy_show_chart(handle C.helm_sdkpy_handle, chart_path *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)

	// Create show action
	client := action.NewShow(action.ShowChart, state.cfg)

	// Locate the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Run the show
	output, err := client.Run(cp)
	if err != nil {
		return setError(fmt.Errorf("show chart failed: %w", err))
	}

	*result_json = C.CString(output)
	return 0
}

// Show values action

//export helm_sdkpy_show_values
func helm_sdkpy_show_values(handle C.helm_sdkpy_handle, chart_path *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)

	// Create show action
	client := action.NewShow(action.ShowValues, state.cfg)

	// Locate the chart (supports local, OCI, and HTTP)
	cp, err := client.ChartPathOptions.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Run the show
	output, err := client.Run(cp)
	if err != nil {
		return setError(fmt.Errorf("show values failed: %w", err))
	}

	*result_json = C.CString(output)
	return 0
}

// Test action

//export helm_sdkpy_test
func helm_sdkpy_test(handle C.helm_sdkpy_handle, release_name *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	releaseName := C.GoString(release_name)

	// Create test action
	client := action.NewReleaseTesting(state.cfg)

	// Run the test
	rel, err := client.Run(releaseName)
	if err != nil {
		return setError(fmt.Errorf("test failed: %w", err))
	}

	// Serialize result
	resultData, err := json.Marshal(rel)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Lint action

//export helm_sdkpy_lint
func helm_sdkpy_lint(handle C.helm_sdkpy_handle, chart_path *C.char, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)

	// For remote charts (OCI/HTTP), we need to locate them first
	// For local charts, LocateChart will just return the path as-is
	var pathOpts action.ChartPathOptions

	cp, err := pathOpts.LocateChart(chartPath, state.envs)
	if err != nil {
		return setError(fmt.Errorf("failed to locate chart: %w", err))
	}

	// Create lint action
	client := action.NewLint()

	// Run the lint
	result := client.Run([]string{cp}, map[string]interface{}{})

	// Serialize result
	resultData, err := json.Marshal(result)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

// Package action

//export helm_sdkpy_package
func helm_sdkpy_package(handle C.helm_sdkpy_handle, chart_path *C.char, dest_dir *C.char, result_path **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartPath := C.GoString(chart_path)
	destDir := C.GoString(dest_dir)

	// Create package action
	client := action.NewPackage()
	if destDir != "" {
		client.Destination = destDir
	}

	// Run the package
	path, err := client.Run(chartPath, nil)
	if err != nil {
		return setError(fmt.Errorf("package failed: %w", err))
	}

	*result_path = C.CString(path)
	return 0
}

// Repository management actions

//export helm_sdkpy_repo_add
func helm_sdkpy_repo_add(handle C.helm_sdkpy_handle, name *C.char, url *C.char, username *C.char, password *C.char, options_json *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	repoName := C.GoString(name)
	repoURL := C.GoString(url)
	userName := C.GoString(username)
	passWord := C.GoString(password)
	optionsJSON := C.GoString(options_json)

	// Parse options if provided
	var options map[string]interface{}
	if optionsJSON != "" {
		if err := json.Unmarshal([]byte(optionsJSON), &options); err != nil {
			return setError(fmt.Errorf("failed to parse options JSON: %w", err))
		}
	}

	// Create repo entry
	entry := &repo.Entry{
		Name:     repoName,
		URL:      repoURL,
		Username: userName,
		Password: passWord,
	}

	// Apply additional options
	if options != nil {
		if v, ok := options["insecure_skip_tls_verify"].(bool); ok {
			entry.InsecureSkipTLSverify = v
		}
		if v, ok := options["pass_credentials_all"].(bool); ok {
			entry.PassCredentialsAll = v
		}
		if v, ok := options["cert_file"].(string); ok {
			entry.CertFile = v
		}
		if v, ok := options["key_file"].(string); ok {
			entry.KeyFile = v
		}
		if v, ok := options["ca_file"].(string); ok {
			entry.CAFile = v
		}
	}

	// Get repository file path
	repoFile := state.envs.RepositoryConfig

	// Load existing repos
	f, err := repo.LoadFile(repoFile)
	if err != nil && !os.IsNotExist(err) {
		return setError(fmt.Errorf("failed to load repository file: %w", err))
	}
	if f == nil {
		f = repo.NewFile()
	}

	// Check if repo already exists
	if f.Has(repoName) {
		return setError(fmt.Errorf("repository %s already exists", repoName))
	}

	// Create chart repository and download index
	r, err := repo.NewChartRepository(entry, getter.All(state.envs))
	if err != nil {
		return setError(fmt.Errorf("failed to create chart repository: %w", err))
	}

	// Set cache path if available
	if state.envs.RepositoryCache != "" {
		r.CachePath = state.envs.RepositoryCache
	}

	// Download the index file
	_, err = r.DownloadIndexFile()
	if err != nil {
		return setError(fmt.Errorf("failed to download index file: %w", err))
	}

	// Add to repo file
	f.Update(entry)

	// Write the repo file
	if err := f.WriteFile(repoFile, 0644); err != nil {
		return setError(fmt.Errorf("failed to write repository file: %w", err))
	}

	return 0
}

//export helm_sdkpy_repo_remove
func helm_sdkpy_repo_remove(handle C.helm_sdkpy_handle, name *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	repoName := C.GoString(name)

	// Get repository file path
	repoFile := state.envs.RepositoryConfig

	// Load existing repos
	f, err := repo.LoadFile(repoFile)
	if err != nil {
		return setError(fmt.Errorf("failed to load repository file: %w", err))
	}

	// Remove the repo
	if !f.Remove(repoName) {
		return setError(fmt.Errorf("no repository named %q found", repoName))
	}

	// Write the repo file
	if err := f.WriteFile(repoFile, 0644); err != nil {
		return setError(fmt.Errorf("failed to write repository file: %w", err))
	}

	return 0
}

//export helm_sdkpy_repo_list
func helm_sdkpy_repo_list(handle C.helm_sdkpy_handle, result_json **C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	// Get repository file path
	repoFile := state.envs.RepositoryConfig

	// Load existing repos
	f, err := repo.LoadFile(repoFile)
	if err != nil && !os.IsNotExist(err) {
		return setError(fmt.Errorf("failed to load repository file: %w", err))
	}
	if f == nil || len(f.Repositories) == 0 {
		*result_json = C.CString("[]")
		return 0
	}

	// Serialize result
	resultData, err := json.Marshal(f.Repositories)
	if err != nil {
		return setError(fmt.Errorf("failed to serialize result: %w", err))
	}

	*result_json = C.CString(string(resultData))
	return 0
}

//export helm_sdkpy_repo_update
func helm_sdkpy_repo_update(handle C.helm_sdkpy_handle, name *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	repoName := C.GoString(name)

	// Get repository file path
	repoFile := state.envs.RepositoryConfig

	// Load existing repos
	f, err := repo.LoadFile(repoFile)
	if err != nil {
		return setError(fmt.Errorf("failed to load repository file: %w", err))
	}

	// Find the repo to update
	var entry *repo.Entry
	if repoName != "" {
		entry = f.Get(repoName)
		if entry == nil {
			return setError(fmt.Errorf("no repository named %q found", repoName))
		}
	}

	// Update the specified repo or all repos
	if repoName != "" {
		// Update single repo
		r, err := repo.NewChartRepository(entry, getter.All(state.envs))
		if err != nil {
			return setError(fmt.Errorf("failed to create chart repository: %w", err))
		}

		if state.envs.RepositoryCache != "" {
			r.CachePath = state.envs.RepositoryCache
		}

		if _, err := r.DownloadIndexFile(); err != nil {
			return setError(fmt.Errorf("failed to update repository %q: %w", repoName, err))
		}
	} else {
		// Update all repos
		for _, entry := range f.Repositories {
			r, err := repo.NewChartRepository(entry, getter.All(state.envs))
			if err != nil {
				return setError(fmt.Errorf("failed to create chart repository %q: %w", entry.Name, err))
			}

			if state.envs.RepositoryCache != "" {
				r.CachePath = state.envs.RepositoryCache
			}

			if _, err := r.DownloadIndexFile(); err != nil {
				return setError(fmt.Errorf("failed to update repository %q: %w", entry.Name, err))
			}
		}
	}

	return 0
}

// Registry login action

//export helm_sdkpy_registry_login
func helm_sdkpy_registry_login(handle C.helm_sdkpy_handle, hostname *C.char, username *C.char, password *C.char, options_json *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	host := C.GoString(hostname)
	user := C.GoString(username)
	pass := C.GoString(password)

	// Parse options
	var options struct {
		CertFile              string `json:"cert_file"`
		KeyFile               string `json:"key_file"`
		CAFile                string `json:"ca_file"`
		Insecure              bool   `json:"insecure"`
		PlainHTTP             bool   `json:"plain_http"`
	}

	optionsStr := C.GoString(options_json)
	if optionsStr != "" {
		if err := json.Unmarshal([]byte(optionsStr), &options); err != nil {
			return setError(fmt.Errorf("failed to parse options: %w", err))
		}
	}

	// Create registry login action
	client := action.NewRegistryLogin(state.cfg)

	// Build options slice
	var loginOpts []action.RegistryLoginOpt
	
	if options.CertFile != "" {
		loginOpts = append(loginOpts, action.WithCertFile(options.CertFile))
	}
	if options.KeyFile != "" {
		loginOpts = append(loginOpts, action.WithKeyFile(options.KeyFile))
	}
	if options.CAFile != "" {
		loginOpts = append(loginOpts, action.WithCAFile(options.CAFile))
	}
	if options.Insecure {
		loginOpts = append(loginOpts, action.WithInsecure(options.Insecure))
	}
	if options.PlainHTTP {
		loginOpts = append(loginOpts, action.WithPlainHTTPLogin(options.PlainHTTP))
	}

	// Run the login
	err = client.Run(os.Stdout, host, user, pass, loginOpts...)
	if err != nil {
		return setError(fmt.Errorf("registry login failed: %w", err))
	}

	return 0
}

// Registry logout action

//export helm_sdkpy_registry_logout
func helm_sdkpy_registry_logout(handle C.helm_sdkpy_handle, hostname *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	host := C.GoString(hostname)

	// Create registry logout action
	client := action.NewRegistryLogout(state.cfg)

	// Run the logout
	err = client.Run(os.Stdout, host)
	if err != nil {
		return setError(fmt.Errorf("registry logout failed: %w", err))
	}

	return 0
}

// Push action (for pushing charts to OCI registries)

//export helm_sdkpy_push
func helm_sdkpy_push(handle C.helm_sdkpy_handle, chart_ref *C.char, remote *C.char, options_json *C.char) C.int {
	state, err := getConfig(handle)
	if err != nil {
		return setError(err)
	}

	state.mu.Lock()
	defer state.mu.Unlock()

	chartRef := C.GoString(chart_ref)
	remoteRef := C.GoString(remote)

	// Parse options
	var options struct {
		CertFile              string `json:"cert_file"`
		KeyFile               string `json:"key_file"`
		CAFile                string `json:"ca_file"`
		InsecureSkipTLSVerify bool   `json:"insecure_skip_tls_verify"`
		PlainHTTP             bool   `json:"plain_http"`
	}

	optionsStr := C.GoString(options_json)
	if optionsStr != "" {
		if err := json.Unmarshal([]byte(optionsStr), &options); err != nil {
			return setError(fmt.Errorf("failed to parse options: %w", err))
		}
	}

	// Create push action
	var pushOpts []action.PushOpt
	pushOpts = append(pushOpts, action.WithPushConfig(state.cfg))
	
	if options.CertFile != "" || options.KeyFile != "" || options.CAFile != "" {
		pushOpts = append(pushOpts, action.WithTLSClientConfig(options.CertFile, options.KeyFile, options.CAFile))
	}
	if options.InsecureSkipTLSVerify {
		pushOpts = append(pushOpts, action.WithInsecureSkipTLSVerify(options.InsecureSkipTLSVerify))
	}
	if options.PlainHTTP {
		pushOpts = append(pushOpts, action.WithPlainHTTP(options.PlainHTTP))
	}

	client := action.NewPushWithOpts(pushOpts...)
	client.Settings = state.envs

	// Run the push
	_, err = client.Run(chartRef, remoteRef)
	if err != nil {
		return setError(fmt.Errorf("push failed: %w", err))
	}

	return 0
}

func main() {
	// Required for CGO shared library
}
