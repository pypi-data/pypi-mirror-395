import json
from typing import Any
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Record


def http_file_format(
    record: "Record",
    msg_format: str = (
        '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" '
        '{status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
    ),
    tz: str = "localtime",
) -> str:
    """Http access log file format.

    Args:
        record     (Record, required): Log record as dictionary.
        msg_format (str   , optional): Log message format.
        tz         (str   , optional): Timezone for datetime field. Defaults to 'localtime'.

    Returns:
        str: Format for http access log record.
    """

    if "http_info" not in record["extra"]:
        return ""

    if "http_message" in record["extra"]:
        del record["extra"]["http_message"]

    _http_info: dict[str, Any] = record["extra"]["http_info"]
    if "datetime" not in _http_info:
        _dt = record["time"]
        if tz != "localtime":
            if not _dt.tzinfo:
                _dt = _dt.replace(tzinfo=ZoneInfo("UTC"))

            _dt = _dt.astimezone(ZoneInfo(tz))

        _http_info["datetime"] = _dt.isoformat(timespec="milliseconds")

    if "content_length" not in _http_info:
        _http_info["content_length"] = 0

    if "h_referer" not in _http_info:
        _http_info["h_referer"] = "-"

    if "h_user_agent" not in _http_info:
        _http_info["h_user_agent"] = "-"

    if "response_time" not in _http_info:
        _http_info["response_time"] = 0

    record["extra"]["http_info"] = _http_info
    _msg = msg_format.format(**_http_info)

    record["extra"]["http_message"] = _msg
    return "{extra[http_message]}\n"


def http_file_json_format(record: "Record") -> str:
    """Http access json log file format.

    Args:
        record (Record, required): Log record as dictionary.

    Returns:
        str: Format for http access json log record.
    """

    if "http_info" not in record["extra"]:
        return ""

    if "datetime" not in record["extra"]["http_info"]:
        record["extra"]["http_info"]["datetime"] = record["time"].isoformat(
            timespec="milliseconds"
        )

    if "http_serialized" in record["extra"]:
        del record["extra"]["http_serialized"]

    _http_info = record["extra"]["http_info"]
    record["extra"]["http_serialized"] = json.dumps(_http_info)

    return "{extra[http_serialized]}\n"


__all__ = [
    "http_file_format",
    "http_file_json_format",
]
