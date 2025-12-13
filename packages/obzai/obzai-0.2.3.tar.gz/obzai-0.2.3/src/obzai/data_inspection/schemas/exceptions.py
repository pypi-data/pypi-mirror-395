# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Data Inspector Related
class DataInspectorError(RuntimeError):
    """Raised within Data Inspector"""
    pass

class CheckpointError(DataInspectorError):
    """Raised when checkpoint save/load fails."""
    pass

class CheckpointVersionError(CheckpointError):
    """Raised when checkpoint version is incompatible."""
    pass

class CheckpointCorruptedError(CheckpointError):
    """Raised when checkpoint files are missing or corrupted."""
    pass


# Feature Pipeline Related
class FeaturePipelineError(RuntimeError):
    """Raised within Feature Pipeline"""
    pass


# OD Model Related
class ODModelError(RuntimeError):
    """Raised within OD Model"""
    pass
