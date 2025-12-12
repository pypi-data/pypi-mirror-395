"""Datatables Module for SWS API.

This module provides functionality for managing datatables, including retrieving
information, exporting data, and handling CSV paths through the SWS API client.
"""

import logging
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from sws_api_client.sws_api_client import SwsApiClient
from typing import Literal
from datetime import datetime
from time import sleep
from sws_api_client.s3 import S3
import json
logger = logging.getLogger(__name__)

class LabelModel(BaseModel):
    """Model for multilingual labels.

    Attributes:
        en (str): English label text
    """
    en: str

class DescriptionModel(BaseModel):
    """Model for multilingual descriptions.

    Attributes:
        en (str): English description text
    """
    en: str

class ColumnModel(BaseModel):
    """Model representing a datatable column.

    Attributes:
        id (str): Column identifier
        label (LabelModel): Column labels in different languages
        description (DescriptionModel): Column descriptions in different languages
        type (str): Data type of the column
        constraints (List[Any]): List of column constraints
        defaultValue (Optional[Any]): Default value for the column
        facets (List[Any]): List of column facets
    """
    id: str
    label: LabelModel
    description: DescriptionModel
    type: str
    constraints: List[Any]
    defaultValue: Optional[Any]
    facets: List[Any]

class DataModel(BaseModel):
    """Model representing datatable data status.

    Attributes:
        url (Optional[str]): URL to access the data
        available (bool): Whether the data is available
        uptodate (bool): Whether the data is up to date
    """
    url: Optional[str]
    available: bool
    uptodate: bool

class DatatableModel(BaseModel):
    """Model representing a complete datatable.

    Attributes:
        id (str): Datatable identifier
        name (str): Name of the datatable
        label (LabelModel): Labels in different languages
        description (DescriptionModel): Descriptions in different languages
        schema_name (str): Schema name
        domains (List[str]): List of associated domains
        plugins (List[Any]): List of associated plugins
        columns (List[ColumnModel]): List of table columns
        facets (List[Any]): List of table facets
        last_update (datetime): Last update timestamp
        data (DataModel): Data status information
    """
    id: str
    name: str
    label: LabelModel
    description: DescriptionModel
    schema_name: str = Field(..., alias="schema")
    domains: List[str]
    plugins: List[Any]
    columns: List[ColumnModel]
    facets: List[Any]
    last_update: datetime
    data: DataModel

