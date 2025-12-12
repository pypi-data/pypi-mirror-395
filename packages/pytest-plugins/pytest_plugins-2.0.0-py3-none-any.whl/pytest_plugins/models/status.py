from enum import StrEnum


class ExecutionStatus(StrEnum):
    COLLECTED = "collected"
    STARTED = "started"
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    XFAIL = "xfailed"
    XPASS = "xpassed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"
    FAILED_SKIPPED = "failed-skipped"  # Force skipped, used in fail2skip plugin
