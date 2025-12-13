# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
from typing import Dict, Optional

from obzai.client.schemas.types import MLTask


@dataclass
class ProjectMeta:
    """
    Class specifying key 
    project metadata.
    """
    project_id: int
    ml_task: MLTask
    data_inspector_local2remote_id: Optional[Dict[str, int]] = None