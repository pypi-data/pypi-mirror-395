""" Shared pipeline configuration utility. """
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Union
import copy
from ipulse_shared_base_ftredge import (StatusCounts,
                                        StatusTrackingMixin,
                                        eval_statuses,
                                        map_progress_status_to_log_level,
                                        to_enum_or_none,
                                        LogLevel,
                                        Action,
                                        DataResource,
                                        ProgressStatus)
from .function_result import FunctionResult
from .dependency import Dependency, DependencyType


###############################################################################################
########################################   STEP   #############################################
class Step:
    """Base class for all pipeline steps - contains only core pipeline functionality"""

    def __init__(self, name: str,
                 disabled: bool = False,
                 dependencies: Optional[List[Union[str, Dependency, Dict[str,DependencyType]]]] = None,
                 config: Optional[Dict] = None,
                 issues_allowed: bool = True):
        self.id = uuid.uuid4()
        self._name = name
        self._issues_allowed = issues_allowed # Allow issues by default
        self._dependencies = self._normalize_dependencies(dependencies or [])
        self._disabled = disabled
        self._progress_status = ProgressStatus.DISABLED if disabled else ProgressStatus.NOT_STARTED
        self._pipeline_flow = None
        self._config = config or {}
        self._start_time: Optional[datetime] = None
        self._duration_s: float = 0.0
        self._final_log_level=LogLevel.NOTSET
        self._validation_error = None

    @property
    def duration_s(self) -> float:
        """Get execution duration in seconds"""
        if not self._start_time:
            return 0.0
        if self.is_closed_or_skipped:
            return self._duration_s
        return (datetime.now(timezone.utc) - self._start_time).total_seconds()

    def calculate_duration(self) -> None:
        """Calculate and store final duration"""
        if self._start_time:
            self._duration_s = (datetime.now(timezone.utc) - self._start_time).total_seconds()


    @property
    def final_log_level(self) -> Optional[LogLevel]:
        """Get final log level based on status"""
        return self._final_log_level
    
    @final_log_level.setter
    def final_log_level(self, value: LogLevel):
        """Set final log level"""
        self._final_log_level = value

    @property
    def name(self) -> str:
        """Get name"""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set name"""
        self._name = value


    @property
    def issues_allowed(self) -> bool:
        """Check if issues are allowed"""
        return self._issues_allowed

    @issues_allowed.setter
    def issues_allowed(self, value: bool):
        """Set whether issues are allowed"""
        self._issues_allowed = value

    @property
    def pipeline_flow(self) -> Optional['PipelineFlow']:
        """Get pipeline flow"""
        return self._pipeline_flow

    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """Set pipeline flow for step, which is used for dependency resolution. As dependencies status is updated during execution this has to be referenced."""
        self._pipeline_flow = pipeline_flow

    @property
    def dependencies(self) -> List[Dependency]:
        """Get dependencies"""
        return self._dependencies

    @dependencies.setter
    def dependencies(self, value: List[Union[str, Dependency, Dict[str,DependencyType]]]):
        """Set dependencies"""
        self._dependencies = self._normalize_dependencies(value)

    @property
    def config(self) -> Dict:
        return self._config

    @config.setter
    def config(self, value: Dict):
        if not isinstance(value, dict):
            raise ValueError("Config must be a dictionary")
        self._config = value

    @property
    def progress_status(self) -> ProgressStatus:
        """Get progress status"""
        return self._progress_status
    
    @progress_status.setter
    def progress_status(self, value: Union[ProgressStatus, str, int]) -> None:
        self._progress_status = to_enum_or_none(value=value, enum_class=ProgressStatus, required=True, raise_if_unknown=True)

    @property
    def disabled(self) -> bool:
        """Check if step is disabled"""
        return self._disabled

    @disabled.setter
    def disabled(self, value: bool):
        """
        Set disabled status.
        If step is disabled, status is set to DISABLE
        """
        self._disabled = value
        if value:
            self.progress_status = ProgressStatus.DISABLED

    @property
    def is_success(self) -> bool:
        return self.progress_status in ProgressStatus.success_statuses()

    @property
    def is_success_or_skipped(self) -> bool:
        return self.progress_status in ProgressStatus.success_statuses() or self.progress_status in ProgressStatus.skipped_statuses()
    
    @property
    def is_closed(self) -> bool:
        return self.progress_status in ProgressStatus.closed_statuses()

    @property
    def is_closed_or_skipped(self) -> bool:
        return self.progress_status in ProgressStatus.closed_statuses() or self.progress_status in ProgressStatus.skipped_statuses()
    
    @property
    def is_closed_or_skipped_or_blocked(self) -> bool:
        return self.progress_status in ProgressStatus.closed_statuses() or self.progress_status in ProgressStatus.skipped_statuses() or self.progress_status == ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY

    @property
    def is_failure(self) -> bool:
        return self.progress_status in ProgressStatus.failure_statuses()

    @property
    def is_pending(self) -> bool:
        return self.progress_status in ProgressStatus.pending_statuses()

    @property
    def has_issues(self) -> bool:
        return self.progress_status in ProgressStatus.issue_statuses()

    @property 
    def validation_error(self) -> Optional[str]:
        """Get last validation error message"""
        return self._validation_error

    # ------------------
    # Dependencies
    # ------------------
    def _normalize_dependencies(self, deps: List[Union[str, Dependency, Dict[str,DependencyType]]]) -> List[Dependency]:
        """Convert string dependencies to Dependency objects"""
        normalized = []
        for dep in deps:
            if isinstance(dep, str):
                normalized.append(Dependency(dep))
            elif isinstance(dep, Dependency):
                normalized.append(dep)
            elif isinstance(dep, dict):
                for step_name, dep_type in dep.items():
                    normalized.append(Dependency(step_name, str(dep_type)))
            else:
                raise ValueError(f"Invalid dependency type: {type(dep)}")
        return normalized

    # ------------------
    # Validation Functions
    # ------------------
    def validate_dependencies(self, sequence_ref: Optional[Union[int, str]] = None) -> bool:
        """
        Validate all dependencies are satisfied.
        Returns (is_satisfied, reason_if_not)
        """
        self._validation_error = None
        
        if not self.dependencies:
            return True

        if not self.pipeline_flow:
            self._validation_error = "Pipeline flow not set for dependency resolution"
            return False

        unsatisfied = []
        skip_triggers = []
        for dep in self.dependencies:
            if isinstance(dep, str):
                dep = Dependency(dep)
            if not dep.optional:
                try:
                    if self._pipeline_flow is None:
                        raise ValueError("Pipeline flow is not set and = None. Because of this Dependency resolution not possible.")
                    dep_step = self._pipeline_flow.get_step(dep.step_name, sequence_ref)
                    if dep_step.progress_status in ProgressStatus.skipped_statuses():
                        skip_triggers.append(f"{dep.step_name} is {dep_step.progress_status}")
                    elif not dep.check_satisfied(dep_step):
                        unsatisfied.append(f"{str(dep)} : {dep_step.progress_status}")
                except KeyError:
                    unsatisfied.append(f"Missing dependency: {dep.step_name}")

        # If any dependencies are skipped, mark this step as skipped
        if skip_triggers:
            self.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            self._validation_error = f"Dependencies skipped: {', '.join(skip_triggers)}"
            return False

        if unsatisfied:
            self._validation_error = f"Unsatisfied dependencies: {', '.join(unsatisfied)}"
            return False

        return True

    def validate_and_start(self, set_status: ProgressStatus=ProgressStatus.IN_PROGRESS,
                      sequence_ref: Optional[Union[int, str]]=None,
                      intentionally_skip:bool=False) -> bool:
        """Validate and start step execution"""
        self._validation_error = None

        if intentionally_skip:
            self.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            self._validation_error = "Step is Intentionally Skipped because of intentionally_skip flag"
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False
        
        if self.progress_status == ProgressStatus.DISABLED:
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False
        
        if self.disabled:
            self.progress_status = ProgressStatus.DISABLED
            self._validation_error = "Step is disabled"
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False
        
        # Prevent restarting completed steps
        if self.is_closed:
            self._validation_error = f"Step already completed with status {self.progress_status}"
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False
            
        if self.progress_status in ProgressStatus.skipped_statuses():
            self.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            self._validation_error = "Step is Intentionally Skipped because of progress_status set to it"
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False

        deps_ok = self.validate_dependencies(sequence_ref)
        if not deps_ok:
            # If validation set status to INTENTIONALLY_SKIPPED, keep it
            if self.progress_status != ProgressStatus.INTENTIONALLY_SKIPPED:
                self.progress_status = ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False

        # Start execution tracking
        self._start_time = datetime.now(timezone.utc)
        if set_status is not None:
            if set_status is not None:
                self.progress_status = set_status
            else:
                raise ValueError("set_status cannot be None")
        else:
            raise ValueError("set_status cannot be None")
        return True

    def nb_tasks(self) -> int:
        """Get number of tasks - Each subclas must implement its own version"""
        raise NotImplementedError
    
    def final(self, force_if_closed: bool = False, force_status:Optional[ProgressStatus]=None) -> Optional[ProgressStatus]:
        """Finalize step execution"""
        raise NotImplementedError

###############################################################################################
########################################   PipelineTask   #############################################

class PipelineTask(Step, StatusTrackingMixin):
    """Represents a single task in a pipeline with full status tracking capabilities"""
    
    def __init__(
        self,
        n: str,
        a: Optional[Action] = None,
        s: Optional[DataResource] = None,
        d: Optional[DataResource] = None,
        dependencies: Optional[List[Union[str, Dependency, Dict[str,DependencyType]]]] = None,
        disabled: bool = False,
        config: Optional[Dict] = None,
        issues_allowed: bool = False
    ):
        """Initialize PipelineTask with both Step and StatusTracking capabilities"""
        Step.__init__(self, name=n,
                      disabled=disabled,
                      dependencies=dependencies,
                      config=config,
                      issues_allowed=issues_allowed)
        StatusTrackingMixin.__init__(self)
        self._action = a
        self._source = s
        self._destination = d
        self._final_report = None

    @property
    def action(self) -> Optional[Action]:
        """Get action"""
        return self._action
    
    @property
    def source(self) -> Optional[DataResource]:
        """Get source"""
        return self._source
    
    @property
    def destination(self) -> Optional[DataResource]:
        """Get destination"""
        return self._destination
    
    def nb_tasks(self) -> int:
        return 1

    def incorporate_function_result(self, result: FunctionResult, issues_allowed: bool = True, skip_metadata:bool=False, err_msg:Optional[str]=None) -> None:
        """Handle function results
        
        Changed default skip_metadata to False to preserve metadata by default
        """
        self.integrate_status_tracker(next=result,
                                    skip_metadata=skip_metadata,
                                    issues_allowed=issues_allowed,
                                    name=f"Function Result {result.name}")
        
        if not result.is_success and err_msg:
            raise Exception(f"{err_msg} ; Function Result {result.name}  = {result.progress_status}.")
    

    @property
    def final_report(self) -> Optional[str]:
        """Get task completion report including status tracking details"""
        if not self._final_report and self.is_closed_or_skipped_or_blocked:
            self._generate_final_report()
        return self._final_report

    def _generate_final_report(self) -> None:
        """Generate detailed task execution report"""
        if not self.is_closed_or_skipped_or_blocked:
            return

        report_parts = [
            f"\n Final Report for Task {self.name} ",
            f"Progress Status: {str(self.progress_status)}",
            f"Validation Error: {self.validation_error or 'None'}",
            f"Duration: {self.duration_s:.2f}s",
            f"Action: {str(self.action) if self.action else 'None'}",
            f"Source: {str(self.source) if self.source else 'None'}",
            f"Destination: {str(self.destination) if self.destination else 'None'}"
        ]

        # Add status tracking info
        if self.issues:
            report_parts.append("\n====>Issues:")
            report_parts.extend(f"  {issue}" for issue in self.issues)
            
        if self.warnings:
            report_parts.append("\n====>Warnings:")
            report_parts.extend(f"  {warning}" for warning in self.warnings)
            
        if self.notices:
            report_parts.append("\n====>Notices:")
            report_parts.extend(f"  {notice}" for notice in self.notices)

        # Add execution state
        if self.execution_state:
            report_parts.append("\n====>Execution State:")
            report_parts.extend(f"  {state}" for state in self.execution_state)

        self._final_report = "\n".join(report_parts)

    def final(self, force_if_closed: bool = False, force_status:Optional[ProgressStatus]=None, issues_allowed: Optional[bool] = None) -> None:
        """Finalize with task-specific reporting"""
        
        if issues_allowed is  None:
            issues_allowed = self.issues_allowed

        if not (self.is_closed_or_skipped and not force_if_closed):      
            final_status = self.base_final(force_if_closed=force_if_closed, force_status=force_status,issues_allowed=issues_allowed)

            self.final_log_level = map_progress_status_to_log_level(final_status)
        else:
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)

        self.calculate_duration()
        self._generate_final_report()

    def __str__(self):
        if self.is_success:
            status_symbol = "✔"
        elif self.progress_status in ProgressStatus.failure_statuses():
            status_symbol = "✖"
        elif self.progress_status in ProgressStatus.pending_statuses():
            status_symbol = "..."
        elif self.progress_status in ProgressStatus.skipped_statuses():
            status_symbol = "//"
        else:
            status_symbol = "?"

        parts = [f">> {self.name}"]
        if self._action:
            parts.append(str(self._action))
        if self._source:
            parts.append(f"from {str(self._source)}")
        if self._destination:
            parts.append(f"to {str(self._destination)}")

        parts.append(f"[Status: {status_symbol} {str(self.progress_status)}] ")
        return f"{' :: '.join(parts)}"


###############################################################################################
########################################   PipelineSequenceTemplate   #############################################
class PipelineSequenceTemplate:
    """
    Template for creating sequences of steps.
    Handles any Step-based classes including tasks, sequences, and iterators.
    """
    def __init__(self, steps: List[Step]):
        """
        Initialize template with steps.

        Args:
            steps: List of steps that can be:
                - Any Step-based instance (Task, Sequence, Iterator)
        """
        self.steps: Dict[str, Step] = {}
        self._process_steps(steps)

    def _process_steps(self, steps: List[Step]) -> None:
        """Process and normalize different types of step inputs"""
        for step in steps:
            if isinstance(step, Step):
                # Direct Step instance (Task, Sequence, Iterator.)
                self.steps[step.name] = step
            else:
                raise ValueError(f"Invalid step type: {type(step)}")

    def clone_steps(self) -> Dict[str, Step]:
        """Create a deep copy of all steps"""
        return {name: copy.deepcopy(step) for name, step in self.steps.items()}
    
    @property
    def nb_tasks(self) -> int:
        """Get total number of tasks across all steps"""
        return sum(
            step.nb_tasks() 
            for step in self.steps.values() 
            if not step.disabled
        )
    
    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow') -> None:
        """Associate all steps with the pipeline flow"""
        for step in self.steps.values():
            step.set_pipeline_flow(pipeline_flow)

    def __str__(self) -> str:
        """String representation showing all steps"""
        return "\n".join(f"    {str(step)}" for step in self.steps.values())




###############################################################################################
########################################   PipelineSequence   #############################################

class PipelineSequence(Step):
    """Represents a sequence of steps that can be initialized from a template or direct steps"""

    def __init__(self,
                 sequence_ref: Union[int, str],
                 sequence_template: Optional[PipelineSequenceTemplate] = None,
                 steps: Optional[List[Union[PipelineTask, 'PipelineDynamicIterator']]] = None,
                 dependencies: Optional[List[Union[str, Dependency, Dict[str,DependencyType]]]] = None,
                 issues_allowed: bool = True,
                 disabled: bool = False,
                  config: Optional[Dict] = None):
        """Initialize sequence with Step base class and status tracking"""
        super().__init__(name=f"sequence_{sequence_ref}",
                         dependencies=dependencies,
                         issues_allowed=issues_allowed,
                         disabled=disabled,
                         config=config)
        self.sequence_ref = sequence_ref
        self._status_counts = StatusCounts()
        self._final_report = None
        self._failure_reason = None

        # Initialize steps either from template or direct list
        if sequence_template is not None:
            self.steps = sequence_template.clone_steps()
        elif steps is not None:
            self.steps = {step.name: step for step in steps}
        else:
            self.steps = {}
        self._disabled_steps = {}

    @property
    def status_counts(self) -> StatusCounts:
        """Get status counts object"""
        return self._status_counts
    
    @property
    def failure_reason(self) -> Optional[str]:
        """Get failure reason if any"""
        return self._failure_reason
    
    @failure_reason.setter
    def failure_reason(self, value: str):
        """Set failure reason"""
        self._failure_reason = value

    def add_step(self, step: Union[PipelineTask, 'PipelineDynamicIterator']) -> None:
        """Add a step to the sequence"""
        if step.name in self.steps:
            raise ValueError(f"Step {step.name} already exists in sequence {self.sequence_ref}")
        if step.disabled:
            self._disabled_steps[step.name] = step
        self.steps[step.name] = step
        if self._pipeline_flow:
            step.set_pipeline_flow(self._pipeline_flow)

    def add_steps(self, steps: List[Union[PipelineTask, 'PipelineDynamicIterator']]) -> None:
        """Add multiple steps to the sequence"""
        for step in steps:
            self.add_step(step)

    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """Associate the sequence's tasks with the pipeline flow."""
        super().set_pipeline_flow(pipeline_flow)
        for step in self.steps.values():
            step.set_pipeline_flow(pipeline_flow)

    def collect_status_counts(self) -> StatusCounts:
        """Collect status counts from steps without modifying them"""
        counts = StatusCounts()
        if not self.steps:
            return counts
            
        for step in self.steps.values():
            if not step.disabled:
                counts.add_status(step.progress_status)
                
        return counts

    def update_status_counts_and_progress_status(self, fail_or_unfinish_if_any_pending: bool=False,skip_updating_progress_status:bool=False) -> None:
        """Update own status based on current step statuses"""
        counts = self.collect_status_counts()
        self._status_counts = counts  # Store for reporting
        # Update own status based on counts
        if not skip_updating_progress_status:
            self.progress_status = eval_statuses(
                status_input=counts,
                fail_or_unfinish_if_any_pending=fail_or_unfinish_if_any_pending,
                issues_allowed=self.issues_allowed
            )

    def final(self, force_if_closed:bool=False, force_status:Optional[ProgressStatus]=None) -> None:
        """
        Finalize sequence using current step statuses.
        Does not modify child steps - assumes their statuses are already final or will be evaluated as FAILED
        """
        if self.is_closed_or_skipped and not (force_if_closed or force_status):
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return
            
        if force_status:
            self.progress_status = force_status
            self.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=True, skip_updating_progress_status=True)
        else:
            self.update_status_counts_and_progress_status(fail_or_unfinish_if_any_pending=True)
            
        # Calculate own duration and status based on current step statuses
        self.calculate_duration()
        self.final_log_level = map_progress_status_to_log_level(self.progress_status)
        self._generate_final_report()

    def _generate_final_report(self) -> None:
        """Generate a detailed report of sequence execution"""
        if not self.is_closed_or_skipped:
            return
            
        report_parts = [
            f"\n Final Report for Sequence {self.name} "
            f"Status: {str(self.progress_status)}",
            f"Validation Error: {self.validation_error or 'None'}",
            f"Failure Reason: {self.failure_reason or 'None'}",
            f"Duration: {self.duration_s:.2f}s",
            f"Total Steps: {len(self.steps)}",
            f"Status Summary: {self._status_counts.get_summary()}"
        ]
        
        # Add step details
        if self.steps:
            report_parts.append("\nStep Details:")
            for step in self.steps.values():
                if not step.disabled:
                    report_parts.append(f"  {step}")
                    
        self._final_report = "\n".join(report_parts)

    @property
    def final_report(self) -> Optional[str]:
        """Get sequence completion report"""
        if not self._final_report and self.is_closed_or_skipped:
            self._generate_final_report()
        return self._final_report

    def nb_tasks(self) -> int:
        """
        Get total number of tasks in sequence.
        Only counts enabled tasks.
        """
        if not self.steps:
            return 0
            
        total = 0
        for step in self.steps.values():
            if not step.disabled:
                if isinstance(step, PipelineDynamicIterator):
                    # For iterators, count template tasks * number of iterations
                    total += step.nb_tasks()
                else:
                    total += step.nb_tasks()
        return total

    def __str__(self):
        """Generate string representation with status info"""
        sequence_status = f"[Sequence {self.sequence_ref} :: Status: {str(self.progress_status)}]"

        if self._status_counts.total_count > 0:
            sequence_status += f" [{self._status_counts.get_summary()}]"
            
        steps_str = "\n".join(f"    {str(step)}" for step in self.steps.values())
        return f"{sequence_status}\n{steps_str}"

    
