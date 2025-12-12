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

"""Exception classes for helm_sdkpy."""

from __future__ import annotations


class HelmError(Exception):
    """Base exception for all Helm errors."""

    pass


class HelmLibraryNotFound(HelmError):
    """Raised when the Helm shared library cannot be found."""

    pass


class ConfigurationError(HelmError):
    """Raised when there's an error in Helm configuration."""

    pass


class InstallError(HelmError):
    """Raised when chart installation fails."""

    pass


class UpgradeError(HelmError):
    """Raised when chart upgrade fails."""

    pass


class UninstallError(HelmError):
    """Raised when chart uninstallation fails."""

    pass


class RollbackError(HelmError):
    """Raised when rollback fails."""

    pass


class ChartError(HelmError):
    """Raised when there's an error with chart operations."""

    pass


class ReleaseError(HelmError):
    """Raised when there's an error with release operations."""

    pass


class RegistryError(HelmError):
    """Raised when there's an error with registry operations."""

    pass


class ValidationError(HelmError):
    """Raised when validation fails."""

    pass
