# pylint: disable=line-too-long
from copy import deepcopy
from typing import Dict, List, Union, Optional, Callable
import inspect
import logging 
import datetime
from ipulse_shared_base_ftredge import StructLog, LogLevel, Action, DataResource, log_by_lvl, val_as_str
from ipulse_shared_data_eng_ftredge.pipelines import Pipelinemon, handle_pipeline_operation_exception, FunctionResult

def _ensure_list_input(records_input: Union[Dict, List[Dict]]) -> List[Dict]:
    """Convert single dict to list if needed"""
    return [records_input] if isinstance(records_input, dict) else records_input

def _get_provider_processor(records_origin_short_ref: str) -> Optional[Callable]:
    """Get the appropriate processor function for a provider"""
    processors = {
        "eodhd__eod_historic_bulk_single_symbol": lambda record: {
            # Transform date to date_id
            'date_id': record.pop('date', None),
            # We return only the transformed field, other fields stay as they are
        },
        "eodhd__eod_last_day_multiple_symbols": lambda record: {
            # Transform date to date_id
            'date_id': record.pop('date', None),
            # We return only the transformed field, other fields stay as they are
        }
    }
    return processors.get(records_origin_short_ref)

def market_single_symbol_provider_preproc(
    records_origin_short_ref: str,
    records_input: Union[Dict, List[Dict]],
    asset_id: str,
    asset_symbol_pulse: str,
    exchange_id: str,
    event_time: Union[str, datetime.datetime],
    exchange_code_pulse: str,
    subject_category: str,
    change_id: str,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
) -> FunctionResult:
    """
    Preprocesses the original records for a single symbol by applying provider-specific transformations.
    Supports both a single record (dict) and multiple records (list of dicts).
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        asset_symbol_pulse=asset_symbol_pulse,
        records_origin_short_ref=records_origin_short_ref,
        exchange_code_pulse=exchange_code_pulse,
        change_id=change_id
    )

    try:
        processor = _get_provider_processor(records_origin_short_ref)
        if not processor:
            raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")
        #check and ensure that event time is in isoformat:
        if isinstance(event_time, str):
            # Check if it's already in ISO format
            try:
                datetime.datetime.fromisoformat(event_time)  # Validate ISO format
            except ValueError:
                raise ValueError(f"Invalid ISO format for event_time: {event_time}")
        elif isinstance(event_time, datetime.datetime):
            # Convert datetime to ISO string
            event_time = val_as_str(event_time)
        else:
            raise ValueError(f"event_time must be a string or datetime, got {type(event_time)}")
        
        processed_description = [">>Provider-specific preprocessing steps:"]
        processed_records = deepcopy(_ensure_list_input(records_input))

        # Process records
        for record in processed_records:
            processed_fields = processor(record)
            record.update(processed_fields)
            
            record.update({
                "asset_id": asset_id,
                "asset_symbol_pulse": asset_symbol_pulse,
                "exchange_id": exchange_id,
                "exchange_code_pulse": exchange_code_pulse,
                "subject_category": subject_category,
                "change_id": change_id,
                "updated_at": event_time
            })

        processed_description.append("--Field transformations applied--")
        processed_description.append("--Added asset/exchange metadata fields--")
        
        result.data = processed_records
        result.add_metadata(
            processed_description='--'.join(processed_description),
            original_date_col_name="date"
        )
        result.final()

        if pipelinemon:
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=Action.TRANSFORM_PREPROCESS,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.IN_MEMORY_DATA,
                progress_status=result.progress_status,
                q=len(processed_records),
                description=result.get_final_report()
            ))
        
        log_by_lvl(
            info_msg=f"{function_name}: {len(processed_records)} records",
            debug_msg=result.get_final_report(),
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.TRANSFORM_PREPROCESS,
            resource=DataResource.DATA,
            pipelinemon=pipelinemon
        )
        
    return result

def market_single_symbol_common_preproc(
    records_input: Union[List[Dict], Dict],
    round_prices: bool = True,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    **kwargs
) -> FunctionResult:
    """
    Applies common preprocessing steps to market data for a single symbol.
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    try:
        processed_description = [">> Common preprocessing steps:"]
        processed_records = []

        price_fields = ['open', 'high', 'low', 'close']
        def round_value(value): return round(value, 3 if value <= 1 else 2)

        # Process entries
        adjusted_close_removed = False
        for entry in _ensure_list_input(records_input):
            processed_entry = entry.copy()
            
            # Remove adjusted_close if present (we don't use it anymore)
            if 'adjusted_close' in processed_entry:
                processed_entry.pop('adjusted_close')
                adjusted_close_removed = True
            
            if round_prices:
                for key in price_fields:
                    if processed_entry.get(key) is not None:
                        processed_entry[key] = round_value(float(processed_entry[key]))
            
            processed_records.append(processed_entry)
        
        if adjusted_close_removed:
            processed_description.append("--Removed adjusted_close field (not stored)--")
        
        if round_prices:
            processed_description.append("--Rounded prices to 2 decimals (3 decimals if price <= 1)--")

        result.data = processed_records
        result.add_metadata(processed_description='--'.join(processed_description))
        result.final()


        if pipelinemon:
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.IN_MEMORY_DATA,
                action=Action.TRANSFORM_PREPROCESS,
                progress_status=result.progress_status,
                q=len(processed_records),
                description=result.get_final_report()
            ))
        log_by_lvl(
            info_msg=f"{function_name}: {len(processed_records)} records",
            debug_msg=result.get_final_report(),
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.TRANSFORM_PREPROCESS,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon
        )

    return result

