# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
import json
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from contextlib import contextmanager
from typing import List, Optional, Union, Set, Dict, Any, Tuple
import logging
from ipulse_shared_base_ftredge import LogLevel, AbstractResource, ProgressStatus, Action,Alert, Resource, StructLog as SLog

############################################################################
##### PIPINEMON Collector for Logs and Statuses of running pipelines #######
class Pipelinemon:
    """A class for collecting logs and statuses of running pipelines.
    This class is designed to be used as a context manager, allowing logs to be
    collected, stored and reported in a structured format. The logs can be retrieved and
    analyzed at the end of the pipeline executieon, or only the counts.
    """

    # LEVELS_DIFF = 10000  # The difference in value between major log levels

    def __init__(self, base_context: str, logger,
                 max_log_field_len:Optional[int]=8000, #by detault PipelineLog has 8000 per field length Limit
                 max_log_dict_byte_size:Optional[float]=256 * 1024 * 0.80): #by detault PipelineLog dict has 256 * 1024 * 0.80 -80% of 256Kb Limit 
        # Create ID with timestamp prefix and UUID suffix
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        uuid_suffix = str(uuid.uuid4())[:8]  # Take first 8 chars of UUID
        self._id = f"{timestamp}_{uuid_suffix}"
        
        self._logs = []
        self._early_stop = False
        self._early_stop_reason = None  # Track what caused early stop
        self._systems_impacted = []
        self._by_event_count = defaultdict(int)
        self._by_level_code_count = defaultdict(int)
        self._base_context = base_context
        self._context_stack = []
        self._logger = logger
        self._max_log_field_len = max_log_field_len
        self._max_log_bytes_limit = max_log_dict_byte_size
        self._start_time = None  # Add start time variable
        self._progress_status = None  # Add progress status for access after end()
        self._final_level = None  # Add final level for access after end()
        
        # Subject-specific counting for ETL tracking
        self._subject_counts = {
            'total_countables': 0,
            'countables_success': 0,
            'countables_errors': 0,
            'countables_warnings': 0,
            'countables_notices': 0,
            'countable_subject_name': None,
            'subject_resource': AbstractResource.PIPELINE_SUBJECT_SEQUENCE
        }

    @contextmanager
    def context(self, context: str):
        """Safer context management with type checking"""
        if not isinstance(context, str):
            raise TypeError("Context must be a string")
        self.push_context(context)
        try:
            yield
        finally:
            self.pop_context()

    def push_context(self, context):
        self._context_stack.append(context)

    def pop_context(self):
        if self._context_stack:
            self._context_stack.pop()

    @property
    def current_context(self):
        return " >> ".join(self._context_stack)

    @property
    def base_context(self):
        return self._base_context
    
    @base_context.setter
    def base_context(self, value):
        self._base_context = value

    @property
    def id(self):
        return self._id

    @property
    def logger(self):
        return self._logger

    @property
    def by_event_count(self):
        return dict(self._by_event_count)

    @property
    def by_level_code_count(self):
        return dict(self._by_level_code_count)

    @property
    def systems_impacted(self):
        return self._systems_impacted

    @systems_impacted.setter
    def systems_impacted(self, list_of_si: List[str]):
        self._systems_impacted = list_of_si

    def add_system_impacted(self, system_impacted: str)-> None:
        if self._systems_impacted is None:
            self._systems_impacted = []
        self._systems_impacted.append(system_impacted)

    def clear_systems_impacted(self):
        self._systems_impacted = []

    @property
    def max_log_dict_byte_size(self):
        return self._max_log_bytes_limit

    @max_log_dict_byte_size.setter
    def max_log_dict_byte_size(self, value):
        self._max_log_bytes_limit = value

    @property
    def max_log_field_size(self):
        return self._max_log_field_len

    @max_log_field_size.setter
    def max_log_field_size(self, value):
        self._max_log_field_len = value

    @property
    def early_stop(self):
        return self._early_stop

    def set_early_stop(self, reason: str, e: Optional[Exception] = None):
        """Sets the early stop flag and optionally logs an error."""
        self._early_stop = True
        self._early_stop_reason = f"{reason} : {str(e)}" if e else reason  # Store the reason for early stop
        self.add_log(SLog( level=LogLevel.ERROR,
                resource=AbstractResource.PIPELINEMON,
                alert=Alert.SYSTEM_EARLY_TERMINATION,
                e=e))
        

    def reset_early_stop(self):
        self._early_stop = False

    @property
    def early_stop_reason(self):
        return self._early_stop_reason

    @property
    def progress_status(self) -> Optional[ProgressStatus]:
        """Get the final progress status set after end() is called"""
        return self._progress_status

    @property
    def final_level(self) -> Optional[LogLevel]:
        """Get the final log level set after end() is called"""
        return self._final_level

    @property
    def subject_counts(self) -> Dict[str, Any]:
        """Get subject-specific counts for ETL tracking"""
        return self._subject_counts.copy()


    def start(self, pipeline_description: str):
        """Logs the start of the pipeline execution."""
        self._start_time = datetime.now(timezone.utc)  # Capture the start time
        self.add_log(SLog(
                        level=LogLevel.INFO,
                        resource=AbstractResource.PIPELINEMON,
                        action=Action.EXECUTE,
                        progress_status=ProgressStatus.IN_PROGRESS,
                        description=pipeline_description
                    ))

    def get_duration_since_start(self) -> Optional[str]:
        """Returns the duration since the pipeline started, formatted as HH:MM:SS."""
        if self._start_time is None:
            return None
        elapsed_time = datetime.now(timezone.utc) - self._start_time
        return str(elapsed_time)


    def _update_counts(self, log: SLog, remove=False):
        """Update counts for event tracking considering source and destination"""
        event_tuple = log.getEvent()  # Now includes source and destination
        level = log.level

        if remove:
            self._by_event_count[event_tuple] -= 1
            self._by_level_code_count[level.value] -= 1
        else:
            self._by_event_count[event_tuple] += 1
            self._by_level_code_count[level.value] += 1


    def add_log(self, log: SLog ):
        log.base_context = self.base_context
        log.context = self.current_context if self.current_context else "root"
        log.collector_id = self.id
        log.systems_impacted = self.systems_impacted
        log_dict = log.to_dict(max_field_len=self.max_log_field_size,
                               byte_size_limit=self.max_log_dict_byte_size)
        self._logs.append(log_dict)
        self._update_counts(log=log)  # Pass the context to _update_counts

        if self._logger:
            # We specifically want to avoid having an ERROR log level for this structured Pipelinemon reporting, to ensure Errors are alerting on Critical Application Services.
            # A single ERROR log level is usually added at the end of the entire pipeline
            if log.level.value >= LogLevel.WARNING.value:
                self._logger.warning(log_dict)
            elif log.level.value >= LogLevel.INFO.value:
                self._logger.info(log_dict)
            else:
                self._logger.debug(log_dict)

    def add_logs(self, logs: List[SLog]):
        for log in logs:
            self.add_log(log)

    def clear_logs_and_counts(self):
        self._logs = []
        self._by_level_code_count = defaultdict(int)
        self._by_event_count= defaultdict(int)
    

    def clear_logs(self):
        self._logs = []
        self.clear_systems_impacted()

    def get_all_logs(self,in_json_format=False):
        if in_json_format:
            return json.dumps(self._logs)
        return self._logs

    def contains_any_logs_for_levels(
        self,
        levels: Union[LogLevel, List[LogLevel]],
    ) -> bool:
        """
        Checks if any logs exist at the given log level(s).
        """
        if isinstance(levels, LogLevel):
            levels = [levels]
        return any(
            self.by_level_code_count.get(lvl.value, 0) > 0
            for lvl in levels
        )
    def contains_any_errors(self) -> bool:
        """
        Check if any logs exist at ERROR level or higher.
        (WARNING, ERROR, CRITICAL, etc.)
        """
        return any(
            count > 0 and code >= LogLevel.ERROR.value
            for code, count in self.by_level_code_count.items()
        )
    

    def count_total_logs_for_levels(self, level:  Union[LogLevel, List[LogLevel]]) -> int:
        """
        Returns the total number of logs at a specific level or list of levels (long-term memory).
        """
        if isinstance(level, LogLevel):
            level = [level]
        return sum(
            count
            for code, count in self.by_level_code_count.items()
            if code in {lvl.value for lvl in level}
        )


    def count_warnings_and_errors(self) -> int:
        """
        Count logs at WARNING level or higher.
        (WARNING, ERROR, CRITICAL, etc.)
        """
        return sum(
            count
            for code, count in self.by_level_code_count.items()
            if code >= LogLevel.WARNING.value
        )

    
    ######### VERY IMPORTANT FUNCTION FOR COUNTING #########
    def count_logs_for_events_containing(
    self,
    levels: Optional[Union[LogLevel, List[LogLevel]]] = None,
    context: Optional[str] = None,
    exclude_nested_contexts: bool = False,
    progress_statuses: Optional[Union[ProgressStatus, List[ProgressStatus], set, frozenset]] = None,
    resources: Optional[Union[Resource, List[Resource]]] = None,
    sources: Optional[Union[Resource, List[Resource]]] = None,  # New parameter
    destinations: Optional[Union[Resource, List[Resource]]] = None  # New parameter
    ) -> int:
        """
        Count logs matching specified criteria.

        Args:
            levels: LogLevel(s) to match. If None, count logs for all levels.
            context: Context to filter by.
            exclude_nested_contexts: If True, match context exactly. +@ If False, match context prefix.@
            +,
            
            progress_statuses: Single ProgressStatus, list of ProgressStatus values,
                            set/frozenset of ProgressStatus values, or a ProgressStatus class attribute containing a frozenset.
            resource: Single Resource or list of Resources to filter by.
            sources: Source resource(s) to match
            destinations: Destination resource(s) to match
        """
        # If levels is None, consider all log levels
        if levels is None:
            level_values = {level.value for level in LogLevel}
        else:
            # Convert single LogLevel to a list
            if isinstance(levels, LogLevel):
                levels = [levels]
            level_values = {level.value for level in levels}

        # Convert progress_statuses to set of names if needed
        allowed_status_names = None
        if progress_statuses is not None:
            if isinstance(progress_statuses, (set, frozenset)):
                allowed_status_names = {str(ps) for ps in progress_statuses if isinstance(ps, ProgressStatus)}
            elif isinstance(progress_statuses, list):
                allowed_status_names = {str(ps) for ps in progress_statuses if isinstance(ps, ProgressStatus)}
            elif isinstance(progress_statuses, ProgressStatus):
                allowed_status_names = {str(progress_statuses)}

        # Convert resource to set of names if needed
        allowed_resource_names = None
        if resources is not None:
            if isinstance(resources, list):
                allowed_resource_names = {str(res) for res in resources if isinstance(res, Resource)}
            elif isinstance(resources, Resource):
                allowed_resource_names = {str(resources)}

        # Convert sources to set of names if needed
        allowed_source_names = None
        if sources is not None:
            if isinstance(sources, list):
                allowed_source_names = {str(src) for src in sources if isinstance(src, Resource)}
            elif isinstance(sources, Resource):
                allowed_source_names = {str(sources)}

        # Convert destinations to set of names if needed
        allowed_destination_names = None
        if destinations is not None:
            if isinstance(destinations, list):
                allowed_destination_names = {str(dst) for dst in destinations if isinstance(dst, Resource)}
            elif isinstance(destinations, Resource):
                allowed_destination_names = {str(destinations)}

        def matches_criteria(log: Dict[str, Any]) -> bool:
            # Check level
            if log["level_code"] not in level_values:
                return False

            # Check context
            if context is not None:
                log_ctx = log.get("context", "")
                if exclude_nested_contexts:
                    if log_ctx != context:
                        return False
                else:
                    if not log_ctx.startswith(context):
                        return False

            # Check resource
            if allowed_resource_names is not None:
                if log.get("resource") not in allowed_resource_names:
                    return False

            # Check progress status
            if allowed_status_names is not None:
                if log.get("progress_status") not in allowed_status_names:
                    return False

            # Check source
            if allowed_source_names is not None:
                if log.get("source") not in allowed_source_names:
                    return False

            # Check destination
            if allowed_destination_names is not None:
                if log.get("destination") not in allowed_destination_names:
                    return False

            return True

        return sum(matches_criteria(log) for log in self._logs)



    def count_logs_for_current_context(
        self,
        levels: Optional[Union[LogLevel, List[LogLevel]]] = None,
        exclude_nested_contexts: bool = False,
        progress_status: Optional[ProgressStatus] = None
    ) -> int:
        """Count logs in current context matching criteria."""
        return self.count_logs_for_events_containing(
            levels=levels,
            context=self.current_context,
            exclude_nested_contexts=exclude_nested_contexts,
            progress_statuses=progress_status
        )
    
    def log_level_and_progress_status_for_context(self) -> Tuple[LogLevel, ProgressStatus]:
        if self.count_logs_for_current_context(levels=LogLevel.ERROR) >0:
            return  LogLevel.ERROR, ProgressStatus.FAILED
        if self.count_logs_for_current_context(levels=LogLevel.WARNING) > 0:
            return LogLevel.WARNING, ProgressStatus.DONE_WITH_WARNINGS
        if self.count_logs_for_current_context(levels=LogLevel.NOTICE)>0:
            return LogLevel.NOTICE, ProgressStatus.DONE_WITH_NOTICES
        
        return LogLevel.INFO, ProgressStatus.IN_PROGRESS
        

    def generate_execution_summary(self, countable_subj_name: str, total_countables: int, subj_resource:Resource=AbstractResource.PIPELINE_SUBJECT_SEQUENCE, final_level:Optional[LogLevel]=None) -> str:
        duration = self.get_duration_since_start()
        
        # Check if we already have calculated subject counts (from _calculate_and_store_subject_counts)
        if (self._subject_counts and 
            self._subject_counts.get('countable_subject_name') == countable_subj_name and
            self._subject_counts.get('subject_resource') == subj_resource):
            
            # Reuse already calculated counts
            success = self._subject_counts.get('countables_success', 0)
            done_with_notices = self._subject_counts.get('countables_notices', 0)
            done_with_warnings = self._subject_counts.get('countables_warnings', 0)
            failed = self._subject_counts.get('countables_failed', 0)
            finished_with_issues = self._subject_counts.get('countables_finished_with_issues', 0)
            unfinished = self._subject_counts.get('countables_unfinished', 0)
            pending = self._subject_counts.get('countables_pending', 0)
            skipped = self._subject_counts.get('countables_skipped', 0)
            
        else:
            # Fallback to calculating counts (for backwards compatibility or when called independently)
            # Step 1: Find all events for the specified resource and collect their statuses
            event_counts = defaultdict(int)
            for event_tuple, count in self._by_event_count.items():
                if not isinstance(event_tuple, tuple):
                    continue
                    
                # Look for resource, source, or destination name and status in tuple
                found_resource = False
                found_status = None
                
                for item in event_tuple:
                    if item == str(subj_resource):
                        found_resource = True
                    elif isinstance(item, str) and any(item == str(status) for status in ProgressStatus):
                        found_status = item
                    # Also match source and destination
                    elif item == str(subj_resource):  # Match source/destination resources
                        found_resource = True
                        
                if found_resource and found_status:
                    event_counts[found_status] += count

            # Step 2: Categorize the counts
            success = sum(event_counts[str(status)] for status in ProgressStatus.success_statuses())
            done_with_notices = event_counts[str(ProgressStatus.DONE_WITH_NOTICES)]
            done_with_warnings = event_counts[str(ProgressStatus.DONE_WITH_WARNINGS)]
            failed = event_counts[str(ProgressStatus.FAILED)]
            finished_with_issues = event_counts[str(ProgressStatus.FINISHED_WITH_ISSUES)]
            unfinished = event_counts[str(ProgressStatus.UNFINISHED)]
            pending = sum(event_counts[str(status)] for status in ProgressStatus.pending_statuses())
            skipped = sum(event_counts[str(status)] for status in ProgressStatus.skipped_statuses())

        # Count different log levels from level code counts
        errors = self._by_level_code_count.get(LogLevel.ERROR.value, 0) + self._by_level_code_count.get(LogLevel.CRITICAL.value, 0)
        warnings = self._by_level_code_count.get(LogLevel.WARNING.value, 0)
        notices = self._by_level_code_count.get(LogLevel.NOTICE.value, 0)
        infos = self._by_level_code_count.get(LogLevel.INFO.value, 0)
        debugs = self._by_level_code_count.get(LogLevel.DEBUG.value, 0)

        summary = f"""
        --------------------------------------------------
        Pipeline Execution Report(Except Final PIPELINE {final_level} level)
        --------------------------------------------------
        Base Context: {self.base_context}
        Pipeline ID: {self.id}
        Early Stop: {self.early_stop}
        Early Stop Reason: {self.early_stop_reason}
        Duration: {duration}

        --------------------------------------------------
        Status Summary:
        --------------------------------------------------
        - DONE {str(subj_resource)}(s): [{success}/{total_countables}] {countable_subj_name}(s)
            - Of Which :
                    - DONE_WITH_NOTICES: [{done_with_notices}]
                    - DONE_WITH_WARNINGS: [{done_with_warnings}]
        - FAILED {str(subj_resource)}(s): [{failed}/{total_countables}] {countable_subj_name}(s)
        - FINISHED_WITH_ISSUES {str(subj_resource)}(s): [{finished_with_issues}/{total_countables}] {countable_subj_name}(s)
        - UNFINISHED {str(subj_resource)}(s): [{unfinished}/{total_countables}] {countable_subj_name}(s)
        - PENDING {str(subj_resource)}(s): [{pending}/{total_countables}] {countable_subj_name}(s)
        - SKIPPED {str(subj_resource)}(s): [{skipped}/{total_countables}] {countable_subj_name}(s)

        --------------------------------------------------
        Log Level Summary(Except Final PIPELINE {final_level} level):
        --------------------------------------------------
        - Debugs: {debugs}
        - Infos: {infos}
        - Notices: {notices}
        - Warnings: {warnings}
        - Errors: {errors}
        --------------------------------------------------
        """
        return summary
    
    def get_breakdown_by_event(self):
        """Returns a str event breakdowns."""
        breakdown_print = """
        --------------------------------------------------
        Detailed Event Breakdown (Action-Resource-Source-Destination-Alert-ProgressStatus):
        --------------------------------------------------
        """
        for event, count in self._by_event_count.items():
            # Updated to handle source and destination in event tuple
            if isinstance(event, tuple):
                event_str = " | ".join(str(e) for e in event if e is not None)
            else:
                event_str = str(event)
            breakdown_print += f"\n     - {event_str}: {count}  "
        
        breakdown_print += "\n      -------------------------------------------------- \n"
        
        return breakdown_print
    
    def _calculate_and_store_subject_counts(self, countable_subj_name: str, total_countables: int, subj_resource: Resource = AbstractResource.PIPELINE_SUBJECT_SEQUENCE):
        """Calculate and store subject-specific counts for ETL tracking reuse"""
        
        # Step 1: Find all events for the specified resource and collect their statuses
        event_counts = defaultdict(int)
        for event_tuple, count in self._by_event_count.items():
            if not isinstance(event_tuple, tuple):
                continue
                
            # Look for resource name and status in tuple
            found_resource = False
            found_status = None
            
            for item in event_tuple:
                if item == str(subj_resource):
                    found_resource = True
                elif isinstance(item, str) and any(item == str(status) for status in ProgressStatus):
                    found_status = item
                    
            if found_resource and found_status:
                event_counts[found_status] += count

        # Step 2: Categorize the counts
        success_statuses = ProgressStatus.success_statuses()
        error_statuses = ProgressStatus.failure_statuses()
        pending_statuses = ProgressStatus.pending_statuses()
        skipped_statuses = ProgressStatus.skipped_statuses()
        
        success_count = sum(event_counts[str(status)] for status in success_statuses)
        error_count = sum(event_counts[str(status)] for status in error_statuses)
        failed_count = event_counts[str(ProgressStatus.FAILED)]
        finished_with_issues_count = event_counts[str(ProgressStatus.FINISHED_WITH_ISSUES)]
        warning_count = event_counts[str(ProgressStatus.DONE_WITH_WARNINGS)]
        notice_count = event_counts[str(ProgressStatus.DONE_WITH_NOTICES)]
        unfinished_count = event_counts[str(ProgressStatus.UNFINISHED)]
        pending_count = sum(event_counts[str(status)] for status in pending_statuses)
        skipped_count = sum(event_counts[str(status)] for status in skipped_statuses)
        
        # Store comprehensive counts for ETL tracker and generate_execution_summary reuse
        self._subject_counts.update({
            'total_countables': total_countables,
            'countables_success': success_count,
            'countables_errors': error_count,
            'countables_failed': failed_count,
            'countables_finished_with_issues': finished_with_issues_count,
            'countables_warnings': warning_count,
            'countables_notices': notice_count,
            'countables_unfinished': unfinished_count,
            'countables_pending': pending_count,
            'countables_skipped': skipped_count,
            'countable_subject_name': countable_subj_name,
            'subject_resource': subj_resource
        })
    
    def log_final_description(self,
                              final_level:LogLevel,
                              countable_subj_name: str,
                              total_countables: int,
                              final_description: Optional[str]=None,
                              generallogger: Optional[logging.Logger]=None):
        if final_description:
            final_log_message = final_description
        else:
            final_log_message = self.generate_execution_summary(countable_subj_name=countable_subj_name, total_countables=total_countables, final_level=final_level)

        
        if generallogger:
            if final_level == LogLevel.ERROR:
                generallogger.error(final_log_message)
            elif final_level == LogLevel.WARNING:
                generallogger.warning(final_log_message)
            else:
                generallogger.info(final_log_message)

    def end(self, countable_subj_name: str, total_countables: int, generallogger: Optional[logging.Logger]=None):
        """Logs the end of the pipeline execution with the appropriate final status.
        Args: 
            countable_subj_name (str): The reference name for the countables processed. --> Can be Tasks, Iterations, Items, Tickers etc.
            total_countables (int): The total number of countables processed in the pipeline.
            generallogger (Optional[logging.Logger], optional): The logger to use for the final log message.
            """

        execution_duration = self.get_duration_since_start()
        final_level = LogLevel.INFO
        description = f"Pipeline execution completed in {execution_duration}."
        progress_status = ProgressStatus.DONE
        if self.early_stop:
            final_level = LogLevel.ERROR
            description = f"Pipeline execution stopped early due to {self.early_stop_reason}. Execution Duration: {execution_duration}."
            progress_status = ProgressStatus.FAILED
        elif self.contains_any_errors():
            final_level = LogLevel.ERROR
            description = f"Pipeline execution completed with errors. Execution Duration: {execution_duration}."
            progress_status = ProgressStatus.FINISHED_WITH_ISSUES
        elif self.contains_any_logs_for_levels(levels= LogLevel.WARNING):
            final_level = LogLevel.WARNING
            description = f"Pipeline execution completed with warnings. Execution Duration: {execution_duration}."
            progress_status = ProgressStatus.DONE_WITH_WARNINGS
        elif self.contains_any_logs_for_levels(levels= LogLevel.NOTICE):
            final_level = LogLevel.NOTICE
            description = f"Pipeline execution completed with notices. Execution Duration: {execution_duration}."
            progress_status = ProgressStatus.DONE_WITH_NOTICES

        # Store final status for external access
        self._progress_status = progress_status
        self._final_level = final_level
        
        # Calculate and store subject-specific counts for ETL tracking
        self._calculate_and_store_subject_counts(countable_subj_name, total_countables)
            
        
        execution_summary = self.generate_execution_summary(countable_subj_name=countable_subj_name,
                                                            total_countables=total_countables,
                                                            subj_resource=AbstractResource.PIPELINE_SUBJECT_SEQUENCE,
                                                            final_level=final_level)
        pipeline_description= description + " \n" + execution_summary

        self.add_log(SLog(
            level=final_level,
            resource=AbstractResource.PIPELINEMON,
            action=Action.EXECUTE,
            progress_status=progress_status,
            description=pipeline_description
        ))

        final_pipeline_descirption_message = pipeline_description + " \n" + self.get_breakdown_by_event()

        if generallogger:
            self.log_final_description(final_level=final_level, countable_subj_name=countable_subj_name, total_countables=total_countables,
                                       final_description=final_pipeline_descirption_message, generallogger=generallogger)