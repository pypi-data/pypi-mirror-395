# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long

"""
Corporate Actions API Sourcing Functions

This module provides functions to source corporate actions data (splits, dividends)
from external providers like EODHD.

EODHD Corporate Actions API Endpoints:
- Splits: https://eodhd.com/api/splits/{SYMBOL}?from={FROM_DATE}&to={TO_DATE}&api_token={API_TOKEN}
- Dividends: https://eodhd.com/api/div/{SYMBOL}?from={FROM_DATE}&to={TO_DATE}&api_token={API_TOKEN}

Response Format Examples:
Splits: [{"date": "2024-06-10", "split": "10/1"}]
Dividends: [{"date": "2024-03-15", "dividend": 0.25, "declarationDate": "2024-02-20", "recordDate": "2024-03-01", "paymentDate": "2024-03-15", "currency": "USD"}]
"""

from typing import Optional, List, Dict, Any
import logging
import time
import requests
from ipulse_shared_base_ftredge import LogLevel, Action, ProgressStatus, log_by_lvl, StructLog, DataResource, CorporateActionType

from ipulse_shared_data_eng_ftredge.pipelines import Pipelinemon, FunctionResult, handle_pipeline_operation_exception
import inspect


def source_splits_for_single_symbol_extended(
    api_token: str,
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    records_origin_short_ref: str = "eodhd__splits_single_symbol",
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False,
    max_retries: int = 3,
    retry_delay_seconds: int = 4
) -> FunctionResult:
    """
    Source stock split data for a single symbol from EODHD API.
    
    Args:
        api_token: EODHD API authentication token
        symbol: Stock symbol (e.g., "AAPL.US")
        from_date: Start date in YYYY-MM-DD format (optional)
        to_date: End date in YYYY-MM-DD format (optional)
        records_origin_short_ref: Data provider reference
        pipelinemon: Pipeline monitor instance
        logger: Logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        max_retries: Maximum number of retries for HTTP requests
        retry_delay_seconds: Delay between retries in seconds
    
    Returns:
        FunctionResult with data as list of split records:
        [{"date": "2024-06-10", "split": "10/1"}, ...]
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        api_url_without_token="",
        symbol=symbol,
        from_date=from_date,
        to_date=to_date,
        records_origin_short_ref=records_origin_short_ref,
        retry_attempts=0,
        max_retries=max_retries
    )

    try:
        if records_origin_short_ref == "eodhd__splits_single_symbol":
            # Build API URL
            api_url_without_token = f"https://eodhd.com/api/splits/{symbol}?fmt=json"
            if from_date:
                api_url_without_token += f"&from={from_date}"
            if to_date:
                api_url_without_token += f"&to={to_date}"
            
            api_url_with_token = api_url_without_token + f"&api_token={api_token}"
            result.add_metadata(api_url_without_token=api_url_without_token)

            # Implement retry mechanism
            retry_count = 0
            last_exception = None
            
            while retry_count <= max_retries:
                try:
                    result.add_state(f"API Request Started (attempt {retry_count + 1}/{max_retries + 1})")
                    response = requests.get(url=api_url_with_token, timeout=30)
                    result.add_state("Response Received")
                    
                    response.raise_for_status()
                    
                    # EODHD returns empty list if no splits found
                    result.data = response.json() if response.text else []
                    result.add_metadata(
                        total_records_fetched=len(result.data),
                        retry_attempts=retry_count
                    )
                    result.final()
                    
                    if pipelinemon:
                        pipelinemon.add_log(StructLog(
                            level=LogLevel.INFO,
                            action=Action.READ_HTTP_GET,
                            source=DataResource.API_EXTERNAL,
                            destination=DataResource.IN_MEMORY_DATA,
                            progress_status=result.progress_status,
                            q=len(result.data),
                            description=f"{result.get_final_report()} (after {retry_count} retries)" if retry_count > 0 else result.get_final_report()
                        ))
                    
                    log_by_lvl(
                        info_msg=f"{function_name}: Fetched {len(result.data)} split records for {symbol}" + (f" after {retry_count} retries" if retry_count > 0 else ""),
                        debug_msg=result.get_final_report(),
                        logger=logger,
                        print_out=print_out
                    )
                    
                    return result
                    
                except requests.RequestException as e:
                    retry_count += 1
                    last_exception = e
                    result.add_metadata(retry_attempts=retry_count)
                    
                    if retry_count <= max_retries:
                        warning_msg = f"API request failed (attempt {retry_count}/{max_retries + 1}): {str(e)}. Retrying in {retry_delay_seconds} seconds..."
                        result.add_state(f"Request failed: {str(e)}. Retrying...")
                        
                        if pipelinemon:
                            pipelinemon.add_log(StructLog(
                                level=LogLevel.WARNING,
                                action=Action.READ_HTTP_GET,
                                source=DataResource.API_EXTERNAL,
                                destination=DataResource.IN_MEMORY_DATA,
                                progress_status=ProgressStatus.IN_PROGRESS_WITH_WARNINGS,
                                description=warning_msg
                            ))
                        
                        log_by_lvl(
                            warning_msg=warning_msg,
                            logger=logger,
                            print_out=print_out
                        )
                        
                        time.sleep(retry_delay_seconds)
                    else:
                        error_msg = f"API request failed after {max_retries + 1} attempts: {str(e)}"
                        result.add_state(f"All retry attempts failed: {str(e)}")
                        raise Exception(error_msg) from e
            
            if last_exception:
                raise last_exception
                
        else:
            raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_HTTP_GET,
            source=DataResource.API_EXTERNAL,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )
    
    return result


def source_dividends_for_single_symbol_extended(
    api_token: str,
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    records_origin_short_ref: str = "eodhd__dividends_single_symbol",
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False,
    max_retries: int = 3,
    retry_delay_seconds: int = 4
) -> FunctionResult:
    """
    Source dividend data for a single symbol from EODHD API.
    
    Args:
        api_token: EODHD API authentication token
        symbol: Stock symbol (e.g., "AAPL.US")
        from_date: Start date in YYYY-MM-DD format (optional)
        to_date: End date in YYYY-MM-DD format (optional)
        records_origin_short_ref: Data provider reference
        pipelinemon: Pipeline monitor instance
        logger: Logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        max_retries: Maximum number of retries for HTTP requests
        retry_delay_seconds: Delay between retries in seconds
    
    Returns:
        FunctionResult with data as list of dividend records:
        [{
            "date": "2024-03-15",
            "dividend": 0.25,
            "declarationDate": "2024-02-20",
            "recordDate": "2024-03-01",
            "paymentDate": "2024-03-15",
            "currency": "USD"
        }, ...]
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        api_url_without_token="",
        symbol=symbol,
        from_date=from_date,
        to_date=to_date,
        records_origin_short_ref=records_origin_short_ref,
        retry_attempts=0,
        max_retries=max_retries
    )

    try:
        if records_origin_short_ref == "eodhd__dividends_single_symbol":
            # Build API URL
            api_url_without_token = f"https://eodhd.com/api/div/{symbol}?fmt=json"
            if from_date:
                api_url_without_token += f"&from={from_date}"
            if to_date:
                api_url_without_token += f"&to={to_date}"
            
            api_url_with_token = api_url_without_token + f"&api_token={api_token}"
            result.add_metadata(api_url_without_token=api_url_without_token)

            # Implement retry mechanism
            retry_count = 0
            last_exception = None
            
            while retry_count <= max_retries:
                try:
                    result.add_state(f"API Request Started (attempt {retry_count + 1}/{max_retries + 1})")
                    response = requests.get(url=api_url_with_token, timeout=30)
                    result.add_state("Response Received")
                    
                    response.raise_for_status()
                    
                    # EODHD returns empty list if no dividends found
                    result.data = response.json() if response.text else []
                    result.add_metadata(
                        total_records_fetched=len(result.data),
                        retry_attempts=retry_count
                    )
                    result.final()
                    
                    if pipelinemon:
                        pipelinemon.add_log(StructLog(
                            level=LogLevel.INFO,
                            action=Action.READ_HTTP_GET,
                            source=DataResource.API_EXTERNAL,
                            destination=DataResource.IN_MEMORY_DATA,
                            progress_status=result.progress_status,
                            q=len(result.data),
                            description=f"{result.get_final_report()} (after {retry_count} retries)" if retry_count > 0 else result.get_final_report()
                        ))
                    
                    log_by_lvl(
                        info_msg=f"{function_name}: Fetched {len(result.data)} dividend records for {symbol}" + (f" after {retry_count} retries" if retry_count > 0 else ""),
                        debug_msg=result.get_final_report(),
                        logger=logger,
                        print_out=print_out
                    )
                    
                    return result
                    
                except requests.RequestException as e:
                    retry_count += 1
                    last_exception = e
                    result.add_metadata(retry_attempts=retry_count)
                    
                    if retry_count <= max_retries:
                        warning_msg = f"API request failed (attempt {retry_count}/{max_retries + 1}): {str(e)}. Retrying in {retry_delay_seconds} seconds..."
                        result.add_state(f"Request failed: {str(e)}. Retrying...")
                        
                        if pipelinemon:
                            pipelinemon.add_log(StructLog(
                                level=LogLevel.WARNING,
                                action=Action.READ_HTTP_GET,
                                source=DataResource.API_EXTERNAL,
                                destination=DataResource.IN_MEMORY_DATA,
                                progress_status=ProgressStatus.IN_PROGRESS_WITH_WARNINGS,
                                description=warning_msg
                            ))
                        
                        log_by_lvl(
                            warning_msg=warning_msg,
                            logger=logger,
                            print_out=print_out
                        )
                        
                        time.sleep(retry_delay_seconds)
                    else:
                        error_msg = f"API request failed after {max_retries + 1} attempts: {str(e)}"
                        result.add_state(f"All retry attempts failed: {str(e)}")
                        raise Exception(error_msg) from e
            
            if last_exception:
                raise last_exception
                
        else:
            raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_HTTP_GET,
            source=DataResource.API_EXTERNAL,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )
    
    return result


