# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


# ObzClient Exceptions
class ObzClientError(Exception):
    """Raise when Obz Client methods fail."""
    pass


# AuthService Exceptions
class APIKeyNotFoundError(Exception):
    """
    Raised when AuthService cannot properly load API Key
    from an evironment or local .netrc file.
    """
    pass

class APIKeyVerificationError(Exception):
    """
    Raised when API key verification fails due to
    connection with backend issue or server-side error.
    """
    pass

class WrongAPIKey(Exception):
    """
    Raised when provided API key turn out to be not valid.
    """
    pass

class SavingCredentialsFailed(Exception):
    """
    Raised when saving API key fails.
    """
    pass


# ProjectService Exceptions
class ProjectSetupError(Exception):
    """
    Raised when a project setup fails.
    """
    pass

# CacheService Exceptions
class CacheServiceError(Exception):
    """
    Raised within Cache Service.
    """
    pass


# UploadService Exceptions
class UploadServiceError(Exception):
    """
    Raised when within UploadService
    """
    pass