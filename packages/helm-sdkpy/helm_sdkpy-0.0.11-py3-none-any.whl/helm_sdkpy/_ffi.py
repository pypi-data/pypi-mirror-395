# Copyright 2025 Vantage Compute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import os
import platform
import threading
from pathlib import Path
from typing import Any

from cffi import FFI  # type: ignore[import]

from .exceptions import HelmError, HelmLibraryNotFound

ffi: Any = FFI()
ffi.cdef(
    """
    typedef unsigned long long helm_sdkpy_handle;

    // Configuration management
    int helm_sdkpy_config_create(const char *namespace, const char *kubeconfig, const char *kubecontext, helm_sdkpy_handle *handle_out);
    void helm_sdkpy_config_destroy(helm_sdkpy_handle handle);

    // Install action
    int helm_sdkpy_install(helm_sdkpy_handle handle, const char *release_name, const char *chart_path, const char *values_json, const char *version, int create_namespace, int wait, int timeout_seconds, char **result_json);

    // Upgrade action
    int helm_sdkpy_upgrade(helm_sdkpy_handle handle, const char *release_name, const char *chart_path, const char *values_json, const char *version, char **result_json);

    // Uninstall action
    int helm_sdkpy_uninstall(helm_sdkpy_handle handle, const char *release_name, int wait, int timeout_seconds, char **result_json);

    // List action
    int helm_sdkpy_list(helm_sdkpy_handle handle, int all, char **result_json);

    // Status action
    int helm_sdkpy_status(helm_sdkpy_handle handle, const char *release_name, char **result_json);

    // Rollback action
    int helm_sdkpy_rollback(helm_sdkpy_handle handle, const char *release_name, int revision, char **result_json);

    // Get values action
    int helm_sdkpy_get_values(helm_sdkpy_handle handle, const char *release_name, int all_values, char **result_json);

    // History action
    int helm_sdkpy_history(helm_sdkpy_handle handle, const char *release_name, char **result_json);

    // Pull action
    int helm_sdkpy_pull(helm_sdkpy_handle handle, const char *chart_ref, const char *dest_dir);

    // Show chart action
    int helm_sdkpy_show_chart(helm_sdkpy_handle handle, const char *chart_path, char **result_json);

    // Show values action
    int helm_sdkpy_show_values(helm_sdkpy_handle handle, const char *chart_path, char **result_json);

    // Test action
    int helm_sdkpy_test(helm_sdkpy_handle handle, const char *release_name, char **result_json);

    // Lint action
    int helm_sdkpy_lint(helm_sdkpy_handle handle, const char *chart_path, char **result_json);

    // Package action
    int helm_sdkpy_package(helm_sdkpy_handle handle, const char *chart_path, const char *dest_dir, char **result_path);

    // Repository management actions
    int helm_sdkpy_repo_add(helm_sdkpy_handle handle, const char *name, const char *url, const char *username, const char *password, const char *options_json);
    int helm_sdkpy_repo_remove(helm_sdkpy_handle handle, const char *name);
    int helm_sdkpy_repo_list(helm_sdkpy_handle handle, char **result_json);
    int helm_sdkpy_repo_update(helm_sdkpy_handle handle, const char *name);

    // Registry management actions
    int helm_sdkpy_registry_login(helm_sdkpy_handle handle, const char *hostname, const char *username, const char *password, const char *options_json);
    int helm_sdkpy_registry_logout(helm_sdkpy_handle handle, const char *hostname);
    
    // Push action (for OCI registries)
    int helm_sdkpy_push(helm_sdkpy_handle handle, const char *chart_ref, const char *remote, const char *options_json);

    // Utility functions
    const char *helm_sdkpy_last_error(void);
    void helm_sdkpy_free(void *ptr);
    int helm_sdkpy_version_number(void);
    const char *helm_sdkpy_version_string(void);
    """
)


__all__ = [
    "HelmError",
    "HelmLibraryNotFound",
    "configure",
    "ffi",
    "get_library",
    "get_version",
    "string_from_c",
    "_reset_for_tests",
]


_library_lock = threading.Lock()
_library = None
_library_path: str | None = None


def configure(path: str | None) -> None:
    """Force the bindings to load libhelm_sdkpy from ``path``.

    Passing ``None`` clears the override and re-enables auto-discovery.
    """

    global _library_path, _library
    with _library_lock:
        _library_path = path
        _library = None


def _find_library() -> str | None:
    """Find the helm_sdkpy shared library."""

    # Check for configured path first
    if _library_path is not None:
        return _library_path

    # Determine platform-specific library name and search paths
    system = platform.system()
    machine = platform.machine()

    # Normalize architecture names to match Go's convention
    if machine == "x86_64":
        machine = "amd64"
    elif machine == "aarch64":
        machine = "arm64"

    if system == "Linux":
        lib_name = "libhelm_sdkpy.so"
        platform_dir = f"linux-{machine}"
    elif system == "Darwin":
        lib_name = "libhelm_sdkpy.dylib"
        platform_dir = f"darwin-{machine}"
    elif system == "Windows":
        lib_name = "helm_sdkpy.dll"
        platform_dir = f"windows-{machine}"
    else:
        return None

    # Search in package directory first
    package_dir = Path(__file__).parent
    lib_dir = package_dir / "_lib" / platform_dir
    lib_path = lib_dir / lib_name

    if lib_path.exists():
        return str(lib_path)

    # Try just the platform directory
    lib_path = lib_dir / lib_name
    if lib_path.exists():
        return str(lib_path)

    # Try environment variable
    env_path = os.environ.get("HELMPY_LIBRARY_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    return None


def get_library():
    """Get the loaded Helm library, loading it if necessary."""
    global _library

    with _library_lock:
        if _library is not None:
            return _library

        lib_path = _find_library()
        if lib_path is None:
            raise HelmLibraryNotFound(
                "Could not find helm_sdkpy shared library. Please ensure helm_sdkpy is properly installed."
            )

        try:
            _library = ffi.dlopen(lib_path)
        except OSError as e:
            raise HelmLibraryNotFound(
                f"Failed to load helm_sdkpy library from {lib_path}: {e}"
            ) from e

        return _library


def get_version() -> str:
    """Get the version string from the native library."""
    lib = get_library()
    version_ptr = lib.helm_sdkpy_version_string()
    if version_ptr == ffi.NULL:
        return "unknown"
    return ffi.string(version_ptr).decode("utf-8")


def string_from_c(c_str) -> str:
    """Convert a C string to Python string and free it."""
    if c_str == ffi.NULL:
        return ""
    try:
        s = ffi.string(c_str).decode("utf-8")
        return s
    finally:
        lib = get_library()
        lib.helm_sdkpy_free(c_str)


def check_error(result: int) -> None:
    """Check if a C function returned an error and raise an exception if so."""
    if result != 0:
        lib = get_library()
        err_ptr = lib.helm_sdkpy_last_error()
        if err_ptr != ffi.NULL:
            err_msg = ffi.string(err_ptr).decode("utf-8")
            raise HelmError(err_msg)
        else:
            raise HelmError("Unknown error occurred")


def _reset_for_tests() -> None:
    """Reset library state for testing. Internal use only."""
    global _library, _library_path
    with _library_lock:
        _library = None
        _library_path = None
