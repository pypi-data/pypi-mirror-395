import logging
import warnings
from time import sleep
import os
import zipfile
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Union
from sws_api_client.codelist import Codelists
from sws_api_client.generic_models import Code, Multilanguage
from sws_api_client.sws_api_client import SwsApiClient
from sws_api_client.s3 import S3
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


warnings.filterwarnings(
    "ignore",
    message='Field name "schema" in "DatasetBinding" shadows an attribute in parent "BaseModel"',
)

logger = logging.getLogger(__name__)

class Lifecycle(BaseModel):
    state: str
    type: str
    previousState: Optional[str] = None
    created: int
    lastModified: Optional[int] = None
    lastModifiedBy: Optional[str] = None

class Domain(BaseModel):
    id: str
    label: Multilanguage
    description: Dict

class Binding(BaseModel):
    joinColumn: Optional[str] = None

class Dimension(BaseModel):
    id: str
    label: Multilanguage
    description: Dict
    sdmxName: Optional[str] = None
    codelist: str
    roots: List[str]
    binding: Optional[Binding] = None
    checkValidityPeriod: bool
    formulas: List
    type: str

class Dimensions(BaseModel):
    dimensions: List[Dimension]

class PivotingGrouped(BaseModel):
    id: str
    ascending: bool

class Pivoting(BaseModel):
    grouped: List[PivotingGrouped]
    row: PivotingGrouped
    cols: PivotingGrouped