###############################################################################################
########################################   PipelineDynamicIterator   ########################################
class PipelineDynamicIterator(Step):
    """
    Represents a dynamic iterator that can create multiple iterations of a sequence.
    Each iteration is a separate PipelineSequence instance.
    Initially we stored all iterations in a list, but this could be memory-intensive.
    Instead, we store only the overall iterations and remove one by one once it's completed.
    """
    def __init__(self,
                 name: str,
                 iteration_template: PipelineSequenceTemplate,
                 dependencies: Optional[List[Union[str, Dependency, Dict[str,DependencyType]]]] = None,
                 disabled: bool = False,
                 max_iterations_allowed: int = 100,
                 max_issues_allowed: int = 3,
                 max_warnings_allowed: int = 3):
        super().__init__(name=name, disabled=disabled, dependencies=dependencies, issues_allowed=max_issues_allowed > 0)
        self._iteration_template = iteration_template
        self._iterations: Dict[Union[int, str], PipelineSequence] = {}
        self._max_iterations_allowed = max_iterations_allowed
        self._max_issues_allowed = max_issues_allowed
        self._max_warnings_allowed = max_warnings_allowed
        self._status_counts = StatusCounts()
        self._final_report = None
        self._step_status_counts: Dict[str, StatusCounts] = {}  # Track per-step status counts
        self._current_iteration: Optional[PipelineSequence] = None
        self._failure_reason = None
        self._total_iterations_processed = 0  # Add counter for total iterations processed
        self._total_tasks_processed = 0  # Add counter for total tasks
        self._tasks_per_iteration = sum(  # Calculate tasks per iteration once
            step.nb_tasks()
            for step in iteration_template.steps.values()
            if not step.disabled
        )
        self._total_initial_iterations = 0  # Add counter for initial iterations count

    @property
    def iteration_template(self) -> PipelineSequenceTemplate:
        return self._iteration_template

    @property
    def iterations(self) -> Dict[Union[int, str], PipelineSequence]:
        return self._iterations

    @property
    def total_iterations(self) -> int:
        return len(self._iterations)
        
    @property
    def status_counts(self) -> StatusCounts:
        return self._status_counts

    @property
    def max_iterations_allowed(self) -> int:
        return self._max_iterations_allowed if self._max_iterations_allowed is not None else 0
    
    @max_iterations_allowed.setter
    def max_iterations_allowed(self, value: int) -> None:
        if value < 0:
            raise ValueError("Max iterations must be positive")
        self._max_iterations_allowed = value

    @property
    def max_issues_allowed(self) -> int:
        return self._max_issues_allowed if self._max_issues_allowed is not None else 0
    
    @max_issues_allowed.setter
    def max_issues_allowed(self, value: int) -> None:
        if value < 0:
            raise ValueError("Max issues must be positive")
        self._max_issues_allowed = value

    @property
    def max_warnings_allowed(self) -> int:
        return self._max_warnings_allowed if self._max_warnings_allowed is not None else 0
    
    @max_warnings_allowed.setter
    def max_warnings_allowed(self, value: int) -> None:
        if value < 0:
            raise ValueError("Max warnings must be positive")
        self._max_warnings_allowed = value

    @property
    def failure_reason(self) -> Optional[str]:
        """Get failure reason if any"""
        return self._failure_reason
    
    @failure_reason.setter
    def failure_reason(self, value: str):
        """Set failure reason"""
        self._failure_reason = value

    def can_continue(self, raise_if_false: bool = False) -> bool:
        """
        Check if iterator can continue based on status counts and limits.
        
        Args:
            raise_if_false: If True, raises Exception when cannot continue
            
        Returns:
            bool: True if can continue, False otherwise
        """
        if self.is_closed_or_skipped:
            reason = f"Iterator is already closed with status {self.progress_status}"
            self.failure_reason = reason
            if raise_if_false:
                raise RuntimeError(reason)
            return False
            
        if self.total_iterations == 0:
            reason = "No more iterations configured"
            self.failure_reason = reason
            if raise_if_false:
                raise RuntimeError(reason)
            return False
            
        # Use status counts to check limits
        issues_count = self.status_counts.get_category_count('issue_statuses')
        if issues_count > self.max_issues_allowed:
            reason = f"Max issues exceeded: {issues_count} > {self.max_issues_allowed}"
            self.failure_reason = reason
            if raise_if_false:
                raise RuntimeError(reason)
            return False
            
        warning_count = self.status_counts.count_statuses(ProgressStatus.DONE_WITH_WARNINGS)
        if warning_count > self.max_warnings_allowed:
            reason = f"Max warnings exceeded: {warning_count} > {self.max_warnings_allowed}"
            self.failure_reason = reason
            if raise_if_false:
                raise RuntimeError(reason)
            return False
            
        # Check if we've hit max iterations
        if self.total_iterations >= self.max_iterations_allowed:
            reason = f"Max iterations reached: {self.total_iterations} >= {self.max_iterations_allowed}"
            self.failure_reason = reason
            if raise_if_false:
                raise RuntimeError(reason)
            return False
            
        return True

    def set_iterations_from_refs(self, iteration_refs: List[Union[int, str]]) -> None:
        """Set up iterations for given references"""
        if len(iteration_refs) > self.max_iterations_allowed:
            raise ValueError(f"Cannot set {len(iteration_refs)} iterations - exceeds max_iterations {self.max_iterations_allowed}")
        
        self._iterations = {}
        self._total_initial_iterations = len(iteration_refs)  # Store initial count
        for ref in iteration_refs:
            self.add_iteration_from_ref(ref)

    def add_iteration_from_ref(self, iteration_ref: Union[int, str]) -> None:
        """Add a single iteration if limits not exceeded"""
            
        if iteration_ref in self._iterations:
            raise ValueError(f"Iteration {iteration_ref} already exists in {self.name}")  
        sequence = PipelineSequence(
            sequence_ref=iteration_ref,
            sequence_template=self.iteration_template
        )
        if self._pipeline_flow:
            sequence.set_pipeline_flow(self._pipeline_flow)
            
        self._iterations[iteration_ref] = sequence

    def remove_iteration_and_update_counts(self, iteration_ref: Union[int, str]) -> None:
        """
        Clean up iteration data while preserving status information.
        Must be called after iteration completion.
        """
        if iteration_ref not in self._iterations:
            return
            
        iteration = self._iterations[iteration_ref]
        if not iteration.is_closed_or_skipped:
            iteration.final()
            
        # Update overall iteration status counts    
        self.status_counts.add_status(iteration.progress_status)
        
        # Update per-step status counts
        for step_name, step in iteration.steps.items():
            if step.disabled:
                continue
                
            if step_name not in self._step_status_counts:
                self._step_status_counts[step_name] = StatusCounts()
                
            self._step_status_counts[step_name].add_status(step.progress_status)
            
        # Remove iteration data
        del self._iterations[iteration_ref]
        self._total_iterations_processed += 1  # Increment counter when cleaning up
        self._total_tasks_processed += self._tasks_per_iteration

    def remove_iteration(self, iteration_ref: Union[int, str]):
        """Remove an iteration by reference"""
        if iteration_ref in self._iterations:
            del self._iterations[iteration_ref]

    def clear_iterations(self):
        """Remove all iterations"""
        self._iterations.clear()

    def get_iteration(self, iteration_ref: Union[int, str]) -> Optional[PipelineSequence]:
        """Get iteration by reference"""
        if iteration_ref not in self._iterations:
            raise KeyError(f"Iteration {iteration_ref} not found in {self.name}")
        return self._iterations[iteration_ref]

    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """Set pipeline flow for self and all iterations"""
        super().set_pipeline_flow(pipeline_flow)
        for iteration in self._iterations.values():
            iteration.set_pipeline_flow(pipeline_flow)

    def validate_and_start(self, set_status: ProgressStatus = ProgressStatus.IN_PROGRESS,
                      sequence_ref: Optional[Union[int, str]] = None,
                      intentionally_skip: bool = False) -> bool:
        """
        Enhanced validation for dynamic iterator including iteration checks.
        """
        # Check intentionally_skip first
        if intentionally_skip:
            self.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False
        
        # First validate common step requirements
        if not super().validate_and_start(set_status, sequence_ref):
            return False

        # Validate iterator-specific requirements
        if self.total_iterations == 0:
            self._validation_error = "No iterations configured"
            self.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False

        if self.max_iterations_allowed < self.total_iterations:
            self._validation_error = f"Total iterations {self.total_iterations} exceeds max {self._max_iterations_allowed}"
            self.progress_status = ProgressStatus.FAILED
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return False

        self.progress_status = set_status
        return True
    

    def nb_tasks(self) -> int:
        """
        Get total number of tasks including completed iterations.
        Uses total initial iterations count rather than current iterations.
        """
        if not self.iteration_template:
            return 0
            
        return self._tasks_per_iteration * self._total_initial_iterations

    def collect_status_counts(self) -> StatusCounts:
        """Collect status counts from iterations without modifying them"""
        counts = StatusCounts()
        if not self.iterations:
            return counts
            
        for iteration in self.iterations.values():
            if not iteration.disabled:
                counts.add_status(iteration.progress_status)
                
        return counts
    

    def evaluate_progress_status(self, fail_or_unfinish_if_any_pending: bool,skip_updating_progress_status:bool=False) -> None:
        """Update own status based on current step statuses"""
        if not self.status_counts or self.status_counts.total_count==0:
            self._status_counts = self.collect_status_counts()  # Store for reporting
        
        # Update own status based on counts
        if not skip_updating_progress_status:
            self.progress_status = eval_statuses(
                status_input=self.status_counts,
                fail_or_unfinish_if_any_pending=fail_or_unfinish_if_any_pending,
                issues_allowed=self.issues_allowed
            )

    def final(self, force_if_closed:bool=False, force_status:Optional[ProgressStatus]=None) -> None:
        """
        Finalize sequence using current step statuses.
        Does not modify child steps - assumes their statuses are already final or will be evaluated as FAILED
        """
        if self.is_closed_or_skipped and not (force_if_closed or force_status):
            self.final_log_level = map_progress_status_to_log_level(self.progress_status)
            return
            
        # Clean up any remaining iterations
        remaining_iterations = list(self._iterations.keys())  # Create a list to avoid modification during iteration
        for iter_ref in remaining_iterations:
            self.remove_iteration_and_update_counts(iter_ref)
            
        if force_status:
            self.progress_status = force_status
            self.evaluate_progress_status(fail_or_unfinish_if_any_pending=True, skip_updating_progress_status=True)
        else:
            self.evaluate_progress_status(fail_or_unfinish_if_any_pending=True)
            
        # Calculate own duration and status based on current step statuses
        self.calculate_duration()
        self.final_log_level = map_progress_status_to_log_level(self.progress_status)
        self._generate_final_report()

    def get_status_counts_across_iterations_for_step(self, step_name: str) -> StatusCounts:
        """
        Get status counts for a specific step across all iterations.
        
        Args:
            step_name: Name of the step to analyze
            
        Returns:
            StatusCounts object containing aggregated status info
            
        Raises:
            KeyError: If step not found in template
            ValueError: If no iterations exist
        """
        if step_name not in self.iteration_template.steps:
            raise KeyError(f"Step {step_name} not found in template")
            
        return self._step_status_counts.get(step_name, StatusCounts())

    @property
    def final_report(self) -> Optional[str]:
        """Get iterator completion report"""
        if not self._final_report and self.is_closed_or_skipped:
            self._generate_final_report()
        return self._final_report

    def _generate_final_report(self) -> None:
        """Generate a detailed report of iterator execution without storing iteration details"""
        if not self.is_closed_or_skipped:
            return

        report_parts = [
            f"\n Final Report for Iterator {self.name} ",
            f"Status: {str(self.progress_status)}",
            f"Validation Error: {self.validation_error or 'None'}",
            f"Failure Reason: {self.failure_reason or 'None'}",
            f"Duration: {self.duration_s:.2f}s",
            f"Total Iterations: {self.total_iterations}",
            f"Status Summary: {self._status_counts.get_summary()}\n",
            "Step Status Summary Across All Iterations:"
        ]

        # Use cached step status counts
        for step_name in self.iteration_template.steps:
            step_counts = self._step_status_counts.get(step_name, StatusCounts())
            report_parts.append(f"  {step_name}: {step_counts.get_summary()}")

        self._final_report = "\n".join(report_parts)


    def __str__(self):
        indent = 0
        header = f"{' ' * indent}**  {self.name} [Status: {str(self.progress_status)}]"

        # Use status counts regardless of current iterations
        if self._status_counts.total_count > 0:
            iteration_info = (f"Total Iterations Processed: {self._total_iterations_processed}, "
                            f"Total_Statuses: {self._status_counts.total_count}, "
                            + ", ".join(f"{status}: {count}" 
                                      for status, count in self._status_counts.by_status_count.items()
                                      if count > 0))
            header += f" [{iteration_info}]"
        elif self.iterations:  # Only check iterations if no status counts yet
            header += " [Processing in progress]"
        else:
            header += " [No iterations yet]"

        # Template tasks with their aggregated statuses
        template_flow = []
        for step_name in self._iteration_template.steps:
            step_status_counts = self._step_status_counts.get(step_name, StatusCounts())
            if step_status_counts.total_count > 0:
                step_info = ("[" + ", ".join(f"{status}: {count}" 
                            for status, count in step_status_counts.by_status_count.items() 
                            if count > 0) + "]")
            else:
                step_info = "[DISABLED/NO DATA]"
                
            template_flow.append(f"{' ' * (indent + 2)}>> {step_name} {step_info}")

        return f"{header}\n{chr(10).join(template_flow)}" if template_flow else header


