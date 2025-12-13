# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import StrEnum, auto

class AutoLower(StrEnum):
    """
    StrEnum contrary to simple Enum is of type `str`, so it can be used as a string.
    StrEnum whose `auto()  # type: ignore` values are lower-case.
    (Identical to StrEnum's own default, but keeps naming symmetrical.)
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()            # StrEnum already does this

class AutoUpper(StrEnum):
    """
    StrEnum contrary to simple Enum is of type `str`, so it can be used as a string.
    StrEnum whose `auto()  # type: ignore` values stay as-is (UPPER_CASE).
    """
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name                    # keep original upper-case



class IAMUnit(AutoLower):
    GROUP = auto()  # type: ignore
    ROLE = auto()  # type: ignore


class IAMAction(AutoLower):
    ALLOW = auto()  # type: ignore
    DENY = auto()  # type: ignore
    GRANT = auto()  # type: ignore
    REVOKE = auto()  # type: ignore


class IAMUserType(AutoLower):
    ANONYMOUS = auto()  # type: ignore
    AUTHENTICATED = auto()  # type: ignore
    CUSTOMER = auto()  # type: ignore
    EXTERNAL = auto()  # type: ignore
    PARTNER = auto()  # type: ignore
    INTERNAL = auto()  # type: ignore
    EMPLOYEE = auto()  # type: ignore
    SYSTEM = auto()  # type: ignore
    ADMIN = auto()  # type: ignore
    SUPERADMIN = auto()  # type: ignore
