# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-raised
import logging
import uuid
import datetime
import inspect
from typing import List, Dict, Any, Union, Optional, Tuple
from google.api_core.exceptions import NotFound
from google.cloud import  bigquery
from ipulse_shared_base_ftredge import (DataResource,
                                        LogLevel,
                                        Action ,
                                        Alert,
                                        ProgressStatus,
                                        StructLog ,
                                        DataUnit,
                                        log_info,
                                        log_warning,
                                        log_by_lvl,
                                        format_exception)
from ipulse_shared_base_ftredge.enums.enums_data_eng import BigqueryTableWriteOption

from ..pipelines import FunctionResult, Pipelinemon, handle_pipeline_operation_exception
from ..utils.utils_json import process_data_for_bigquery

###########################################################################################
#################################### BIGQUERY SCHEMA/TYPES Helpers ############################
###########################################################################################

def _convert_python_type_to_bigquery(value: Any) -> str:
    """
    Determine BigQuery column type from Python value.        
    Returns:
        str: BigQuery data type
    """
    if value is None:
        raise ValueError("Cannot determine BigQuery type from None value")
    if isinstance(value, datetime.datetime):
        return "TIMESTAMP"
    if isinstance(value, datetime.date):
        return "DATE"
    if isinstance(value, str):
        if not value.strip():
            raise ValueError("Cannot determine BigQuery type from empty string")
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
            return "DATE"
        except ValueError:
            return "STRING"
            
     # Handle boolean before int!
    if isinstance(value, bool):
        return "BOOLEAN"
    # Handle numeric types
    if isinstance(value, int):
        return "INTEGER"
    if isinstance(value, float):
        return "FLOAT"
        
    return "STRING"

def create_bigquery_schema_from_json_schema(json_schema: list) -> List[bigquery.SchemaField]:
    schema = []
    for field in json_schema:
        if "max_length" in field:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"], max_length=field["max_length"]))
        else:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]))
    return schema


def format_value_for_bigquery_sql(value: Any) -> str:
    """
    Format a Python value as a SQL literal string for BigQuery INSERT/UPDATE statements.
    
    Handles type-specific formatting and escaping for safe SQL construction.
    
    Args:
        value: Python value to format (None, bool, int, float, datetime, str, etc.)
        
    Returns:
        SQL literal string representation (e.g., "NULL", "TRUE", "'escaped string'", "TIMESTAMP('2025-11-23T10:00:00')")
        
    Examples:
        >>> format_value_for_bigquery_sql(None)
        'NULL'
        >>> format_value_for_bigquery_sql(True)
        'TRUE'
        >>> format_value_for_bigquery_sql(42)
        '42'
        >>> format_value_for_bigquery_sql(3.14)
        '3.14'
        >>> format_value_for_bigquery_sql(datetime(2025, 11, 23, 10, 0, 0))
        "TIMESTAMP('2025-11-23T10:00:00')"
        >>> format_value_for_bigquery_sql("O'Reilly")
        "'O\\'Reilly'"
    """
    if value is None:
        return "NULL"
    
    if isinstance(value, bool):
        return str(value).upper()  # TRUE/FALSE
    
    if isinstance(value, (int, float)):
        # Handle special float values
        if isinstance(value, float):
            if value != value:  # NaN check (NaN != NaN in Python)
                return "NULL"  # BigQuery doesn't support NaN
            if value == float('inf'):
                return "NULL"  # BigQuery doesn't support infinity
            if value == float('-inf'):
                return "NULL"  # BigQuery doesn't support negative infinity
        return str(value)
    
    if isinstance(value, datetime.datetime):
        return f"TIMESTAMP('{value.isoformat()}')"
    
    if isinstance(value, datetime.date):
        return f"DATE('{value.isoformat()}')"
    
    # String - escape single quotes for SQL
    escaped_value = str(value).replace("'", "\\'")
    return f"'{escaped_value}'"


def _convert_cerberus_type_to_bigquery(field_rules: dict) -> str:
    """Maps a Cerberus type to a BigQuery data type, handling custom rules."""

    if 'check_with' in field_rules:
        if field_rules['check_with'] == 'standard_str_date':
            return 'DATE'
        if field_rules['check_with'] == 'iso_str_timestamp':
            return 'TIMESTAMP'
        if field_rules['check_with'] == 'standard_str_time':
            return 'TIME'

    # Default type mapping if no custom rule is found
    type_mapping = {
        'string': 'STRING',
        'integer': 'INT64',
        'float': 'FLOAT64',
        'boolean': 'BOOL',
        'datetime': 'TIMESTAMP',
        'date': 'DATE',
        'time': 'TIME'
    }
    # Handle the case where 'type' is a list
    field_type = field_rules.get('type', 'string')
    if isinstance(field_type, list):
        # Choose the first valid type from the list or default to 'STRING'
        for ft in field_type:
            if ft in type_mapping:
                return type_mapping[ft]
        return 'STRING'  # Default if no valid type found
    else:
        return type_mapping.get(field_type, 'STRING')


def create_bigquery_schema_from_cerberus_schema(cerberus_schema: dict) -> List[bigquery.SchemaField]:
    """Converts a Cerberus validation schema to a BigQuery schema.
        Handles 'custom_date' and 'custom_timestamp' rules as DATE and TIMESTAMP.
    """
    bq_schema = []
    for field_name, field_rules in cerberus_schema.items():
        field_type = _convert_cerberus_type_to_bigquery(field_rules)  # Pass field_name for rule checks
        mode = 'REQUIRED' if field_rules.get('required') else 'NULLABLE'
        max_length = field_rules.get('maxlength')
        
        if max_length and field_type == 'STRING':
            field = bigquery.SchemaField(field_name, field_type, mode=mode, max_length=max_length)
        else:
            field = bigquery.SchemaField(field_name, field_type, mode=mode)
        
        bq_schema.append(field)

    return bq_schema


def get_bigquery_table_schema(
    table_full_path: str,
    project_id: Optional[str] = None,
    bigquery_client: Optional[bigquery.Client] = None
) -> Optional[List[bigquery.SchemaField]]:
    """
    Get the schema directly from an existing BigQuery table.
    This is more efficient than converting from Cerberus schema when you're validating 
    against an existing table structure.
    
    Args:
        table_full_path: Full table path (project.dataset.table)
        project_id: Optional GCP Project ID (if not included in table_full_path)
        bigquery_client: Optional pre-initialized BigQuery client
        
    Returns:
        List[bigquery.SchemaField]: Table schema or None if table doesn't exist
        
    Example:
        # Get schema from existing table
        schema = get_bigquery_table_schema("project.dataset.table")
        
        # Use for data loading instead of Cerberus conversion
        load_from_json_bigquery_table_extended(
            data=data,
            table_full_path="project.dataset.table",
            schema=schema  # Direct BigQuery schema
        )
    """
    try:
        # Parse table path
        path_parts = table_full_path.split('.')
        if len(path_parts) == 3:
            path_project_id, dataset_name, table_name = path_parts
            if project_id and project_id != path_project_id:
                raise ValueError(f"Conflicting project IDs: {project_id} vs {path_project_id} in path")
            project_id = path_project_id
        elif len(path_parts) == 2:
            if not project_id:
                raise ValueError("project_id is required when not included in table_full_path")
            dataset_name, table_name = path_parts
        else:
            raise ValueError(f"Invalid table_full_path format: {table_full_path}")

        # Initialize client if needed
        if not bigquery_client:
            bigquery_client = bigquery.Client(project=project_id)

        # Get table and return schema
        table_ref = bigquery.TableReference.from_string(table_full_path)
        table = bigquery_client.get_table(table_ref)
        return table.schema
        
    except NotFound:
        # Table doesn't exist - this is expected for new tables
        return None
    except Exception:
        # Silently return None for other errors - caller will handle it
        return None


