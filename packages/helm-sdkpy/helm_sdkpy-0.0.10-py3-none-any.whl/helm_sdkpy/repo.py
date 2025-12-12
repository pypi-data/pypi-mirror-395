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

"""Repository management operations."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from ._ffi import check_error, ffi, get_library, string_from_c
from .exceptions import RegistryError


class RepoAdd:
    """Helm repo add action.

    Adds a chart repository to the local configuration.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> repo_add = RepoAdd(config)
        >>> asyncio.run(repo_add.run("stable", "https://charts.helm.sh/stable"))
        >>> # With authentication
        >>> asyncio.run(repo_add.run(
        ...     "private-repo",
        ...     "https://charts.example.com",
        ...     username="user",
        ...     password="pass"
        ... ))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(
        self,
        name: str,
        url: str,
        username: str | None = None,
        password: str | None = None,
        insecure_skip_tls_verify: bool = False,
        pass_credentials_all: bool = False,
        cert_file: str | None = None,
        key_file: str | None = None,
        ca_file: str | None = None,
    ) -> None:
        """Add a chart repository asynchronously.

        Args:
            name: Repository name
            url: Repository URL
            username: Username for authentication
            password: Password for authentication
            insecure_skip_tls_verify: Skip TLS certificate verification
            pass_credentials_all: Pass credentials to all domains
            cert_file: Path to TLS certificate file
            key_file: Path to TLS key file
            ca_file: Path to CA bundle file

        Raises:
            RegistryError: If adding the repository fails
        """

        def _repo_add():
            name_cstr = ffi.new("char[]", name.encode("utf-8"))
            url_cstr = ffi.new("char[]", url.encode("utf-8"))
            username_cstr = ffi.new("char[]", username.encode("utf-8")) if username else ffi.NULL
            password_cstr = ffi.new("char[]", password.encode("utf-8")) if password else ffi.NULL

            # Build options JSON
            options = {}
            if insecure_skip_tls_verify:
                options["insecure_skip_tls_verify"] = True
            if pass_credentials_all:
                options["pass_credentials_all"] = True
            if cert_file:
                options["cert_file"] = cert_file
            if key_file:
                options["key_file"] = key_file
            if ca_file:
                options["ca_file"] = ca_file

            options_json = json.dumps(options) if options else ""
            options_cstr = ffi.new("char[]", options_json.encode("utf-8"))

            result = self._lib.helm_sdkpy_repo_add(
                self.config._handle_value,
                name_cstr,
                url_cstr,
                username_cstr,
                password_cstr,
                options_cstr,
            )

            if result != 0:
                check_error(result)

        return await asyncio.to_thread(_repo_add)


class RepoRemove:
    """Helm repo remove action.

    Removes a chart repository from the local configuration.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> repo_remove = RepoRemove(config)
        >>> asyncio.run(repo_remove.run("stable"))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(self, name: str) -> None:
        """Remove a chart repository asynchronously.

        Args:
            name: Repository name to remove

        Raises:
            RegistryError: If removing the repository fails
        """

        def _repo_remove():
            name_cstr = ffi.new("char[]", name.encode("utf-8"))

            result = self._lib.helm_sdkpy_repo_remove(self.config._handle_value, name_cstr)

            if result != 0:
                check_error(result)

        return await asyncio.to_thread(_repo_remove)


class RepoList:
    """Helm repo list action.

    Lists all configured chart repositories.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> repo_list = RepoList(config)
        >>> repos = asyncio.run(repo_list.run())
        >>> for repo in repos:
        ...     print(f"{repo['name']}: {repo['url']}")
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(self) -> list[dict[str, Any]]:
        """List configured repositories asynchronously.

        Returns:
            List of repository dictionaries with name, url, and other fields

        Raises:
            RegistryError: If listing repositories fails
        """

        def _repo_list():
            result_json = ffi.new("char **")

            result = self._lib.helm_sdkpy_repo_list(self.config._handle_value, result_json)

            if result != 0:
                check_error(result)

            json_str = string_from_c(result_json[0])
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise RegistryError(f"Failed to parse repository list: {e}") from e

        return await asyncio.to_thread(_repo_list)


class RepoUpdate:
    """Helm repo update action.

    Updates the local cache of chart repositories.

    Args:
        config: Helm configuration object

    Example:
        >>> import asyncio
        >>> config = Configuration()
        >>> repo_update = RepoUpdate(config)
        >>> # Update all repositories
        >>> asyncio.run(repo_update.run())
        >>> # Update specific repository
        >>> asyncio.run(repo_update.run("stable"))
    """

    def __init__(self, config):
        self.config = config
        self._lib = get_library()

    async def run(self, name: str | None = None) -> None:
        """Update repository indexes asynchronously.

        Args:
            name: Optional repository name to update. If not provided,
                  updates all repositories.

        Raises:
            RegistryError: If updating fails
        """

        def _repo_update():
            name_cstr = ffi.new("char[]", name.encode("utf-8")) if name else ffi.NULL

            result = self._lib.helm_sdkpy_repo_update(self.config._handle_value, name_cstr)

            if result != 0:
                check_error(result)

        return await asyncio.to_thread(_repo_update)
