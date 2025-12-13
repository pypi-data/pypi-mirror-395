# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from dataclasses import dataclass
from typing import Optional, List
import numpy as np


@dataclass
class XAIResults:
    """
    Data Class specyfying format of results returned by each XAI Tool.
    """
    tool_id: str
    method_name: str
    xai_maps: List[np.ndarray]
    target_idxs: Optional[List[int]] = None
    postprocessing_method: Optional[str] = None
