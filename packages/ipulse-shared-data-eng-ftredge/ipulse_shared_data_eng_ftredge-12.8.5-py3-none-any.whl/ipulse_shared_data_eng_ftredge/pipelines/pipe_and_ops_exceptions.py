from typing import Any, Dict, Optional, Union
import logging
import inspect
import json
from ipulse_shared_base_ftredge import (StructLog,
                                        LogLevel,
                                        log_warning,
                                        ProgressStatus,
                                        Resource,
                                        Action,
                                        Alert,
                                        Unit,
                                        format_exception,
                                        stringify_multiline_msg)

from .pipelineflow import  PipelineTask, Step
from .function_result import FunctionResult

class PipelineEarlyTermination(Exception):
    """
    Exception raised for controlled pipeline termination.
    
    Attributes:
        reason: Detailed explanation of termination
        step_name: Name of step that triggered termination
        log_level: LogLevel for this termination
    """
    def __init__(
        self,
        reason: str,
        step: Optional[Step]=None,
        already_logged: bool = False,
        context:Optional[str]=None,
        log_level: LogLevel = LogLevel.ERROR
    ):
        self.log_level = log_level
        self.reason = reason
        if step:
            self.step_name = step.name
            if isinstance(step, PipelineTask):
                step.add_issue(reason)
            step.final(force_status=ProgressStatus.FAILED)
        self.already_logged = already_logged
        if step:
            super().__init__(f"Exception in context {context} : STEP '{step.name}': {reason} . - Pipeline Early Termination")
        else:
            super().__init__(f"Exception in context {context} : {reason} . - Pipeline Early Termination")

def handle_pipeline_step_exception(
    e: Exception,
    context:Optional[str]=None,
    pipelinemon = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> None:
    """Centralized error handler for pipeline steps"""
    
    caller_frame = inspect.currentframe().f_back
    func_name = caller_frame.f_code.co_name if caller_frame else "unknown_step"
    
    error_details = format_exception(e, func_name)
    error_str = stringify_multiline_msg(error_details)
    log_warning(
        msg=f"EXCEPTION in {context}: {error_str}" if context else f"EXCEPTION in {func_name}: {error_str}",
        logger=logger,
        print_out=print_out
    )
    if pipelinemon:
        pipelinemon.add_log(StructLog(
            level=LogLevel.ERROR,
            e=e,
            description=error_str
        ))

    if raise_e:
        raise e from e


def handle_pipeline_operation_exception(
    e: Exception,
    result: Union[Dict[str, Any], FunctionResult],
    action: Optional[Union[Action,str]] = None,
    resource: Optional[Union[Resource,str]] = None,
    source: Optional[Union[Resource,str]] = None,
    destination: Optional[Union[Resource,str]] = None,
    alert: Optional[Alert] = None,
    q: Optional[Union[int, float]] = None,
    q_unit: Optional[Union[Unit, Resource]] = None,
    pipelinemon = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> None:
    """Centralized error handler for operations"""
    
    caller_frame = inspect.currentframe().f_back
    operation_name = caller_frame.f_code.co_name if caller_frame else "unknown_operation"
    error_details = format_exception(e, operation_name)
    result_status_info=""
    # Handle both Dict and OpResult
    if isinstance(result, FunctionResult):
        result.add_issue(json.dumps(error_details, indent=2, default=str), state_msg=str(e)) #add state
        result.final(force_status=ProgressStatus.FAILED)
        result.add_metadata(exception_details=error_details)
        result_status_info = result.get_final_report()
    elif isinstance(result, dict):
        # Legacy dict handling
        result["status"]["execution_state"] += ">>EXCEPTION "
        result["status"]["progress_status"] = ProgressStatus.FAILED
        result["status"]["issues"] += f'>> {json.dumps(error_details, indent=2, default=str)}'
        result_status_info = stringify_multiline_msg(result['status'])

    log_warning(
        msg=f"EXCEPTION: {result_status_info}",
        logger=logger,
        print_out=print_out
    )

    if pipelinemon:
        pipelinemon.add_log(StructLog(
            level=LogLevel.ERROR,
            progress_status=ProgressStatus.FAILED,
            action=action,
            resource=resource,
            source=source,
            destination=destination,
            alert=alert,
            q=q,
            q_unit=q_unit,
            e=e,
            description=result_status_info
        ))
    if raise_e:
        raise e from e