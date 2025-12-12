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

"""Chart-related Helm operations."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from ._ffi import check_error, ffi, get_library, string_from_c
from .exceptions import ChartError


class Pull:
    """Helm pull action.

    Downloads a chart from a repository.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> pull = Pull(config)
        >>> asyncio.run(pull.run("stable/nginx", dest_dir="./charts"))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(
        self, chart_ref: str, dest_dir: str | None = None, version: str | None = None
    ) -> None:
        """Pull a chart asynchronously.

        Args:
            chart_ref: Chart reference (e.g., "repo/chart" or "oci://...")
            dest_dir: Destination directory (default: current directory)
            version: Chart version to pull (e.g., "1.2.3"). If not specified, uses latest

        Raises:
            ChartError: If pull fails
        """

        def _pull():
            ref_cstr = ffi.new("char[]", chart_ref.encode("utf-8"))
            dest_cstr = ffi.new("char[]", dest_dir.encode("utf-8")) if dest_dir else ffi.NULL
            version_str = version or ""
            version_cstr = ffi.new("char[]", version_str.encode("utf-8"))

            result = self._lib.helm_sdkpy_pull(
                self.config._handle_value, ref_cstr, dest_cstr, version_cstr
            )

            if result != 0:
                check_error(result)

        return await asyncio.to_thread(_pull)


class Show:
    """Helm show actions.

    Shows information about a chart.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> show = Show(config)
        >>> chart_yaml = asyncio.run(show.chart("./mychart"))
        >>> values_yaml = asyncio.run(show.values("./mychart"))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def chart(self, chart_path: str) -> str:
        """Show the chart's Chart.yaml content asynchronously.

        Args:
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

        Returns:
            Chart.yaml content as string

        Raises:
            ChartError: If show fails
        """

        def _chart():
            result_json = ffi.new("char **")
            path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

            result = self._lib.helm_sdkpy_show_chart(
                self.config._handle_value, path_cstr, result_json
            )

            if result != 0:
                check_error(result)

            return string_from_c(result_json[0])

        return await asyncio.to_thread(_chart)

    async def values(self, chart_path: str) -> str:
        """Show the chart's values.yaml content asynchronously.

        Args:
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

        Returns:
            values.yaml content as string

        Raises:
            ChartError: If show fails
        """

        def _values():
            result_json = ffi.new("char **")
            path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

            result = self._lib.helm_sdkpy_show_values(
                self.config._handle_value, path_cstr, result_json
            )

            if result != 0:
                check_error(result)

            return string_from_c(result_json[0])

        return await asyncio.to_thread(_values)


class ReleaseTest:
    """Helm test action.

    Runs tests for a release.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> test = ReleaseTest(config)
        >>> result = asyncio.run(test.run("my-release"))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(self, release_name: str) -> dict[str, Any]:
        """Run tests for a release asynchronously.

        Args:
            release_name: Name of the release

        Returns:
            Dictionary containing test results

        Raises:
            ChartError: If test fails
        """

        def _test():
            result_json = ffi.new("char **")
            name_cstr = ffi.new("char[]", release_name.encode("utf-8"))

            result = self._lib.helm_sdkpy_test(self.config._handle_value, name_cstr, result_json)

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ChartError(f"Failed to parse test result: {e}") from e

        return await asyncio.to_thread(_test)


class Lint:
    """Helm lint action.

    Lints a chart for errors.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> lint = Lint(config)
        >>> result = asyncio.run(lint.run("./mychart"))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(self, chart_path: str) -> dict[str, Any]:
        """Lint a chart asynchronously.

        Args:
            chart_path: Path to the chart. Supports:
                - Local paths: "./mychart" or "/path/to/chart"
                - OCI registries: "oci://ghcr.io/org/chart"
                - HTTP(S) URLs: "https://example.com/chart-1.0.0.tgz"

        Returns:
            Dictionary containing lint results

        Raises:
            ChartError: If lint operation fails
        """

        def _lint():
            result_json = ffi.new("char **")
            path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))

            result = self._lib.helm_sdkpy_lint(self.config._handle_value, path_cstr, result_json)

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ChartError(f"Failed to parse lint result: {e}") from e

        return await asyncio.to_thread(_lint)


class Package:
    """Helm package action.

    Packages a chart into a versioned archive.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> package = Package(config)
        >>> archive_path = asyncio.run(package.run("./mychart", dest_dir="./dist"))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(self, chart_path: str, dest_dir: str | None = None) -> str:
        """Package a chart asynchronously.

        Args:
            chart_path: Path to the chart directory to package
            dest_dir: Destination directory (default: current directory)

        Returns:
            Path to the packaged chart archive

        Raises:
            ChartError: If package fails
        """

        def _package():
            result_path = ffi.new("char **")
            path_cstr = ffi.new("char[]", chart_path.encode("utf-8"))
            dest_cstr = ffi.new("char[]", dest_dir.encode("utf-8")) if dest_dir else ffi.NULL

            result = self._lib.helm_sdkpy_package(
                self.config._handle_value, path_cstr, dest_cstr, result_path
            )

            if result != 0:
                check_error(result)

            return string_from_c(result_path[0])

        return await asyncio.to_thread(_package)


class Push:
    """Helm push action.

    Pushes a chart to an OCI registry.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> push = Push(config)
        >>> asyncio.run(push.run(
        ...     chart_path="./mychart-1.0.0.tgz",
        ...     remote="oci://ghcr.io/myorg/charts"
        ... ))
        >>> # With TLS configuration
        >>> asyncio.run(push.run(
        ...     chart_path="./mychart-1.0.0.tgz",
        ...     remote="oci://registry.example.com/charts",
        ...     cert_file="/path/to/cert.pem",
        ...     key_file="/path/to/key.pem",
        ...     ca_file="/path/to/ca.pem"
        ... ))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(
        self,
        chart_path: str,
        remote: str,
        cert_file: str | None = None,
        key_file: str | None = None,
        ca_file: str | None = None,
        insecure_skip_tls_verify: bool = False,
        plain_http: bool = False,
    ) -> None:
        """Push a chart to an OCI registry asynchronously.

        Args:
            chart_path: Path to the packaged chart (.tgz file)
            remote: OCI registry URL (e.g., "oci://ghcr.io/org/charts")
            cert_file: Path to client certificate file for TLS
            key_file: Path to client key file for TLS
            ca_file: Path to CA certificate file for TLS verification
            insecure_skip_tls_verify: Skip TLS certificate verification
            plain_http: Use HTTP instead of HTTPS

        Raises:
            ChartError: If push fails
        """

        def _push():
            chart_cstr = ffi.new("char[]", chart_path.encode("utf-8"))
            remote_cstr = ffi.new("char[]", remote.encode("utf-8"))

            # Build options JSON
            options = {}
            if cert_file:
                options["cert_file"] = cert_file
            if key_file:
                options["key_file"] = key_file
            if ca_file:
                options["ca_file"] = ca_file
            if insecure_skip_tls_verify:
                options["insecure_skip_tls_verify"] = insecure_skip_tls_verify
            if plain_http:
                options["plain_http"] = plain_http

            options_json = json.dumps(options)
            options_cstr = ffi.new("char[]", options_json.encode("utf-8"))

            result = self._lib.helm_sdkpy_push(
                self.config._handle_value,
                chart_cstr,
                remote_cstr,
                options_cstr,
            )

            if result != 0:
                check_error(result)

        return await asyncio.to_thread(_push)
