# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Union, List, Optional, Dict

# Types & Dataclasses
from obzai.xai.schemas.xai_results import XAIResults
from obzai.data_inspection.schemas.dataclasses import DataInspectionResults
from obzai.client.schemas.types import CachedResults

# Custom Exceptions
from obzai.client.schemas.exceptions import CacheServiceError


class _CacheService:
    """
    Class enabling easy storage and removing
    of both XAI and Data Inspection results.
    """
    def __init__(self):
        """
        Constructs an instance of a CacheService object.
        """
        self._data_inspection_results: Optional[List[DataInspectionResults]] = None
        self._xai_results: Optional[List[XAIResults]] = None


    def add_results_data(
            self, 
            data_inspection_results: Optional[List[DataInspectionResults]] = None, 
            xai_results: Optional[List[XAIResults]] = None
            ) -> None:
        """
        The method adds new results into the Cache Service.

        Args:
            data_inspection_results: (Optional) List of DataInspectionResults objects.
            xai_results: (Optional) List of XAIResults objects.
        
        Raises:
            CacheServiceError when provided results_data argument is not valid.
        """
        if data_inspection_results is not None:
            if (isinstance(data_inspection_results, list) 
                and 
                all([isinstance(res, DataInspectionResults) for res in data_inspection_results])):
                self._data_inspection_results = data_inspection_results
            else: 
                raise CacheServiceError("Provided data_inspection_results argument is not valid.")
        
        if xai_results is not None:
            if (isinstance(xai_results, list) 
                and 
                all([isinstance(res, XAIResults) for res in xai_results])):
                self._xai_results = xai_results
            else:
                raise CacheServiceError("Provided xai_results argument is not valid.")
    

    def retrieve_results_data(self) -> CachedResults:
        """
        The method returns all available data from the CacheService.
        In case there is no cached data, empty dict is returned.

        Returns:
            a dictionary containing available results
        """
        data_dict: CachedResults = {}

        # If available, return DataInspectionResults
        if self._data_inspection_results is not None:
            data_dict["data_inspection_results"] = self._data_inspection_results

        # If available, return XAIResults
        if self._xai_results is not None:
            data_dict["xai_results"] = self._xai_results
        
        return data_dict


    def clear_xai_results(self) -> None:
        """
        Removes XAI Results from the cache.
        """
        self._xai_results = None


    def clear_data_inspection_results(self) -> None:
        """
        Removes Data Inspection Results from the cache.
        """
        self._data_inspection_results = None


    def clear_cache(self) -> None:
        """
        Removes all data from the cache.
        """
        self.clear_xai_results()
        self.clear_data_inspection_results()  