from datetime import datetime, time
from cerberus import Validator

class RecordSchemaCerberusValidator(Validator):
    """Custom validator class for data validation."""
    def _check_with_standard_str_date(self, field, value):
        """Custom validation rule for date fields accepting 
           both datetime.date and YYYY-MM-DD strings.
        """
        if isinstance(value, datetime):
            return True  # Valid datetime.date object
        elif isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return True # Valid date string
            except ValueError:
                self._error(field, f"Must be a valid date in YYYY-MM-DD format or a datetime.date object, got: {value}")
        else:
            self._error(field, f"Must be a valid date in YYYY-MM-DD format or a datetime.date object, got: {value}")

    def _check_with_iso_str_timestamp(self, field, value):
        """Custom validation for timestamp fields accepting 
           both datetime.datetime objects and ISO format strings.
        """
        if isinstance(value, datetime):
            return True  # Valid datetime.datetime object
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value) 
                return True # Valid ISO format string
            except ValueError:
                self._error(field, f"Must be a valid ISO format timestamp string or a datetime.datetime object, got: {value}")
        else:
            self._error(field, f"Must be a valid ISO format timestamp string or a datetime.datetime object, got: {value}")

    def _check_with_standard_str_time(self, field, value):
        """Custom validation rule for time fields accepting 
           both datetime.time and HH:MM:SS strings.
        """
        if isinstance(value, time):
            return True  # Valid datetime.time object
        elif isinstance(value, str):
            try:
                datetime.strptime(value, "%H:%M:%S")
                return True # Valid time string
            except ValueError:
                self._error(field, f"Must be a valid time in HH:MM:SS format or a datetime.time object, got: {value}")
        else:
            self._error(field, f"Must be a valid time in HH:MM:SS format or a datetime.time object, got: {value}")