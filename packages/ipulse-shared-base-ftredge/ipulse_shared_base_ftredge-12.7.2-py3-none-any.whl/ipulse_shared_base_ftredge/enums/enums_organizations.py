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


class OrganizationRelation(AutoLower):
    """Organization relationship types"""

    RETAIL_CUSTOMER = auto()  # type: ignore
    CORPORATE_CUSTOMER = auto()  # type: ignore
    PARENT = auto()  # type: ignore
    SISTER = auto()  # type: ignore
    SELF = auto()  # type: ignore
    PARTNER = auto()  # type: ignore
    SUPPLIER = auto()  # type: ignore
    SPONSOR = auto()  # type: ignore
    INVESTOR = auto()  # type: ignore
    REGULATOR = auto()  # type: ignore
    OTHER = auto()  # type: ignore

class OrganizationIndustry(AutoLower):
    """Organization industry types"""
    DATA = auto()  # type: ignore
    GOVERNMENT = auto()  # type: ignore
    MEDIA = auto()  # type: ignore
    ACADEMIC = auto()  # type: ignore
    COMMERCIAL = auto()  # type: ignore
    FUND = auto()  # type: ignore
    FINANCE = auto()  # type: ignore
    ADVISORY = auto()  # type: ignore
    HEDGEFUND = auto()  # type: ignore
    BANK = auto()  # type: ignore
    VC = auto()  # type: ignore
    PE = auto()  # type: ignore
    CONSTRUCTION = auto()  # type: ignore
    HEALTHCARE = auto()  # type: ignore
    TECHNOLOGY = auto()  # type: ignore
    CONSULTING = auto()  # type: ignore
    RETAIL = auto()  # type: ignore
    NON_PROFIT = auto()  # type: ignore
    INDIVIDUAL = auto()  # type: ignore
    FREELANCER = auto()  # type: ignore
    OTHER = auto()  # type: ignore