def validate_records_against_bigquery_schema_extended(
    records: List[Dict[str, Any]],
    table_full_path: str,
    project_id: str,
    bigquery_client: Optional[bigquery.Client] = None,
    schema: Optional[List[bigquery.SchemaField]] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    max_errors_to_log: int = 10,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Validate records against BigQuery table schema.
    
    Checks REQUIRED vs NULLABLE fields and validates types (FLOAT64, STRING, DATE, TIMESTAMP).
    This replaces Cerberus validation with direct BigQuery schema validation.
    
    Args:
        records: List of dictionaries to validate
        table_full_path: Full table path (project.dataset.table)
        project_id: GCP Project ID
        bigquery_client: Optional pre-initialized BigQuery client
        schema: Optional BigQuery schema. If not provided, it will be fetched from the table.
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger
        max_errors_to_log: Maximum number of validation errors to log (default: 10)
        print_out: Whether to print validation results
        raise_e: Whether to raise exception on validation errors
        
    Returns:
        FunctionResult with:
        - data: List of validation errors (empty if all valid)
        - progress_status: DONE if all valid, DONE_WITH_WARNINGS if errors found
        - metadata: validation_errors_count, records_count, valid_records_count
        
    Example:
        result = validate_records_against_bigquery_schema_extended(
            records=transformed_records,
            table_full_path="project.dataset.table",
            project_id="my-project",
            bigquery_client=client,
            pipelinemon=pipelinemon,
            max_errors_to_log=10
        )
        
        if not result.is_success:
            # Handle validation errors
            for error in result.data:
                logger.warning(f"Validation error: {error}")
    """
    function_name = inspect.currentframe().f_code.co_name if inspect.currentframe() else "<unknown>"
    result = FunctionResult(function_name)
    
    try:
        # Initialize client if needed
        if not bigquery_client:
            bigquery_client = bigquery.Client(project=project_id)
        
        # Fetch BigQuery schema if not provided
        bq_schema = schema
        if not bq_schema:
            bq_schema = get_bigquery_table_schema(
                table_full_path=table_full_path,
                project_id=project_id,
                bigquery_client=bigquery_client
            )
        
        if not bq_schema:
            error_msg = f"Could not fetch schema for table {table_full_path}"
            result.progress_status = ProgressStatus.FAILED
            result.add_issue(error_msg)
            log_warning(msg=error_msg, logger=logger, print_out=print_out)
            return result
        
        # Validate each record
        all_validation_errors = []
        valid_records_count = 0
        
        for idx, record in enumerate(records):
            record_validation_errors = []
            
            for field in bq_schema:
                field_name = field.name
                field_mode = field.mode  # REQUIRED or NULLABLE
                field_type = field.field_type  # STRING, FLOAT64, DATE, TIMESTAMP, etc.
                record_value = record.get(field_name)
                
                # Check REQUIRED fields
                if field_mode == "REQUIRED" and record_value is None:
                    record_validation_errors.append(
                        f"Record {idx}: Field '{field_name}' is REQUIRED but value is None"
                    )
                
                # Type validation for non-None values
                if record_value is not None:
                    # Numeric types
                    if field_type in ("FLOAT64", "FLOAT", "NUMERIC", "BIGNUMERIC"):
                        if not isinstance(record_value, (int, float)):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected {field_type}, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Integer types
                    elif field_type in ("INT64", "INTEGER"):
                        if not isinstance(record_value, int):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected {field_type}, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # String type
                    elif field_type == "STRING":
                        if not isinstance(record_value, str):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected STRING, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Boolean types
                    elif field_type in ("BOOL", "BOOLEAN"):
                        if not isinstance(record_value, bool):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected {field_type}, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Date types
                    elif field_type == "DATE":
                        if not isinstance(record_value, (str, datetime.date)):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected DATE, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Timestamp types
                    elif field_type in ("TIMESTAMP", "DATETIME"):
                        if not isinstance(record_value, (str, datetime.datetime)):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected {field_type}, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Time type
                    elif field_type == "TIME":
                        if not isinstance(record_value, (str, datetime.time)):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected TIME, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Bytes type
                    elif field_type == "BYTES":
                        if not isinstance(record_value, (bytes, str)):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected BYTES, got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Complex types (ARRAY, STRUCT, RECORD, GEOGRAPHY, JSON) - validate as dict/list
                    elif field_type in ("ARRAY", "STRUCT", "RECORD", "JSON"):
                        if not isinstance(record_value, (list, dict)):
                            record_validation_errors.append(
                                f"Record {idx}: Field '{field_name}' expected {field_type} (list or dict), got {type(record_value).__name__} (value: {record_value})"
                            )
                    # Unknown type - log warning but don't fail
                    else:
                        record_validation_errors.append(
                            f"Record {idx}: Field '{field_name}' has unknown BigQuery type '{field_type}' - validation skipped"
                        )
            
            if record_validation_errors:
                all_validation_errors.extend(record_validation_errors)
            else:
                valid_records_count += 1
        
        # Update result
        result.add_metadata(
            validation_errors_count=len(all_validation_errors),
            records_count=len(records),
            valid_records_count=valid_records_count
        )
        
        if all_validation_errors:
            result.progress_status = ProgressStatus.DONE_WITH_WARNINGS
            result.data = all_validation_errors
            
            # Log errors (limited by max_errors_to_log)
            errors_to_log = all_validation_errors[:max_errors_to_log]
            for error in errors_to_log:
                log_warning(msg=error, logger=logger, print_out=print_out)
                if pipelinemon:
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.WARNING,
                        resource=DataResource.DB_BIGQUERY_TABLE,
                        action=Action.VALIDATE,
                        progress_status=ProgressStatus.FAILED,
                        description=error
                    ))
            
            if len(all_validation_errors) > max_errors_to_log:
                remaining_msg = f"... and {len(all_validation_errors) - max_errors_to_log} more validation errors"
                log_warning(msg=remaining_msg, logger=logger, print_out=print_out)
            
            summary_msg = f"Validation failed: {len(all_validation_errors)} errors in {len(records)} records. Valid: {valid_records_count}"
            log_warning(msg=summary_msg, logger=logger, print_out=print_out)
            
            if raise_e:
                raise ValueError(f"Validation failed with {len(all_validation_errors)} errors")
        else:
            result.progress_status = ProgressStatus.DONE
            result.data = []
            success_msg = f"Validation successful: All {len(records)} records valid"
            log_info(msg=success_msg, logger=logger, print_out=print_out)
        
        return result
        
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.VALIDATE,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            print_out=print_out,
            raise_e=raise_e
        )
    finally:
        result.final()
    return result


###########################################################################################
#################################### BIGQUERY JOBS HELPER FUNCTIONS ###############################
###########################################################################################

def _truncate_table_preserving_schema(
    table_full_path: str, 
    bigquery_client: bigquery.Client, 
    logger: Optional[logging.Logger] = None,
    print_out: bool = False
) -> bool:
    """
    Safely truncate a BigQuery table while preserving its schema, descriptions, and structure.
    This is better than WRITE_TRUNCATE which recreates the table and loses metadata.
    
    Args:
        table_full_path: Full BigQuery table path (project.dataset.table)
        bigquery_client: BigQuery client instance
        logger: Optional logger for status messages
        print_out: Whether to print status messages
        
    Returns:
        bool: True if truncation was successful, False otherwise
    """
    try:
        # Use DELETE to remove all rows while preserving table structure
        delete_query = f"DELETE FROM `{table_full_path}` WHERE true"
        
        log_info(
            msg=f"Truncating table {table_full_path} while preserving schema...",
            logger=logger,
            print_out=print_out
        )
        
        query_job = bigquery_client.query(delete_query)
        query_job.result()  # Wait for completion
        
        log_info(
            msg=f"✅ Successfully truncated {table_full_path} (schema preserved)",
            logger=logger,
            print_out=print_out
        )
        return True
        
    except Exception as e:
        error_msg = f"Failed to truncate table {table_full_path}: {format_exception(e)}"
        log_warning(
            msg=error_msg,
            logger=logger,
            print_out=print_out
        )
        return False


def _get_bigquery_job_details(job: Union[bigquery.LoadJob, bigquery.QueryJob, bigquery.CopyJob, bigquery.ExtractJob]) -> Dict[str, Any]:

    """
    Get BigQuery job status while preserving existing values through appending.
    Returns a status dict with appended values instead of overwriting.
    """
    details ={} # shortcut
    details["execution_errors_count"]= len(job.errors or [])
    details["execution_errors_detail"]=_summarize_bigquery_job_errors (job)
    details["bigquery_job_id"] = job.job_id or ""
    details["job_user_email"] = job.user_email or ""

    if isinstance(job, bigquery.QueryJob):
        details["total_bytes_billed"] = job.total_bytes_billed
        details["total_bytes_processed"] = job.total_bytes_processed
        details["cache_hit"] = job.cache_hit
        details["slot_millis"] = job.slot_millis
        details["num_dml_affected_rows"] = job.num_dml_affected_rows
        if job.started and job.ended:
            details["duration_ms"] = (job.ended - job.started).total_seconds() * 1000
    elif isinstance(job, bigquery.LoadJob): # Add LoadJob specifics
        if job.started and job.ended:
            details["job_duration_ms"] = (job.ended - job.started).total_seconds() * 1000
        details["job_output_bytes"] = job.output_bytes or 0
        details["job_output_rows"] = job.output_rows or 0    
    elif isinstance(job, (bigquery.CopyJob, bigquery.ExtractJob)): # Add any required fields for other job types
        pass # for now we will keep this empty, you might need to add specific fields

    return {str(job.job_id): details}

def _summarize_bigquery_job_errors(job: Union[bigquery.LoadJob, bigquery.QueryJob, bigquery.CopyJob, bigquery.ExtractJob], max_errors_to_log: int = 7) -> str:
    """Summarizes job errors for logging."""
    if job.errors:
        limited_errors = " >> ERRORS DURING JOB:\n"
        for error in job.errors[:max_errors_to_log]:
            if isinstance(error, dict) and "message" in error:
                limited_errors += error["message"] + "\n"
            else:
                limited_errors += str(error) + "\n"
        if len(job.errors) > max_errors_to_log:
            limited_errors += f"\n...and {len(job.errors) - max_errors_to_log} more errors."
        return limited_errors
    return ""

def _handle_query_job_result(query_job: Union[bigquery.LoadJob, bigquery.QueryJob, bigquery.CopyJob, bigquery.ExtractJob],
                             result: FunctionResult,
                             action: Action,
                             source: DataResource,
                             destination: DataResource,
                             max_job_issues_to_log: int = 7,
                             rows: Optional[List[bigquery.Row]] = None,
                             pipelinemon: Optional[Pipelinemon] = None,
                             logger: Optional[logging.Logger] = None,
                             single_column: bool = False,) -> None:
    """Helper to standardize query job result handling"""
    # Add job details and errors if any
    result.add_metadata(**_get_bigquery_job_details(job=query_job))
    q = 0  # Initialize with 0 for consistent tracking
    
    if query_job.state == "DONE":
        # Initialize data and records_fetched for read operations
        if rows is not None:  # Explicitly check if rows were provided (even if empty)
            if single_column:
                result.data = [row[0] for row in rows]  # Extract single column values
            else:
                result.data = [dict(row) for row in rows]
            q = len(result.data)
            result.add_metadata(records_fetched=q)
            result.add_state(f"FETCHED_{q}_RECORDS")
        
        # For DML operations (including MERGE), track affected rows
        if isinstance(query_job, bigquery.QueryJob) and query_job.num_dml_affected_rows is not None:
            q = query_job.num_dml_affected_rows
            result.add_metadata(records_affected=q)
            result.add_state(f"AFFECTED_{q}_RECORDS")
            
            # Add notice if no records were affected during DML operation
            if q == 0:
                notice_msg = f"No records were affected by the {action} operation. All records may already exist in the target table."
                result.add_notice(notice_msg)
                result.progress_status = ProgressStatus.DONE_WITH_NOTICES
                log_info(msg=notice_msg, logger=logger)
            
        # For load operations, track output rows
        if isinstance(query_job, bigquery.LoadJob) and query_job.output_rows is not None:
            q = query_job.output_rows
            result.add_metadata(records_loaded=q)
            result.add_state(f"LOADED_{q}_RECORDS")
            
            # Add notice if no records were loaded
            if q == 0:
                notice_msg = f"No records were loaded during the {action} operation. All records may already exist in the target table."
                result.add_notice(notice_msg)
                result.progress_status = ProgressStatus.DONE_WITH_NOTICES
                log_info(msg=notice_msg, logger=logger)

        # # Specially handle MERGE operations where we have attempted_count available
        # if action in [Action.PERSIST_MERGE_UPDATE_AND_INSERT_NEW_QUERY, 
        #               Action.PERSIST_MERGE_INSERT_NEW_AND_DONT_UPDATE_QUERY,
        #               Action.PERSIST_MERGE_UPDATE_DONT_INSERT_NEW_QUERY]:
        #     attempted_count = result.metadata.get("records_to_be_merged_count", 0)
        #     if attempted_count > 0 and q < attempted_count:
        #         notice_msg = f"Only {q} out of {attempted_count} records were affected. {attempted_count - q} records likely already exist in the target table."
        #         result.add_notice(notice_msg)
        #         result.progress_status = ProgressStatus.DONE_WITH_NOTICES
        #         log_info(msg=notice_msg, logger=logger)
        #     elif q == 0:
        #         notice_msg = f"No records were affected by the merge operation. All {attempted_count} records likely already exist in the target table."
        #         result.add_notice(notice_msg)
        #         result.progress_status = ProgressStatus.DONE_WITH_NOTICES
        #         log_info(msg=notice_msg, logger=logger)
        
        if query_job.errors:
            result.add_issue(f"{action}_JOB_COMPLETED_WITH_ERRORS")
            result.add_issue(_summarize_bigquery_job_errors(job=query_job, max_errors_to_log=max_job_issues_to_log), update_state=False)
            result.final(issues_allowed=True)
        else:
            result.add_state(f"{action}_COMPLETED")
    else:
        result.add_issue(f"{action} failed with state {query_job.state}")
        result.add_issue(_summarize_bigquery_job_errors(job=query_job, max_errors_to_log=max_job_issues_to_log), update_state=False)
    result.final()
    
    log_by_lvl(
        info_msg=f"{action} job completed with state {query_job.state}.",
        debug_msg=result.get_final_report(),
        logger=logger
    )
    
    if pipelinemon:
        # Use q_unit=DataUnit.DBROW for proper record type indication
        pipelinemon.add_log(StructLog(
            level=LogLevel.INFO if result.is_success else LogLevel.ERROR,
            action=action,
            source=source,
            destination=destination,
            progress_status=result.progress_status,
            q=q,  # Will be 0 if no records processed
            q_unit=DataUnit.DBROW,  # Indicate the unit is database records
            description=result.get_final_report()
        ))


###########################################################################################
#################################### BIGQUERY CREATE TABLE and LOAD FROM JSON ###############################
###########################################################################################


def create_or_replace_bigquery_table_extended(
    table_full_path: str,
    schema: List[bigquery.SchemaField],
    project_id: Optional[str] = None,
    replace_if_exists: bool = False,
    temp: bool = False,
    bigquery_client: Optional[bigquery.Client] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Creates a BigQuery table with the specified schema.

    Args:
        table_full_path: Full table path (project.dataset.table)
        schema: Table schema as list of SchemaField objects
        project_id: Optional GCP Project ID (if not included in table_full_path)
        replace_if_exists: If True, replace existing table
        temp: Whether this is a temporary table
        bigquery_client: Optional pre-initialized BigQuery client
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        
    Returns:
        FunctionResult with creation status
    """
    function_name = inspect.currentframe().f_code.co_name if inspect.currentframe() else "<unknown>"
    result = FunctionResult(function_name)

    try:
        # Parse table path
        path_parts = table_full_path.split('.')
        if len(path_parts) == 3:
            path_project_id, dataset_name, table_name = path_parts
            if project_id and project_id != path_project_id:
                raise ValueError(f"Conflicting project IDs: {project_id} vs {path_project_id} in path")
            project_id = path_project_id
        elif len(path_parts) == 2:
            if not project_id:
                raise ValueError("project_id is required when not included in table_full_path")
            dataset_name, table_name = path_parts
        else:
            raise ValueError(f"Invalid table_full_path format: {table_full_path}")

        result.add_metadata(
            project_id=project_id,
            dataset_name=dataset_name,
            table_name=table_name,
            table_full_path=table_full_path,
            replace_if_exists=replace_if_exists,
            temp=temp
        )

        # Initialize client if needed
        if not bigquery_client:
            bigquery_client = bigquery.Client(project=project_id)

        # Check if dataset exists
        dataset_ref = bigquery_client.dataset(dataset_name)
        try:
            bigquery_client.get_dataset(dataset_ref)
        except NotFound as e:
            raise ValueError(f"Dataset {dataset_name} does not exist. Please create it first via Terraform") from e

        # Check if table exists
        table_ref = dataset_ref.table(table_name)
        table_exists = False
        try:
            bigquery_client.get_table(table_ref)
            table_exists = True
            if pipelinemon:
                pipelinemon.add_log(StructLog(
                    level=LogLevel.NOTICE,
                    alert=Alert.ALREADY_EXISTS,
                    destination=DataResource.DB_BIGQUERY_TABLE,
                    description=f"Table {table_name} already existed in {dataset_name}."
                ))
        except NotFound:
            table_exists = False

        # Handle existing table

        if temp:
            del_action=Action.PERSIST_DELETE_TABLE_TEMP
            cr_action=Action.PERSIST_CREATE_OR_REPLACE_TABLE_TEMP
        else:
            del_action=Action.PERSIST_DELETE_TABLE
            cr_action=Action.PERSIST_CREATE_OR_REPLACE_TABLE
        if table_exists:
            if replace_if_exists:
                # Get the row count before deletion
                table = bigquery_client.get_table(table_ref)
                row_count = table.num_rows or 0
                
                # Delete the table
                bigquery_client.delete_table(table_ref)
                result.add_metadata(existing_table_deleted=True, deleted_row_count=row_count)
                result.add_state("TABLE_DELETED")
                msg = f"Table {table_name} in dataset {dataset_name} with {row_count} rows was deleted."
                log_by_lvl(debug_msg=result.get_final_report(), info_msg=msg, logger=logger, print_out=print_out)
                
                if pipelinemon:
                    pipelinemon.add_system_impacted(f"bigquery_delete_table: {table_name}")
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.INFO,
                        action=del_action,
                        destination=DataResource.DB_BIGQUERY_TABLE,
                        progress_status=ProgressStatus.DONE,
                        description=result.get_final_report(),
                        q=row_count,  # Record the number of rows that were in the deleted table
                        q_unit=DataUnit.DBROW  # Track by records, not tables
                    ))
            else:
            
                notice_msg = "CREATION_SKIPPED as Table exists and replace_if_exists=False"
                result.add_notice(notice_msg)
                result.final()
                
                if pipelinemon:
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.NOTICE,
                        action=cr_action,
                        destination=DataResource.DB_BIGQUERY_TABLE,
                        alert=Alert.ALREADY_EXISTS,
                        progress_status=result.progress_status,
                        description=notice_msg,
                        q=1,  # One table exists
                        q_unit=DataUnit.TABLE  # Table operation, not record operation
                    ))
                
                log_warning(
                    msg=notice_msg,
                    logger=logger,
                    print_out=print_out
                )
                return result

        # Create table
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        result.add_state("TABLE_CREATED")
        result.final()

        msg = f"Table {table_name} created in dataset {dataset_name}."
        log_by_lvl(debug_msg=result.get_final_report(), info_msg=msg, logger=logger, print_out=print_out)

        if pipelinemon:
            pipelinemon.add_system_impacted(f"bigquery_create_table: {table_name}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=Action.PERSIST_CREATE_OR_REPLACE_TABLE,
                destination=DataResource.DB_BIGQUERY_TABLE,
                progress_status=result.progress_status,
                description=result.get_final_report(),
                q=1,  # One table created
                q_unit=DataUnit.TABLE  # Table operation, not record operation
            ))

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_CREATE_OR_REPLACE_TABLE,
            destination=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            print_out=print_out,
            raise_e=raise_e
        )
    finally:
        result.final()
    return result

