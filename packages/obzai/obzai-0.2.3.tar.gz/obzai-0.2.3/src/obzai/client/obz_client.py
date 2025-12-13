# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Dict, List, Optional, Union
import logging
import torch
import httpx
import os

# ObzAI Client module
## Services
from obzai.client.services.auth_service import _AuthService
from obzai.client.services.project_service import _ProjectService
from obzai.client.services.upload_service import _UploadService
from obzai.client.services.cache_service import _CacheService

## Types & Dataclasses
from obzai.client.schemas.types import OneOrManyDataInspectors, OneOrManyXAITools, MLTask

## Exceptions
from obzai.client.schemas.exceptions import ObzClientError, ProjectSetupError

# Data Inspection Module
## Base Data Inspector class
from obzai.data_inspection.inspectors.base_data_inspector import _BaseDataInspector

## Types & Dataclasses
from obzai.data_inspection.schemas.dataclasses import DataInspectionResults
from obzai.data_inspection.schemas.types import TensorOrSequenceOrDict

## Exceptions
from obzai.data_inspection.schemas.exceptions import DataInspectorError

# XAI Module
## Base XAI Tool
from obzai.xai.tools.xai_tool import BaseXAITool

## Types & Dataclasses
from obzai.xai.schemas.xai_results import XAIResults

## Exceptions
from obzai.xai.schemas.exceptions import XAIToolError


logger = logging.getLogger(__name__)


