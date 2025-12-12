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

"""Core Helm configuration and action classes."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from ._ffi import check_error, ffi, get_library, string_from_c
from .exceptions import (
    InstallError,
    ReleaseError,
    RollbackError,
    UninstallError,
    UpgradeError,
)


class Configuration:
    """Helm configuration for interacting with Kubernetes clusters.

    This class manages the connection to a Kubernetes cluster and provides
    the context for all Helm operations.

    Args:
        namespace: Kubernetes namespace to operate in (default: "default")
        kubeconfig: Path to kubeconfig file (default: uses $KUBECONFIG or ~/.kube/config)
        kubecontext: Kubernetes context to use (default: current context)

    Example:
        >>> import asyncio
        >>> config = Configuration(namespace="my-namespace")
        >>> install = Install(config)
        >>> result = asyncio.run(install.run("my-release", "/path/to/chart"))
    """

    def __init__(
        self,
        namespace: str = "default",
        kubeconfig: str | None = None,
        kubecontext: str | None = None,
    ):
        self._lib = get_library()
        self._handle = ffi.new("helm_sdkpy_handle *")

        ns_cstr = ffi.new("char[]", namespace.encode("utf-8"))
        kc_cstr = ffi.new("char[]", kubeconfig.encode("utf-8")) if kubeconfig else ffi.NULL
        kctx_cstr = ffi.new("char[]", kubecontext.encode("utf-8")) if kubecontext else ffi.NULL

        result = self._lib.helm_sdkpy_config_create(ns_cstr, kc_cstr, kctx_cstr, self._handle)
        check_error(result)

        self._handle_value = self._handle[0]

    def __del__(self):
        """Clean up the configuration handle."""
        if hasattr(self, "_lib") and hasattr(self, "_handle_value"):
            self._lib.helm_sdkpy_config_destroy(self._handle_value)

    def __enter__(self):
        """Support for context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for context manager."""
        self.__del__()
        return False


class Install:
    """Helm install action.

    Installs a chart into a Kubernetes cluster.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> install = Install(config)
        >>> result = asyncio.run(install.run("my-release", "./mychart", values={"replicas": 3}))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(
        self,
        release_name: str,
        chart_path: str,
        values: dict[str, Any] | None = None,
        version: str | None = None,
        create_namespace: bool = False,
        wait: bool = True,
        timeout: int = 300,
    ) -> dict[str, Any]:
        """Install a chart asynchronously.

        Args:
            release_name: Name of the release
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"
            values: Values to pass to the chart
            version: Chart version to install (e.g., "1.2.3"). If not specified, uses latest
            create_namespace: Create the release namespace if not present
            wait: Wait for all resources to be ready (default: True)
            timeout: Timeout in seconds for wait (default: 300)

        Returns:
            Dictionary containing release information

        Raises:
            InstallError: If installation fails
        """

        def _install():
            result_json = ffi.new("char **")

            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))
            path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

            values_json = json.dumps(values) if values else ""
            values_cstr = ffi.new("char[]", values_json.encode("utf-8"))

            version_str = version or ""
            version_cstr = ffi.new("char[]", version_str.encode("utf-8"))

            result = self._lib.helm_sdkpy_install(
                self.config._handle_value,
                name_cstr,
                path_cstr,
                values_cstr,
                version_cstr,
                1 if create_namespace else 0,
                1 if wait else 0,
                timeout,
                result_json,
            )

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise InstallError(f"Failed to parse install result: {e}") from e

        return await asyncio.to_thread(_install)


