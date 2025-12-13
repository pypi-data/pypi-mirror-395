from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
import json
from ..enums import ProgressStatus
from ..utils import to_enum_or_none
from . import eval_statuses

class StatusTrackingMixin:
    """Mixin class providing common status tracking functionality"""
    
    def __init__(self):
        self._issues: List[Any] = []
        self._warnings: List[Any] = []
        self._notices: List[Any] = []
        self._execution_state: List[str] = []
        self._metadata: Dict[str, Any] = {}
        self._statuses_aggregated: int = 1
        self._progress_status: ProgressStatus = ProgressStatus.NOT_STARTED
        self._issues_allowed = False  # Default to allowing issues

    @property
    def progress_status(self) -> ProgressStatus:
        """Get progress status"""
        return self._progress_status
    
    @progress_status.setter
    def progress_status(self, value: Union[ProgressStatus, str, int]) -> None:
        """Set progress status"""
        self._progress_status = to_enum_or_none(value=value, enum_class=ProgressStatus, required=True, raise_if_unknown=True)

    

    @property
    def is_success(self) -> bool:
        """Check if operation is successful"""
        return self.progress_status in ProgressStatus.success_statuses()

    @property 
    def is_closed(self) -> bool:
        """Check if operation is closed"""
        return self.progress_status in ProgressStatus.closed_or_skipped_statuses()

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
        # Format timestamp as HH:MM:SS.ms (2 decimal places for milliseconds)
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

    def add_issue(self, issue: Any, update_state:bool=True) -> None:
        """Add issue"""
        if issue:
            self._issues.append(issue)
            if update_state:
                self.add_state(f"Issue: {issue}")

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

    def add_warning(self, warning: Any, update_state:bool=True) -> None:
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

    def add_notice(self, notice: Any, update_state:bool=True) -> None:
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

    @property
    def statuses_aggregated(self) -> int:
        """Get total statuses tracked"""
        return self._statuses_aggregated

    @statuses_aggregated.setter
    def statuses_aggregated(self, value: int) -> None:
        """Set total statuses tracked"""
        self._statuses_aggregated = value

    def increment_statuses_aggregated(self, value: int) -> None:
        """Increment total statuses tracked"""
        self._statuses_aggregated += value

    @property
    def issues_allowed(self) -> bool:
        """Whether issues are allowed when determining final status"""
        return self._issues_allowed
    
    @issues_allowed.setter
    def issues_allowed(self, value: bool):
        """Set whether issues are allowed"""
        self._issues_allowed = value

    def _evaluate_current_status_based_on_notes(self,close_if_pending:bool=False, issues_allowed: bool = True) -> ProgressStatus:
        """Core method to determine status based on presence of issues/warnings/notices"""

        if self.progress_status in ProgressStatus.closed_or_skipped_statuses():
            if self.issues:
                return ProgressStatus.FINISHED_WITH_ISSUES if issues_allowed else ProgressStatus.FAILED
            return self.progress_status
        if close_if_pending:
            if self.progress_status == ProgressStatus.NOT_STARTED:
                return ProgressStatus.FAILED
            if self.issues or self.progress_status in ProgressStatus.issue_statuses():
                return ProgressStatus.FAILED if not issues_allowed else ProgressStatus.FINISHED_WITH_ISSUES
            if self.warnings or self.progress_status==ProgressStatus.IN_PROGRESS_WITH_WARNINGS:
                return ProgressStatus.DONE_WITH_WARNINGS
            if self.notices or self.progress_status==ProgressStatus.IN_PROGRESS_WITH_NOTICES:
                return ProgressStatus.DONE_WITH_NOTICES
            else:
                return ProgressStatus.DONE
        if self.issues:
                return ProgressStatus.IN_PROGRESS_WITH_ISSUES if issues_allowed else ProgressStatus.FAILED
        if self.warnings:
            return ProgressStatus.IN_PROGRESS_WITH_WARNINGS 
        if self.notices:
            return ProgressStatus.IN_PROGRESS_WITH_NOTICES 
        return ProgressStatus.IN_PROGRESS
    
    def integrate_status_tracker(self, next: 'StatusTrackingMixin',
                               combine_status: bool = True,
                               issues_allowed: bool = False,
                               skip_metadata: bool = True,
                               name: Optional[str] = None) -> None:
        """Merge another tracker's state into this one"""
        # Add integration state
        integration_name = name if name else "subtask_status_tracker"
        self.add_state(f"Integrating {integration_name}.")

        # Aggregate issues, warnings, notices
        self._issues.extend(next.issues)
        self._warnings.extend(next.warnings)
        self._notices.extend(next.notices)

        # Merge execution states
        self._execution_state.extend(next.execution_state)

        # Sum total functions
        self.increment_statuses_aggregated(next.statuses_aggregated)

        # Handle metadata - improved to avoid key conflicts
        if not skip_metadata:
            # For operations like merge_into_bigquery_table, preserve original metadata 
            # but prefix child metadata to avoid overwrites
            for key, value in next.metadata.items():
                prefix = f"{integration_name}>{key}"
                if prefix in self._metadata:
                    # If the key already exists, append a unique suffix
                    suffix = 1
                    while f"{prefix}__{suffix}" in self._metadata:
                        suffix += 1
                    self._metadata[f"{prefix}__{suffix}"] = value
                else:
                    self._metadata[prefix] = value

        # Update progress status if requested
        if combine_status:
            # First evaluate status based on combined issues/warnings/notices
            updated_current_status = self._evaluate_current_status_based_on_notes(issues_allowed=issues_allowed)
  
            # Then combine with next's status using eval_statuses
            self.progress_status = eval_statuses(
                [updated_current_status, next.progress_status],
                fail_or_unfinish_if_any_pending=False, #MUST BE FALSE AS THIS IS NOT .final() function call
                issues_allowed=issues_allowed
            )

        # Add completion state
        self.add_state(f"Completed integrating {integration_name} got status {self.progress_status}.")

    def base_final(self, force_if_closed: bool = False,
                  force_status: Optional[ProgressStatus] = None,
                  issues_allowed: Optional[bool] = None) -> ProgressStatus:
        """
        Base finalization logic used by all components.
        
        Args:
            force_if_closed: Whether to force status change if already closed
            force_status: Optional status to force (must be closed/skipped status)
            issues_allowed: Whether issues are allowed, defaults to self.issues_allowed
        """
        # Use instance's issues_allowed if not explicitly provided
        issues_allowed = self.issues_allowed if issues_allowed is None else issues_allowed
        
        if self.is_closed and not force_if_closed:
            return self.progress_status

        # Use forced status or evaluate based on current state
        if force_status and force_status in ProgressStatus.closed_or_skipped_statuses():
            final_status = force_status
        else:
            final_status = self._evaluate_current_status_based_on_notes(close_if_pending=True, 
                                               issues_allowed=issues_allowed)
        
        self.progress_status = final_status
        self.add_state(f"CLOSED STATUS: {final_status}")
        return final_status

    def get_status_report(self, exclude_none: bool = True) -> str:
        """Get all information as a JSON string"""
        info_dict = {
            "progress_status": str(self.progress_status),
            "execution_state": self.execution_state_str,
            "issues": self.issues_str,
            "warnings": self.warnings_str,
            "notices": self.notices_str,
            "metadata": self.metadata,
            "statuses_aggregated": self.statuses_aggregated
        }
        
        if exclude_none:
            info_dict = {k: v for k, v in info_dict.items() if v is not None}
            
        return json.dumps(info_dict, default=str, indent=2)

    def __str__(self) -> str:
        """String representation of the object"""
        return self.get_status_report()

    def to_dict(self, infos_as_str: bool = True, exclude_none: bool = True) -> Dict[str, Any]:
        """Convert to dictionary format"""
        status_dict = {
            "progress_status": str(self.progress_status),
            "execution_state": self.execution_state_str if infos_as_str else self.execution_state,
            "issues": self.issues_str if infos_as_str else self.issues,
            "warnings": self.warnings_str if infos_as_str else self.warnings,
            "notices": self.notices_str if infos_as_str else self.notices,
            "metadata": json.dumps(self.metadata, default=str, indent=2) if infos_as_str else self.metadata,
            "statuses_aggregated": self.statuses_aggregated
        }
        
        if exclude_none:
            status_dict = {k: v for k, v in status_dict.items() if v is not None}

        return status_dict
