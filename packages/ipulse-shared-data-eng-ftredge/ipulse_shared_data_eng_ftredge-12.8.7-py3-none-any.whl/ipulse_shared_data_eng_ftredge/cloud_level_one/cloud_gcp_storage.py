# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-raised
import json
import csv
from io import BytesIO, StringIO, TextIOWrapper
import os
import time
from typing import Optional
from google.api_core.exceptions import NotFound
from google.cloud.storage import Client as GCSClient
from ipulse_shared_base_ftredge import (DuplicationHandling,
                                        DuplicationHandlingStatus,
                                        MatchCondition,
                                        DataResource,
                                        Alert,
                                        LogLevel,
                                        Action,
                                        ProgressStatus,
                                        StructLog,
                                        FileExtension,
                                        log_error, log_by_lvl)
from ipulse_shared_data_eng_ftredge import (Pipelinemon)

from ..pipelines.pipe_and_ops_exceptions import handle_pipeline_operation_exception
import inspect
from ..pipelines import FunctionResult


###########################################################################################
############################### GCP CLOUD STORAGE EXTENDED FUNCTIONS ######################
###########################################################################################


def read_file_from_gcs_extended(storage_client:GCSClient, bucket_name:str, file_path:str,
                                 file_extension:Optional[FileExtension]=None,
                                 pipelinemon: Optional[Pipelinemon] = None, logger=None, print_out=False, raise_e=False) -> FunctionResult:
    """Helper function to read a JSON or CSV file from Google Cloud Storage with optional Pipelinemon monitoring."""
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(bucket_name=bucket_name, file_path=file_path)

    try:
        # Determine the file extension
        base_file_name, ext = os.path.splitext(file_path)  # ext includes the dot (.) if present
        ext = ext.lower()
        if not ext:
            if file_extension:
                ext = str(file_extension)
                if not ext.startswith('.'):
                    ext = f".{ext}"
                file_path = f"{base_file_name}{ext}"
            else:
                raise ValueError(f"File '{file_path}' has no extension and no file_extension parameter provided.")
        else:
            if file_extension:
                expected_ext = str(file_extension)
                if not expected_ext.startswith('.'):
                    expected_ext = f".{expected_ext}"
                if ext != expected_ext:
                    raise ValueError(f"File extension '{ext}' does not match the expected extension '{expected_ext}'")

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)

        # Check if the blob (file) exists
        if not blob.exists():
            raise NotFound(f"File '{file_path}' not found in bucket '{bucket_name}'")

        # Download the file content
        data_string = blob.download_as_text()

        # Check if the file is empty , better alternative to if blob.size == 0 as blob.size might not be populated or accurate without reloading the blob metadata
        if not data_string:
            raise ValueError(f"File '{file_path}' is empty in bucket '{bucket_name}'")
        
        result.add_state("BLOB_DOWNLOADED")
        # Initialize data variable
        data = None

        # Parse the data based on file extension
        if ext == ".json":
            try:
                data = json.loads(data_string)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from GCS: {file_path} in bucket {bucket_name}: {e}") from e
        elif ext == ".ndjson":
            try:
                # Parse newline-delimited JSON (one JSON object per line)
                data = [json.loads(line) for line in data_string.strip().split('\n') if line.strip()]
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding NDJSON from GCS: {file_path} in bucket {bucket_name}: {e}") from e
        elif ext == ".csv":
            try:
                data_io = StringIO(data_string)
                reader = csv.DictReader(data_io)
                data = list(reader)
            except csv.Error as e:
                raise ValueError(f"Error reading CSV from GCS: {file_path} in bucket {bucket_name}: {e}") from e
        else:
            raise ValueError(f"Unsupported file extension '{ext}'")

        result.data = data
        result.add_metadata(total_records_fetched=len(data))
        result.final()

        if pipelinemon:
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=Action.READ_FILE,
                source=DataResource.GCS,
                destination=DataResource.IN_MEMORY_DATA,
                progress_status=result.progress_status,
                q=1,
                description=result.get_final_report()
            ))

        log_by_lvl(
            info_msg=f"{function_name}: Fetched File {file_path} successfully",
            debug_msg=result.get_final_report(),
            logger=logger,
            print_out=print_out
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_FILE,
            source=DataResource.GCS,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )

    return result