def market_multi_symbol_provider_preproc(
    records_origin_short_ref: str,
    assets_records: Dict[str, Dict],  # Dict of asset_id -> record data
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
) -> FunctionResult:
    """
    Batch preprocess multiple assets' records by applying provider-specific transformations.
    
    Args:
        records_origin_short_ref: Provider reference
        assets_records: Dictionary where:
            - keys are asset_ids
            - values are dictionaries containing:
                - records_input: The record data (dict or list of dicts)
                - asset_symbol_pulse: Symbol
                - exchange_id: Exchange ID
                - exchange_code_pulse: Exchange code
                - subject_category: Asset subject category
                - event_time: Processing time
                - change_id: Change ID
                
    Returns:
        FunctionResult with processed records keyed by asset_id
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        records_origin_short_ref=records_origin_short_ref,
        assets_count=len(assets_records)
    )

    try:
        processor = _get_provider_processor(records_origin_short_ref)
        if not processor:
            raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")
        
        total_processed_records = 0
        processed_results = {}
        
        # Process each asset's records
        for asset_id, asset_data in assets_records.items():
            # Validate required fields
            required_fields = ["records_input", "asset_symbol_pulse", "exchange_id", 
                              "exchange_code_pulse", "subject_category", "event_time", "change_id"]
            
            for field in required_fields:
                if field not in asset_data:
                    raise ValueError(f"Missing required field {field} for asset {asset_id}")
            
            # Format event_time if needed
            event_time = asset_data["event_time"]
            if isinstance(event_time, datetime.datetime):
                event_time = val_as_str(event_time)
            elif not isinstance(event_time, str):
                raise ValueError(f"event_time must be a string or datetime, got {type(event_time)}")
            
            # Process the records - for EOD bulk sourcing, this will be a single record per asset
            processed_records = deepcopy(_ensure_list_input(asset_data["records_input"]))
            
            for record in processed_records:
                # First, remove all unwanted fields from provider data
                unwanted_fields = ['code', 'exchange_short_name', 'prev_close', 'change', 'change_p']
                for field in unwanted_fields:
                    if field in record:
                        record.pop(field, None)
                
                # Apply provider-specific processing to transform date to date_id
                processed_fields = processor(record)
                record.update(processed_fields)
                
                # Add required metadata fields to match BigQuery schema
                record.update({
                    "asset_id": asset_id,
                    "asset_symbol_pulse": asset_data["asset_symbol_pulse"],
                    "exchange_id": asset_data["exchange_id"],
                    "exchange_code_pulse": asset_data["exchange_code_pulse"],
                    "subject_category": asset_data["subject_category"],
                    "change_id": asset_data["change_id"],
                    "updated_at": event_time,
                    "values_history": asset_data.get("values_history"),
                    "changelog_history": asset_data.get("changelog_history")
                })
            
            processed_results[asset_id] = processed_records
            total_processed_records += len(processed_records)
        
        result.data = processed_results
        result.add_metadata(
            processed_description='Provider-specific preprocessing completed: date→date_id transformation, field standardization, metadata enrichment',
            total_processed_records=total_processed_records
        )
        result.final()

        if pipelinemon:
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=Action.TRANSFORM_PREPROCESS,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.IN_MEMORY_DATA,
                progress_status=result.progress_status,
                q=total_processed_records,
                description=f"Processed {len(assets_records)} assets with {total_processed_records} total records"
            ))
        
        log_by_lvl(
            info_msg=f"{function_name}: {total_processed_records} records across {len(assets_records)} assets",
            debug_msg=result.get_final_report(),
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.TRANSFORM_PREPROCESS,
            resource=DataResource.DATA,
            pipelinemon=pipelinemon
        )
        
    return result

def market_multi_symbol_common_preproc(
    assets_records: Dict[str, List[Dict]],  # Dict of asset_id -> record list
    round_prices: bool = True,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
) -> FunctionResult:
    """
    Applies common preprocessing steps to market data for multiple assets in batch.
    
    Args:
        assets_records: Dictionary where keys are asset_ids and values are lists of records
        round_prices: Whether to round price values
        
    Returns:
        FunctionResult with processed records keyed by asset_id
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)

    try:
        price_fields = ['open', 'high', 'low', 'close']
        def round_value(value): 
            if value is None:
                return None
            return round(float(value), 3 if float(value) <= 1 else 2)
        
        total_processed_records = 0
        processed_results = {}
        
        # Process each asset's records
        for asset_id, records in assets_records.items():
            processed_records = []
            
            for entry in records:
                processed_entry = entry.copy()
                
                # Remove adjusted_close if present (we don't use it anymore)
                if 'adjusted_close' in processed_entry:
                    processed_entry.pop('adjusted_close')
                
                # Round price fields for better display and storage consistency
                if round_prices:
                    for key in price_fields:
                        if processed_entry.get(key) is not None:
                            processed_entry[key] = round_value(float(processed_entry[key]))
                                    
                processed_records.append(processed_entry)
            
            processed_results[asset_id] = processed_records
            total_processed_records += len(processed_records)
        
        result.data = processed_results
        result.add_metadata(
            processed_description='Common preprocessing completed: removed adjusted_close field, price rounding',
            total_processed_records=total_processed_records
        )
        result.final()

        if pipelinemon:
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.IN_MEMORY_DATA,
                action=Action.TRANSFORM_PREPROCESS,
                progress_status=result.progress_status,
                q=total_processed_records,
                description=f"Common processing for {len(assets_records)} assets with {total_processed_records} total records"
            ))
        
        log_by_lvl(
            info_msg=f"{function_name}: {total_processed_records} records across {len(assets_records)} assets",
            debug_msg=result.get_final_report(),
            logger=logger
        )

    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.TRANSFORM_PREPROCESS,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon
        )

    return result