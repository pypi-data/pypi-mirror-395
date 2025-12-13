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



class RecordsSamplingType(AutoLower):
    # -- Same but with names used in Trading
    OPEN                  = auto()  # type: ignore
    HIGH                 = auto()  # type: ignore
    LOW                  = auto()  # type: ignore
    CLOSE                = auto()  # type: ignore
    VOLUME               = auto()  # type: ignore
    ADJ_CLOSE       = auto()  # type: ignore
    ADJ_VOLUME      = auto()  # type: ignore
    OHLC                 = auto()  # type: ignore
    OHLCV                = auto()  # type: ignore
    OHLCVA               = auto()  # type: ignore
    CORP_ACTIONS        = auto()  # type: ignore

    # -- TIMING
    TIMESTAMP            = auto()  # type: ignore

    # -- Same but with names used in Statistics
    MIN                = auto()  # type: ignore
    MAX                = auto()  # type: ignore
    COUNT               = auto()  # type: ignore
    DISTINCTCOUNT      = auto()  # type: ignore
    
    SUM                = auto()  # type: ignore
    MEAN               = auto()  # type: ignore
    MEDIAN             = auto()  # type: ignore
    LAST               = auto()  # type: ignore
    FIRST              = auto()  # type: ignore
    OTHER              = auto()  # type: ignore

class MatchCondition(AutoLower):
    EXACT = auto()  # type: ignore
    PREFIX = auto()  # type: ignore
    SUFFIX = auto()  # type: ignore
    CONTAINS = auto()  # type: ignore
    REGEX = auto()  # type: ignore
    IN_RANGE = auto()  # type: ignore
    NOT_IN_RANGE = auto()  # type: ignore
    GREATER_THAN = auto()  # type: ignore
    LESS_THAN = auto()  # type: ignore
    GREATER_THAN_OR_EQUAL = auto()  # type: ignore
    LESS_THAN_OR_EQUAL = auto()  # type: ignore
    IN_LIST = auto()  # type: ignore
    NOT_IN_LIST = auto()  # type: ignore
    ON_FIELD_MATCH = auto()  # type: ignore
    ON_FIELD_EQUAL = auto()  # type: ignore
    ON_FIELDS_EQUAL_TO = auto()  # type: ignore
    ON_FIELDS_COMBINATION = auto()  # type: ignore
    NOT_APPLICABLE = auto()  # type: ignore

class DuplicationHandling(AutoLower):
    RAISE_ERROR = auto()  # type: ignore
    OVERWRITE = auto()  # type: ignore
    INCREMENT = auto()  # type: ignore
    SKIP = auto()  # type: ignore
    SYSTEM_DEFAULT = auto()  # type: ignore
    ALLOW = auto()  # type: ignore ## applicable for databases allowing this operation i.e. BigQuery
    MERGE_DEFAULT = auto()  # type: ignore
    MERGE_PRESERVE_SOURCE_ON_DUPLICATES = auto()  # type: ignore
    MERGE_PRESERVE_TARGET_ON_DUPLICATES = auto()  # type: ignore
    MERGE_PRESERVE_BOTH_ON_DUPLICATES = auto()  # type: ignore
    MERGE_RAISE_ERROR_ON_DUPLICATES = auto()  # type: ignore
    MERGE_CUSTOM = auto()  # type: ignore

class DuplicationHandlingStatus(AutoLower):
    ALLOWED = auto()  # type: ignore
    RAISED_ERROR = auto()  # type: ignore
    SYSTEM_DEFAULT = auto()  # type: ignore
    OVERWRITTEN = auto()  # type: ignore
    SKIPPED = auto()  # type: ignore
    INCREMENTED = auto()  # type: ignore
    OPERATION_CANCELLED = auto()  # type: ignore
    MERGED = auto()  # type: ignore
    MERGED_PRESERVED_SOURCE = auto()  # type: ignore
    MERGED_PRESERVED_TARGET = auto()  # type: ignore
    MERGED_PRESERVED_BOTH = auto()  # type: ignore
    MERGED_RAISED_ERROR = auto()  # type: ignore
    MERGED_CUSTOM = auto()  # type: ignore
    NO_DUPLICATES = auto()  # type: ignore
    UNKNOWN = auto()  # type: ignore
    UNEXPECTED_ERROR= auto()  # type: ignore
    CONDITIONAL_ERROR = auto()  # type: ignore
    NOT_APPLICABLE = auto()  # type: ignore