def load_from_json_bigquery_table_extended(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    table_full_path: str,
    project_id: Optional[str] = None,
    source: DataResource = DataResource.IN_MEMORY_DATA,
    schema: Optional[List[bigquery.SchemaField]] = None,
    create_table_if_not_exists: bool = False,
    records_write_approach: BigqueryTableWriteOption = BigqueryTableWriteOption.WRITE_APPEND,
    temp: bool = False,
    bigquery_client: Optional[bigquery.Client] = None,
    max_job_errors_to_log: int = 7,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Creates or appends to a BigQuery table from JSON data.

    Args:
        data: Data to load as dict or list of dicts
        table_full_path: Full table path (project.dataset.table)
        project_id: Optional GCP Project ID (if not in table_full_path)
        schema: Optional schema for table creation
        create_if_not_exists: Whether to create table if missing
        records_write_approach: BigQuery write disposition (WRITE_APPEND, WRITE_TRUNCATE, or WRITE_EMPTY)
        temp: Whether this is a temporary table
        bigquery_client: Optional pre-initialized BigQuery client
        max_job_errors_to_log: Max number of job errors to include in logs
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions

    Returns:
        FunctionResult with operation status
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    action = Action.PERSIST_CREATE_OR_LOAD_TABLE_FROM_JSON_TEMP if temp else Action.PERSIST_CREATE_OR_LOAD_TABLE_FROM_JSON
    try:
        # Parse table path
        path_parts = table_full_path.split('.')
        if len(path_parts) == 3:
            path_project_id, dataset_name, table_name = path_parts
            if project_id and project_id != path_project_id:
                raise ValueError(f"Conflicting project IDs: {project_id} vs {path_project_id} in path")
            project_id = path_project_id
        elif len(path_parts) == 2:
            if not project_id:
                raise ValueError("project_id is required when not included in table_full_path")
            dataset_name, table_name = path_parts
        else:
            raise ValueError(f"Invalid table_full_path format: {table_full_path}")

        result.add_metadata(
            project_id=project_id,
            table_full_path=table_full_path,
            create_if_not_exists=create_table_if_not_exists,
            records_write_approach=records_write_approach.value,
            temp=temp
        )

        # Initialize client
        if not bigquery_client:
            bigquery_client = bigquery.Client(project=project_id)

        # Process data to ensure it's JSON serializable
        processed_data = process_data_for_bigquery(data)

        # Check if dataset exists
        dataset_ref = bigquery_client.dataset(dataset_name)
        try:
            bigquery_client.get_dataset(dataset_ref)
        except NotFound as e:
            raise ValueError(f"Dataset {dataset_name} does not exist. Please create it first via Terraform") from e

        # Check table existence and get schema
        table_ref = dataset_ref.table(table_name)
        table_exists = False
        table_schema = None
       
        try:
            table = bigquery_client.get_table(table_ref)
            table_exists = True
            table_schema = table.schema  # Get schema from existing table
        except NotFound:
            table_exists = False

        # Configure job - use table schema if available, otherwise fall back to provided schema parameter
        final_schema = table_schema or schema
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            schema=final_schema,  # Use schema from existing table or provided parameter
            autodetect=(final_schema is None),  # Only autodetect if no schema available
        )

        if table_exists:
            # Handle schema-preserving truncation first
            if records_write_approach == BigqueryTableWriteOption.WRITE_TRUNCATE_PRESERVE_SCHEMA:
                result.add_state("TRUNCATING TABLE WHILE PRESERVING SCHEMA")
                if not _truncate_table_preserving_schema(table_full_path, bigquery_client, logger, print_out):
                    raise Exception(f"Failed to truncate table {table_full_path} while preserving schema")
                # After successful truncation, use APPEND mode for the actual data load
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
                result.add_state("SCHEMA-PRESERVING TRUNCATION COMPLETED, PROCEEDING WITH APPEND")
            elif records_write_approach == BigqueryTableWriteOption.WRITE_APPEND:
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
                result.add_state("CHOOSING OPTION TO APPEND TO EXISTING TABLE")
            elif records_write_approach == BigqueryTableWriteOption.WRITE_EMPTY:
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
                result.add_state("CHOOSING OPTION TO ERROR IF TABLE NOT EMPTY")
        else:
            if create_table_if_not_exists:
                job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
                result.add_state("CHOOSING OPTION TO CREATE NEW TABLE")
            else:
                # New handling for non-existent table
                warning_msg = "CREATION_SKIPPED as Table does not exist and create_if_not_exists=False"
                result.add_warning(warning_msg)
                result.final()
                
                if pipelinemon:
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.WARNING,
                        alert=Alert.TABLE_NOT_FOUND,
                        action=action,
                        source=source,
                        destination=DataResource.DB_BIGQUERY_TABLE,
                        progress_status=result.progress_status,
                        description=warning_msg
                    ))
                
                log_warning(
                    msg=warning_msg,
                    logger=logger,
                    print_out=print_out
                )
                return result

        # Load data
        result.add_state(f"{action}_LOAD_STARTED")
        
        load_job = bigquery_client.load_table_from_json(
            processed_data,  # Use our processed data
            table_full_path,
            job_config=job_config,
            project=project_id
        )
        load_job.result()  # Wait for completion

        _handle_query_job_result(
            query_job=load_job,
            result=result,
            action=action,
            source=source,
            destination=DataResource.DB_BIGQUERY_TABLE,
            max_job_issues_to_log=max_job_errors_to_log,
            pipelinemon=pipelinemon,
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=action,
            source=source,
            destination=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
        
    return result




###########################################################################################
#################### BIGQUERY LOAD FROM URI FUNCTIONS ##################################
###########################################################################################


# Standard Practice Comparison
# Format	BigQuery Load Jobs	Streaming	Performance	Size Limit
# NDJSON	✅ Preferred	✅ Yes	🚀 Fast	🔥 Large
# JSON Array	⚠️ Limited	❌ No	🐌 Slower	⚠️ Small

def load_from_uri_bigquery_table_extended(
    source_uris: Union[str, List[str]],
    table_full_path: str,
    project_id: Optional[str] = None,
    source: DataResource = DataResource.GCS,
    source_format: str = "NEWLINE_DELIMITED_JSON",
    schema: Optional[List[bigquery.SchemaField]] = None,
    create_table_if_not_exists: bool = False,
    records_write_approach: BigqueryTableWriteOption = BigqueryTableWriteOption.WRITE_APPEND,
    skip_leading_rows: int = 0,
    field_delimiter: Optional[str] = None,
    allow_jagged_rows: bool = False,
    allow_quoted_newlines: bool = False,
    encoding: str = "UTF-8",
    bigquery_client: Optional[bigquery.Client] = None,
    max_job_errors_to_log: int = 7,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Load data directly from GCS URIs into BigQuery table without loading into memory.
    
    This is more efficient than the memory-based approach for large files as data
    streams directly from GCS to BigQuery.
    
    Args:
        source_uris: GCS URI(s) like 'gs://bucket/path/file.json' or list of URIs
        table_full_path: Full table path (project.dataset.table)
        project_id: Optional GCP Project ID (if not in table_full_path)
        source_format: Data format - "NEWLINE_DELIMITED_JSON", "CSV", "PARQUET", etc.
        schema: Optional schema for table creation
        create_table_if_not_exists: Whether to create table if missing
        records_write_approach: BigQuery write disposition (WRITE_APPEND, WRITE_TRUNCATE, or WRITE_EMPTY)
        skip_leading_rows: Number of header rows to skip (mainly for CSV)
        field_delimiter: Field delimiter for CSV files
        allow_jagged_rows: Allow rows with varying column counts
        allow_quoted_newlines: Allow quoted newlines in CSV
        encoding: File encoding
        bigquery_client: Optional pre-initialized BigQuery client
        max_job_errors_to_log: Max number of job errors to include in logs
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        
    Returns:
        FunctionResult with operation status
    """
    function_name = "load_from_uri_bigquery_table_extended"
    result = FunctionResult(function_name)
    action = Action.PERSIST_CREATE_OR_LOAD_TABLE_FROM_URI
    
    try:
        # Validate inputs
        if not source_uris or not table_full_path:
            raise ValueError("source_uris and table_full_path are required")
        
        # Ensure source_uris is a list
        if isinstance(source_uris, str):
            source_uris = [source_uris]
        
        # Validate GCS URIs
        for uri in source_uris:
            if not uri.startswith('gs://'):
                raise ValueError(f"Invalid GCS URI format: {uri}")
        
        # Parse table path
        path_parts = table_full_path.split('.')
        if len(path_parts) == 3:
            path_project_id, dataset_name, table_name = path_parts
            if project_id and project_id != path_project_id:
                raise ValueError(f"Conflicting project IDs: {project_id} vs {path_project_id} in path")
            project_id = path_project_id
        elif len(path_parts) == 2:
            if not project_id:
                raise ValueError("project_id is required when not included in table_full_path")
            dataset_name, table_name = path_parts
        else:
            raise ValueError(f"Invalid table_full_path format: {table_full_path}")
        
        # Add metadata
        result.add_metadata(
            project_id=project_id,
            table_full_path=table_full_path,
            source_uris=source_uris,
            source_format=source_format,
            create_if_not_exists=create_table_if_not_exists,
            records_write_approach=records_write_approach.value
        )
        
        # Initialize client
        if not bigquery_client:
            bigquery_client = bigquery.Client(project=project_id)
        
        # Configure load job
        job_config = bigquery.LoadJobConfig(
            source_format=getattr(bigquery.SourceFormat, source_format),
            encoding=encoding,
            allow_jagged_rows=allow_jagged_rows,
            allow_quoted_newlines=allow_quoted_newlines
        )
        
        # Set skip_leading_rows only for CSV files
        if source_format == "CSV" and skip_leading_rows > 0:
            job_config.skip_leading_rows = skip_leading_rows
        
        # Set schema if provided
        if schema:
            job_config.schema = schema
        else:
            job_config.autodetect = True
        
        # Set field delimiter for CSV
        if field_delimiter and source_format == "CSV":
            job_config.field_delimiter = field_delimiter
        
        # Check table existence and configure write disposition
        table_ref = bigquery.TableReference.from_string(table_full_path)
        table_exists = False
        table_schema = None
       
        try:
            table = bigquery_client.get_table(table_ref)
            table_exists = True
            table_schema = table.schema  # Get schema from existing table
        except NotFound:
            table_exists = False

        # Configure job
        job_config = bigquery.LoadJobConfig(
            source_format=source_format,
            schema=table_schema,  # Always provide the schema to disable auto-detection
            autodetect=False,  # Explicitly disable autodetect
        )

        if table_exists:
            # Handle schema-preserving truncation first
            if records_write_approach == BigqueryTableWriteOption.WRITE_TRUNCATE_PRESERVE_SCHEMA:
                result.add_state("TRUNCATING TABLE WHILE PRESERVING SCHEMA")
                if not _truncate_table_preserving_schema(table_full_path, bigquery_client, logger, print_out):
                    raise Exception(f"Failed to truncate table {table_full_path} while preserving schema")
                # After successful truncation, use APPEND mode for the actual data load
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
                result.add_state("SCHEMA-PRESERVING TRUNCATION COMPLETED, PROCEEDING WITH APPEND")
            elif records_write_approach == BigqueryTableWriteOption.WRITE_APPEND:
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
                result.add_state("CHOOSING OPTION TO APPEND TO EXISTING TABLE")
            elif records_write_approach == BigqueryTableWriteOption.WRITE_EMPTY:
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_EMPTY
                result.add_state("CHOOSING OPTION TO ERROR IF TABLE NOT EMPTY")
        else:
            if create_table_if_not_exists:
                job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
                result.add_state("CHOOSING OPTION TO CREATE NEW TABLE")
            else:
                # New handling for non-existent table
                warning_msg = "CREATION_SKIPPED as Table does not exist and create_if_not_exists=False"
                result.add_warning(warning_msg)
                result.final()
                
                if pipelinemon:
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.WARNING,
                        alert=Alert.TABLE_NOT_FOUND,
                        action=action,
                        source=source,
                        destination=DataResource.DB_BIGQUERY_TABLE,
                        progress_status=result.progress_status,
                        description=warning_msg
                    ))
                
                log_warning(
                    msg=warning_msg,
                    logger=logger,
                    print_out=print_out
                )
                return result

        # Load data
        result.add_state(f"{action}_LOAD_STARTED")
        
        load_job = bigquery_client.load_table_from_uri(
            source_uris,
            table_ref,
            job_config=job_config
        )
        
        # Wait for job completion
        load_job.result()
        
        # Handle job result using the existing helper
        _handle_query_job_result(
            query_job=load_job,
            result=result,
            action=action,
            source=DataResource.GCS,
            destination=DataResource.DB_BIGQUERY_TABLE,
            max_job_issues_to_log=max_job_errors_to_log,
            pipelinemon=pipelinemon,
            logger=logger
        )
        
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=action,
            source=DataResource.GCS,
            destination=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    
    return result





###########################################################################################
#################################### BIGQUERY WRITE WITH PARAMS ###############################
###########################################################################################


def write_query_with_params_bigquery_extended(
    project_id: str,
    query: str,
    query_parameters: List[bigquery.ScalarQueryParameter],
    bigquery_client: Optional[bigquery.Client] = None,
    max_job_errors_to_log: int = 7,
    pipelinemon: Optional[Pipelinemon] = None,
    source: DataResource = DataResource.IN_MEMORY_DATA,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Execute parameterized BigQuery write query (UPDATE, DELETE, INSERT).
    
    Provides safer SQL execution with:
    - Automatic parameter escaping (prevents SQL injection)
    - Comprehensive error handling and logging
    - Job metrics tracking (rows affected, bytes processed, duration)
    - Pipeline monitoring integration
    
    Args:
        project_id: GCP Project ID
        query: SQL query with @ parameter placeholders (e.g., @task_id, @new_status)
        query_parameters: List of bigquery.ScalarQueryParameter for safe parameterization
        bigquery_client: Optional pre-initialized BigQuery client
        max_job_errors_to_log: Max number of job errors to include in logs
        pipelinemon: Optional pipeline monitoring object for observability
        source: Source data resource type (default: IN_MEMORY_DATA)
        logger: Optional logger instance
        print_out: Whether to print operation results
        raise_e: Whether to raise exceptions (False returns error in FunctionResult)
    
    Returns:
        FunctionResult with:
        - result.is_success: Boolean indicating success/failure
        - result.data: None (write operations don't return data)
        - result.metadata: Job details (rows_affected, bytes_processed, duration_ms, etc.)
        - result.errors/warnings/notices: Comprehensive issue tracking
    
    Example:
        ```python
        from google.cloud import bigquery
        
        result = write_query_with_params_bigquery_extended(
            project_id='my-project',
            query='''
                UPDATE `my-project.dataset.table`
                SET status = @new_status, updated_at = CURRENT_TIMESTAMP()
                WHERE task_id = @task_id
            ''',
            query_parameters=[
                bigquery.ScalarQueryParameter("new_status", "STRING", "COMPLETED"),
                bigquery.ScalarQueryParameter("task_id", "STRING", "task-123"),
            ],
            logger=my_logger
        )
        
        if result.is_success:
            rows_affected = result.metadata.get('records_affected', 0)
            print(f"Updated {rows_affected} rows")
        else:
            print(f"Update failed: {result.errors}")
        ```
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(project_id=project_id, query=query, parameter_count=len(query_parameters))

    try:
        # Validate inputs
        if not project_id:
            raise ValueError("project_id is required")
        if not query:
            raise ValueError("query cannot be empty")
        if not query_parameters:
            raise ValueError("query_parameters list cannot be empty")
        
        # Initialize client
        bigquery_client = bigquery_client or bigquery.Client(project=project_id)

        # Execute parameterized query
        result.add_state("PARAMETERIZED_QUERY_WRITE_STARTED")
        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        query_job = bigquery_client.query(query, job_config=job_config)
        query_job.result()  # Wait for completion
        
        # Handle job result with standardized error tracking
        _handle_query_job_result(
            query_job=query_job,
            result=result,
            action=Action.PERSIST_WRITE_QUERY,
            source=source,
            destination=DataResource.DB_BIGQUERY_TABLE,
            max_job_issues_to_log=max_job_errors_to_log,
            pipelinemon=pipelinemon,
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_WRITE_QUERY,
            source=source,
            destination=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result


###########################################################################################
#################################### BIGQUERY MERGE and WRITE QUERY ###############################
###########################################################################################


def merge_into_bigquery_via_temp_table_extended(
    project_id: str,
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    table_full_path: str,
    merge_key_columns: Union[str, List[str]], # Columns to use for identifying duplicates
    max_job_errors_to_log: int = 7,
    bigquery_client: Optional[bigquery.Client] = None,
    schema: Optional[List[bigquery.SchemaField]] = None,
    pipelinemon: Optional[Pipelinemon]=None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False,
    merge_type: Action = Action.PERSIST_MERGE_UPDATE_AND_INSERT_NEW_QUERY,
    update_columns: Optional[List[str]] = None,
) -> FunctionResult:
    """
    Merges data into a BigQuery table, avoiding duplicates based on the provided merge key columns.
    
    Args:
        project_id: GCP Project ID
        data: JSON-serializable data to merge
        table_full_path: Full path of target table (project.dataset.table)
        merge_key_columns: Column(s) to use for identifying duplicates
        max_job_errors_to_log: Maximum number of job errors to include in logs
        bigquery_client: Optional pre-initialized BigQuery client
        schema: Optional schema for the table
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        merge_type: Type of merge operation to perform:
            - PERSIST_MERGE_UPDATE_AND_INSERT_NEW_QUERY: Update existing rows and insert new rows
            - PERSIST_MERGE_UPDATE_DONT_INSERT_NEW_QUERY: Update existing rows only
            - PERSIST_MERGE_INSERT_NEW_AND_DONT_UPDATE_QUERY: Insert new rows only
        update_columns: Optional list of column names to update. If None, uses 'UPDATE SET *' to update all columns.
            If provided, only specified columns will be updated (e.g., ['field1', 'field2']).
            This prevents overwriting unrelated fields that may have been updated concurrently.
        
    Returns:
        Dict[str, Any]: Status information about the merge operation.
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    
    # Handle single record case early for consistent counting
    if isinstance(data, dict):
        data = [data]
    
    # Calculate record count consistently
    records_to_be_merged_count = len(data) if isinstance(data, list) else 0
    
    result.add_metadata(
        project_id=project_id,
        table_full_path=table_full_path,
        merge_key_columns=merge_key_columns,
        merge_type=str(merge_type) if merge_type else None,
        records_to_be_merged_count=records_to_be_merged_count
    )
    temp_table_name = None
    temp_table_full_path = None # Initialize here

    try:
        # Input validation
        if not project_id or not table_full_path:
            raise ValueError("project_id and table_full_path are required")
        if not merge_key_columns:
            raise ValueError("merge_key_columns cannot be empty")

        # Check if data is empty
        if records_to_be_merged_count == 0:
            notice_msg = "MERGE_SKIPPED: No data to merge (empty data provided)"
            result.add_notice(notice_msg)
            result.add_metadata(
                records_to_be_merged_count=0,
                records_inserted_count=0,
                records_updated_count=0
            )
            result.final()
            
            if pipelinemon:
                pipelinemon.add_log(StructLog(
                    level=LogLevel.NOTICE,
                    action=merge_type,
                    source=DataResource.IN_MEMORY_DATA,
                    destination=DataResource.DB_BIGQUERY_TABLE,
                    progress_status=ProgressStatus.DONE_WITH_NOTICES,
                    description=notice_msg,
                    q=0,  # Explicitly set to 0 for empty data
                    q_unit=DataUnit.DBROW  # Use proper unit for records
                ))
            
            log_info(
                msg=notice_msg,
                logger=logger,
                print_out=print_out
            )
            return result

        # Setup
        bigquery_client = bigquery_client or bigquery.Client(project=project_id)
        dataset_name, table_name = table_full_path.split('.')[1:3]
        temp_table_name = f"{table_name}_temp_{datetime.datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
        temp_table_full_path = f"{project_id}.{dataset_name}.{temp_table_name}"
        
        result.add_metadata(
            temp_table_full_path=temp_table_full_path,
            dataset_name=dataset_name,
            table_name=table_name
        )

        # Fetch schema from target table if not provided
        if schema is None:
            result.add_state("FETCHING_TARGET_TABLE_SCHEMA")
            try:
                schema = get_bigquery_table_schema(
                    table_full_path=table_full_path,
                    project_id=project_id,
                    bigquery_client=bigquery_client
                )
                if schema:
                    result.add_notice(f"Fetched schema from target table: {len(schema)} fields")
                else:
                    result.add_warning(f"Could not fetch schema from target table {table_full_path}, will attempt schema auto-detection")
            except Exception as e:
                result.add_warning(f"Error fetching schema from target table {table_full_path}: {str(e)}, will attempt schema auto-detection")
                schema = None

        # Process data to ensure it's JSON serializable
        processed_data = process_data_for_bigquery(data)

        # Filter schema to only include fields present in the data
        # This is critical for selective column updates where we don't provide all table fields
        if schema and processed_data:
            # Get field names from first record (all records should have same structure)
            sample_record = processed_data[0] if isinstance(processed_data, list) else processed_data
            data_fields = set(sample_record.keys())
            
            # Filter schema to only fields present in data
            original_field_count = len(schema)
            schema = [field for field in schema if field.name in data_fields]
            
            if len(schema) < original_field_count:
                result.add_notice(f"Filtered schema to {len(schema)} fields present in data (was {original_field_count})")

        # Create temp table
        result.add_state("CREATING_TEMP_TABLE")
        create_result:FunctionResult = load_from_json_bigquery_table_extended(
            bigquery_client=bigquery_client,
            data=processed_data,  # Use processed data
            project_id=project_id,
            table_full_path=temp_table_full_path,
            create_table_if_not_exists=True,
            records_write_approach=BigqueryTableWriteOption.WRITE_TRUNCATE_PRESERVE_SCHEMA,
            max_job_errors_to_log=max_job_errors_to_log,
            # Pass the schema explicitly
            schema=schema,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
        )
        result.integrate_result(create_result)
        
        if not create_result.is_success:
            result.add_state("TEMP_TABLE_CREATION_FAILED")
            result.add_issue(f"Failed to create temp table: {create_result.get_final_report()}")
            result.add_metadata(
                records_inserted_count=0,
                records_updated_count=0
            )
            result.final()
            return result

        # Merge tables
        result.add_state("MERGING_TABLES")
        merge_func_result:FunctionResult = merge_two_bigquery_tables_extended(
            bigquery_client=bigquery_client,
            project_id=project_id,
            target_table_full_path=table_full_path,
            source_table_full_path=temp_table_full_path,
            merge_key_columns=merge_key_columns,
            pipelinemon=pipelinemon,
            logger=logger,
            raise_e=raise_e,
            print_out=print_out,
            merge_type=merge_type,
            update_columns=update_columns
        )
        result.integrate_result(merge_func_result)

        # Process merge results for tracking inserted/updated counts
        records_affected = merge_func_result.metadata.get('records_affected', 0)
        
        # Set updated and inserted counts based on merge type
        if merge_type == Action.PERSIST_MERGE_UPDATE_AND_INSERT_NEW_QUERY:
            # Can't determine exact split between inserts and updates
            # Will be tracked via "records_affected" which includes both
            result.add_metadata(
                records_affected=records_affected,
                records_inserted_count=None,  # Can't determine exact split
                records_updated_count=None    # Can't determine exact split
            )
            result.add_state(f"MERGED_OR_UPDATED_{records_affected}_RECORDS")
            
        elif merge_type == Action.PERSIST_MERGE_UPDATE_DONT_INSERT_NEW_QUERY:
            # All affected records were updates
            result.add_metadata(
                records_affected=records_affected,
                records_inserted_count=0,
                records_updated_count=records_affected
            )
            result.add_state(f"UPDATED_{records_affected}_RECORDS")
            
        elif merge_type == Action.PERSIST_MERGE_INSERT_NEW_AND_DONT_UPDATE_QUERY:
            # All affected records were inserts
            result.add_metadata(
                records_affected=records_affected,
                records_inserted_count=records_affected,
                records_updated_count=0
            )
            result.add_state(f"INSERTED_{records_affected}_RECORDS")

        # Final status based on merge result
        if merge_func_result.is_success:
            result.add_state("MERGE_COMPLETED")
        else:
            result.add_issue("MERGE_FAILED")
        result.final()

        # Log after finalizing
        log_by_lvl(
            info_msg=f"Merge operation completed for table {table_full_path}.",
            debug_msg=result.get_final_report(),
            logger=logger,
            print_out=print_out
        )
        if pipelinemon:
            pipelinemon.add_system_impacted(f"bigquery_merge: {table_full_path}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=merge_type,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.DB_BIGQUERY_TABLE,
                progress_status=result.progress_status,
                description=result.get_final_report(),
                q=records_affected,  # Number of records affected by the merge
                q_unit=DataUnit.DBROW # Use proper unit for records
            ))

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=merge_type,
            resource=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            print_out=print_out,
            raise_e=raise_e
        )
        # Ensure counts are present even in exception case
        if 'records_inserted_count' not in result.metadata:
            result.add_metadata(records_inserted_count=0)
        if 'records_updated_count' not in result.metadata:
            result.add_metadata(records_updated_count=0)
    finally:
        if temp_table_name and temp_table_full_path: # Check if temp table was intended and path is set
            rows_in_temp = 0
            table_existed = False
            try:
                # Explicitly check if the table exists and get row count
                temp_table = bigquery_client.get_table(temp_table_full_path)
                table_existed = True
                rows_in_temp = temp_table.num_rows or 0
                
                # If table exists, attempt deletion
                bigquery_client.delete_table(temp_table_full_path, not_found_ok=False) # Set not_found_ok=False as we know it exists
                result.add_state("TEMP_TABLE_DELETED")
                msg=f"Temp table {temp_table_full_path} with {rows_in_temp} rows deleted."
                log_info(msg=msg, logger=logger, print_out=print_out)
                if pipelinemon:
                    pipelinemon.add_system_impacted(f"bigquery_delete_table: {temp_table_full_path}")
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.INFO, 
                        action=Action.PERSIST_DELETE_TABLE_TEMP, 
                        resource=DataResource.DB_BIGQUERY_TABLE, 
                        progress_status=ProgressStatus.DONE, 
                        description=msg, # Use the specific message
                        q=rows_in_temp,
                        q_unit=DataUnit.DBROW
                    ))

            except NotFound:
                # Table didn't exist when we tried to get/delete it
                msg = f"Temp table {temp_table_full_path} not found during cleanup (already deleted or never created)."
                log_info(msg=msg, logger=logger, print_out=print_out)
                # Optionally add a notice to the result or pipelinemon if needed
                # result.add_notice("Temp table not found for cleanup.")

            except Exception as cleanup_e:
                # Handle errors during the get_table or delete_table calls (other than NotFound)
                err_msg = f"Failed to cleanup temp table {temp_table_full_path}: {cleanup_e}"
                result.add_warning(err_msg)
                log_warning(msg=err_msg, logger=logger, print_out=print_out)
                if pipelinemon:
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.WARNING, 
                        action=Action.PERSIST_DELETE_TABLE_TEMP, 
                        resource=DataResource.DB_BIGQUERY_TABLE, 
                        progress_status=ProgressStatus.FAILED, 
                        description=err_msg,
                        q=rows_in_temp if table_existed else 0, # Log rows only if we knew the table existed
                        q_unit=DataUnit.DBROW
                    ))
        result.final() # Ensure result is finalized regardless of cleanup outcome
    return result