class ObzClient:
    """
    Class provides usefull interface for logging data to the ObzAI ecosystem.
    """
    def __init__(
            self, 
            data_inspectors: Optional[OneOrManyDataInspectors] = None,
            xai_tools: Optional[OneOrManyXAITools] = None
            ) -> None:
        """
        Creates an instance of the Obz Client.
        """
        # Set Data Inspectors
        self._set_data_inspectors(data_inspectors=data_inspectors)

        # Set XAI Tools
        self._set_xai_tools(xai_tools=xai_tools)

        # Set Session
        self._set_session()

        # Services
        self.auth_service = _AuthService(session=self._session)
        self.project_service = _ProjectService(session=self._session)
        self.upload_service = _UploadService(client=self._session)
        self.cache_service = _CacheService()

        # Initialize cache directory
        self._setup_obz_directory()

    def _set_data_inspectors(
            self, data_inspectors: Optional[OneOrManyDataInspectors]
            ) -> None:
        """
        Checks whether provided Data Inspectors are valid.

        Args:
            data_inspectors: Single instance or list of DataInspector instances
        
        Raises:
            ObzClientError when data_inspectors argument is not valid.
        """
        if data_inspectors is None:
            self._data_inspectors = None
        elif isinstance(data_inspectors, _BaseDataInspector):
            self._data_inspectors = [data_inspectors]
        elif isinstance(data_inspectors, list) and all([isinstance(inspctr, _BaseDataInspector) for inspctr in data_inspectors]):
            self._data_inspectors = data_inspectors
        else:
            raise ObzClientError("Provided data_inspectors argument is not valid.")

    def _set_xai_tools(
            self, xai_tools: Optional[OneOrManyXAITools]
            ) -> None:
        """
        Checks whether provided XAI Tools are valid.

        Args:
            xai_tools: Single instance or list of XAITool instances
        
        Raises:
            ObzClientError when xai_tools argument is not valid.
        """
        if xai_tools is None:
            self._xai_tools = None
        elif isinstance(xai_tools, BaseXAITool):
            self._xai_tools = [xai_tools]
        elif isinstance(xai_tools, list) and all([isinstance(tool, BaseXAITool) for tool in xai_tools]):
            self._xai_tools = xai_tools
        else:
            raise ObzClientError("Provided data_inspectors argument is not valid.")

    def _set_session(self) -> None:
        """
        Creates session handling connection with backend.
        """
        self._session = httpx.Client()

    def _setup_obz_directory(self) -> None:
        """
        Creates a directory containing cached files.
        """
        self._root_dir = os.path.join(os.getcwd(), ".obz")
        os.makedirs(self._root_dir, exist_ok=True)

    def _check_service_state(self) -> None:
        """
        The private method validates whether all services
        utilized by the ObzAI Client are ready to log data.

        Raises:
            RuntimeError when AuthService is not authenticated or project is not initialized.
        """
        # (1) Check AuthService whether is authenticated.
        if not self.auth_service.authenticated:
            raise RuntimeError("ObzAI Client wasn't properly authenticated!")

        # (2) Check ProjectService whether project is initialized.
        if not self.project_service.project_ready:
            raise RuntimeError("Project wasn't correctly initialized!")

    def login(
            self, api_key: Optional[str] = None, override_credentials: bool = False
            ) -> None:
        """
        The method authenticates user and unlocks connection to ObzAI API.

        Args:
            api_key: (string) Your ObzAI API key enabling connection with our API. 
                If not provided, attempts to read cached locally credentials.
            override_credentials: (bool) If True will override cached locally credentials.
        
        Raises:
            ObzClientError in case authentication fails.
        """
        try:
            self.auth_service.authenticate(api_key=api_key, override_credentials=override_credentials)
            logger.info("Authentication successful.")
        except Exception as e:
            logger.exception("Authentication failed.")
            raise ObzClientError("Authentication failed") from e

    def setup_project(
            self, 
            project_name: str,
            ml_task: Optional[MLTask] = None,
            index2name: Optional[Dict[int, str]] = None
            ) -> None:
        """
        Creates or connects to a project at the ObzAI Platform. When a new
        project is created and data inspectors are available, reference data is
        uploaded automatically.

        Args:
            project_name: (str) Name of the project to connect to.
            ml_task: (MLTask Enum) Expected ML task. Must be provided if project does not exist.
            index2name: (dict) Optional mapping of prediction indices to names. Used when creating a project.
        
        Raises:
            ObzClientError when project setup fails.
        """
        # (1) Check whether client is authenticated.
        if not self.auth_service.authenticated:
            # (1.1) Attempt to log with cache credentials.
            logger.info("Not logged in – attempting to authenticate with cached credentials.")
            try:
                self.login()
            except ObzClientError as e:
                logger.exception("Authentication failed during project connection.")
                raise ObzClientError("Error occured during authentication. Connection to the project failed.") from e

        # (2) Retrieve inspectors metadata
        if self._data_inspectors is not None:
            inspectors_metadata = [inspctr.metadata for inspctr in self._data_inspectors]
        else:
            inspectors_metadata = None

        # (3) Setup project using the unified endpoint
        try:
            setup_response = self.project_service.setup_project(
                api_key=self.auth_service.api_key,
                project_name=project_name,
                ml_task=ml_task,
                index2name=index2name,
                inspectors_metadata=inspectors_metadata,
            )
        except ProjectSetupError as setup_err:
            logger.exception("Project setup failed.")
            raise ObzClientError(f"Error occured during project setup: {setup_err}") from setup_err
        except Exception as e:
            logger.exception("Unexpected error occured during project setup.")
            raise ObzClientError(f"Error occured during connection to the project: {e}") from e

        action = setup_response.get("action")
        message = setup_response.get("message")

        if action == "created":
            logger.info(message)
            if self._data_inspectors:
                logger.info("Uploading reference data to a newly created project ...")
                try:
                    self._log_reference()
                except Exception as err:
                    logger.exception("Error occured during logging reference data.")
                    raise ObzClientError(f"Error occured during logging reference data: {err}") from err
            else:
                logger.info("Skipping reference data upload - no Data Inspectors were provided.")
        elif action == "reused":
            logger.info(message)

    def run_inspectors(
            self, input_images: TensorOrSequenceOrDict, return_results: bool = False
            ) -> Optional[List[DataInspectionResults]]:
        """
        The method performs data inspection with Data Inspectors provided during ObzAI Client initialization.

        Args:
            input_images: Batch of input images provided in the following forms:
                (i) a simple torch.Tensor of shape (B, C, H, W) or (B, C, D, H, W);
                (ii) a tuple[torch.Tensor, ...] or a list[torch.Tensor, ...] containing images at the first position;
                (iii) a dict[str, torch.Tensor | Any] containing images under key `images`.
            return_results: (bool) Boolean flag indicating whether results should be returned or not.
        
        Raises:
            ObzClientError when running data inspectors fails

        Returns:
            data_inspection_results: (List[DataInspectionResults]) Return results of inspection, if return_results was set True.
        """
        # (1) Check whether Data Inspectors are available
        if self._data_inspectors is None:
            msg = "Data Inspector instances weren't provided during the client initialization."
            logger.error(msg)
            raise ObzClientError(msg)
        
        # (2) Clear cache 
        self.cache_service.clear_data_inspection_results()
        
        # (3) Feed Data Inspectors with an input batch
        data_inspection_results_lst = []
        for inspector in self._data_inspectors:
            try:
                inspection_results = inspector.inspect(input_images=input_images)
            except DataInspectorError as e:
                logger.error(f"DataInspector {inspector.__class__.__name__} failed during inspection.")
                raise ObzClientError(f"An error occured during data inspection: {e} ") from e
            data_inspection_results_lst.append(inspection_results)

        # (4) Cache results
        self.cache_service.add_results_data(data_inspection_results=data_inspection_results_lst)

        # (5) Return results if needed
        if return_results:
            return data_inspection_results_lst
        
    def run_explainers(
            self, images: torch.Tensor, target_idxs: Union[int, List[int]], return_results: bool = False) -> Optional[List[XAIResults]]:
        """
        The method prepares XAI maps for input images utilizing XAI Tools provided during the client initialization.

        Args:
            images: (torch.Tensor) Torch Tensor of images for predictions must be explained.
            target_idxs: (integer or list of integers) Target indices for which XAI maps should be prepared. It affects only target-aware XAI methods.
            return_results: (bool) Boolean flag indicating whether return results or not.
        
        Raises:
            ObzClientError when running XAI tools fails.    
        
        Returns:
            xai_results: (List[XAIResults]) List of achieved XAI Results.
        """
        # (1) Check whether XAI Tools are available
        if self._xai_tools is None:
            msg = "XAI Tools weren't provided during the client initialization. Preparing XAI Maps not possible."
            logger.error(msg)
            raise ObzClientError(msg)
        
        # (2) Clear cache
        self.cache_service.clear_xai_results()

        # (3) Feed XAI Tools with input batch
        xai_results_lst = []
        for tool in self._xai_tools:
            try:
                if tool.requires_target:
                    xai_results = tool.explain(images, target_idxs)
                else:
                    xai_results = tool.explain(images)
            except XAIToolError as e:
                logger.error(f"XAI Tool {tool.__class__.__name__} failed during explanation.")
                raise ObzClientError(f"XAI Tool {tool.__class__.__name__} failed during explanation: {e}") from e
            xai_results_lst.append(xai_results)

        # (4) Cache results
        self.cache_service.add_results_data(xai_results = xai_results_lst)
        
        # (5) Return results if needed
        if return_results:
            return xai_results_lst

    def log(
            self, 
            input_images: TensorOrSequenceOrDict, 
            predictions: torch.Tensor
            ) -> None:
        """
        The method logs data obtained with ObzAI Client to the ObzAI Dashboard.

        Args:
            input_images: Batch of input images provided in the following forms:
                (i) a simple torch.Tensor of shape (B, C, H, W) or (B, C, D, H, W);
                (ii) a tuple[torch.Tensor, ...] or a list[torch.Tensor, ...] containing images at the first position;
                (iii) a dict[str, torch.Tensor | Any] containing images under key `images`.
            predictions (torch.Tensor): Model output predictions.
                Expected shape depends on the task:
                    - For regression: 2D tensor (B, K), where K is the number of predicted variables.
                    - For classification: 2D tensor (B, K), where K is the number of classes.
                    - For translation: 4D (B, C, H, W) or 5D tensor (B, C, D, H, W).
                    - For segmentation: 4D tensor (B, C, H, W).
        
        Raises:
            ObzClientError when logging data fails
        """
        # (1) Ensure that all services are ready to log data.
        try:
            self._check_service_state()
        except Exception as e:
            logger.exception("Services not ready for logging: %s", str(e))
            raise ObzClientError("ObzAI Client's services are not ready for logging data.") from e
        
        # (2) Retrieve data from the cache
        cached_results = self.cache_service.retrieve_results_data()

        # (3) Upload data with the UploadService
        try:
            self.upload_service.upload_inference_log(
                api_key=self.auth_service.api_key,
                project_meta=self.project_service.project_meta,
                input_images=input_images,
                predictions=predictions,
                xai_results=cached_results.get("xai_results", None),
                data_inspection_results=cached_results.get("data_inspection_results", None)
            )
            logger.info("Succesfully logged inference data.")
        except Exception as e:
            logger.exception("Failed to upload inference data: %s", str(e))
            raise ObzClientError("Error occured during logging inference data.") from e

        # Clear data cache
        self.cache_service.clear_cache()

    def _log_reference(self) -> None:
        """
        Private helper to log reference data from fitted Data Inspectors.
        
        Raises:
            ObzClientError when logging reference data fails.
        """

        # (1.1) Check whether ObzClient is ready to upload reference data
        try:
            self._check_service_state()
        except Exception as e:
            logger.exception("Services not ready for logging reference data.")
            raise ObzClientError("ObzAI Client's services are not ready for logging data.") from e
        
        # (1.2) Check whether there are any Data Inspectors
        if self._data_inspectors is None or self.project_service.project_meta.data_inspector_local2remote_id is None:
            logger.error("Logging reference data failed. Data Inspector instances not available.")
            raise ObzClientError("Data Inspector instances weren't provided during ObzClient initialization.")

        # (2) Retrieve reference data from Data Inspectors
        try:
            reference_data = [inspector.load_reference_data() for inspector in self._data_inspectors]
        except Exception as e:
            logger.exception("Failed to retrieve reference data from Data Inspectors.")
            raise ObzClientError("Error occured during retrieving reference features from data inspector.") from e

        # (3) Upload reference data to the ObzAI platform.
        try:
            self.upload_service.upload_reference_log(
                api_key=self.auth_service.api_key,
                reference_data=reference_data,
                data_inspector_local2remote_id=self.project_service.project_meta.data_inspector_local2remote_id
            )
            logger.info("Successfully uploaded reference data.")
        except Exception as e:
            logger.exception("Error occured during logging reference data.")
            raise ObzClientError(f"Error occured during logging reference data: {e}") from e
