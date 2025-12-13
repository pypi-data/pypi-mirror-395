# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import StrEnum, unique
from typing import Union


# ──────────────────────────────────────────────────────────────────────────────
# Unit Builder Utility Functions
# ──────────────────────────────────────────────────────────────────────────────
def build_composite_unit(numerator: Union[str, 'Unit'], denominator: Union[str, 'Unit']) -> str:
    """Build a composite unit string like 'USD/share' or 'km/h'."""
    num_str = numerator.value if hasattr(numerator, 'value') else str(numerator)
    den_str = denominator.value if hasattr(denominator, 'value') else str(denominator)
    return f"{num_str}/{den_str}"


def build_rate_unit(base_unit: Union[str, 'Unit'], time_unit: Union[str, 'Unit']) -> str:
    """Build a rate unit like 'records/second' or 'USD/year'."""
    return build_composite_unit(base_unit, time_unit)


def build_density_unit(mass_unit: Union[str, 'Unit'], volume_unit: Union[str, 'Unit']) -> str:
    """Build a density unit like 'kg/m3' or 'g/l'.""" 
    return build_composite_unit(mass_unit, volume_unit)


def build_price_unit(currency: Union[str, 'Unit'], item: Union[str, 'Unit']) -> str:
    """Build a price unit like 'USD/share' or 'EUR/barrel'."""
    return build_composite_unit(currency, item)


# ──────────────────────────────────────────────────────────────────────────────
# Abstract marker – lets you type-hint a generic "kind of enum we serialise".
# ──────────────────────────────────────────────────────────────────────────────
# Abstract marker – lets you type-hint a generic "kind of enum we serialise".
# ──────────────────────────────────────────────────────────────────────────────
class Unit(StrEnum):
    """Marker base for all serialisable dimension / code enums.
    
    Supports both simple units (USD, kg, m) and composite units using format:
    - Division: numerator/denominator (e.g., "USD/share", "km/h", "kg/m3")
    - Multiplication: factor*unit (e.g., "1000*USD" for thousands)
    - Complex: combine both (e.g., "USD*1000/share/year")
    """

# ──────────────────────────────────────────────────────────────────────────────
# Financial or *countable* units , data nad Memory
# ──────────────────────────────────────────────────────────────────────────────
@unique
class FinancialUnit(Unit):
    """Units commonly used in finance and data-commerce."""
    # Basic financial units
    SHARE = "share"               # Number of shares
    BPS = "bps"                   # Basis points
    PERCENT = "percent"           # %
    INDEX_POINT = "index_point"
    RATIO = "ratio"
    COUNT = "count"
    ITEM = "item"
    RECORD = "record"             # Generic record
    COLUMN = "column"
    UNIT = "unit"                 # Fallback generic
    
    # Common composite financial units
    USD_PER_SHARE = "USD/share"   # Price per share
    BPS_PER_YEAR = "bps/year"     # Basis points per year (yields, spreads)
    PERCENT_PER_YEAR = "percent/year"  # Annual percentage rates
    SHARES_PER_USD = "share/USD"  # Shares you can buy per dollar
    USD_PER_UNIT = "USD/unit"     # Generic price per unit
    RATIO_PER_YEAR = "ratio/year" # Annual ratios (P/E, etc.)
    COUNT_PER_DAY = "count/day"   # Daily transaction count, etc.

@unique
class DataUnit(Unit):
    DBROW = "dbrow"                # Generic row
    DBCOLUMN = "dbcolumn"          # Generic column
    DBVALUE = "dbvalue"            # Generic value
    DBRECORD = "dbrecord"          # Generic record
    DOCUMENT = "document"      # Generic document
    TABLE = "table"            # Generic table
    COLLECTION = "collection"  # Generic collection
    MESSAGE = "message"          # Generic message
    FILE = "file"              # Generic file
    DATABASE = "database"        # Generic database
    HTTP_REQUEST = "http_request"      # Generic HTTP request
    HTTP_RESPONSE = "http_response"    # Generic HTTP response
    
    # Data throughput composite units
    RECORDS_PER_SECOND = "record/second"
    BYTES_PER_SECOND = "byte/second"
    REQUESTS_PER_MINUTE = "http_request/minute"
    MESSAGES_PER_HOUR = "message/hour"


