from typing import List, Set, Union
from ipulse_shared_base_ftredge import ProgressStatus, LogLevel, to_enum_or_none
from .status_counts import StatusCounts


def map_progress_status_to_log_level(status: ProgressStatus) -> LogLevel:
    """Map ProgressStatus to LogLevel"""
    status = to_enum_or_none(enum_class=ProgressStatus, value=status, raise_if_unknown=True)
    if status in ProgressStatus.issue_statuses():
        return LogLevel.ERROR
    if status in [ProgressStatus.IN_PROGRESS_WITH_WARNINGS, ProgressStatus.DONE_WITH_WARNINGS]:
        return LogLevel.WARNING
    if status in [ProgressStatus.IN_PROGRESS_WITH_NOTICES, ProgressStatus.DONE_WITH_NOTICES]:
        return LogLevel.NOTICE
    return LogLevel.INFO


def eval_statuses(
    status_input: Union[Set[ProgressStatus], List[ProgressStatus], StatusCounts],
    fail_or_unfinish_if_any_pending: bool = False,
    issues_allowed: bool = True
) -> ProgressStatus:
    """
    Determine overall status from either a set of statuses or StatusCounts object.
    !!! IF final is True, ensure all statuses are closed before determining final status.
    If not all statuses are closed, it will return FAILED OR UNFINISHED. !!!
    Args:
        status_input: Either a set/list of ProgressStatus or StatusCounts object
        final: Whether this is final status calculation
        issues_allowed: Whether issues are allowed in non-final status
        
    Returns:
        ProgressStatus representing overall status
    """
    # Convert input to set of statuses if needed
    if isinstance(status_input, StatusCounts):
        statuses = status_input.to_status_set()
    else:
        statuses = set(status_input)
    
    total_count = len(statuses)
    
    if total_count == 0:
        return ProgressStatus.NOT_STARTED
    
    disabled = {s for s in statuses if s == ProgressStatus.DISABLED}
    if len(disabled) == total_count:
        return ProgressStatus.DISABLED
    
    # Handle fully skipped case
    skipped = {s for s in statuses if s in ProgressStatus.skipped_statuses()}
    if len(skipped) == total_count:
        return ProgressStatus.INTENTIONALLY_SKIPPED

    # Count various status types
    pending_statuses = {s for s in statuses if s in ProgressStatus.pending_statuses()}
    blocked_statuses = {s for s in statuses if s == ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY}
    failed = {s for s in statuses if s == ProgressStatus.FAILED}
    in_progress_with_issues = {s for s in statuses if s == ProgressStatus.IN_PROGRESS_WITH_ISSUES}
    failed_or_failed_with_issues = {s for s in statuses if s in [ProgressStatus.FAILED, ProgressStatus.FINISHED_WITH_ISSUES]}
    issues_statuses = {s for s in statuses if s in ProgressStatus.issue_statuses()}
    warnings_statuses = {s for s in statuses if s in [ProgressStatus.IN_PROGRESS_WITH_WARNINGS, ProgressStatus.DONE_WITH_WARNINGS]}
    notices_statuses = {s for s in statuses if s in [ProgressStatus.IN_PROGRESS_WITH_NOTICES, ProgressStatus.DONE_WITH_NOTICES]}
    unfinished_or_blocked_by_deps = {s for s in statuses if s in [ProgressStatus.UNFINISHED, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY]}
    not_started = {s for s in statuses if s == ProgressStatus.NOT_STARTED}

    # Non-final status calculation
    # All items are complete at this point

    # progress with issues,  blocked , unfinished, finished with issues, failed, unknown

    if pending_statuses :
        if fail_or_unfinish_if_any_pending:
            failed_or_failed_with_issues=failed_or_failed_with_issues.union(in_progress_with_issues)
            unfinished_or_blocked_by_deps=unfinished_or_blocked_by_deps.union(pending_statuses.difference(in_progress_with_issues))
            if failed_or_failed_with_issues or in_progress_with_issues:
                # if issues_allowed:
                #     return ProgressStatus.FINISHED_WITH_ISSUES
                return ProgressStatus.FAILED
            return ProgressStatus.UNFINISHED
        if not issues_allowed:
            failed_or_failed_with_issues=failed_or_failed_with_issues.union(in_progress_with_issues)

        if issues_statuses:
            if issues_allowed:
                return ProgressStatus.IN_PROGRESS_WITH_ISSUES
            if failed_or_failed_with_issues:
                return ProgressStatus.FAILED
        if warnings_statuses:
            return ProgressStatus.IN_PROGRESS_WITH_WARNINGS
        if notices_statuses:
            return ProgressStatus.IN_PROGRESS_WITH_NOTICES
        if len(not_started) == total_count:
            return ProgressStatus.NOT_STARTED
        return ProgressStatus.IN_PROGRESS
    
    if issues_statuses:
        if (len(failed) + len(skipped)) == total_count:
            return ProgressStatus.FAILED
        if not failed_or_failed_with_issues:
            return ProgressStatus.UNFINISHED
        if not failed and not issues_allowed:
            if blocked_statuses:
                return ProgressStatus.FAILED
            return ProgressStatus.FINISHED_WITH_ISSUES
        if not issues_allowed or unfinished_or_blocked_by_deps:
            return ProgressStatus.FAILED
        return ProgressStatus.FINISHED_WITH_ISSUES

    # Fallback to highest priority status
    return max(statuses, key=lambda s: s.value)