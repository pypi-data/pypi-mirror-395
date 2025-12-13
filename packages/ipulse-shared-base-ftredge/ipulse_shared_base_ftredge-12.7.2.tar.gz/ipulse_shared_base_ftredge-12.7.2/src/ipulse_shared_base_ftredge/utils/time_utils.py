from ipulse_shared_base_ftredge.enums.enums_units import TimeFrame

def calculate_timeframe_from_days(diff_days: int) -> str:
    """
    Calculates the TimeFrame enum string based on the difference in days.
    
    Args:
        diff_days: The difference in days between two dates.
        
    Returns:
        The string value of the corresponding TimeFrame enum.
    """
    if diff_days <= 1:
        return str(TimeFrame.ONE_DAY)
    elif diff_days <= 7:
        return str(TimeFrame.ONE_WEEK)
    elif diff_days <= 14:
        return str(TimeFrame.TWO_WEEKS)
    elif diff_days <= 31:
        return str(TimeFrame.ONE_MONTH)
    elif diff_days <= 61:
        return str(TimeFrame.TWO_MONTHS)
    elif diff_days <= 92:
        return str(TimeFrame.THREE_MONTHS)
    elif diff_days <= 183:
        return str(TimeFrame.SIX_MONTHS)
    elif diff_days <= 366:
        return str(TimeFrame.ONE_YEAR)
    elif diff_days <= 731:
        return str(TimeFrame.TWO_YEARS)
    elif diff_days <= 1096:
        return str(TimeFrame.THREE_YEARS)
    elif diff_days <= 1461:
        return str(TimeFrame.FOUR_YEARS)
    else:
        return str(TimeFrame.FIVE_YEARS)