class DatasetBinding(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    observationTable: Optional[str] = None
    coordinateTable: Optional[str] = None
    sessionObservationTable: Optional[str] = None
    metadataTable: Optional[str] = None
    metadataElementTable:  Optional[str] = None
    sessionMetadataTable: Optional[str] = None
    sessionMetadataElementTable: Optional[str] = None
    validationTable: Optional[str] = None
    sessionValidationTable: Optional[str] = None
    tagObservationTable: Optional[str] = None
    tags: Optional[List] = None
    schema: Optional[str] = None

class Dataset(BaseModel):
    id: str
    label: Multilanguage
    description: Dict
    sdmxName: Optional[str] = None
    lifecycle: Lifecycle
    domain: Domain
    dimensions: Dimensions
    flags: Dict
    rules: Dict
    pivoting: Pivoting
    pluginbar: Dict
    showEmptyRows: bool
    showRealCalc: bool
    useApproveCycle: bool
    binding: Optional[DatasetBinding] = None

class Fingerprint(BaseModel):
    empty: bool
    sessions: int
    queries: int
    tags: int
    computationTags: int
    modules: int
class DataModel(BaseModel):
    dataset: Dataset
    fingerprint: Optional[Fingerprint] = None

class MappedCode(BaseModel):
    code: Code
    include: bool
class Datasets:

    def __init__(self, sws_client: SwsApiClient) -> None:
        self.sws_client = sws_client
        self.codelists = Codelists(sws_client)
        self.s3_client = S3(sws_client)

    def get_all(self) -> List[dict]:
        """Retrieve all datasets.

        Returns:
            List[Dataset]: List of all datasets
        """
        url = "/admin/dataset"
        response = self.sws_client.discoverable.get('is_api', url)
        return response

    def scan(self, dataset_id: str, body: dict) -> dict:
        """Scan a dataset using the session_api endpoint.

        Args:
            dataset_id (str): The dataset identifier.
            body (dict): The scan request body.

        Returns:
            dict: The scan response.
        """
        url = f"/dataset/{dataset_id}/scan"
        response = self.sws_client.discoverable.put('session_api', url, data=body, options={"json_body": True})
        return response

    def get_dataset_export_details(self, dataset_id: str) -> dict:

        url = f"/dataset/{dataset_id}/info"
        params = {"extended": "true"}

        response = self.sws_client.discoverable.get('session_api', url, params=params)

        return response
    
    def get_dataset_info(self, dataset_id: str) -> DataModel:

        url = f"/admin/dataset/{dataset_id}"

        response = self.sws_client.discoverable.get('is_api', url)
        return DataModel(**response)

    def create_dataset(self, dataset: Dataset) -> DataModel:

        url = "/admin/dataset"

        response = self.sws_client.discoverable.post('is_api', url, data=dataset.model_dump())

        return response
    
    def clone_dataset(self, dataset_id: str, new_id: str) -> DataModel:

        dataset = self.get_dataset_info(dataset_id)
        dataset.dataset.id = new_id
        new_dataset = self.create_dataset(dataset.dataset)
        return new_dataset
    
    def get_job_status(self, jobId: str) -> dict:

        url = f"/job/status/{jobId}"

        response = self.sws_client.discoverable.get('is_api', url)

        result:bool = response.get('result')
        success:bool = response.get('success')
        return dict(result=result, success=success)

    def import_data(
        self,
        dataset_id: str,
        file_path,
        sessionId = None,
        zip=False,
        data: bool = True,
        metadata: bool = False,
        separator: str = ",",
        quote: str = "\"",
        isS3: bool = False
    ) -> bool:
        """Import data into a dataset, optionally including metadata and custom CSV settings."""

        if isS3:
            return self.import_data_from_s3(
                dataset_id,
                file_path,
                sessionId,
                data=data,
                metadata=metadata,
                separator=separator,
                quote=quote
            )

        return self.import_data_chunk(
            dataset_id,
            file_path,
            sessionId,
            data=data,
            metadata=metadata,
            separator=separator,
            quote=quote
        )

    def import_data_from_s3(
        self,
        dataset_id: str,
        file_path: str,
        sessionId: Optional[int] = None,
        data: Optional[bool] = True,
        metadata: Optional[bool] = False,
        separator: Optional[str] = ",",
        quote: Optional[str] = "\""
    ) -> dict:

        is_zip = zipfile.is_zipfile(file_path)
        mediaType = 'application/zip' if is_zip else 'text/csv'

        s3_key = self.s3_client.upload_file_to_s3(file_path)

        url = "/observations/import-v2"

        dataset_info = self.get_dataset_info(dataset_id)

        scope: List[str] = ["DATA"]

        if data and metadata:
            scope = ["DATA", "METADATA"]

        dataPayload = {
            "domain": dataset_info.dataset.domain.id,
            "dataset": dataset_id,
            "sessionId": -1 if sessionId is None else sessionId,
            "format": "CSV",
            "scope": scope,
            "execution": "ASYNC",
            "fieldSeparator": separator,
            "quoteOptions": quote,
            "filedownload": "ASYNC",
            "lineSeparator": "\n",
            "headers": "CODE",
            "structure": "NORMALIZED",
            "s3Key": s3_key,
            "mediaType": mediaType
        }

        response = self.sws_client.discoverable.post('is_api', url, data=dataPayload)
        logger.debug(f"Import data from s3 response: {response}")

        job_id = response['result']
        return self.get_job_result(job_id, sleepTime=5)
        

    def get_dataset_dimension_codes(self, dataset_id: str) -> Dict[str, List[Code]]:
        dataset_info = self.get_dataset_info(dataset_id)
        dimensions = dataset_info.dataset.dimensions.dimensions

        # Fetch codelist codes for each dimension and use the dimension name for the CSV header
        dimensions_map:Dict[str, Dict[str, Dict[str, MappedCode]]] = {}
        for dimension in dimensions:
            logger.debug(f"Fetching codelist for dimension: {dimension}")
            codelist = self.codelists.get_codelist(dimension.codelist)
            # filter out codes that have more than 0 children
            
            dimensions_map[dimension.id] = {}
            for code in codelist.codes:
                dimensions_map[dimension.id][code.id] = {"code":code, "include":False}
        
        
        def include_children(code:Code, dimension_id:str):
            if dimensions_map[dimension_id][code.id]["include"] is False:
                dimensions_map[dimension_id][code.id]["include"] = True
            if len(code.children) > 0:
                for child in code.children:
                    if dimensions_map[dimension_id][child]["include"] is False:
                        dimensions_map[dimension_id][child]["include"] = True
                        include_children(dimensions_map[dimension_id][child]["code"], dimension_id)

        dimensions_codes = {}
        for dimension in dimensions:
            dimensions_codes[dimension.id] = []
            if len(dimension.roots) > 0:
                for root in dimension.roots:
                    # Check if root exists in the dimension's codelist
                    if root in dimensions_map[dimension.id]:
                        include_children(dimensions_map[dimension.id][root]["code"], dimension.id)
                    else:
                        logger.warning(f"Root code '{root}' not found in dimension '{dimension.id}' codelist")
                for code in dimensions_map[dimension.id]:
                    if dimensions_map[dimension.id][code]["include"]:
                        dimensions_codes[dimension.id].append(code)
            else:
                for code in dimensions_map[dimension.id]:
                    dimensions_codes[dimension.id].append(code)
        return dimensions_codes

    def get_sql_queries(self, dataset_id: str, include_history: bool, include_metadata: bool,
                       dimension: Optional[Dict] = None, value: Optional[Dict] = None,
                       flag: Optional[Dict] = None, metadata: Optional[Dict] = None,
                       s3_export: Optional[bool] = None, show_username: Optional[bool] = None,
                       sort_by_id: Optional[bool] = None, tags: Optional[list] = None,
                       limit: Optional[int] = None, metadata_as_array: Optional[bool] = None) -> Dict:
        """Generate SQL queries for dataset.

        Generates SQL queries based on various filter parameters for a specific dataset.

        Args:
            dataset_id (str): The ID of the dataset
            include_history (bool): Whether to include history
            include_metadata (bool): Whether to include metadata
            dimension (Optional[Dict]): Dimension filters with structure {dimensionId: filter_criteria}
            value (Optional[Dict]): Value filtering with equal, less, higher, lessOrEqual, higherOrEqual
            flag (Optional[Dict]): Flags filtering with key-value pairs
            metadata (Optional[Dict]): Metadata filtering with startsWith, endsWith, contains, equal
            s3_export (Optional[bool]): S3 export flag
            show_username (Optional[bool]): Show username flag
            sort_by_id (Optional[bool]): Sort by ID flag
            tags (Optional[list]): List of tag numbers
            limit (Optional[int]): Numeric limit for results
            metadata_as_array (Optional[bool]): Metadata as array flag

        Returns:
            Dict: Dictionary containing the query and optionally S3 information including 
                  originalQuery, bucketName, s3Key, queryHash, region

        Raises:
            Exception: If failed to generate SQL queries
        """
        url = f"/dataset/{dataset_id}/sql_queries"
        
        # Build the request body
        body = {
            "includeHistory": include_history,
            "includeMetadata": include_metadata
        }
        
        # Add optional parameters if provided
        if dimension is not None:
            body["dimension"] = dimension
            logger.debug(f"Added dimension filter to body: {dimension}")
        if value is not None:
            body["value"] = value
        if flag is not None:
            body["flag"] = flag
        if metadata is not None:
            body["metadata"] = metadata
        if s3_export is not None:
            body["s3Export"] = s3_export
        if show_username is not None:
            body["showUsername"] = show_username
        if sort_by_id is not None:
            body["sortById"] = sort_by_id
        if tags is not None:
            body["tags"] = tags
        if limit is not None:
            body["limit"] = limit
        if metadata_as_array is not None:
            body["metadataAsArray"] = metadata_as_array
        
        logger.debug(f"Final request body: {body}")
        logger.debug(f"Generating SQL queries for dataset {dataset_id}")
        
        try:
            result = self.sws_client.discoverable.post("session_api", url, data=body)
            logger.info(f"SQL queries generated successfully for dataset {dataset_id}")
            
            # Return the result as-is since the API already provides the correct format
            return result
        except Exception as e:
            logger.error(f"Failed to generate SQL queries for dataset {dataset_id}: {str(e)}")
            raise Exception(f"Failed to generate SQL queries: {str(e)}")

    def import_data_chunk(
        self,
        dataset_id: str,
        file_path: str,
        sessionId: Optional[int] = None,
        data: Optional[bool] = True,
        metadata: Optional[bool] = False,
        separator: Optional[str] = ",",
        quote: Optional[str] = "\""
    ) -> dict:
        """Helper function to import a single data chunk, zipping files over 10MB automatically."""

        is_zip = zipfile.is_zipfile(file_path)
        zip_file_path = None
        if not is_zip:
            # Check file size and zip if greater than 10MB
            if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10MB in bytes
                zip_file_path = f"{file_path}.zip"
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(file_path, arcname=os.path.basename(file_path))
                file_path = zip_file_path  # Use zipped file for upload
                is_zip = True
            else:
                is_zip = False

        url = "/observations/import"
        dataset_info = self.get_dataset_info(dataset_id)

        scope: Union[str, List[str]] = "DATA"
        if data and metadata:
            scope = ["DATA", "METADATA"]
        elif metadata:
            scope = "METADATA"

        dataPayload = {
            "domain": dataset_info.dataset.domain.id,
            "dataset": dataset_id,
            "sessionId": -1 if sessionId is None else sessionId,
            "format": "CSV",
            "scope": scope,
            "execution": "ASYNC",
            "fieldSeparator": separator,
            "quoteOptions": quote,
            "filedownload": "ASYNC",
            "lineSeparator": "\n",
            "headers": "CODE",
            "structure": "NORMALIZED",
        }

        file_name = os.path.basename(file_path)
        files = {"file": (file_name, open(file_path, 'rb'), "application/zip" if is_zip else "text/csv")}
        
        response = self.sws_client.discoverable.multipartpost('is_api', url, data=dataPayload, files=files)
        logger.debug(f"Import data response for chunk: {response}")

        # Clean up the zip file if it was created
        if zip_file_path:
            os.remove(zip_file_path)

        job_id = response['result']
        return self.get_job_result(job_id)

    def get_job_result(self, job_id: str, sleepTime: int = 5) -> bool:
        """Check job status until it's completed."""
        while True:
            logger.debug(f"Checking job status for job ID {job_id}")
            job_status = self.get_job_status(job_id)
            if job_status['result']:
                return job_status['success']

            if not job_status['result'] and not job_status['success']:
                return False
            sleep(sleepTime)

    def chunk_csv_file(self, file_path: str, chunk_size: int) -> List[str]:
        """Splits the CSV file into smaller chunks while preserving leading zeros for all columns except 'value'."""
        temp_files = []
        
        # Load the data in chunks and process each chunk
        for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size, dtype=str)):
            # Convert 'value' column to numeric, allowing other columns to stay as strings to preserve leading zeros
            if 'value' in chunk.columns:
                chunk['value'] = pd.to_numeric(chunk['value'], errors='coerce')
            
            chunk_file = f"{file_path}_chunk_{i}.csv"
            chunk.to_csv(chunk_file, index=False, quoting=1)  # quoting=1 ensures quotes around strings to preserve zeros
            temp_files.append(chunk_file)
        
        return temp_files

    def import_data_concurrent(
        self,
        dataset_id: str,
        file_path: str,
        sessionId: Optional[int] = None,
        data: bool = True,
        metadata: bool = False,
        separator: str = ",",
        quote: str = "\"",
        chunk_size: int = 10000,
        max_workers: int = 5
    ) -> None:
        """Splits the CSV and imports chunks concurrently with limited workers, showing progress in the logs."""
        
        # Step 1: Split the file into chunks
        chunk_files = self.chunk_csv_file(file_path, chunk_size)
        total_chunks = len(chunk_files)  # Total number of chunks for progress tracking
        completed_chunks = 0  # Initialize counter for completed chunks
        
        logger.info(f"Importing chunks: started")
        # Step 2: Use ThreadPoolExecutor to manage parallel imports
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_chunk = {
                executor.submit(
                    self.import_data_chunk,
                    dataset_id,
                    chunk_file,
                    sessionId,
                    data,
                    metadata,
                    separator,
                    quote
                ): chunk_file for chunk_file in chunk_files
            }
            results = []

            # Step 3: Collect and manage job statuses
            for future in as_completed(future_to_chunk):
                chunk_file = future_to_chunk[future]
                try:
                    chunk_result = future.result()
                    result = {"result": chunk_result, "chunk_file": chunk_file}
                    results.append(result)
                    logger.debug(f"Chunk {chunk_file} ended successfully")
                except Exception as exc:
                    logger.error(f"Chunk {chunk_file} generated an exception: {exc}")
                finally:
                    # Update and log progress
                    completed_chunks += 1
                    logger.info(f"Importing chunks: {completed_chunks}/{total_chunks} cmopleted")
        
        # Step 4: Wait for all jobs to complete and clean up temporary files
        for result in results:
            success = result.get('result')
            if not success:
                logger.error(f"Chunk {result.get('chunk_file')} failed to import.")
            else:
                logger.debug(f"Chunk {result.get('chunk_file')} completed successfully.")
                os.remove(result.get('chunk_file'))

        logger.info("Importing chunks: completed")



