import contextlib
from typing import Optional
import logging
from ipulse_shared_base_ftredge import LogLevel, AbstractResource, StructLog, ProgressStatus, format_exception
from .pipelinemon import Pipelinemon
from .pipelineflow import PipelineTask

@contextlib.contextmanager
def task_validation_and_execution_context(task: PipelineTask, 
                         pipelinemon: Pipelinemon, 
                         generallogger: logging.Logger,
                         sequence_ref: Optional[str] = None,
                         intentionally_skip: bool = False):
    """Context manager for standardized task execution handling."""
    if not task.validate_and_start(sequence_ref=sequence_ref,intentionally_skip=intentionally_skip):
        if task.progress_status in ( ProgressStatus.DISABLED, ProgressStatus.INTENTIONALLY_SKIPPED):
            generallogger.info(f"Task '{task.name}' didn't pass validation. Task Stauts :{task.progress_status}.")
        else:
            generallogger.warning(f"Task '{task.name}' failed validation. Task Stauts :{task.progress_status}. Final report: {task.final_report}")
        yield False
        return

    with pipelinemon.context(task.name):
        try:
            yield True
            ##### =====>  CHECK IF task.final() was required here
            # Don't call task.final() here to avoid double finalization

        except Exception as e:
            task.add_issue(f"Exception Occured {format_exception(e)}")

        finally:
            # Only call final() once, here in the finally block
            task.final()
            if task.final_log_level == LogLevel.ERROR:
                generallogger.warning(f"Task {task.name} FAILED. Final report: {task.final_report}")
                pipelinemon.add_log(StructLog(
                    level=LogLevel.ERROR,
                    resource=AbstractResource.PIPELINE_TASK,
                    progress_status=task.progress_status,
                    description=task.final_report
                ))
            elif task.final_log_level == LogLevel.WARNING:
                generallogger.warning(f"Task has WARNINGS. Final report: {task.final_report}")
                pipelinemon.add_log(StructLog(
                    level=LogLevel.WARNING,
                    resource=AbstractResource.PIPELINE_TASK,
                    progress_status=task.progress_status,
                    description=task.final_report
                ))
            else:
                notices = ""
                if task.final_log_level == LogLevel.NOTICE:
                    notices = f"NOTICES: {task.notices}"
                generallogger.info(f"Task '{task.name}' finished with Status: {task.progress_status}. {notices}")