class DataFillMethod(AutoLower):
    """Data filling/interpolation methods."""
    FORWARD_FILL = auto()  # type: ignore
    BACKWARD_FILL = auto()  # type: ignore
    LINEAR = auto()  # type: ignore
    POLYNOMIAL = auto()  # type: ignore
    SPLINE = auto()  # type: ignore
    CUBIC = auto()  # type: ignore
    NEAREST = auto()  # type: ignore
    MEAN = auto()  # type: ignore
    MEDIAN = auto()  # type: ignore
    MODE = auto()  # type: ignore
    ZERO = auto()  # type: ignore
    CONSTANT = auto()  # type: ignore
    SEASONAL = auto()  # type: ignore
    TREND = auto()  # type: ignore
    NULL = auto()  # type: ignore

class DataSupplier(AutoLower):
    """Common data origin sources."""
    EODHD = auto()  # type: ignore
    GOOGLE_FINANCE = auto()  # type: ignore
    YAHOO_FINANCE = auto()  # type: ignore
    ALPHA_VANTAGE = auto()  # type: ignore
    QUANDL = auto()  # type: ignore
    BLOOMBERG = auto()  # type: ignore
    REFINITIV = auto()  # type: ignore
    X_COM = auto()  # type: ignore
    TWELVE_DATA = auto()  # type: ignore
    POLYGON = auto()  # type: ignore
    FINNHUB = auto()  # type: ignore
    FRED = auto()  # type: ignore
    WORLD_BANK = auto()  # type: ignore
    IMF = auto()  # type: ignore
    BINANCE = auto()  # type: ignore
    COINBASE = auto()  # type: ignore
    SIMULATION = auto()  # type: ignore
    MANUAL_INPUT = auto()  # type: ignore
    CALCULATED = auto()  # type: ignore
    DERIVED = auto()  # type: ignore
    GOOGLE_GEMINI_LLM_GENERATED = auto()  # type: ignore
    OPENAI_GPT_LLM_GENERATED = auto()  # type: ignore
    ANTHROPIC_CLAUDE_LLM_GENERATED = auto()  # type: ignore
    LLM_GENERATED = auto()  # type: ignore  # Generic LLM generated data
    TIME_SERIES_MODEL_GENERATED = auto()  # type: ignore  # Data generated by time series models
    CLASSIFIER_MODEL_GENERATED = auto()  # type: ignore  # Data generated by classification models
    REGRESSION_MODEL_GENERATED = auto()  # type: ignore  # Data generated by regression models
    AI_MODEL_GENERATED = auto()  # type: ignore  # Data generated by AI models
    CUSTOM = auto()  # type: ignore  # User-defined custom data source

class BigqueryTableWriteOption(AutoUpper):
    """BigQuery write disposition options."""

    """If the table already exists, BigQuery overwrites the table data. """
    """ ==>>>>> WRITE_TRUNCATE is DISABLED because clears up the SCHEMA, NOT ALLOWED. MANUALLY TRUNCATE IF REQUIRED. <======"""
    # WRITE_TRUNCATE = auto()  # type: ignore

    """Safely clears table data while preserving schema, descriptions, and table structure, then appends new data."""
    WRITE_TRUNCATE_PRESERVE_SCHEMA = auto()  # type: ignore

    """If the table already exists, BigQuery appends the data to the table."""
    WRITE_APPEND = auto()  # type: ignore

    """If the table already exists and contains data, a 'duplicate' error is  returned in the job result."""
    WRITE_EMPTY = auto()  # type: ignore
    
   

class FileExtension(StrEnum):

    JSON = ".json"
    NDJSON = ".ndjson"
    CSV = ".csv"
    EXCEL = ".xlsx"
    TXT = ".txt"
    PDF = ".pdf"
    PARQUET = ".parquet"
    AVRO = ".avro"
    WORD = ".docx"
    PPT = ".pptx"
    HTML = ".html"
    MARKDOWN = ".md"
    XML = ".xml"
    YAML = ".yaml"
    TOML = ".toml"
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"