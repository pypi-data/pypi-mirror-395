# Created Date: 2024.???.??
# Version: 2025.01.03

import datetime
from typing import  Any, Union, Optional, Type, TypeVar
import json
import traceback
from pprint import pformat
from enum import Enum

EnumT = TypeVar("EnumT", bound=Enum)


def list_enums_as_strings(*enums):
    """Converts enums to their string values. Handles individual enums, lists, sets, and frozensets."""
    result = []
    for enum_item in enums:
        if isinstance(enum_item, (list, tuple, set, frozenset)):
            # If it's a collection, iterate through it
            result.extend([str(item) for item in enum_item])
        else:
            # If it's a single enum, convert it directly
            result.append(str(enum_item))
    return result

def list_enums_as_lower_strings(*enums):
    """Converts enums to their lowercase string values. Handles individual enums, lists, sets, and frozensets."""
    result = []
    for enum_item in enums:
        if isinstance(enum_item, (list, tuple, set, frozenset)):
            # If it's a collection, iterate through it
            result.extend([str(item).lower() for item in enum_item])
        else:
            # If it's a single enum, convert it directly
            result.append(str(enum_item).lower())
    return result

def val_as_str(value):
    """
    Converts various data types to a string representation.
    """
    if isinstance(value, str):
        return value
    elif value is None:
        return ""  # Return an empty string for NoneType
    elif isinstance(value, bool):
        return str(value)  # Return 'True' or 'False' (without quotes)
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, datetime.datetime):
        return value.isoformat()  # Example: '2024-08-16T14:30:00'
    elif isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')  # Date-only format
    elif isinstance(value, datetime.time):
        return value.strftime('%H:%M:%S')  # Time-only format
    return str(value)  # Fallback to basic string conversion


def any_as_str_or_none(value):
    """
    Converts various data types to a string representation.
    """
    if isinstance(value, str):
        return value
    elif value is None:
        return None  # Return an empty string for NoneType
    elif isinstance(value, bool):
        return str(value)  # Return 'True' or 'False' (without quotes)
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, datetime.datetime):
        return value.isoformat()  # Example: '2024-08-16T14:30:00'
    elif isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')  # Date-only format
    elif isinstance(value, datetime.time):
        return value.strftime('%H:%M:%S')  # Time-only format
    try:
        # Handle collections and complex objects
        return json.dumps(value, default=str, ensure_ascii=False)
    except Exception as e:
        print(f"Error serializing value {value} of type {type(value)}: {e}")
        return str(value)  # Fallback to basic string conversion in case of failure


def stringify_multiline_msg(msg: Union[str, dict, set, Any]) -> str:
    """
    Format multiline messages for better readability in logs.
    Handles dictionaries, sets, and other serializable types.
    """
    try:
        # Use json.dumps for structured types
        if isinstance(msg, (dict, set, list, tuple)):
            return json.dumps(msg if not isinstance(msg, set) else list(msg), indent=2, default=str)
        return str(msg)
    except (TypeError, ValueError):
        # Fallback to pprint for non-serializable objects
        return pformat(msg, indent=2, width=80)


def format_exception(e: Exception, operation_name: Optional[str]="Not Provided") -> dict:
    """
    Format detailed error message as a dictionary.
    """
    return {
        "Exception operation": operation_name,
        "Type": type(e).__name__,
        "Message": str(e),
        "Caused_by": str(e.__cause__ or ""),
        "Stack Trace": traceback.format_tb(e.__traceback__)  # List of stack trace lines
    }


# def to_enum_or_none(value: Any, enum_class: type, required: bool = False, default: Any = None, raise_if_unknown:bool=False) -> Optional[Any]:
#     """Convert value to enum, handling None and string inputs"""

#     if isinstance(value, enum_class):
#         return value
    
#     if value is None:
#         if required:
#             if default:
#                 return default
#             raise ValueError(f"Value is required but was None. Enum class: {enum_class}")
#         return None

#     if isinstance(value, str):
#         try:
#             # Try direct attribute access first (for uppercase)
#             return getattr(enum_class, value.upper())
#         except AttributeError:
#             # Try by value (for lowercase)
#             try:
#                 return enum_class(value.lower())
#             except ValueError:
#                 pass
#     if isinstance(value, (int, str, float)):
#         try:
#             return enum_class(value)
#         except Exception:
#             pass
#     if raise_if_unknown:
#         raise ValueError(f"Unknown value {value} for enum {enum_class} provided")
#     return default



def to_enum_or_none(
    value: Any,
    enum_class: Type[EnumT],
    *,
    required: bool = False,
    default: Optional[EnumT] = None,
    raise_if_unknown: bool = False,
) -> Optional[EnumT]:
    # --- Guard -------------------------------------------------------------
    if not (isinstance(enum_class, type) and issubclass(enum_class, Enum)):
        raise TypeError(f"{enum_class!r} is not an Enum subclass")

    # --- 1. Already correct type ------------------------------------------
    if isinstance(value, enum_class):
        return value

    # --- 2. None handling --------------------------------------------------
    if value is None:
        if required:
            if default is not None:
                return default
            if raise_if_unknown:
                raise ValueError(f"value is required but None for {enum_class.__name__}")
        return None

    # Helper when everything fails
    def _fail() -> Optional[EnumT]:
        if raise_if_unknown:
            raise ValueError(f"Unknown {enum_class.__name__}: {value!r}")
        if default is not None:
            return default
        if required:
            raise ValueError(f"Unknown {enum_class.__name__}: {value!r}")
        return None

    # --- 3. Int branch (❗ patched) ----------------------------------------
    if isinstance(value, int):
        # First try direct (works for IntEnum)
        try:
            return enum_class(value)  # type: ignore[arg-type]
        except ValueError:
            # Second chance: enum stores numeric *strings* (e.g. "380")
            try:
                return enum_class(str(value))  # type: ignore[arg-type]
            except ValueError:
                return _fail()

    # --- 4. Str branch -----------------------------------------------------
    if isinstance(value, str):
        s = value.strip()

        # (a) numeric string
        if s.isdigit():
            try:
                return enum_class(int(s))  # type: ignore[arg-type]
            except ValueError:
                try:
                    return enum_class(s)  # fallback to direct match
                except ValueError:
                    pass

        # (b) member name (case-insensitive)
        m = (enum_class.__members__.get(s)
             or enum_class.__members__.get(s.upper())
             or next((mem for name, mem in enum_class.__members__.items()
                      if name.lower() == s.lower()), None))
        if m:
            return m  # type: ignore[return-value]

        # (c) match by .value directly
        try:
            return enum_class(s)  # type: ignore[arg-type]
        except ValueError:
            return _fail()

    # --- 5. Any other type -------------------------------------------------
    return _fail()


def make_json_serializable(data: Any) -> Any:
    """
    Recursively convert data to JSON serializable format.
    Handles:
    - Enums (converts to name)
    - Datetime objects (converts to ISO format)
    - Sets (converts to lists)
    - Custom objects with to_dict() method
    - Nested dicts and lists
    """
    if hasattr(data, 'name'):  # Enum-like objects
        return str(data)
    if isinstance(data, (datetime.datetime, datetime.date, datetime.time)):
        return data.isoformat()
    if isinstance(data, (set, frozenset)):
        return list(data)
    if hasattr(data, 'to_dict'):  # Custom objects with to_dict method
        return make_json_serializable(data.to_dict())
    if isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    if isinstance(data, (list, tuple)):
        return [make_json_serializable(item) for item in data]
    if isinstance(data, (int, float, str, bool, type(None))):
        return data
    return str(data)  # Fallback to string representation