class Datatables:
    """Class for managing datatable operations through the SWS API.

    This class provides methods for retrieving datatable information
    and managing data exports.

    Args:
        sws_client (SwsApiClient): An instance of the SWS API client
    """

    def __init__(self, sws_client: SwsApiClient) -> None:
        """Initialize the Datatables manager with SWS client."""
        self.sws_client = sws_client
        self.s3_client = S3(sws_client)
    
    def get_datatable_info(self, datatable_id: str) -> DatatableModel:
        """Retrieve information about a specific datatable.

        Args:
            datatable_id (str): The identifier of the datatable

        Returns:
            DatatableModel: Datatable information if found, None otherwise
        """
        url = f"/datatables/{datatable_id}"

        response = self.sws_client.discoverable.get('datatable_api', url)
        if(response.get('id') is not None):
            return DatatableModel(**response)
        else:
            return None
        
    def invoke_export_datatable(self, datatable_id: str) -> Dict:
        """Trigger an export operation for a datatable.

        Args:
            datatable_id (str): The identifier of the datatable

        Returns:
            Dict: Response containing export operation status
        """
        url = f"/datatables/{datatable_id}/invoke_export_2_s3"

        response = self.sws_client.discoverable.post('datatable_api', url)

        return response

    def get_datatable_csv_path(self, datatable, timeout=60*15, interval=2) -> HttpUrl:
        """Get the CSV file path for a datatable, waiting for export if necessary.

        Args:
            datatable: The datatable identifier
            timeout (int): Maximum time to wait for export in seconds (default: 15 minutes)
            interval (int): Time between checks in seconds (default: 2)

        Returns:
            HttpUrl: URL to the CSV file

        Raises:
            TimeoutError: If export doesn't complete within timeout period
        """
        info = self.get_datatable_info(datatable)
        if info.data.available and info.data.uptodate:
            return info.data.url
        else:
            self.invoke_export_datatable(datatable)
            # get the updated info every interval seconds until the data are available to a maximum of timeout seconds
            start = datetime.now()
            while (datetime.now() - start).seconds < timeout:
                info = self.get_datatable_info(datatable)
                if info.data.available:
                    return info.data.url
                sleep(interval)

    def import_data_from_s3(self, datatable_id: str, file_path: str, mode: Literal['new', 'clone', 'append'] = 'append', separator: Optional[str] = ",", quote: Optional[str] = "\"", columns = []) -> dict:
        """Import a file to a datatable using S3 as data exchange

        Args:
            datatable_id (str): The id of the target data table.
            file_path (str): The file that needs to be ingested.
            mode (Literal[str]): The ingestion mode. can be one of:
                    - new: Cleans the target data table before ingesting.
                    - clone: Create a new data table with the data sent.
                    - append (default): Appends data to an existing data table.
            separator (Optional[str]): The separator of the csv file (default is ,).
            quote (Optional[str]): The quoting char of the strings in the csv (default is ").
            columns (str[]): The columns used to ingest data (default [] = all).

        Returns:
            str: status
        """
        s3_key = self.s3_client.upload_file_to_s3(file_path)
        
        url = f"/datatable/{datatable_id}/import/s3"

        cloneOnImport = False
        clearOnImport = False

        if mode == 'new':
            clearOnImport = True
        elif mode == 'clone':
            cloneOnImport = True
                
        dataPayload = {
            "format": "csv",
            "skip": 0,
            "cloneOnImport": cloneOnImport,
            "clearOnImport": clearOnImport,
            "hasHeader": True,
            "delimiter": separator,
            "quote": quote,
            "encoding": "UTF-8",
            "columns": columns
        }

        print(dataPayload)

        files = {
            'directives': (None, json.dumps(dataPayload)),
            's3Key': (None, s3_key)
        }
                    
        response = self.sws_client.discoverable.multipartpost('is_api', url, files=files)
        logger.info(f"Import data from s3 response: {response}")
        
        return response['success']

    def get_sql_queries(self, datatable_id: str, filter: Optional[Dict] = None, 
                       limit: Optional[int] = None, distinct: Optional[bool] = None,
                       group_by: Optional[list] = None, s3_export: Optional[bool] = None) -> Dict:
        """Generate SQL queries for datatable.

        Generates SQL queries based on various filter parameters for a specific datatable.

        Args:
            datatable_id (str): The ID of the datatable
            filter (Optional[Dict]): Filter criteria with structure {column: {operator: value}}
                Supported operators: equal, contains, startsWith, endsWith, in, higher, less, 
                higherOrEqual, lessOrEqual, isNull, isNotNull
                Example: {"country": {"equal": "USA"}, "population": {"higher": 1000000}}
            limit (Optional[int]): Numeric limit for results
            distinct (Optional[bool]): Whether to return only distinct rows
            group_by (Optional[list]): List of column names to group results by
            s3_export (Optional[bool]): S3 export flag

        Returns:
            Dict: Dictionary containing the query and optionally S3 information including 
                  originalQuery, bucketName, s3Key, queryHash, region

        Raises:
            Exception: If failed to generate SQL queries
        """
        url = f"/datatable/{datatable_id}/sql_queries"
        
        # Build the request body
        body = {}
        
        # Add optional parameters if provided
        if filter is not None:
            body["filter"] = filter
            logger.debug(f"Added filter to body: {filter}")
        if limit is not None:
            body["limit"] = limit
        if distinct is not None:
            body["distinct"] = distinct
        if group_by is not None:
            body["groupBy"] = group_by
        if s3_export is not None:
            body["s3Export"] = s3_export
        
        logger.debug(f"Final request body: {body}")
        logger.debug(f"Generating SQL queries for datatable {datatable_id}")
        
        try:
            result = self.sws_client.discoverable.post("session_api", url, data=body)
            logger.info(f"SQL queries generated successfully for datatable {datatable_id}")
            
            # Return the result as-is since the API already provides the correct format
            return result
        except Exception as e:
            logger.error(f"Failed to generate SQL queries for datatable {datatable_id}: {str(e)}")
            raise Exception(f"Failed to generate SQL queries: {str(e)}")