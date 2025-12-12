from collections.abc import Callable

from pydantic import validate_call

from beans_logging import LoggerLoader

from ._filters import use_http_filter
from ._formats import http_file_format, http_file_json_format


@validate_call(config={"arbitrary_types_allowed": True})
def add_http_file_handler(
    logger_loader: LoggerLoader,
    log_path: str = "http/{app_name}.http.access.log",
    err_path: str = "http/{app_name}.http.err.log",
    formatter: Callable | str = http_file_format,
) -> None:
    """Add http access log file and error file handler.

    Args:
        logger_loader (LoggerLoader,         required): LoggerLoader instance.
        log_path      (str,                  optional): Log file path. Defaults to "http/{app_name}.http.access.log".
        err_path      (str,                  optional): Error log file path. Defaults to "http/{app_name}.http.err.log".
        formatter     (Union[Callable, str], optional): Log formatter. Defaults to `http_file_format` function.
    """

    logger_loader.add_handler(
        name="default.http.access.file_handler",
        handler={
            "type": "FILE",
            "sink": log_path,
            "filter": use_http_filter,
            "format": formatter,
        },
    )

    logger_loader.add_handler(
        name="default.http.err.file_handler",
        handler={
            "type": "FILE",
            "sink": err_path,
            "filter": use_http_filter,
            "format": formatter,
            "error": True,
        },
    )

    return


@validate_call(config={"arbitrary_types_allowed": True})
def add_http_file_json_handler(
    logger_loader: LoggerLoader,
    log_path: str = "http.json/{app_name}.http.json.access.log",
    err_path: str = "http.json/{app_name}.http.json.err.log",
    formatter: Callable | str = http_file_json_format,
) -> None:
    """Add http access json log file and json error file handler.

    Args:
        logger_loader (LoggerLoader,         required): LoggerLoader instance.
        log_path      (str,                  optional): Json log file path. Defaults to
                                                            "http.json/{app_name}.http.json.access.log".
        err_path      (str,                  optional): Json error log file path. Defaults to
                                                            "http.json/{app_name}.http.json.err.log".
        formatter     (Union[Callable, str], optional): Log formatter. Defaults to `http_file_json_format` function.
    """

    logger_loader.add_handler(
        name="default.http.access.json_handler",
        handler={
            "type": "FILE",
            "sink": log_path,
            "filter": use_http_filter,
            "format": formatter,
        },
    )

    logger_loader.add_handler(
        name="default.http.err.json_handler",
        handler={
            "type": "FILE",
            "sink": err_path,
            "filter": use_http_filter,
            "format": formatter,
            "error": True,
        },
    )

    return


__all__ = [
    "add_http_file_handler",
    "add_http_file_json_handler",
]
