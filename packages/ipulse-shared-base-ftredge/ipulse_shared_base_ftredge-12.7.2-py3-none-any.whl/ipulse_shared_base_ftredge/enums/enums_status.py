# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long

from enum import Enum, auto
class AutoNameEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self) -> str:
        return self.name
        

class Status(AutoNameEnum):
    pass

class ProgressStatus(Status):

    # Skipped statuses
    DISABLED = 10
    INTENTIONALLY_SKIPPED = 20

    # Success statuses
    DONE= 200
    DONE_WITH_NOTICES = 205
    DONE_WITH_WARNINGS = 210

    # Pending statuses
    NOT_STARTED = 300
    STARTED=350
    IN_PROGRESS = 360
    IN_PROGRESS_WITH_NOTICES = 363
    IN_PROGRESS_WITH_WARNINGS = 364
    IN_PROGRESS_WITH_ISSUES = 365
    PAUSED = 370
    BLOCKED_BY_UNRESOLVED_DEPENDENCY = 380

    UNKNOWN = 400

    FINISHED_WITH_ISSUES= 510
    UNFINISHED = 610
    FAILED = 620
    

    @classmethod
    def pending_statuses(cls):
        return frozenset({
            cls.UNKNOWN,
            cls.NOT_STARTED,
            cls.STARTED,
            cls.IN_PROGRESS,
            cls.IN_PROGRESS_WITH_ISSUES,
            cls.IN_PROGRESS_WITH_WARNINGS,
            cls.IN_PROGRESS_WITH_NOTICES
        })
    
    @classmethod
    def pending_or_blocked_statuses(cls):
        return frozenset.union(
            cls.pending_statuses(),
            {cls.BLOCKED_BY_UNRESOLVED_DEPENDENCY}
        )
    

    @classmethod
    def skipped_statuses(cls):
        return frozenset({
            cls.INTENTIONALLY_SKIPPED,
            cls.DISABLED,
            cls.PAUSED
        })

    @classmethod
    def success_statuses(cls):
        return frozenset({
            cls.DONE,
            cls.DONE_WITH_NOTICES,
            cls.DONE_WITH_WARNINGS,
        })

    @classmethod
    def failure_statuses(cls):
        return frozenset({
            cls.FINISHED_WITH_ISSUES,
            cls.UNFINISHED,
            cls.FAILED,
        })
    
    @classmethod
    def issue_statuses(cls):
        return frozenset.union(
            cls.failure_statuses(),
            {cls.IN_PROGRESS_WITH_ISSUES,
            cls.UNKNOWN,
            cls.BLOCKED_BY_UNRESOLVED_DEPENDENCY}
        )

    @classmethod
    def closed_statuses(cls):
        return frozenset.union(
            cls.success_statuses(),
            cls.failure_statuses()
        )

    @classmethod
    def closed_or_skipped_statuses(cls):
        return frozenset.union(
            cls.closed_statuses(),
            cls.skipped_statuses()
        )
    
    @classmethod
    def at_least_started_statuses(cls):
        return frozenset.union(
            frozenset({
                cls.STARTED,
                cls.IN_PROGRESS,
                cls.IN_PROGRESS_WITH_ISSUES,
                cls.IN_PROGRESS_WITH_WARNINGS,
                cls.IN_PROGRESS_WITH_NOTICES
            }),
            cls.closed_statuses()
        )
class ReviewStatus(Status):
    OPEN =  auto()  # type: ignore
    ACKNOWLEDGED = auto()  # type: ignore
    ESCALATED = auto()  # type: ignore
    IN_PROGRESS = auto()  # type: ignore
    IN_REVIEW = auto()  # type: ignore
    RESOLVED = auto()  # type: ignore
    APPROVED = auto()  # type: ignore
    REJECTED = auto()  # type: ignore
    WAITING_FOR_INPUT = auto()  # type: ignore
    IGNORED = auto()  # type: ignore
    CANCELLED = auto()  # type: ignore
    CLOSED = auto()  # type: ignore

class ApprovalStatus(Status):
    PENDING = auto()  # type: ignore
    APPROVED = auto()  # type: ignore
    DISABLED = auto()  # type: ignore
    REJECTED = auto()  # type: ignore
    ESCALATED = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore

class ObjectOverallStatus(Status):
    ACTIVE = auto()  # type: ignore
    MAINTENANCE = auto()  # type: ignore
    STASHED = auto()  # type: ignore
    DISABLED = auto()  # type: ignore
    DELETED = auto()  # type: ignore
    PENDING = auto()  # type: ignore
    DEPRECATED = auto()  # type: ignore
    PAUSED = auto()  # type: ignore
    ARCHIVED = auto()  # type: ignore
    LOST = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore

class TradingStatus(Status):
    TRADED_ON_PUBLIC_EXCHANGE = auto()  # type: ignore
    TRADED_OTC = auto()  # type: ignore
    TRADED_ON_PUBLIC_SITE_OR_APP = auto()  # type: ignore
    NOT_FOR_SALE = auto()  # type: ignore
    TRADED_VIA_BROKER = auto()  # type: ignore
    UNLISTED = auto()  # type: ignore
    PRIVATE = auto()  # type: ignore
    DELISTED = auto()  # type: ignore
    SUSPENDED = auto()  # type: ignore
    LIQUIDATED = auto()  # type: ignore
    DELIVERED = auto()  # type: ignore
    BANKRUPT = auto()  # type: ignore
    MERGED = auto()  # type: ignore
    ACQUIRED = auto()  # type: ignore
    EXPIRED = auto()  # type: ignore
    EXERCISED = auto()  # type: ignore
    REDEEMED = auto()  # type: ignore
    CALLED = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore

class WorkScheduleStatus(Status):
    OPEN = auto()  # type: ignore
    CLOSED = auto()  # type: ignore
    CANCELLED = auto()  # type: ignore
    MAINTENANCE = auto()  # type: ignore
    BREAK = auto()  # type: ignore
    HOLIDAY = auto()  # type: ignore
    UNREACHABLE = auto()  # type: ignore
    PERMANENTLY_CLOSED = auto()  # type: ignore
    TEMPORARILY_CLOSED = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore


class SubscriptionStatus(Status):
    ACTIVE = auto()  # type: ignore
    TRIAL = auto()  # type: ignore
    DISABLED = auto()  # type: ignore
    CANCELLED = auto()  # type: ignore
    UPGRADED = auto()  # type: ignore
    DOWNGRADED = auto()  # type: ignore
    EXPIRED = auto()  # type: ignore
    SUSPENDED = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore


class AIModelStatus(Status):
    """Model lifecycle status."""
    DRAFT = auto()  # type: ignore
    TRAINING = auto()  # type: ignore
    TRAINED = auto()  # type: ignore
    VALIDATING = auto()  # type: ignore
    VALIDATED = auto()  # type: ignore
    TESTING = auto()  # type: ignore
    TESTED = auto()  # type: ignore
    DEPLOYED = auto()  # type: ignore
    SERVING = auto()  # type: ignore
    DEGRADED = auto()  # type: ignore
    FAILED = auto()  # type: ignore
    RETIRED = auto()  # type: ignore
    ARCHIVED = auto()  # type: ignore
    DELETED = auto()  # type: ignore


class PredictionPipelineStatus(Status):
    """Prediction pipeline execution status."""
    NOT_STARTED = auto()  # type: ignore
    PREDICTION_REQUEST_SUBMISSION = auto()  # type: ignore
    AWAITING_PREDICTION_RESPONSE = auto()  # type: ignore
    PARSING_PREDICTION_RESPONSE = auto()  # type: ignore
    QA_PRE_SAVING_TO_DP = auto()  # type: ignore #basically if response quality is ok or not
    SAVING_TO_DP = auto()  # type: ignore
    QA_PRE_SYNC_TO_PAPP=auto()  # type: ignore
    SYNCING_TO_PAPP = auto()  # type: ignore
    FINISHED = auto()  # type: ignore
    FAILED = auto()  # type: ignore
    CANCELLED = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore


class ComputeResourceStatus(Status):
    """Compute Resource lifecycle status."""
    PROVISIONING = auto()  # type: ignore
    ACTIVE = auto()  # type: ignore
    UPDATING = auto()  # type: ignore
    SCALING = auto()  # type: ignore
    DEGRADED = auto()  # type: ignore
    FAILED = auto()  # type: ignore
    TERMINATING = auto()  # type: ignore
    TERMINATED = auto()  # type: ignore
    RESTARTING = auto()  # type: ignore
    STOPPING = auto()  # type: ignore
    STOPPED = auto()  # type: ignore
    STARTING = auto()  # type: ignore
    MIGRATING = auto()  # type: ignore
    BACKING_UP = auto()  # type: ignore
    RESTORING = auto()  # type: ignore
    MAINTENANCE = auto()  # type: ignore
    SUSPENDED = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore