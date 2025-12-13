import inspect
import logging
from typing import Any, Dict, List, Optional, Union
from google.cloud import firestore
from google.api_core.exceptions import GoogleAPICallError
from ipulse_shared_base_ftredge import (
    LogLevel, DataResource, Action, ProgressStatus, StructLog, log_info, log_warning, log_by_lvl, DataUnit
)
from ..pipelines import FunctionResult, Pipelinemon, handle_pipeline_operation_exception
from datetime import datetime, date,  timezone
import json
from pydantic import BaseModel


# Helper functions remain unchanged
def _datetime_safe_json(obj):
    """Helper function to JSON serialize objects with datetime values."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def _sanitize_firestore_data(data: Any) -> Any:
    """
    Recursively sanitize data before sending to Firestore.
    Converts Pydantic models to dicts while preserving Firestore-native types like datetime.
    """
    if isinstance(data, BaseModel):
        # Convert Pydantic model to dict. Do NOT use mode='json' as it converts
        # datetime to string. We want to preserve datetime objects for Firestore.
        return _sanitize_firestore_data(data.model_dump())

    if isinstance(data, dict):
        # Recurse into dictionaries
        return {str(k): _sanitize_firestore_data(v) for k, v in data.items()}

    if isinstance(data, list):
        # Recurse into lists
        return [_sanitize_firestore_data(item) for item in data]

    # Return native types that Firestore supports directly.
    # This includes: None, bool, int, float, str, bytes, datetime, and date.
    # Enums inside Pydantic models will have been converted to their values by model_dump().
    return data


def add_creat_updt_info(data: Dict[str, Any], force_creat_info: bool, updater_user_id: str) -> Dict[str, Any]:
    """
    Add standard metadata fields to document data.
    
    Args:
        data: Dictionary to add metadata to
        force_creat: Boolean to determine if creation fields should be added even if they exist
        updater_user_id: ID of user/system creating/updating the document
        
    Returns:
        Dictionary with added metadata
    """
    now = datetime.now(timezone.utc)
    result = data.copy()  # Don't modify the original

    # For update fields, either always update or only if missing

    result['updated_at'] = now
    result['updated_by'] = updater_user_id
    # Add creation fields only if they don't exist
    if 'created_at' not in result and force_creat_info:
        result['created_at'] = now
    if 'created_by' not in result and force_creat_info:
        result['created_by'] = updater_user_id
        
    return result

def create_or_merge_firestore_document_extended(
    document_id: str,
    collection: str,
    data: Dict[str, Any],
    firestore_client: firestore.Client,
    merge: bool = True,  # Default to merge for safety
    replace_if_exists: bool = False,  # Default to not replacing existing docs
    insert_creat_updt_info: bool = False,
    force_creat_info: bool = False,
    updater_user_id: str = "system",
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Create or merge a Firestore document with standard error handling and optional metadata.
    
    Args:
        document_id: Document ID
        collection: Collection name
        data: Data to save
        firestore_client: Firestore client
        merge: Whether to merge fields (True) or overwrite (False) when updating
        replace_if_exists: Whether to replace an entire document if document exists (True) or not. Then it depends on merge flag
        insert_creat_updt_info: Whether to add standard metadata
        updater_user_id: ID of creator for metadata
        pipelinemon: Optional Pipelinemon instance
        logger: Optional logger
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        
    Returns:
        FunctionResult with operation status
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        document_id=document_id,
        collection=collection,
        merge=merge,
        replace_if_exists=replace_if_exists,
        add_metadata=insert_creat_updt_info,
        force_creat_info=force_creat_info
    )
    
    # Set initial action as a default - will be refined after checking document existence
    # This ensures we have a valid action type even if exception occurs during document check
    action = Action.PERSIST_CREATE_OR_MERGE if merge else Action.PERSIST_CREATE_OR_REPLACE
    
    try:
        # Input validation
        if not document_id:
            raise ValueError("document_id cannot be empty")
        if not collection:
            raise ValueError("collection cannot be empty")
        if not data:
            raise ValueError("data cannot be empty")
        
        
        
        # Make a copy to avoid modifying original data
        processed_data = data.copy()
        
        # Add standard metadata if requested
        if insert_creat_updt_info:
            processed_data = add_creat_updt_info(
                data=processed_data,
                force_creat_info=force_creat_info,
                # Use the provided updater_user_id or default to "system"
                updater_user_id=updater_user_id
            )
        
        # Sanitize data to prevent common Firestore errors
        try:
            sanitized_data = _sanitize_firestore_data(processed_data)
        except Exception as sanitize_error:
            raise ValueError(f"Failed to sanitize data: {str(sanitize_error)}") from sanitize_error
        
        # Get document reference
        doc_ref = firestore_client.collection(collection).document(document_id)
        
        # Check if document exists
        doc = doc_ref.get()
        document_exists = doc.exists
        
        # Handle document existence check - FIXED LOGIC
        # Only apply replace_if_exists check when we're actually replacing (merge=False)
        if document_exists and not merge and not replace_if_exists:
            if pipelinemon:
                pipelinemon.add_log(StructLog(
                    level=LogLevel.WARNING,
                    action=action,
                    source=DataResource.IN_MEMORY_DATA,
                    destination=DataResource.DB_FIRESTORE,
                    progress_status=ProgressStatus.INTENTIONALLY_SKIPPED,
                    q=1,
                    q_unit=DataUnit.DOCUMENT,
                    description=f"Document {document_id} already exists in collection {collection}. " +
                                "Use replace_if_exists=True to replace it."
                ))
            result.add_notice(f"Document {document_id} already exists in collection {collection}. " +
                            "Use replace_if_exists=True to replace it.")
            result.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            result.final()
            return result
        
        # Determine precise action based on document existence
        if document_exists:
            # Validate parameter consistency - add proper logical validation
            if replace_if_exists and merge:
                raise ValueError("Contradicting parameters: replace_if_exists=True cannot be used with merge=True. " +
                                "If you want to merge with an existing document, set replace_if_exists=False. " +
                                "If you want to replace an existing document, set replace_if_exists=True.")
            # Document exists and we're allowed to modify it
            if merge:
                action = Action.PERSIST_MERGE
            else:
                # We've already checked replace_if_exists above, so we're good to proceed
                action = Action.PERSIST_REPLACE
        else:
            # Document doesn't exist, so we're creating a new one
            action = Action.PERSIST_CREATE

        result.add_metadata(action=action) # Add the determined action to the result metadata

        if pipelinemon:
            pipelinemon.add_system_impacted(f"firestore_document: {document_id}")
        # Perform the actual write operation
        doc_ref.set(sanitized_data, merge=(merge and document_exists))
        
        result.add_state(f"DOCUMENT_{str(action)}_COMPLETED")
        
        # Use the custom JSON serializer for logging
        try:
            json_data = json.dumps(sanitized_data, default=_datetime_safe_json)
            # Log success with proper datetime handling
            log_by_lvl(
                info_msg=f"Firestore {str(action)} document {document_id} in collection {collection} completed",
                debug_msg = (json_data[:200] + "...") if len(json_data) > 200 else json_data,
                logger=logger,
                print_out=print_out
            )
        except Exception as json_error:
            # Fall back to a simpler message if JSON serialization fails
            log_by_lvl(
                info_msg=f"Firestore {str(action)} document {document_id} in collection {collection} completed",
                debug_msg=f"Data serialization for logging failed: {str(json_error)}",
                logger=logger,
                print_out=print_out
            )
        
        if pipelinemon:
            pipelinemon.add_system_impacted(f"firestore_document: {document_id}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=action,  # Use our refined action for logging
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.DB_FIRESTORE,
                progress_status=ProgressStatus.DONE,
                q=1,
                q_unit=DataUnit.DOCUMENT,
                description=result.get_final_report()
            ))
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=action,  # Use our current action value for exception handling
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.DB_FIRESTORE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result

def merge_firestore_document_extended(
    document_id: str,
    collection: str,
    data: Dict[str, Any],
    firestore_client: firestore.Client,
    merge: bool = True,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Merges data into a Firestore document.
    
    Args:
        document_id: Document ID
        collection: Collection name
        data: Data to merge
        firestore_client: Firestore client
        merge: Whether to merge or overwrite document
        pipelinemon: Optional Pipelinemon instance
        logger: Optional logger
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        
    Returns:
        FunctionResult with operation status
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        document_id=document_id,
        collection=collection,
        merge=merge
    )
    action = Action.PERSIST_MERGE if merge else Action.PERSIST_CREATE_OR_MERGE
    
    try:
        # Input validation
        if not document_id:
            raise ValueError("document_id cannot be empty")
        if not collection:
            raise ValueError("collection cannot be empty")
        if not data:
            raise ValueError("data cannot be empty")
            
        # Sanitize data to prevent common Firestore errors
        try:
            sanitized_data = _sanitize_firestore_data(data)
        except Exception as sanitize_error:
            raise ValueError(f"Failed to sanitize data: {str(sanitize_error)}") from sanitize_error
        
        # Get document reference
        doc_ref = firestore_client.collection(collection).document(document_id)
        
        # Attempt to set/merge document
        doc_ref.set(sanitized_data, merge=merge)
        
        result.add_state("DOCUMENT_SET_COMPLETED")
        
        # Log success
        log_by_lvl(
            info_msg=f"Updated Firestore document {document_id} in collection {collection}",
            debug_msg=json.dumps(sanitized_data)[:200] + "..." if len(json.dumps(sanitized_data)) > 200 else json.dumps(sanitized_data),
            logger=logger,
            print_out=print_out
        )
        
        if pipelinemon:
            pipelinemon.add_system_impacted(f"firestore_write: {document_id}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=action,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.DB_FIRESTORE,
                progress_status=ProgressStatus.DONE,
                description=result.get_final_report()
            ))
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=action,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.DB_FIRESTORE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result


def batch_update_firestore_documents_array_union_extended(
    updates: List[Dict[str, Any]],
    collection: str,
    firestore_client: firestore.Client,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Updates multiple Firestore documents in a batch using ArrayUnion.

    Args:
        updates: A list of dictionaries, each containing:
            - 'document_id': The ID of the document to update.
            - 'array_field': The name of the array field to update.
            - 'data_to_add': A list containing the single item to add to the array.
        collection: The name of the Firestore collection.
        firestore_client: Initialized Firestore client.
        pipelinemon: Optional pipeline monitoring object.
        logger: Optional logger instance.
        print_out: Whether to print output.
        raise_e: Whether to raise exceptions.

    Returns:
        FunctionResult indicating the status of the batch operation.
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(collection=collection, documents_to_update_count=len(updates))
    action = Action.PERSIST_MERGE_DOCUMENT # Using MERGE as we are adding to existing arrays

    batch = firestore_client.batch()
    updated_doc_ids = []

    try:
        result.add_state("BATCH_UPDATE_STARTED")
        if not updates:
            result.add_notice("No updates provided for batch operation.")
            result.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            result.final()
            return result

        for update_info in updates:
            doc_id = update_info.get('document_id')
            array_field = update_info.get('array_field')
            data_to_add = update_info.get('data_to_add') # Should be a list with one element

            if not doc_id or not array_field or data_to_add is None:
                result.add_warning(f"Skipping invalid update instruction: {update_info}")
                continue

            doc_ref = firestore_client.collection(collection).document(doc_id)
            # Use ArrayUnion to append elements to the array field
            batch.update(doc_ref, {array_field: firestore.ArrayUnion(data_to_add)})
            updated_doc_ids.append(doc_id)

        if not updated_doc_ids:
             result.add_notice("No valid documents to update after filtering instructions.")
             result.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
             result.final()
             return result

        batch_results = batch.commit() # This returns a list of WriteResult objects
        result.add_state("BATCH_UPDATE_COMMITTED")
        result.add_metadata(documents_updated_count=len(updated_doc_ids), batch_commit_results=str(batch_results)) # Store commit results as string for simplicity
        result.final()

        msg = f"Successfully updated {len(updated_doc_ids)} documents in collection '{collection}'."
        log_info(msg=msg, logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_system_impacted(f"firestore_batch_update: {collection}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=action,
                resource=DataResource.DB_FIRESTORE,
                progress_status=result.progress_status,
                q=len(updated_doc_ids),
                q_unit=DataResource.DB_DOCUMENT,
                description=msg
            ))

    except GoogleAPICallError as firestore_e:
        # Handle specific Firestore API errors if needed
        handle_pipeline_operation_exception(
            e=firestore_e, result=result, action=action, resource=DataResource.DB_FIRESTORE,
            pipelinemon=pipelinemon, logger=logger, print_out=print_out, raise_e=raise_e
        )
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e, result=result, action=action, resource=DataResource.DB_FIRESTORE,
            pipelinemon=pipelinemon, logger=logger, print_out=print_out, raise_e=raise_e
        )
    finally:
        # Ensure final state is set even if commit fails partially or fully
        if result.progress_status not in ProgressStatus.get_closed_statuses():
             result.final() # Call final if not already closed by exception handler

    return result
