
# Version:  2024.06.23
from typing import Dict, List, Any, Union, Set


def filter_records(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    column_to_filter_on: str,
    values_to_filter: Set[Any],
) -> List[Dict[str, Any]]:
    """
    Filters records based on a provided column and values, 
    with early type checking and handling for empty data.

    Args:
        data (Union[Dict[str, Any], List[Dict[str, Any]]]): Input data.
        column_to_filter_on (str): Filtering column name.
        values_to_filter (Set[Any]): Values to filter against.

    Returns:
        List[Dict[str, Any]]: Filtered records.

    Raises:
        TypeError: If a type mismatch is detected during the early check.
    """

    if isinstance(data, dict):
        data = [data]

    # Handle empty data
    if not data:
        return []

    # If values_to_filter is empty, no filtering needed
    if not values_to_filter:
        return data

    # Early Type Check using only the first value in the set
    first_record_value = data[0].get(column_to_filter_on)
    
    if first_record_value is None:
        raise ValueError(f"Column '{column_to_filter_on}' not found in the data.")

    filter_value_type = type(first_record_value)

    # Check the type of the first value in values_to_filter
    first_filter_value = next(iter(values_to_filter))
    if not isinstance(first_filter_value, filter_value_type):
        raise TypeError(
            f"Type mismatch detected: column '{column_to_filter_on}' has values of type "
            f"{filter_value_type}, but 'values_to_filter' contains values of type {type(first_filter_value)}."
        )

    # Filtering: No type conversion, just filtering
    filtered_records = [
        record
        for record in data
        if record[column_to_filter_on] not in values_to_filter
    ]

    return filtered_records
