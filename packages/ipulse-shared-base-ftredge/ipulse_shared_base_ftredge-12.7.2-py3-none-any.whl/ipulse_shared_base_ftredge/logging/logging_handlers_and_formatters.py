# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught

import logging
import traceback
import json
import os
from google.cloud import error_reporting
from google.cloud import logging as cloud_logging

##########################################################################################################################
####################################    Custom logging FORMATTERS    ##################################################### 
##########################################################################################################################

class CloudLogFormatter(logging.Formatter):
    """Formats log records as structured JSON."""

    def format(self, record):
        log_entry = {
            'message': record.msg,
            'timestamp': self.formatTime(record, self.datefmt),
            'name': record.name,
            'severity': record.levelname,
            'pathname': record.pathname,
            'lineno': record.lineno,
        }
        if record.exc_info:
            log_entry['exception_traceback'] = ''.join(traceback.format_exception(*record.exc_info))
        if isinstance(record.msg, dict):
            log_entry.update(record.msg)
        return json.dumps(log_entry)


class LocalLogFormatter(logging.Formatter):
    """Formats log records for local output to the console."""

    def format(self, record):  # Make sure you have the 'record' argument here!
        path_parts = record.pathname.split(os.sep)

        # Get the last two parts of the path if they exist
        if len(path_parts) >= 2:
            short_path = os.path.join(path_parts[-2], path_parts[-1])
        else:
            short_path = record.pathname
        
        # Format log messages differently based on the log level
        if record.levelno == logging.INFO:
            log_message = f"[INFO] {self.formatTime(record, self.datefmt)} :: {record.msg}"
        elif record.levelno == logging.DEBUG:
            log_message = f"[DEBUG] {self.formatTime(record, self.datefmt)} :: {record.msg} :: {short_path} :: lineno {record.lineno} :: {record.name}"
        elif record.levelno == logging.ERROR:
            log_message = f"[ERROR] {self.formatTime(record, self.datefmt)} :: {record.msg} :: {short_path} :: lineno {record.lineno} :: {record.name}"
            if record.exc_info:
                log_message += "\n" + ''.join(traceback.format_exception(*record.exc_info))
        else:
            log_message = f"[{record.levelname}] {self.formatTime(record, self.datefmt)} :: {record.msg} :: {short_path} :: lineno {record.lineno} :: {record.name}"


        return log_message

#############################################################################################################################################
######################################## Logging handlers for Google Cloud ########################################
#############################################################################################################################################

class CustomGCPLoggingHandler(cloud_logging.handlers.CloudLoggingHandler):
    """Custom handler for Google Cloud Logging with a dynamic logName."""
    def __init__(self, client, name, resource=None, labels=None):
        super().__init__(client=client, name=name, resource=resource, labels=labels)
        self.client = client  # Ensure client is consistently used

    def emit(self, record):
        try:
            # 1. Create the basic log entry dictionary
            log_entry = {
                'message': record.msg,
                'severity': record.levelname,
                'name': record.name,
                'pathname': record.filename,
                'lineno': record.lineno,
            }
            if record.exc_info:
                log_entry['exception_traceback'] = ''.join(
                    traceback.format_exception(*record.exc_info)
                )

            # 2. Apply the formatter to the 'message' field if it's a dictionary
            if isinstance(record.msg, dict):
                formatted_message = self.formatter.format(record)
                try:
                    log_entry['message'] = json.loads(formatted_message)
                except json.JSONDecodeError:
                    log_entry['message'] = formatted_message
            else:
                log_entry['message'] = record.msg

            # 3. Set the custom logName
            log_entry['logName'] = f"projects/{self.client.project}/logs/{record.name}"

            # 4. Send to Google Cloud Logging
            super().emit(record)
        except Exception as e:
            self.handleError(record)

class CustomGCPErrorReportingHandler(logging.Handler):
    def __init__(self, client=None, level=logging.ERROR):
        super().__init__(level)
        self.error_client = error_reporting.Client() if client is None else client
        self.propagate = True

    def emit(self, record):
        try:
            log_struct = {  # Create a log entry dictionary
                'message': self.format(record),
                'severity': record.levelname,
                'pathname': getattr(record, 'pathname', None),
                'lineno': getattr(record, 'lineno', None)
            }
            if record.levelno >= logging.ERROR:
                log_struct = {
                'message': self.format(record),
                'severity': record.levelname,
                'pathname': getattr(record, 'pathname', None),
                'lineno': getattr(record, 'lineno', None)
            }
            if record.exc_info:
                log_struct['exception'] = ''.join(
                    traceback.format_exception(*record.exc_info)
                )
            self.error_client.report(str(log_struct))
        except Exception as e:
            self.handleError(record)


def add_gcp_cloud_logging(logger, formatter, project_id=None):
    """Add Google Cloud Logging handler to the logger."""
    
    client = cloud_logging.Client(project=project_id) if project_id else cloud_logging.Client()
    handler = CustomGCPLoggingHandler(client, name=logger.name)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def add_gcp_error_reporting(logger, project_id=None):
    """Add Google Cloud Error Reporting handler to the logger."""
    client = error_reporting.Client(project=project_id) if project_id else error_reporting.Client()
    handler = CustomGCPErrorReportingHandler(client=client)
    handler.setFormatter(LocalLogFormatter())
    logger.addHandler(handler)