# ──────────────────────────────────────────────────────────────────────────────
# Common Composite Units (Cross-Category)
# ──────────────────────────────────────────────────────────────────────────────
@unique  
class CompositeUnit(Unit):
    """Common composite units that cross multiple categories."""
    # Velocity/Speed
    KM_PER_HOUR = "km/h"
    METERS_PER_SECOND = "m/s" 
    MILES_PER_HOUR = "mph"
    
    # Density
    KG_PER_CUBIC_METER = "kg/m3"
    GRAMS_PER_LITER = "g/l"
    
    # Financial rates
    USD_PER_BARREL = "USD/bbl"      # Oil prices
    USD_PER_OUNCE = "USD/oz"        # Precious metals
    USD_PER_TON = "USD/t"           # Commodities
    USD_PER_KILOGRAM = "USD/kg"     # Generic commodity pricing
    
    # Energy/Power  
    WATTS_PER_HOUR = "W/h"
    CALORIES_PER_GRAM = "cal/g"
    
    # Data rates
    GIGABYTES_PER_SECOND = "GB/s"
    MEGABITS_PER_SECOND = "Mbps"
    
    # Productivity
    ITEMS_PER_HOUR = "item/h"
    TASKS_PER_DAY = "task/day"
    ERRORS_PER_THOUSAND = "error/1000"

    tokens_per_minute = "token/minute"  # NLP processing rate
    words_per_minute = "word/minute"    # Reading/speaking rate
    characters_per_page = "character/page"  # Text density
    sentences_per_paragraph = "sentence/paragraph"  # Text structure

@unique
class MemoryUnit(Unit):
    BYTE = "BYTE"
    KILOBYTE = "KILOBYTE"
    MEGABYTE = "MEGABYTE"
    GIGABYTE = "GIGABYTE"
    TERABYTE = "TERABYTE"
    PETABYTE = "PETABYTE"
    EXABYTE = "EXABYTE"

@unique
class TSize(StrEnum):
    """T-shirt size enum for categorizing relative sizes (models, datasets, etc).
    
    Automatically converted to lowercase when serialized.
    """
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"
    XXL = "xxl"
    XXXL = "xxxl"

# ──────────────────────────────────────────────────────────────────────────────
# Mass / Volume / Length units
# ──────────────────────────────────────────────────────────────────────────────
@unique
class MassUnit(Unit):
    GRAM = "g"
    KILOGRAM = "kg"
    TONNE = "t"
    POUND = "lb"
    OUNCE = "oz"
    TROY_OUNCE = "ozt"

@unique
class VolumeUnit(Unit):
    LITRE = "l"
    BARREL = "bbl"
    GALLON = "gal"

@unique
class AreaUnit(Unit):
    SQUARE_METER = "m2"
    SQUARE_FOOT = "ft2"
    ACRE = "acre"

# ──────────────────────────────────────────────────────────────────────────────
# Temperature units
# ──────────────────────────────────────────────────────────────────────────────
@unique
class TemperatureUnit(Unit):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"

# ──────────────────────────────────────────────────────────────────────────────
# Time Units
# ──────────────────────────────────────────────────────────────────────────────

@unique
class TimeUnit(Unit):
    NANOSECOND = "nanosecond"
    MICROSECOND = "microsecond"
    MILLISECOND = "millisecond"
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

# ──────────────────────────────────────────────────────────────────────────────
# Currency ISO-4217 codes
# ──────────────────────────────────────────────────────────────────────────────
@unique
class Currency(Unit):
    AED = "AED"
    AUD = "AUD"
    BRL = "BRL"
    CAD = "CAD"
    CHF = "CHF"
    CNY = "CNY"
    EUR = "EUR"
    GBP = "GBP"
    HKD = "HKD"
    INR = "INR"
    JPY = "JPY"
    KRW = "KRW"
    MXN = "MXN"
    NOK = "NOK"
    NZD = "NZD"
    RUB = "RUB"
    SEK = "SEK"
    SGD = "SGD"
    USD = "USD"
    ZAR = "ZAR"