def merge_two_bigquery_tables_extended(
    target_table_full_path: str,
    source_table_full_path: str,
    merge_key_columns: Union[str, List[str]],
    project_id: str,
    bigquery_client: Optional[bigquery.Client] = None,
    max_job_errors_to_log: int = 7,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False,
    merge_type: Action = Action.PERSIST_MERGE_UPDATE_AND_INSERT_NEW_QUERY,
    update_columns: Optional[List[str]] = None,
) -> FunctionResult:
    """Merges two BigQuery tables using a customizable merge query.

    Args:
        target_table_full_path: Full path of target table (project.dataset.table)
        source_table_full_path: Full path of source table (project.dataset.table)
        merge_key_columns: Column(s) to use as merge keys
        project_id: GCP Project ID
        bigquery_client: Optional pre-initialized BigQuery client
        max_job_errors_to_log: Max number of job errors to include in logs
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        merge_type: Type of merge operation to perform:
            - PERSIST_MERGE_UPDATE_AND_INSERT_NEW_QUERY: Update existing rows and insert new rows
            - PERSIST_MERGE_UPDATE_DONT_INSERT_NEW_QUERY: Update existing rows only
            - PERSIST_MERGE_INSERT_NEW_AND_DONT_UPDATE_QUERY: Insert new rows only
        update_columns: Optional list of column names to update. If None, uses 'UPDATE SET *' to update all columns.
            If provided, only specified columns will be updated (e.g., ['field1', 'field2']).
            This prevents overwriting unrelated fields that may have been updated concurrently.

    Returns:
        FunctionResult with merge operation status
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        project_id=project_id,
        target_table=target_table_full_path,
        source_table=source_table_full_path,
        merge_type=str(merge_type) if merge_type else None,
    )
    try:
        if not bigquery_client:
            if not project_id:
                raise ValueError("project_id is required when bigquery_client is not provided.")
            bigquery_client = bigquery.Client(project=project_id)

        if isinstance(merge_key_columns, str):
            merge_key_columns = [merge_key_columns]
        merge_condition = " AND ".join([f"target.{col} = source.{col}" for col in merge_key_columns])
        
        # Build UPDATE SET clause based on update_columns parameter
        if update_columns:
            # Selective column update: UPDATE SET col1 = source.col1, col2 = source.col2, ...
            update_set_clause = ", ".join([f"{col} = source.{col}" for col in update_columns])
            result.add_metadata(update_columns=update_columns, update_mode="selective")
        else:
            # Update all columns: UPDATE SET *
            update_set_clause = "*"
            result.add_metadata(update_mode="all_columns")
        
        # For more accurate counting, we can run a preliminary count query
        # to count how many records match the merge condition (potential updates)
        # and how many don't match (potential inserts)
        # This is optional but would give more accurate counts
        
        # Generate the appropriate merge query based on merge_type
        if merge_type == Action.PERSIST_MERGE_UPDATE_AND_INSERT_NEW_QUERY:
            merge_query = f"""
            MERGE `{target_table_full_path}` AS target
            USING `{source_table_full_path}` AS source
            ON {merge_condition}
            WHEN MATCHED THEN
                UPDATE SET {update_set_clause}
            WHEN NOT MATCHED THEN
                INSERT ROW
            """
            result.add_state("MERGE_QUERY_UPDATE_AND_INSERT_NEW_STARTED")
            
        elif merge_type == Action.PERSIST_MERGE_UPDATE_DONT_INSERT_NEW_QUERY:
            merge_query = f"""
            MERGE `{target_table_full_path}` AS target
            USING `{source_table_full_path}` AS source
            ON {merge_condition}
            WHEN MATCHED THEN
                UPDATE SET {update_set_clause}
            """
            result.add_state("MERGE_QUERY_UPDATE_ONLY_STARTED")
            
        elif merge_type == Action.PERSIST_MERGE_INSERT_NEW_AND_DONT_UPDATE_QUERY:
            merge_query = f"""
            MERGE `{target_table_full_path}` AS target
            USING `{source_table_full_path}` AS source
            ON {merge_condition}
            WHEN NOT MATCHED THEN
                INSERT ROW
            """
            result.add_state("MERGE_QUERY_INSERT_ONLY_STARTED")
            
        else:
            # Default to the most common case if an unsupported merge type is provided
            merge_query = f"""
            MERGE `{target_table_full_path}` AS target
            USING `{source_table_full_path}` AS source
            ON {merge_condition}
            WHEN MATCHED THEN
                UPDATE SET {update_set_clause}
            WHEN NOT MATCHED THEN
                INSERT ROW
            """
            result.add_state("MERGE_QUERY_DEFAULT_STARTED")
            result.add_warning(f"Unknown merge type '{merge_type}', defaulting to UPDATE_AND_INSERT")
        
        query_merge_job = bigquery_client.query(merge_query)
        query_merge_job.result()  # Wait for the merge to complete
        
        _handle_query_job_result(
            query_job=query_merge_job,
            result=result,
            action=merge_type,
            source=DataResource.DB_BIGQUERY_TABLE,
            destination=DataResource.DB_BIGQUERY_TABLE,
            max_job_issues_to_log=max_job_errors_to_log, 
            pipelinemon=pipelinemon, 
            logger=logger
        )
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=merge_type,
            source=DataResource.DB_BIGQUERY_TABLE,
            destination=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            print_out=print_out,
            raise_e=raise_e
        )
        # Ensure count is present even in exception case
        if 'records_affected' not in result.metadata:
            result.add_metadata(records_affected=0)
    finally:
        result.final()
    return result


###########################################################################################
#################################### BIGQUERY WRITE QUERY FUNCTIONS ###############################
###########################################################################################




def write_query_to_bigquery_table_extended(
    project_id: str,
    query: str,
    bigquery_client: Optional[bigquery.Client] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    source: DataResource = DataResource.IN_MEMORY_DATA,
    max_job_errors_to_log: int = 7,
    print_out: bool = False,
    logger: Optional[logging.Logger] = None,
    raise_e: bool = False
) -> FunctionResult:
    """Executes a BigQuery SQL query that modifies data.

    Args:
        project_id: GCP Project ID
        query: SQL query string
        bigquery_client: Optional pre-initialized BigQuery client  
        pipelinemon: Optional pipeline monitoring object
        max_job_errors_to_log: Max number of job errors to include in logs
        print_out: Whether to print output
        logger: Optional logger instance
        raise_e: Whether to raise exceptions

    Returns:
        FunctionResult with query execution status
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(project_id=project_id, query=query)
    try:
        # Validate inputs
        if not project_id:
            raise ValueError("project_id is required")
        if not query:
            raise ValueError("query cannot be empty")
            
        # Get or create client
        bigquery_client = bigquery_client or bigquery.Client(project=project_id)

        # Execute query
        result.add_state("QUERY_WRITE_STARTED")
        query_job = bigquery_client.query(query, project=project_id)
        query_job.result()
        
        _handle_query_job_result(query_job=query_job, result=result,
                                 action=Action.PERSIST_WRITE_QUERY,
                                 source=source,
                                 destination=DataResource.DB_BIGQUERY_TABLE,
                                 max_job_issues_to_log=max_job_errors_to_log,
                                 pipelinemon=pipelinemon,
                                 logger=logger)



    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_WRITE_QUERY,
            source=source,
            destination=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result


