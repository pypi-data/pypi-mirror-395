# Created by: Russlan Ramdowar
# Created on: 

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone
import json
import uuid
from ipulse_shared_base_ftredge import (ProgressStatus,
                                        StatusTrackingMixin)

@dataclass
class FunctionResult(StatusTrackingMixin):
    """Base class for function results with status tracking"""
    name: str = field(default_factory=lambda: str(uuid.uuid4()))
    _data: Any = None
    _start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _duration_s: float = 0.0
    _final_report= None

    def __post_init__(self):
        super().__init__()
        # Set initial status to IN_PROGRESS
        self.progress_status = ProgressStatus.IN_PROGRESS

    @property
    def data(self) -> Any:
        """Get data"""
        return self._data
    
    @data.setter
    def data(self, value: Any) -> None:
        """Set data"""
        self._data = value

    def add_data(self, values: Any, name: str) -> None:
        """Add data to a dict with a name"""
        if not self.data:
            self.data = {}
        elif not isinstance(self.data, dict):
            raise ValueError("Data must be a dictionary to add more values")
        self.data[name] = values

    @property
    def execution_state(self) -> List[str]:
        """Get execution state"""
        return self._execution_state

    @property
    def execution_state_str(self) -> Optional[str]:
        """Get execution state as a formatted string"""
        if not self._execution_state:
            return None
        return "\n".join(f">>[[{entry}]]" for entry in self._execution_state)

    def add_state(self, state: str) -> None:
        """Add execution state with a timestamp"""
        now = datetime.now(timezone.utc)
        ms = f"{now.microsecond // 10000:02d}" # Get milliseconds and format to 2 digits
        timestamp = now.strftime(f"%H:%M:%S.{ms}")
        self._execution_state.append(f"[{timestamp}]->{state}")

    @property
    def issues(self) -> List[Any]:
        """Get issues"""
        return self._issues

    @property
    def issues_str(self) -> Optional[str]:
        """Get issues as a string"""
        if not self._issues:
            return None
        return "\n".join(f">>[i:{issue}]" for issue in self._issues)

    def add_issue(self, issue: Any,  update_state:bool=True,state_msg:Optional[str]=None,) -> None:
        """Add issue"""
        if issue:
            self._issues.append(issue)
            if state_msg:
                self.add_state("Exception/Issue: "+state_msg)
            elif update_state:
                self.add_state(f"Exception/Issue : {issue}")

    @property
    def warnings(self) -> List[Any]:
        """Get warnings"""
        return self._warnings

    @property
    def warnings_str(self) -> Optional[str]:
        """Get warnings as a string"""
        if not self._warnings:
            return None
        return "\n".join(f">>[w:{warning}]" for warning in self._warnings)

    def add_warning(self, warning: Any,update_state:bool=True) -> None:
        """Add warning"""
        if warning:
            self._warnings.append(warning)
            if update_state:
                self.add_state(f"Warning: {warning}")

    @property
    def notices(self) -> List[Any]:
        """Get notices"""
        return self._notices

    @property
    def notices_str(self) -> Optional[str]:
        """Get notices as a string"""
        if not self._notices:
            return None
        return "\n".join(f">>[n:{notice}]" for notice in self._notices)

    def add_notice(self, notice: Any,update_state:bool=True ) -> None:
        """Add notice"""
        if notice:
            self._notices.append(notice)
            if update_state:
                self.add_state(f"Notice: {notice}")

    def get_notes(self, exclude_none: bool = True) -> str:
        """Get all notes"""
        notes = {
            "ISSUES": self.issues_str,
            "WARNINGS": self.warnings_str,
            "NOTICES": self.notices_str
        }
        if exclude_none:
            notes = {k: v for k, v in notes.items() if v is not None}
        
        if not notes:
            return ""
            
        return "\n".join(f">>{k}: {v}" for k, v in notes.items())
    
    # ------------------
    # Metadata
    # ------------------
    @property
    def metadata(self) -> Dict[str, Any]:
        """Get metadata"""
        return self._metadata
    
    @metadata.setter
    def metadata(self, value: Dict[str, Any]) -> None:
        """Set metadata"""
        self._metadata = value

    def add_metadata(self, **kwargs) -> None:
        """Add metadata key-value pairs"""

        self.metadata.update(kwargs)

    def add_metadata_from_dict(self, metadata: Dict[str, Any]) -> None:
        """Add metadata from a dictionary"""
        self.metadata.update(metadata)

    # ------------------
    # Timing
    # ------------------
    @property
    def start_time(self) -> datetime:
        """Get start time"""
        return self._start_time

    @property
    def duration_s(self) -> float:
        """Get duration in seconds"""
        return self._duration_s
    
    @duration_s.setter
    def duration_s(self, value: float) -> None:
        """Set duration in seconds"""
        self._duration_s = value

    def calculate_duration(self) -> None:
        """Set final duration in seconds"""
        self._duration_s = (datetime.now(timezone.utc) - self.start_time).total_seconds()

    # ------------------
    # Aggregation
    # ------------------

    def integrate_result(self, child_result: "FunctionResult", issues_allowed:bool=False, combine_status=True,
                          skip_data: bool = True, skip_metadata: bool = False) -> None:
        """Integrate a child operation result into this result
        
        Changed default skip_metadata to False to preserve metadata by default
        """
        # Integrate status tracking including metadata handling
        self.integrate_status_tracker(
            next=child_result,
            combine_status=combine_status,
            skip_metadata=skip_metadata,
            issues_allowed=issues_allowed,
            name=f"child>{child_result.name}"
        )

        # Handle data
        if not skip_data and child_result.data:
            if self._data is None:
                self._data = child_result.data
            elif isinstance(self._data, dict) and isinstance(child_result.data, dict):
            # Ensure keys don't match to avoid override
                overlapping_keys = set(self._data.keys()) & set(child_result.data.keys())
                if overlapping_keys:
                    raise ValueError(f"Cannot integrate data. Overlapping keys found: {overlapping_keys}")
                self._data.update(child_result.data)
            else:
                raise ValueError("Result Data types do not match for integration")

    # ------------------
    # Closing / Finalizing
    # ------------------

    def final(self, force_if_closed: bool = False,
             force_status: Optional[ProgressStatus] = None,
             issues_allowed: Optional[bool] = None) -> ProgressStatus:
        """Finalize with function-specific handling"""
        final_status = self.base_final(force_if_closed=force_if_closed,
                                     force_status=force_status,
                                     issues_allowed=issues_allowed)
        self.calculate_duration()
        return final_status

        
    def get_final_report(self, exclude_none: bool = True) -> str:
        """Get all information as a JSON string"""
        # Start with parent class status info
        info_dict = json.loads(super().get_status_report(exclude_none=False)) # Will be filtered once at the end for all fields
        
        # Add FunctionResult specific fields
        info_dict.update({
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "duration_s": self.duration_s
        })
        
        if exclude_none:
            info_dict = {k: v for k, v in info_dict.items() if v is not None}
            
        return json.dumps(info_dict, default=str, indent=2)

    def to_dict(self, infos_as_str: bool = True, exclude_none: bool = True) -> Dict[str, Any]:
        """Convert to dictionary format"""
        # Get base status dict from parent
        status_dict = super().to_dict(infos_as_str=infos_as_str, exclude_none=False) # Will be filtered once at the end for all fields
        
        # Add FunctionResult specific fields
        status_dict.update({
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "duration_s": self.duration_s
        })
        
        if exclude_none:
            status_dict = {k: v for k, v in status_dict.items() if v is not None}

        result = {
            "data": self.data,
            "status": status_dict
        }
        
        if exclude_none and result["data"] is None:
            result.pop("data")
            
        return result

    # Can remove __str__ since it's inherited from mixin