# ──────────────────────────────────────────────────────────────────────────────
# Market bar sizes / time frames
# ──────────────────────────────────────────────────────────────────────────────
@unique
class TimeFrame(Unit):
    """Common bar sizes for market data (a.k.a. candle durations)."""
    NEVER = "never"
    ONCE = "once"  # Single point in time, no duration
    REAL_TIME = "real_time"
    ONE_MIN = "1min"
    FIVE_MIN = "5min"
    FIFTEEN_MIN = "15min"
    THIRTY_MIN = "30min"
    ONE_HOUR = "1h"
    TWO_HOURS = "2h"
    THREE_HOURS = "3h"
    FOUR_HOURS = "4h"
    FIVE_HOURS = "5h"
    SIX_HOURS = "6h"
    SEVEN_HOURS = "7h"
    EIGHT_HOURS = "8h"
    NINE_HOURS = "9h"
    TEN_HOURS = "10h"
    ELEVEN_HOURS = "11h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "1d"
    EOD = "eod"
    TWO_DAYS = "2d"
    THREE_DAYS = "3d"
    ONE_WEEK = "1w"
    TWO_WEEKS = "2w"
    THREE_WEEKS = "3w"
    ONE_MONTH = "1m"
    TWO_MONTHS = "2m"
    THREE_MONTHS = "3m"
    SIX_MONTHS = "6m"
    EIGHT_MONTHS = "8m"
    NINE_MONTHS = "9m"
    ONE_YEAR = "1y"
    TWO_YEARS = "2y"
    THREE_YEARS = "3y"
    FOUR_YEARS = "4y"
    FIVE_YEARS = "5y"
    SIX_YEARS = "6y"
    SEVEN_YEARS = "7y"
    EIGHT_YEARS = "8y"
    NINE_YEARS = "9y"
    TEN_YEARS = "10y"
    ELEVEN_YEARS = "11y"
    TWELVE_YEARS = "12y"
    THIRTEEN_YEARS = "13y"
    FOURTEEN_YEARS = "14y"
    FIFTEEN_YEARS = "15y"
    TWENTY_YEARS = "20y"
    THIRTY_YEARS = "30y"
    FOURTY_YEARS = "40y"
    FIFTY_YEARS = "50y"
    HUNDRED_YEARS = "100y"
    MAX= "max"  # Represents the maximum available history of the asset
    ADHOC = "adhoc"  # User-defined custom time frame
    TRIGGER_BASED = "trigger_based"
    DRIFT_DETECTION_BASED = "drift_detection_based"
    THRESHOLD_BASED = "threshold_based"
    VARIABLE = "variable"
    MIXED = "mixed"  # Used for mixed time frames, e.g., different intervals for different assets
    CUSTOM = "custom"  # Custom time frame defined by user
    NA = "na"  # Not applicable or not available
    UNKNOWN = "unknown"


# ──────────────────────────────────────────────────────────────────────────────
# Days of week / schedule codes
# ──────────────────────────────────────────────────────────────────────────────
@unique
class DayOfWeekInt(Unit):
    """ISO-8601 weekday numbers with helpful bundles."""
    MONDAY = "1"
    TUESDAY = "2"
    WEDNESDAY = "3"
    THURSDAY = "4"
    FRIDAY = "5"
    SATURDAY = "6"
    SUNDAY = "7"

    # Combined codes (keep as strings to avoid numeric ambiguity)
    MON_THU = "1-4"
    MON_FRI = "1-5"
    MON_SAT = "1-6"
    WEEKEND = "6-7"
    SUN_THU = "7-4"
    MON_SUN = "1-7"

@unique
class DayOfWeekStr(Unit):
    """ISO-8601 weekday numbers with helpful bundles."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    # Combined codes (keep as strings to avoid numeric ambiguity)
    MON_THU = "mon-thu"
    MON_FRI = "mon-fri"
    MON_SAT = "mon-sat"
    WEEKEND = "sat-sun"
    SUN_THU = "sun-thu"
    MON_SUN = "mon-sun"

# ──────────────────────────────────────────────────────────────────────────────
# Natural Language / Text units
# ──────────────────────────────────────────────────────────────────────────────
@unique
class NaturalLanguageUnit(Unit):
    """Units for measuring natural language text and NLP tasks."""
    # Character-level units
    CHAR = "char"  # Alias for character
    BYTE = "byte"  # For encoding size
    CODEPOINT = "codepoint"  # Unicode codepoint
    
    # Phonetic units
    PHONEME = "phoneme"
    SYLLABLE = "syllable"
    VOWEL = "vowel"
    CONSONANT = "consonant"
    
    # Word-level units
    WORD = "word"
    TOKEN = "token"  # NLP token (subword or word)
    SUBWORD = "subword"  # BPE, WordPiece tokens
    MORPHEME = "morpheme"  # Smallest meaning unit
    
    # Phrase and sentence units
    N_GRAM = "n_gram"
    BIGRAM = "bigram"
    TRIGRAM = "trigram"
    PHRASE = "phrase"
    CLAUSE = "clause"
    SENTENCE = "sentence"
    
    # Paragraph and document units
    PARAGRAPH = "paragraph"
    SECTION = "section"
    CHAPTER = "chapter"
    PAGE = "page"
    DOCUMENT = "document"
    
    # Specialized NLP units
    ENTITY = "entity"  # Named entity
    SPAN = "span"  # Text span/annotation
    UTTERANCE = "utterance"  # Dialog turn
    TURN = "turn"  # Conversation turn
    LINE = "line"  # Line of text