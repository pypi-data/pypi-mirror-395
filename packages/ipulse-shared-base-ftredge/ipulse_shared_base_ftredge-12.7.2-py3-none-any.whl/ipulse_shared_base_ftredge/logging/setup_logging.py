# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
import logging
from typing import List, Union, Optional
import json
from ipulse_shared_base_ftredge import LoggingHandler
from .logging_handlers_and_formatters import (CloudLogFormatter,
                                            LocalLogFormatter,
                                            add_gcp_cloud_logging,
                                            add_gcp_error_reporting)


def get_logger(logger_name:str, level=logging.INFO, 
               logging_handler_providers: Union[LoggingHandler, List[LoggingHandler]] = LoggingHandler.NONE,
               project_id: Optional[str] = None):
    """
    Creates and configures a logger with the specified handlers.
    
    Args:
        logger_name: Name of the logger
        level: Logging level
        logging_handler_providers: List of logging handler providers
        project_id: GCP Project ID for cloud logging (if None, uses default credentials)
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    cloud_formatter = CloudLogFormatter()

    # # Set project ID in environment if specified
    # if project_id:
    #     import os
    #     os.environ["GOOGLE_CLOUD_PROJECT"] = project_id

    # Ensure logging_handler_providers is a list for consistent processing
    if not isinstance(logging_handler_providers, list):
        logging_handler_providers = [logging_handler_providers]

    supported_remote_handlers = [
        LoggingHandler.GCP_CLOUD_LOGGING,
        LoggingHandler.GCP_ERROR_REPORTING,
        LoggingHandler.LOCAL_STREAM,
        LoggingHandler.NONE, # If NONE is considered a remote handler
    ]

    # Remote handlers
    for handler_provider in logging_handler_providers:
        if handler_provider in supported_remote_handlers:
            if handler_provider == LoggingHandler.GCP_CLOUD_LOGGING:
                add_gcp_cloud_logging(logger, cloud_formatter, project_id)
            elif handler_provider == LoggingHandler.GCP_ERROR_REPORTING:
                add_gcp_error_reporting(logger, project_id)
            elif handler_provider == LoggingHandler.LOCAL_STREAM:  # Handle local stream
                local_handler = logging.StreamHandler()
                local_handler.setFormatter(LocalLogFormatter())
                logger.addHandler(local_handler)
        else:
            raise ValueError(
            f"Unsupported logging provider: {handler_provider}. "
            f"Supported providers: {[h.value for h in supported_remote_handlers]}"
            )
    return logger

def log_critical(msg, logger=None, print_out=False, exc_info=False):
    formatted_msg = format_multiline_message(msg)
    if print_out:
        print(formatted_msg)
    if logger:
        logger.critical(formatted_msg, exc_info=exc_info)

def log_error(msg, logger=None, print_out=False, exc_info=False):
    formatted_msg = format_multiline_message(msg)
    if print_out:
        print(formatted_msg)
    if logger:
        logger.error(formatted_msg, exc_info=exc_info)

def log_warning(msg, logger=None, print_out=False):
    formatted_msg = format_multiline_message(msg)
    if print_out:
        print(formatted_msg)
    if logger:
        logger.warning(formatted_msg)

def log_info(msg, logger=None, print_out=False):
    formatted_msg = format_multiline_message(msg)
    if print_out:
        print(formatted_msg)
    if logger:
        logger.info(formatted_msg)

def log_debug(msg, logger=None, print_out=False):
    formatted_msg = format_multiline_message(msg)
    if print_out:
        print(formatted_msg)
    if logger:
        logger.debug(formatted_msg)

def log_by_lvl(debug_msg: Optional[str]=None, info_msg: Optional[str]=None, warning_msg: Optional[str]=None, error_msg: Optional[str]=None, logger=None, print_out=False):
    if debug_msg:
        log_debug(debug_msg, logger, print_out)
    if info_msg:
        log_info(info_msg, logger, print_out)
    if warning_msg:
        log_warning(warning_msg, logger, print_out)
    if error_msg:
        log_error(error_msg, logger, print_out)

def format_multiline_message(msg: Union[str, dict]) -> str:
    """Format multiline messages for better readability in logs."""
    if isinstance(msg, dict):
        return json.dumps(msg, indent=2)
    return str(msg)
