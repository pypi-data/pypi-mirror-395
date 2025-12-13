
""" Shared pipeline configuration utility. """
from datetime import datetime
from typing import Optional
from ipulse_shared_base_ftredge import ProgressStatus
###############################################################################################
########################################   DEPENDENCY   ########################################

class DependencyType:
    """Requirements for dependency resolution"""
    TO_CLOSED = "to_closed"  # Must be in closed statuses
    TO_SUCCESS = "to_success"  # Must be in success statuses
    TO_SUCCESS_OR_SKIPPED = "to_success_or_skipped"  # Must be in success or skipped statuses
    TO_AT_LEAST_STARTED = "to_at_least_started"  # Must be at least started (not in NOT_STARTED)
    TO_FAILURE = "to_failure"  # Must be in failure statuses

    @staticmethod
    def validate_status(status: ProgressStatus, requirement: str) -> bool:
        """Check if status meets requirement"""
        if requirement == DependencyType.TO_CLOSED:
            return status in ProgressStatus.closed_statuses()
        elif requirement == DependencyType.TO_SUCCESS:
            return status in ProgressStatus.success_statuses()
        elif requirement == DependencyType.TO_SUCCESS_OR_SKIPPED:
            return status in ProgressStatus.success_statuses() or status in ProgressStatus.skipped_statuses()
        elif requirement == DependencyType.TO_AT_LEAST_STARTED:
            return status not in ({ProgressStatus.NOT_STARTED, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY} or ProgressStatus.pending_statuses())
        elif requirement == DependencyType.TO_CLOSED:
            return status in ProgressStatus.closed_statuses()
        elif requirement == DependencyType.TO_FAILURE:
            return status in ProgressStatus.failure_statuses()
        return False

class Dependency:
    """Represents a dependency between pipeline steps"""

    def __init__(self,
                 step_name: str,
                 requirement: str = DependencyType.TO_SUCCESS_OR_SKIPPED,
                 optional: bool = False,
                 timeout_s: Optional[int] = None):
        self.step_name = step_name
        self.requirement = requirement
        self.optional = optional
        self.timeout_s = timeout_s
        self._start_time = None

    def start_timeout(self):
        """Start timeout tracking"""
        if self.timeout_s:
            self._start_time = datetime.now()

    def is_timeout(self) -> bool:
        """Check if dependency has timed out"""
        if not self.timeout_s or not self._start_time:
            return False
        elapsed = (datetime.now() - self._start_time).total_seconds()
        return elapsed > self.timeout_s

    def check_satisfied(self, step: 'Step') -> bool:
        """Check if dependency is satisfied by step's progress status"""
        # if self.is_timeout():
        #     return False

        return DependencyType.validate_status(step.progress_status, self.requirement)

    def __str__(self):
        return f"Dependency({self.step_name}, req={self.requirement}, optional={self.optional})"

