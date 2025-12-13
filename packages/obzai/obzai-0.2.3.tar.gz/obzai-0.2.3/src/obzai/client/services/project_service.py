# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, Dict, List
from dataclasses import asdict
import httpx

# API Config
from obzai.client.configs.api_config import APIConfig

# Custom exceptions
from obzai.client.schemas.exceptions import ProjectSetupError

# Custom dataclasses & types
from obzai.data_inspection.schemas.dataclasses import DataInspectorMeta
from obzai.client.schemas.dataclasses import ProjectMeta
from obzai.client.schemas.types import MLTask


class _ProjectService:
    """
    The service handles project initilization
    and project-related credentials storage.
    """
    def __init__(self, session: httpx.Client):
        """
        Constructs an instance of the ProjectService class.

        Args:
            session: A session object from the ObzClient.
        """
        self.session = session
        
        self._project_ready: bool = False
        self._project_id: Optional[int] = None
        self._data_inspector_local2remote_id = None
        self._ml_task: Optional[MLTask] = None

    @property
    def project_ready(self) -> bool:
        """
        Returns bool flag indicating whether project
        is ready or not.
        """
        return self._project_ready

    @property
    def project_meta(self) -> ProjectMeta:
        """
        Returns a project ID and ML Task.
        """
        if (
            self._project_id is None
            or
            self._ml_task is None
            ):
            raise RuntimeError("Project is not initialized yet.")
        else:
            return ProjectMeta(
                project_id=self._project_id,
                ml_task=self._ml_task,
                data_inspector_local2remote_id = self._data_inspector_local2remote_id
                )

    def _reset_state(self) -> None:
        """
        Resets cached project state after failed setup attempts.
        """
        self._project_ready = False
        self._project_id = None
        self._data_inspector_local2remote_id = None
        self._ml_task = None

    def setup_project(
        self,
        api_key: str,
        project_name: str,
        ml_task: Optional[MLTask] = None,
        index2name: Optional[Dict[int, str]] = None,
        inspectors_metadata: Optional[List[DataInspectorMeta]] = None,
    ) -> Dict[str, Optional[object]]:
        """
        Creates or reuses a project via the unified setup endpoint.

        Args:
            api_key: (string) User's API key to Obz.ai API.
            project_name: (string) Project name to create or reuse.
            ml_task: (Enum Type) Desired ML Task when creating a project.
            index2name: (dict) Optional mapping of prediction indices to corresponding names.
            inspectors_metadata: (list[DataInspectorMeta]) Optional metadata from data inspectors.

        Returns:
            A dictionary containing setup details including action, message, project_id, ml_task,
            and data_inspector_local2remote_id.

        Raises:
            ProjectSetupError when backend returns failure or malformed response.
        """
        # (1) Construct payload, headers and send request to the backend.
        metadata_dicts = [asdict(meta) for meta in inspectors_metadata] if inspectors_metadata else None
        payload = {
            "project_name": project_name,
            "ml_task": ml_task.value if ml_task is not None else None,
            "index2name": index2name,
            "inspectors_metadata": metadata_dicts,
        }

        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            response = self.session.post(
                APIConfig.get_url("setup_project"), json=payload, headers=headers, timeout=100
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._reset_state()
            raise ProjectSetupError(f"Backend returned failure with status code: {e.response.status_code} and detail: {e.response.json()['detail']}") from e
        except Exception as e:
            self._reset_state()
            raise ProjectSetupError(f"Unexpected error occured during project setup: {e}") from e

        # (2) Parse response and validate status, action and message.
        data = response.json()

        self._project_id = data.get("project_id")
        self._data_inspector_local2remote_id = data.get("data_inspector_local2remote_id")
        self._ml_task = MLTask(data.get("ml_task"))
        self._project_ready = True

        return {
            "status": data.get("status"),
            "action": data.get("action"),
            "message": data.get("message"),
            "project_id": self._project_id,
            "ml_task": self._ml_task,
            "data_inspector_local2remote_id": self._data_inspector_local2remote_id,
        }