###########################################################################################
#################################### BIGQUERY READ QUERY FUNCTIONS ###############################
###########################################################################################

def read_query_bigquery_table_extended(
    project_id: str,
    query: str,
    bigquery_client: Optional[bigquery.Client] = None,
    max_job_errors_to_log: int = 7,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Executes a BigQuery SQL read query.

    Args:
        project_id: GCP Project ID
        query: SQL query string
        bigquery_client: Optional pre-initialized BigQuery client
        max_job_errors_to_log: Max number of job errors to include in logs
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions

    Returns:
        FunctionResult containing query results
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(project_id=project_id, query=query)

    try:
        # Input validation and client setup
        if not project_id or not query:
            raise ValueError("project_id and query are required")
        bigquery_client = bigquery_client or bigquery.Client(project=project_id)

        # Execute query
        result.add_state("QUERY_READ_STARTED")
        query_job = bigquery_client.query(query)
        rows = query_job.result()

        # Handle job result
        _handle_query_job_result(query_job=query_job,
                                 result=result,
                                 action=Action.READ_QUERY,
                                 destination=DataResource.IN_MEMORY_DATA,
                                 source=DataResource.DB_BIGQUERY_TABLE,
                                 rows=rows,
                                 max_job_issues_to_log=max_job_errors_to_log,
                                 pipelinemon=pipelinemon,
                                 logger=logger)

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_QUERY,
            destination=DataResource.IN_MEMORY_DATA,
            source=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result

def read_query_with_params_bigquery_extended(
    project_id: str,
    query: str,
    query_parameters: List[bigquery.ScalarQueryParameter],
    bigquery_client: Optional[bigquery.Client] = None,
    max_job_errors_to_log: int = 7,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Execute parameterized BigQuery query and return results.
    Handles ARRAY_AGG and structured results.
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(project_id=project_id, query=query)

    try:
        bigquery_client = bigquery_client or bigquery.Client(project=project_id)

        result.add_state("QUERY_READ_STARTED")
        query_job = bigquery_client.query(
            query,
            job_config=bigquery.QueryJobConfig(query_parameters=query_parameters)
        )
        rows = query_job.result()

        _handle_query_job_result(
            query_job=query_job,
            result=result,
            action=Action.READ_QUERY,
            source=DataResource.DB_BIGQUERY_TABLE,
            destination=DataResource.IN_MEMORY_DATA,
            rows=rows,
            max_job_issues_to_log=max_job_errors_to_log,
            pipelinemon=pipelinemon,
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result, 
            action=Action.READ_QUERY,
            source=DataResource.DB_BIGQUERY_TABLE,
            destination=DataResource.IN_MEMORY_DATA,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result



def read_query_for_rows_matching_dates_bigquery_extended(
    project_id: str,
    table_full_path: str,
    date_column: str,
    rows_list: Dict[str, Any],
    date_range: Optional[Tuple[Any, Any]] = None,
    max_job_errors_to_log: int = 7,
    bigquery_client: Optional[bigquery.Client] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    raise_e: bool = False,
    print_out: bool = False
) -> FunctionResult:
    """Queries BigQuery table for rows matching field values and optional date range.

    Args:
        project_id: GCP Project ID
        table_full_path: Full table path (project.dataset.table)
        date_column: Name of date column to filter
        rows_list: Dict of field names and values to match
        date_range: Optional (start_date, end_date) tuple
        max_job_errors_to_log: Max number of job errors to include in logs
        bigquery_client: Optional pre-initialized BigQuery client
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        raise_e: Whether to raise exceptions
        print_out: Whether to print output

    Returns:
        FunctionResult containing matching rows
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        project_id=project_id,
        table_full_path=table_full_path,
        date_column=date_column
    )

    try:
        # Initialize client
        bigquery_client = bigquery_client or bigquery.Client(project=project_id)

        # Build the WHERE clause dynamically
        where_clauses = []
        query_parameters = []

        # Add field conditions
        for field, value in rows_list.items():
            where_clauses.append(f"{field} = @{field}")
            param_type=_convert_python_type_to_bigquery(value)
            query_parameters.append(bigquery.ScalarQueryParameter(field, param_type, value))

        # Add date range if provided
        if date_range:
            start_date, end_date = date_range
            column_type = _convert_python_type_to_bigquery(start_date or end_date)
            if start_date and end_date:
                where_clauses.append(f"{date_column} BETWEEN @start_date AND @end_date")
                query_parameters.extend([
                    bigquery.ScalarQueryParameter("start_date", column_type, start_date),
                    bigquery.ScalarQueryParameter("end_date", column_type, end_date)
                ])
            elif start_date:
                where_clauses.append(f"{date_column} >= @start_date")
                query_parameters.append(
                    bigquery.ScalarQueryParameter("start_date", column_type, start_date)
                )
            elif end_date:
                where_clauses.append(f"{date_column} <= @end_date")
                query_parameters.append(
                    bigquery.ScalarQueryParameter("end_date", column_type, end_date)
                )

        # RETURNING ONLY DATE COLUMN IN STRING FORMAT
        query = f"""
                SELECT 
                FORMAT_DATE('%Y-%m-%d', {date_column}) as {date_column}
                FROM `{table_full_path}`
                WHERE {" AND ".join(where_clauses)}
                ORDER BY {date_column} DESC
                """

        # EXAMPLE HOW IT WILL LOOK TRANSLATES:
        # query = f"""SELECT date_id FROM `{table_full_path}`
        #              WHERE asset_id = @asset_id AND date_id BETWEEN @records_oldest_date AND @records_recent_date  """
        # job_config = bigquery.QueryJobConfig(
        #                   query_parameters=[bigquery.ScalarQueryParameter("asset_id", "STRING", asset_id),
        #                                    bigquery.ScalarQueryParameter("records_recent_date", "DATE", sourced_records_recent_date),
        #                                    bigquery.ScalarQueryParameter("records_oldest_date", "DATE", sourced_records_oldest_date))   

        result.add_state("QUERY_READ_JOB_STARTED")
       
        query_read_job = bigquery_client.query(
                        query,
                        job_config=bigquery.QueryJobConfig(query_parameters=query_parameters),
                        project=project_id
                    )
        query_response_rows = query_read_job.result() # Wait for the job to complete
        _handle_query_job_result(query_job=query_read_job,
                                result=result,
                                action=Action.READ_QUERY,
                                destination=DataResource.IN_MEMORY_DATA,
                                source=DataResource.DB_BIGQUERY_TABLE,
                                rows=query_response_rows,
                                max_job_issues_to_log=max_job_errors_to_log,
                                single_column=True,
                                pipelinemon=pipelinemon,
                                logger=logger)

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_QUERY,
            destination=DataResource.IN_MEMORY_DATA,
            source=DataResource.DB_BIGQUERY_TABLE,
            logger=logger,
            pipelinemon=pipelinemon,
            print_out=print_out,
            raise_e=raise_e
        )
    finally:
        result.final()
    return result

def export_query_table_from_bigquery_to_gcs_extended(
    project_id: str,
    query: str,
    export_uri: str,
    query_parameters: Optional[List[bigquery.ScalarQueryParameter]] = None,
    bigquery_client: Optional[bigquery.Client] = None,
    max_job_errors_to_log: int = 7,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """Executes a BigQuery SQL export query.

    Args:
        project_id: GCP Project ID
        query: SQL query string to be exported
        export_uri: GCS URI where to export the data
        query_parameters: Optional list of query parameters
        bigquery_client: Optional pre-initialized BigQuery client
        max_job_errors_to_log: Max number of job errors to include in logs
        pipelinemon: Optional pipeline monitoring object
        logger: Optional logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions

    Returns:
        FunctionResult containing export operation status
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        project_id=project_id,
        query=query,
        export_uri=export_uri
    )

    try:
        # Input validation and client setup
        if not project_id or not query or not export_uri:
            raise ValueError("project_id, query and export_uri are required")

        bigquery_client = bigquery_client or bigquery.Client(project=project_id)

        # Prepare the export query
        export_query = f"""
        EXPORT DATA OPTIONS(
            uri='{export_uri}',
            format='CSV',
            overwrite=true,
            header=false,
            field_delimiter=','
        ) AS {query}
        """

        # Configure job with parameters if provided
        job_config = None
        if query_parameters:
            job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)

        # Execute query
        result.add_state("EXPORT_QUERY_STARTED")
        query_job = bigquery_client.query(export_query, job_config=job_config)
        query_job.result()  # Wait for completion

        # Handle job result
        _handle_query_job_result(
            query_job=query_job,
            result=result,
            action=Action.PERSIST_EXPORT_FILE_QUERY,
            source=DataResource.DB_BIGQUERY_TABLE,
            destination=DataResource.GCS,
            max_job_issues_to_log=max_job_errors_to_log,
            pipelinemon=pipelinemon,
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_EXPORT_FILE_QUERY,
            source=DataResource.DB_BIGQUERY_TABLE,
            destination=DataResource.GCS,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result