def write_file_to_gcs_extended(storage_client: GCSClient,
                               data: dict | list | str, bucket_name: str, file_path: str,
                                duplication_handling: DuplicationHandling,
                                duplication_match_condition_type: MatchCondition,
                                duplication_match_condition: str = "",
                                max_retries: int = 2,
                                max_deletable_files: int = 1,
                                file_extension: FileExtension = None,
                                json_format_if_json_used: str = "standard", # or "newline_delimited"
                                logger=None, print_out=False, raise_e=False, pipelinemon: Pipelinemon = None) -> FunctionResult:
    """Saves data to Google Cloud Storage with optional Pipelinemon monitoring.
    
    Args:
        json_format: Format for JSON files. "standard" (default) creates regular JSON with indentation.
                    "newline_delimited" creates NEWLINE_DELIMITED_JSON format (one object per line) for BigQuery.
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(bucket_name=bucket_name, file_path=file_path)

    try:
        max_deletable_files_allowed = 3
        cloud_storage_ref = DataResource.GCS

        # GCS-related metadata
        saved_to_path = None
        matched_duplicates_count = 0
        matched_duplicates_deleted = []
        data_str = None
        data_bytes = None
        content_type = None

        increment = 0
        attempts = 0
        success = False
        supported_duplication_handling = [DuplicationHandling.RAISE_ERROR, DuplicationHandling.SKIP, DuplicationHandling.OVERWRITE, DuplicationHandling.INCREMENT]
        supported_match_condition_types=[MatchCondition.PREFIX, MatchCondition.EXACT]

        if max_deletable_files > max_deletable_files_allowed:
            raise ValueError(f"max_deletable_files should be less than or equal to {max_deletable_files_allowed} for safety.")
        if duplication_handling not in supported_duplication_handling:
            msg = f"Error: Duplication handling not supported. Supported types: {[dh for dh in supported_duplication_handling]}"
            raise ValueError(msg)
        if duplication_match_condition_type not in supported_match_condition_types:
            msg = f"Error: Match condition type not supported. Supported types: {[mct for mct in supported_match_condition_types]}"
            raise ValueError(msg)
        elif duplication_match_condition_type != MatchCondition.EXACT and not duplication_match_condition:
            msg = f"Error: Match condition is required for match condition type: {duplication_match_condition_type}"
            raise ValueError(msg)

        # Determine extension
        base_file_name, ext = os.path.splitext(file_path) ## ext is the file extension with the dot (.) included
        ext = ext.lower()
        if not ext:
            if file_extension:
                ext = str(file_extension)
                if not ext.startswith('.'):
                    ext = f".{ext}"
                file_path = f"{base_file_name}{ext}"
            else:
                raise ValueError(f"File '{file_path}' has no extension and no file_extension parameter provided.")
        else:
            if file_extension:
                expected_ext = str(file_extension)
                if not expected_ext.startswith('.'):
                    expected_ext = f".{expected_ext}"
                if ext != expected_ext:
                    raise ValueError(f"File extension '{ext}' does not match the expected extension '{expected_ext}'")

        if ext == '.json' or ext == '.ndjson':
            if isinstance(data, (list, dict)):
                # For .ndjson files or explicit newline_delimited format, use NDJSON
                if ext == '.ndjson' or (json_format_if_json_used == "newline_delimited" and isinstance(data, list)):
                    # Newline-delimited JSON format (one object per line) for BigQuery
                    data_str = "\n".join([json.dumps(item) for item in data])
                else:
                    # Standard JSON format with indentation
                    data_str = json.dumps(data, indent=2)
            else:
                # Assume data is already a string (pre-formatted NDJSON or JSON)
                data_str = str(data)
            data_bytes = data_str.encode('utf-8')  # Encode the string to UTF-8 bytes
            content_type = 'application/json' if ext == '.json' else 'application/x-ndjson'
        elif ext == '.csv':
            # Convert data to CSV
            if isinstance(data, (list, dict)):
                output_bytes = BytesIO()
                output_text = TextIOWrapper(output_bytes, encoding='utf-8', newline='\n')
                if isinstance(data, dict):
                    data = [data]
                if len(data) == 0:
                    raise ValueError("Cannot write empty data to CSV.")
                fieldnames = data[0].keys()
                writer = csv.DictWriter(output_text, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
                writer.writeheader()
                writer.writerows(data)
                output_text.flush()
                output_bytes.seek(0)
                data_bytes = output_bytes.getvalue()
                data_bytes = data_bytes.rstrip(b'\n')
            else:
                data_bytes = data.encode('utf-8')  # Assuming data is already a CSV-formatted string
            content_type = 'text/csv'
        else:
            raise ValueError(f"Unsupported file extension '{ext}'")

        result.add_state("DATA_SERIALIZED_READY_FOR_EXPORT")
        # Check for existing files based on duplication_match_condition_type
        files_matched_on_condition = []
        bucket = storage_client.bucket(bucket_name)
        if duplication_match_condition_type == MatchCondition.PREFIX:
            files_matched_on_condition = list(bucket.list_blobs(prefix=duplication_match_condition))
        elif duplication_match_condition_type == MatchCondition.EXACT:
            duplication_match_condition = file_path if not duplication_match_condition else duplication_match_condition
            if bucket.blob(duplication_match_condition).exists():
                files_matched_on_condition = [bucket.blob(file_path)]

        matched_duplicates_count = len(files_matched_on_condition)
        result.add_metadata(matched_duplicates_count=matched_duplicates_count)

        # Handle duplication based on duplication_handling
        if matched_duplicates_count:
            result.add_state(f"DUPLICATE_FOUND: {matched_duplicates_count} matched files")
            
            if pipelinemon:
                pipelinemon.add_log(StructLog(
                    level=LogLevel.NOTICE,
                    alert=Alert.FILE_ALREADY_EXISTS,
                    source=DataResource.GCS,
                    q=matched_duplicates_count,
                    description=result.get_final_report()
                ))

            if duplication_handling == DuplicationHandling.RAISE_ERROR:
                raise FileExistsError("File(s) matching the condition already exist.")

            if duplication_handling == DuplicationHandling.SKIP:
                result.add_metadata(duplication_handling_status=DuplicationHandlingStatus.SKIPPED)
                result.add_state("SKIPPING_DUPLICATE")
                return result

            if duplication_handling == DuplicationHandling.OVERWRITE:
                if matched_duplicates_count > max_deletable_files:
                    raise ValueError(f"Error: Attempt to delete {matched_duplicates_count} matched files, but limit is {max_deletable_files}. Operation Cancelled.")

                for blob in files_matched_on_condition:
                    cloud_storage_path_to_delete = f"gs://{bucket_name}/{blob.name}"
                    blob.delete()
                    matched_duplicates_deleted.append(cloud_storage_path_to_delete)
                    result.add_state(f"DELETED_DUPLICATE: {cloud_storage_path_to_delete}")
                    if pipelinemon:
                        pipelinemon.add_system_impacted(f"delete: {cloud_storage_ref}_bucket_file: {cloud_storage_path_to_delete}")
                        pipelinemon.add_log(StructLog(
                            level=LogLevel.INFO,
                            action=Action.PERSIST_DELETE_FILE,
                            resource=DataResource.GCS,
                            progress_status=ProgressStatus.DONE,
                            q=len(matched_duplicates_deleted),  # Add quantity for deleted files
                            description=f"Deleted duplicate file: {cloud_storage_path_to_delete}"
                        ))
                    
                result.add_metadata(matched_duplicates_deleted=matched_duplicates_deleted, duplication_handling_status=DuplicationHandlingStatus.OVERWRITTEN)

            elif duplication_handling == DuplicationHandling.INCREMENT:
                while bucket.blob(file_path).exists():
                    increment += 1
                    file_path = f"{base_file_name}_v{increment}{ext}"
                saved_to_path = f"gs://{bucket_name}/{file_path}"
                result.add_metadata(duplication_handling_status=DuplicationHandlingStatus.INCREMENTED)
                result.add_state("INCREMENTING_AS_DUPLICATE_FOUND")

        # GCS Upload
        saved_to_path = f"gs://{bucket_name}/{file_path}"
        while attempts < max_retries and not success:
            try:
                blob = bucket.blob(file_path)
                blob.upload_from_string(data_bytes, content_type=content_type)
                result.add_state(f"UPLOAD_COMPLETE: {saved_to_path}")
                if pipelinemon:
                    pipelinemon.add_system_impacted(f"upload: {cloud_storage_ref}_bucket_file: {saved_to_path}")
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.INFO,
                        action=Action.PERSIST_WRITE_FILE,
                        source=DataResource.IN_MEMORY_DATA,
                        destination=DataResource.GCS,
                        progress_status=ProgressStatus.DONE,
                        q=1,
                        description=result.get_final_report()
                    ))
                success = True
            except Exception as e:
                attempts += 1
                if attempts < max_retries:
                    time.sleep(2 ** attempts)
                else:
                    raise e
        result.add_metadata(saved_to_path=saved_to_path if success else None)
        result.final(force_status=ProgressStatus.DONE if success else ProgressStatus.FAILED)

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_WRITE_FILE,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.GCS,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )

    return result




###########################################################################################
############################### GCP CLOUD STORAGE SIMPLE FUNCTIONS ######################
###########################################################################################


def read_json_from_gcs(storage_client:GCSClient, bucket_name:str, file_name:str, logger=None,print_out=False, raise_e=False):
    """ Helper function to read a JSON or CSV file from Google Cloud Storage """

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data = json.loads(data_string)
        return data
    except NotFound as exc:
        msg = f"The file {file_name} was not found in the bucket {bucket_name}."
        log_error(msg=msg, exc_info=True, logger=logger, print_out=print_out)
        if raise_e:
            raise ValueError(msg) from exc
        return None
    except json.JSONDecodeError as exc:
        msg = f"Error: The file {file_name} could not be decoded as JSON. In bucket '{bucket_name} "
        log_error(msg=msg ,exc_info=True, logger=logger, print_out=print_out)
        if raise_e:
            raise ValueError(msg) from exc
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", exc_info=True, logger=logger, print_out=print_out)
        if raise_e:
            raise e from e
        return None

def read_csv_from_gcs(bucket_name:str, file_name:str, storage_client:GCSClient, logger=None, print_out=False):
    """ Helper function to read a CSV file from Google Cloud Storage """

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data_file = StringIO(data_string)
        reader = csv.DictReader(data_file)
        return list(reader)
    except NotFound:
        log_error(msg=f"Error: The file {file_name} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
        return None
    except csv.Error:
        log_error(msg=f"Error: The file {file_name} could not be read as CSV.", logger=logger, print_out=print_out)
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", logger=logger, print_out=print_out, exc_info=True)
        return None