def _validate_step_name(name: str) -> bool:
    """Validate step name format"""
    if not isinstance(name, str):
        raise ValueError("Step name must be a string")
    if not name.strip():
        raise ValueError("Step name cannot be empty")
    if len(name) > 128:
        raise ValueError("Step name too long (max 128 chars)")
    return True


###############################################################################################
########################################   PipelineFlow   ########################################

class PipelineFlow(PipelineSequence):
    """Top-level pipeline sequence that manages the entire pipeline execution"""
    
    def __init__(self,
                 base_context: str, 
                 steps: Optional[List[Step]] = None,
                 disabled: bool = False,
                 config: Optional[Dict] = None,
                 issues_allowed: bool = False,
                 dependencies: Optional[List[Union[str, Dependency, Dict[str,DependencyType]]]] = None):
        super().__init__(
            sequence_ref=base_context,
            steps=steps,
            dependencies=dependencies,
            issues_allowed=issues_allowed,
            disabled=disabled,
            config=config
        )
        self.base_context = base_context
        self._pipelineflow_id=uuid.uuid4()
        self.set_pipeline_flow(self)# Self-reference for consistent step access
        
        
        # Task tracking
        self._total_tasks = sum(step.nb_tasks() for step in (steps or []))
        self._closed_tasks = 0

    @property
    def completion_percentage(self) -> float:
        """Get completion percentage based on tasks"""
        if self._total_tasks == 0:
            return 0.0
        return round((self._closed_tasks / self._total_tasks) * 100, 2)

    def update_task_completion(self, completed: int):
        """Update completed task count with validation"""
        old_count = self._closed_tasks
        new_count = min(old_count + completed, self._total_tasks)
        if new_count != old_count:
            self._closed_tasks = new_count

    def add_step(self, step: Step) -> bool:
        """Add a step to the pipeline with validation.
        
        Returns:
            bool: True if step was added, False if disabled or already exists
        """
        if step.disabled:
            if not step.name in self._disabled_steps:
                self._disabled_steps[step.name] = step
                return False

        _validate_step_name(step.name)
        
        if step.name in self.steps:
            raise ValueError(f"Step with name '{step.name}' already exists")

        self.steps[step.name] = step
        step.set_pipeline_flow(self)
        self._total_tasks += step.nb_tasks()
        return True
    

    def validate_and_start(self, set_status:ProgressStatus = ProgressStatus.IN_PROGRESS,
                           sequence_ref: Optional[Union[int, str]] = None,
                           intentionally_skip: bool = False) -> bool:
        """Validate and start pipeline execution"""
        self._validation_error = None
        
        if self.progress_status== ProgressStatus.DISABLED:
            return False
        
        if self.disabled:
            self.progress_status = ProgressStatus.DISABLED
            return False
            
        # Validate pipeline dependencies
        try:
            self.validate_steps_dependencies_exist()
        except ValueError as e:
            self.progress_status = ProgressStatus.FAILED
            self._validation_error = f"Dependency validation failed: {str(e)}"
            return False
        
        # Start execution tracking
        self._start_time = datetime.now(timezone.utc)
        self.progress_status = set_status
        return True
    
    def _recalc_total_steps(self) -> int:
        """Recursively calculate total number of tasks including all iterations"""
        return self.nb_tasks()

    def _generate_final_report(self) -> None:
        """Generate detailed pipeline execution report"""
        if not self.is_closed_or_skipped:
            return
                    
        self._total_tasks = self.nb_tasks()  # Recalculate total including all iterations
        self._final_report = self.get_pipeline_description()

    def get_pipeline_description(self) -> str:
        """Generate detailed pipeline flow string with metrics and status breakdown"""
        # status_summary = ""
        # if self.status_counts:
        #     status_summary = (
        #         f"Status Counts Breakdown:\n"
        #         + "\n".join(f"  {status}: {count}" 
        #                    for status, count in self.status_counts.by_status_count.items()
        #                    if count > 0)
        #     )
            
        lines = [
            f"Pipelineflow Context: {self.base_context}",
            f"Pipelineflow_ID: {self._pipelineflow_id}",
            f"Status: {str(self.progress_status)}",
            f"Duration: {self.duration_s:.1f}s",
            f"Progress: {self.completion_percentage:.1f}% ({self._closed_tasks}/{self._total_tasks} tasks closed.)",
            f"\n Flow level Steps Summary: \n   {self._status_counts.get_summary()}"
            "\nSteps:",
            "-------"
        ]
        for step in self.steps.values():
            if not step.disabled:
                lines.append(str(step))

        return "\n".join(lines)
    

    def get_step(self, name: str, sequence_ref: Optional[Union[int, str]] = None) -> Step:
        """Get step by name with improved error handling."""
        try:
            # First check direct steps
            if name in self.steps:
                return self.steps[name]
            
            if name in self._disabled_steps:
                return self._disabled_steps[name]

            # Search in dynamic iterators
            for step in self.steps.values():
                if isinstance(step, PipelineDynamicIterator):
                    # Check specific iteration if reference provided
                    if sequence_ref is not None and sequence_ref in step.iterations:
                        iteration = step.iterations[sequence_ref]
                        if name in iteration.steps:
                            return iteration.steps[name]
                    # Check template steps
                    elif name in step.iteration_template.steps:
                        return step.iteration_template.steps[name]

            raise KeyError(f"Step '{name}' not found")
        except Exception as e:
            raise KeyError(
                f"Step '{name}' not found in pipeline flow "
                f"{'or specified iteration' if sequence_ref else ''}"
            ) from e

    def get_task(self, name: str, sequence_ref: Optional[Union[int, str]] = None) -> 'PipelineTask':
        """
        Get a step by name and cast it to PipelineTask.
        Raises TypeError if the step is not a PipelineTask.
        """
        step = self.get_step(name, sequence_ref)
        if not isinstance(step, PipelineTask):
            raise TypeError(
                f"Step '{name}' is of type {type(step).__name__}, not PipelineTask. "
                f"Use get_step() if you need access to other step types."
            )
        return step

    def get_iterator(self, name: str, sequence_ref: Optional[Union[int, str]] = None) -> 'PipelineDynamicIterator':
        """
        Get a step by name and cast it to PipelineDynamicIterator.
        Raises TypeError if the step is not a PipelineDynamicIterator.
        """
        step = self.get_step(name, sequence_ref)
        if not isinstance(step, PipelineDynamicIterator):
            raise TypeError(
                f"Step '{name}' is of type {type(step).__name__}, not PipelineDynamicIterator. "
                f"Use get_step() if you need access to other step types."
            )
        return step

    def get_sequence(self, name: str, sequence_ref: Optional[Union[int, str]] = None) -> 'PipelineSequence':
        """
        Get a step by name and cast it to PipelineSequence.
        Raises TypeError if the step is not a PipelineSequence.
        """
        step = self.get_step(name, sequence_ref)
        if not isinstance(step, PipelineSequence):
            raise TypeError(
                f"Step '{name}' is of type {type(step).__name__}, not PipelineSequence. "
                f"Use get_step() if you need access to other step types."
            )
        return step

    def validate_steps_dependencies_exist(self) -> bool:
        """Validate all pipeline dependencies"""
        def _validate_step_dependencies(step: Step, path: List[str]) -> None:
            current_path = path + [step.name]

            # Check for circular dependencies
            if len(set(current_path)) != len(current_path):
                cycle = current_path[current_path.index(step.name):]
                raise ValueError(f"Circular dependency detected: {' -> '.join(cycle)}")

            # Validate direct dependencies
            for dep in step.dependencies:
                if isinstance(dep, str):
                    dep = Dependency(dep)
                try:
                    dep_step = self.get_step(dep.step_name)
                    if not dep.optional:
                        _validate_step_dependencies(dep_step, current_path)
                except KeyError as exc:
                    if not dep.optional:
                        raise ValueError(
                            f"Missing required dependency '{dep.step_name}' for step '{step.name}'. "
                            f"Path: {' -> '.join(current_path)}"
                        ) from exc

            # Validate template steps for dynamic iterators
            if isinstance(step, PipelineDynamicIterator):
                for template_step in step.iteration_template.steps.values():
                    _validate_step_dependencies(template_step, current_path)

        # Always validate every step
        for step in self.steps.values():
            _validate_step_dependencies(step, [])

        return True


    def _count_closed_tasks_recursively(self, step: Step) -> int:
        """Recursively count closed tasks in a step and its children"""
        if step.disabled:
            return 0
            
        if isinstance(step, PipelineDynamicIterator):
            # For iterators, count both completed and in-progress tasks
            total_tasks = step._tasks_per_iteration * step._total_initial_iterations
            if step.is_closed_or_skipped:
                return total_tasks
            return 0
        elif isinstance(step, PipelineSequence):
            # For sequences, count tasks in child steps
            return sum(
                self._count_closed_tasks_recursively(child_step)
                for child_step in step.steps.values()
            )
        else:
            # For regular tasks, count if closed or skipped
            return 1 if step.progress_status in ProgressStatus.closed_or_skipped_statuses() else 0

    def update_status_counts_and_progress_status(self, fail_or_unfinish_if_any_pending: bool=False, skip_updating_progress_status:bool=False) -> None:
        """Update own status based on current step statuses and track completions"""
        counts = self.collect_status_counts()
        self._status_counts = counts
        
        # Count completed tasks recursively through all steps and their children
        self._closed_tasks = sum(
            self._count_closed_tasks_recursively(step)
            for step in self.steps.values()
        )
        
        # Update own status based on counts
        if not skip_updating_progress_status:
            self._progress_status = eval_statuses(
                counts,
                fail_or_unfinish_if_any_pending=fail_or_unfinish_if_any_pending,
                issues_allowed=self.issues_allowed
            )

    def __str__(self) -> str:
        """Generate string representation with status info"""
        return self.get_pipeline_description()