class Upgrade:
    """Helm upgrade action.

    Upgrades an existing release.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> upgrade = Upgrade(config)
        >>> result = asyncio.run(upgrade.run("my-release", "./mychart", values={"replicas": 5}))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(
        self,
        release_name: str,
        chart_path: str,
        values: dict[str, Any] | None = None,
        version: str | None = None,
    ) -> dict[str, Any]:
        """Upgrade a release asynchronously.

        Args:
            release_name: Name of the release
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"
            values: Values to pass to the chart
            version: Chart version to upgrade to (e.g., "1.2.3"). If not specified, uses latest

        Returns:
            Dictionary containing release information

        Raises:
            UpgradeError: If upgrade fails
        """

        def _upgrade():
            result_json = ffi.new("char **")

            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))
            path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

            values_json = json.dumps(values) if values else ""
            values_cstr = ffi.new("char[]", values_json.encode("utf-8"))

            version_str = version or ""
            version_cstr = ffi.new("char[]", version_str.encode("utf-8"))

            result = self._lib.helm_sdkpy_upgrade(
                self.config._handle_value,
                name_cstr,
                path_cstr,
                values_cstr,
                version_cstr,
                result_json,
            )

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise UpgradeError(f"Failed to parse upgrade result: {e}") from e

        return await asyncio.to_thread(_upgrade)


class Uninstall:
    """Helm uninstall action.

    Uninstalls a release from the cluster.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> uninstall = Uninstall(config)
        >>> result = asyncio.run(uninstall.run("my-release"))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(self, release_name: str, wait: bool = True, timeout: int = 300) -> dict[str, Any]:
        """Uninstall a release asynchronously.

        Args:
            release_name: Name of the release
            wait: Wait for all resources to be deleted (default: True)
            timeout: Timeout in seconds for wait (default: 300)

        Returns:
            Dictionary containing uninstall response

        Raises:
            UninstallError: If uninstall fails
        """

        def _uninstall():
            result_json = ffi.new("char **")
            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

            result = self._lib.helm_sdkpy_uninstall(
                self.config._handle_value, name_cstr, 1 if wait else 0, timeout, result_json
            )

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise UninstallError(f"Failed to parse uninstall result: {e}") from e

        return await asyncio.to_thread(_uninstall)


class List:
    """Helm list action.

    Lists releases in the cluster.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> list_action = List(config)
        >>> releases = asyncio.run(list_action.run(all=True))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(self, all: bool = False) -> list[dict[str, Any]]:
        """List releases asynchronously.

        Args:
            all: Show all releases, not just deployed ones

        Returns:
            List of release dictionaries

        Raises:
            ReleaseError: If listing fails
        """

        def _list():
            result_json = ffi.new("char **")
            all_flag = 1 if all else 0

            result = self._lib.helm_sdkpy_list(self.config._handle_value, all_flag, result_json)

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ReleaseError(f"Failed to parse list result: {e}") from e

        return await asyncio.to_thread(_list)


class Status:
    """Helm status action.

    Gets the status of a release.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> status = Status(config)
        >>> info = asyncio.run(status.run("my-release"))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(self, release_name: str) -> dict[str, Any]:
        """Get release status asynchronously.

        Args:
            release_name: Name of the release

        Returns:
            Dictionary containing release status

        Raises:
            ReleaseError: If status check fails
        """

        def _status():
            result_json = ffi.new("char **")
            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

            result = self._lib.helm_sdkpy_status(self.config._handle_value, name_cstr, result_json)

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ReleaseError(f"Failed to parse status result: {e}") from e

        return await asyncio.to_thread(_status)


class Rollback:
    """Helm rollback action.

    Rolls back a release to a previous revision.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> rollback = Rollback(config)
        >>> result = asyncio.run(rollback.run("my-release", revision=2))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(self, release_name: str, revision: int = 0) -> dict[str, Any]:
        """Rollback a release asynchronously.

        Args:
            release_name: Name of the release
            revision: Revision to rollback to (0 = previous)

        Returns:
            Dictionary containing rollback result

        Raises:
            RollbackError: If rollback fails
        """

        def _rollback():
            result_json = ffi.new("char **")
            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

            result = self._lib.helm_sdkpy_rollback(
                self.config._handle_value, name_cstr, revision, result_json
            )

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise RollbackError(f"Failed to parse rollback result: {e}") from e

        return await asyncio.to_thread(_rollback)


class GetValues:
    """Helm get values action.

    Gets the values for a release.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> get_values = GetValues(config)
        >>> values = asyncio.run(get_values.run("my-release", all=True))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(self, release_name: str, all: bool = False) -> dict[str, Any]:
        """Get release values asynchronously.

        Args:
            release_name: Name of the release
            all: Get all values, including computed values

        Returns:
            Dictionary containing values

        Raises:
            ReleaseError: If getting values fails
        """

        def _get_values():
            result_json = ffi.new("char **")
            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))
            all_flag = 1 if all else 0

            result = self._lib.helm_sdkpy_get_values(
                self.config._handle_value, name_cstr, all_flag, result_json
            )

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ReleaseError(f"Failed to parse get values result: {e}") from e

        return await asyncio.to_thread(_get_values)


