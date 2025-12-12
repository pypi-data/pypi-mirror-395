from typing import Any

from fastapi import Request, Response
from fastapi.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

from beans_logging import logger


class HttpAccessLogMiddleware(BaseHTTPMiddleware):
    """Http access log middleware for FastAPI.

    Inherits:
        BaseHTTPMiddleware: Base HTTP middleware class from starlette.

    Attributes:
        _DEBUG_FORMAT     (str ): Default http access log debug message format. Defaults to
            '<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'.
        _MSG_FORMAT       (str ): Default http access log message format. Defaults to
            '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"
                {status_code} {content_length}B {response_time}ms'.

        debug_format      (str ): Http access log debug message format. Defaults to
                                    `HttpAccessLogMiddleware._DEBUG_FORMAT`.
        msg_format        (str ): Http access log message format. Defaults to `HttpAccessLogMiddleware._MSG_FORMAT`.
        use_debug_log     (bool): If True, use debug log to log http access log. Defaults to True.
    """

    _DEBUG_FORMAT = '<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
    _MSG_FORMAT = (
        '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> '
        'HTTP/{http_version}" {status_code} {content_length}B {response_time}ms'
    )

    def __init__(
        self,
        app,
        debug_format: str = _DEBUG_FORMAT,
        msg_format: str = _MSG_FORMAT,
        use_debug_log: bool = True,
    ):
        super().__init__(app)
        self.debug_format = debug_format
        self.msg_format = msg_format
        self.use_debug_log = use_debug_log

    async def dispatch(self, request: Request, call_next) -> Response:
        _logger = logger.opt(colors=True, record=True)

        _http_info: dict[str, Any] = {}
        if hasattr(request.state, "http_info") and isinstance(
            request.state.http_info, dict
        ):
            _http_info: dict[str, Any] = request.state.http_info

        # Debug log:
        if self.use_debug_log:
            _debug_msg = self.debug_format.format(**_http_info)

            # _logger.debug(_debug_msg)
            await run_in_threadpool(
                _logger.debug,
                _debug_msg,
            )
        # Debug log

        # Process request:
        response: Response = await call_next(request)
        # Response processed.

        if hasattr(request.state, "http_info") and isinstance(
            request.state.http_info, dict
        ):
            _http_info: dict[str, Any] = request.state.http_info

        # Http access log:
        _LEVEL = "INFO"
        _msg_format = self.msg_format
        if _http_info["status_code"] < 200:
            _LEVEL = "DEBUG"
            _msg_format = f'<d>{_msg_format.replace("{status_code}", "<n><b><k>{status_code}</k></b></n>")}</d>'
        elif (200 <= _http_info["status_code"]) and (_http_info["status_code"] < 300):
            _LEVEL = "SUCCESS"
            _msg_format = f'<w>{_msg_format.replace("{status_code}", "<lvl>{status_code}</lvl>")}</w>'
        elif (300 <= _http_info["status_code"]) and (_http_info["status_code"] < 400):
            _LEVEL = "INFO"
            _msg_format = f'<d>{_msg_format.replace("{status_code}", "<n><b><c>{status_code}</c></b></n>")}</d>'
        elif (400 <= _http_info["status_code"]) and (_http_info["status_code"] < 500):
            _LEVEL = "WARNING"
            _msg_format = _msg_format.replace("{status_code}", "<r>{status_code}</r>")
        elif 500 <= _http_info["status_code"]:
            _LEVEL = "ERROR"
            _msg_format = (
                f'{_msg_format.replace("{status_code}", "<n>{status_code}</n>")}'
            )

        _msg = _msg_format.format(**_http_info)
        # _logger.bind(http_info=_http_info).log(_LEVEL, _msg)
        await run_in_threadpool(_logger.bind(http_info=_http_info).log, _LEVEL, _msg)
        # Http access log

        return response


__all__ = [
    "HttpAccessLogMiddleware",
]