def source_corporate_actions_for_single_symbol_extended(
    api_token: str,
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False,
    max_retries: int = 3,
    retry_delay_seconds: int = 4
) -> FunctionResult:
    """
    Source both splits and dividends for a single symbol.
    
    This is a convenience wrapper that calls both split and dividend APIs
    and combines the results with proper action type labeling.
    
    Returns:
        FunctionResult with data as dict:
        {
            "splits": [...],  # Raw split records from EODHD
            "dividends": [...]  # Raw dividend records from EODHD
        }
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(symbol=symbol, from_date=from_date, to_date=to_date)
    
    try:
        # Fetch splits
        splits_result = source_splits_for_single_symbol_extended(
            api_token=api_token,
            symbol=symbol,
            from_date=from_date,
            to_date=to_date,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e,
            max_retries=max_retries,
            retry_delay_seconds=retry_delay_seconds
        )
        result.integrate_result(splits_result)
        
        # Fetch dividends
        dividends_result = source_dividends_for_single_symbol_extended(
            api_token=api_token,
            symbol=symbol,
            from_date=from_date,
            to_date=to_date,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e,
            max_retries=max_retries,
            retry_delay_seconds=retry_delay_seconds
        )
        result.integrate_result(dividends_result)
        
        # Combine results
        result.data = {
            "splits": splits_result.data if splits_result.is_success else [],
            "dividends": dividends_result.data if dividends_result.is_success else []
        }
        
        result.add_metadata(
            total_splits=len(result.data["splits"]),
            total_dividends=len(result.data["dividends"]),
            total_actions=len(result.data["splits"]) + len(result.data["dividends"])
        )
        
        result.final()
        
        log_by_lvl(
            info_msg=f"{function_name}: Fetched {len(result.data['splits'])} splits and {len(result.data['dividends'])} dividends for {symbol}",
            debug_msg=result.get_final_report(),
            logger=logger,
            print_out=print_out
        )
        
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_HTTP_GET,
            source=DataResource.API_EXTERNAL,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )
    
    return result


def source_last_actions_for_exchange_extended(
    api_token: str,
    exchange_code: str,
    action_type: CorporateActionType,  # 'splits' or 'dividends'
    date: Optional[str] = None,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False,
    max_retries: int = 3,
    retry_delay_seconds: int = 4
) -> FunctionResult:
    """
    Source bulk splits or dividends for an exchange for the latest day.
    
    Args:
        api_token: EODHD API authentication token
        exchange_code: Exchange code (e.g., "US")
        action_type: CorporateActionType (SPLITS or DIVIDENDS)
        date: Specific date to fetch in YYYY-MM-DD format (optional)
        pipelinemon: Pipeline monitor instance
        logger: Logger instance
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        max_retries: Maximum number of retries for HTTP requests
        retry_delay_seconds: Delay between retries in seconds
        
    Returns:
        FunctionResult with data as list of records
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        exchange_code=exchange_code,
        action_type=str(action_type),
        date=date,
        retry_attempts=0,
        max_retries=max_retries
    )
    
    try:
        # EODHD Bulk Last Day supports type=splits and type=dividends
        url = f"https://eodhd.com/api/eod-bulk-last-day/{exchange_code}?api_token={api_token}&fmt=json&type={action_type}"
        if date:
            url += f"&date={date}"
        
        # Mask token for metadata
        url_masked = url.replace(api_token, "***")
        result.add_metadata(api_url_without_token=url_masked)
        
        # Implement retry mechanism
        retry_count = 0
        last_exception = None
        
        while retry_count <= max_retries:
            try:
                result.add_state(f"API Request Started (attempt {retry_count + 1}/{max_retries + 1})")
                response = requests.get(url, timeout=30)
                result.add_state("Response Received")
                
                response.raise_for_status()
                
                # EODHD returns empty list or list of records
                data = response.json()
                result.data = data if isinstance(data, list) else []
                
                result.add_metadata(
                    count=len(result.data), 
                    type=action_type,
                    retry_attempts=retry_count
                )
                result.final()
                
                if pipelinemon:
                    pipelinemon.add_log(StructLog(
                        level=LogLevel.INFO,
                        action=Action.READ_HTTP_GET,
                        source=DataResource.API_EXTERNAL,
                        destination=DataResource.IN_MEMORY_DATA,
                        progress_status=result.progress_status,
                        q=len(result.data),
                        description=f"{result.get_final_report()} (after {retry_count} retries)" if retry_count > 0 else result.get_final_report()
                    ))
                
                log_by_lvl(
                    info_msg=f"{function_name}: Fetched {len(result.data)} {action_type} records for {exchange_code}" + (f" after {retry_count} retries" if retry_count > 0 else ""),
                    debug_msg=result.get_final_report(),
                    logger=logger,
                    print_out=print_out
                )
                
                return result
                
            except requests.RequestException as e:
                retry_count += 1
                last_exception = e
                result.add_metadata(retry_attempts=retry_count)
                
                if retry_count <= max_retries:
                    warning_msg = f"API request failed (attempt {retry_count}/{max_retries + 1}): {str(e)}. Retrying in {retry_delay_seconds} seconds..."
                    result.add_state(f"Request failed: {str(e)}. Retrying...")
                    
                    if pipelinemon:
                        pipelinemon.add_log(StructLog(
                            level=LogLevel.WARNING,
                            action=Action.READ_HTTP_GET,
                            source=DataResource.API_EXTERNAL,
                            destination=DataResource.IN_MEMORY_DATA,
                            progress_status=ProgressStatus.IN_PROGRESS_WITH_WARNINGS,
                            description=warning_msg
                        ))
                    
                    log_by_lvl(
                        warning_msg=warning_msg,
                        logger=logger,
                        print_out=print_out
                    )
                    
                    time.sleep(retry_delay_seconds)
                else:
                    error_msg = f"API request failed after {max_retries + 1} attempts: {str(e)}"
                    result.add_state(f"All retry attempts failed: {str(e)}")
                    raise Exception(error_msg) from e
        
        if last_exception:
            raise last_exception
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.READ_HTTP_GET,
            source=DataResource.API_EXTERNAL,
            destination=DataResource.IN_MEMORY_DATA,
            pipelinemon=pipelinemon,
            logger=logger,
            print_out=print_out,
            raise_e=raise_e
        )
    
    return result