class History:
    """Helm history action.

    Gets the release history.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> history = History(config)
        >>> revisions = asyncio.run(history.run("my-release"))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(self, release_name: str) -> list[dict[str, Any]]:
        """Get release history asynchronously.

        Args:
            release_name: Name of the release

        Returns:
            List of revision dictionaries

        Raises:
            ReleaseError: If getting history fails
        """

        def _history():
            result_json = ffi.new("char **")
            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

            result = self._lib.helm_sdkpy_history(self.config._handle_value, name_cstr, result_json)

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ReleaseError(f"Failed to parse history result: {e}") from e

        return await asyncio.to_thread(_history)


class RegistryLogin:
    """Helm registry login action.

    Logs into an OCI registry for chart operations.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> registry_login = RegistryLogin(config)
        >>> asyncio.run(registry_login.run(
        ...     hostname="ghcr.io",
        ...     username="myuser",
        ...     password="mytoken"
        ... ))
        >>> # With TLS configuration
        >>> asyncio.run(registry_login.run(
        ...     hostname="registry.example.com",
        ...     username="user",
        ...     password="pass",
        ...     cert_file="/path/to/cert.pem",
        ...     key_file="/path/to/key.pem",
        ...     ca_file="/path/to/ca.pem"
        ... ))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(
        self,
        hostname: str,
        username: str,
        password: str,
        cert_file: str | None = None,
        key_file: str | None = None,
        ca_file: str | None = None,
        insecure: bool = False,
        plain_http: bool = False,
    ) -> None:
        """Login to a registry asynchronously.

        Args:
            hostname: Registry hostname (e.g., "ghcr.io", "registry.example.com")
            username: Registry username
            password: Registry password or token
            cert_file: Path to client certificate file for TLS
            key_file: Path to client key file for TLS
            ca_file: Path to CA certificate file for TLS verification
            insecure: Skip TLS certificate verification
            plain_http: Use HTTP instead of HTTPS

        Raises:
            RegistryError: If login fails
        """
        from .exceptions import RegistryError

        def _registry_login():
            hostname_cstr = ffi.new("char[]", hostname.encode("utf-8"))
            username_cstr = ffi.new("char[]", username.encode("utf-8"))
            password_cstr = ffi.new("char[]", password.encode("utf-8"))

            # Build options JSON
            options = {}
            if cert_file:
                options["cert_file"] = cert_file
            if key_file:
                options["key_file"] = key_file
            if ca_file:
                options["ca_file"] = ca_file
            if insecure:
                options["insecure"] = insecure
            if plain_http:
                options["plain_http"] = plain_http

            options_json = json.dumps(options)
            options_cstr = ffi.new("char[]", options_json.encode("utf-8"))

            result = self._lib.helm_sdkpy_registry_login(
                self.config._handle_value,
                hostname_cstr,
                username_cstr,
                password_cstr,
                options_cstr,
            )

            if result != 0:
                check_error(result)

        return await asyncio.to_thread(_registry_login)


class RegistryLogout:
    """Helm registry logout action.

    Logs out from an OCI registry.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> registry_logout = RegistryLogout(config)
        >>> asyncio.run(registry_logout.run(hostname="ghcr.io"))
    """

    def __init__(self, config: Configuration):
        self.config = config
        self._lib = get_library()

    async def run(self, hostname: str) -> None:
        """Logout from a registry asynchronously.

        Args:
            hostname: Registry hostname (e.g., "ghcr.io", "registry.example.com")

        Raises:
            RegistryError: If logout fails
        """
        from .exceptions import RegistryError

        def _registry_logout():
            hostname_cstr = ffi.new("char[]", hostname.encode("utf-8"))

            result = self._lib.helm_sdkpy_registry_logout(
                self.config._handle_value,
                hostname_cstr,
            )

            if result != 0:
                check_error(result)

        return await asyncio.to_thread(_registry_logout)
