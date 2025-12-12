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

"""Python bindings for Helm - The Kubernetes Package Manager."""

from importlib.metadata import version as _get_version

from ._ffi import get_version
from .actions import (
    Configuration,
    GetValues,
    History,
    Install,
    List,
    RegistryLogin,
    RegistryLogout,
    Rollback,
    Status,
    Uninstall,
    Upgrade,
)
from .chart import Lint, Package, Pull, Push, ReleaseTest, Show
from .exceptions import (
    ChartError,
    ConfigurationError,
    HelmError,
    HelmLibraryNotFound,
    InstallError,
    RegistryError,
    ReleaseError,
    RollbackError,
    UninstallError,
    UpgradeError,
    ValidationError,
)
from .repo import RepoAdd, RepoList, RepoRemove, RepoUpdate

# Backwards compatibility alias - ReleaseTest renamed to avoid pytest collection
Test = ReleaseTest

__version__ = _get_version("helm-sdkpy")

__all__ = [
    # Core classes
    "Configuration",
    # Action classes
    "Install",
    "Upgrade",
    "Uninstall",
    "List",
    "Status",
    "Rollback",
    "GetValues",
    "History",
    "RegistryLogin",
    "RegistryLogout",
    # Chart classes
    "Pull",
    "Show",
    "Test",  # Alias for ReleaseTest
    "ReleaseTest",
    "Lint",
    "Package",
    "Push",
    # Repository classes
    "RepoAdd",
    "RepoRemove",
    "RepoList",
    "RepoUpdate",
    # Exceptions - Base
    "HelmError",
    "HelmLibraryNotFound",
    # Exceptions - Specific
    "ConfigurationError",
    "InstallError",
    "UpgradeError",
    "UninstallError",
    "RollbackError",
    "ChartError",
    "ReleaseError",
    "RegistryError",
    "ValidationError",
    # Utilities
    "get_version",
    "__version__",
]
