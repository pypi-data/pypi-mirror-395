import time
from uuid import uuid4
from typing import Any
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from beans_logging import logger


class RequestHTTPInfoMiddleware(BaseHTTPMiddleware):
    """Request HTTP info middleware for FastAPI.
    Get HTTP info from request header or generate a new one and add it to `request.state.http_info`.

    Inherits:
        BaseHTTPMiddleware: Base HTTP middleware from Starlette.

    Attributes:
        has_proxy_headers (bool): Whether has proxy headers. Defaults to False.
        has_cf_headers    (bool): Whether has Cloudflare headers. Defaults to False.
    """

    def __init__(
        self, app, has_proxy_headers: bool = False, has_cf_headers: bool = False
    ):
        super().__init__(app)
        self.has_proxy_headers = has_proxy_headers
        self.has_cf_headers = has_cf_headers

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        _http_info: dict[str, Any] = {}
        if hasattr(request.state, "http_info") and isinstance(
            request.state.http_info, dict
        ):
            _http_info: dict[str, Any] = request.state.http_info

        _http_info["request_id"] = uuid4().hex
        if "X-Request-ID" in request.headers:
            _http_info["request_id"] = request.headers.get("X-Request-ID")
        elif "X-Correlation-ID" in request.headers:
            _http_info["request_id"] = request.headers.get("X-Correlation-ID")

        # Set request_id to request state:
        request.state.request_id = _http_info["request_id"]

        if request.client:
            _http_info["client_host"] = request.client.host

        _http_info["request_proto"] = request.url.scheme
        _http_info["request_host"] = (
            request.url.hostname if request.url.hostname else ""
        )
        if (request.url.port != 80) and (request.url.port != 443):
            _http_info["request_host"] = (
                f"{_http_info['request_host']}:{request.url.port}"
            )

        _http_info["request_port"] = request.url.port
        _http_info["http_version"] = request.scope["http_version"]

        if self.has_proxy_headers:
            if "X-Real-IP" in request.headers:
                _http_info["client_host"] = request.headers.get("X-Real-IP")
            elif "X-Forwarded-For" in request.headers:
                _http_info["client_host"] = request.headers.get(
                    "X-Forwarded-For", ""
                ).split(",")[0]
                _http_info["h_x_forwarded_for"] = request.headers.get("X-Forwarded-For")

            if "X-Forwarded-Proto" in request.headers:
                _http_info["request_proto"] = request.headers.get("X-Forwarded-Proto")

            if "X-Forwarded-Host" in request.headers:
                _http_info["request_host"] = request.headers.get("X-Forwarded-Host")
            elif "Host" in request.headers:
                _http_info["request_host"] = request.headers.get("Host")

            if "X-Forwarded-Port" in request.headers:
                try:
                    _x_forwarded_port = request.headers.get("X-Forwarded-Port")
                    if _x_forwarded_port:
                        _http_info["request_port"] = int(_x_forwarded_port)

                except ValueError:
                    logger.warning(
                        f"`X-Forwarded-Port` header value '{request.headers.get('X-Forwarded-Port')}' is invalid, "
                        "should be parseable to <int>!"
                    )

            if "Via" in request.headers:
                _http_info["h_via"] = request.headers.get("Via")

            if self.has_cf_headers:
                if "CF-Connecting-IP" in request.headers:
                    _http_info["client_host"] = request.headers.get("CF-Connecting-IP")
                    _http_info["h_cf_connecting_ip"] = request.headers.get(
                        "CF-Connecting-IP"
                    )
                elif "True-Client-IP" in request.headers:
                    _http_info["client_host"] = request.headers.get("True-Client-IP")
                    _http_info["h_true_client_ip"] = request.headers.get(
                        "True-Client-IP"
                    )

                if "CF-IPCountry" in request.headers:
                    _http_info["client_country"] = request.headers.get("CF-IPCountry")
                    _http_info["h_cf_ipcountry"] = request.headers.get("CF-IPCountry")

                if "CF-RAY" in request.headers:
                    _http_info["h_cf_ray"] = request.headers.get("CF-RAY")

                if "cf-ipcontinent" in request.headers:
                    _http_info["h_cf_ipcontinent"] = request.headers.get(
                        "cf-ipcontinent"
                    )

                if "cf-ipcity" in request.headers:
                    _http_info["h_cf_ipcity"] = request.headers.get("cf-ipcity")

                if "cf-iplongitude" in request.headers:
                    _http_info["h_cf_iplongitude"] = request.headers.get(
                        "cf-iplongitude"
                    )

                if "cf-iplatitude" in request.headers:
                    _http_info["h_cf_iplatitude"] = request.headers.get("cf-iplatitude")

                if "cf-postal-code" in request.headers:
                    _http_info["h_cf_postal_code"] = request.headers.get(
                        "cf-postal-code"
                    )

                if "cf-timezone" in request.headers:
                    _http_info["h_cf_timezone"] = request.headers.get("cf-timezone")

        _http_info["method"] = request.method
        _http_info["url_path"] = request.url.path
        if "{" in _http_info["url_path"]:
            _http_info["url_path"] = _http_info["url_path"].replace("{", "{{")
        if "}" in _http_info["url_path"]:
            _http_info["url_path"] = _http_info["url_path"].replace("}", "}}")
        if "<" in _http_info["url_path"]:
            _http_info["url_path"] = _http_info["url_path"].replace("<", "\\<")
        if request.url.query:
            _http_info["url_path"] = f"{request.url.path}?{request.url.query}"

        _http_info["url_query_params"] = request.query_params._dict
        _http_info["url_path_params"] = request.path_params

        _http_info["h_referer"] = request.headers.get("Referer", "-")
        _http_info["h_user_agent"] = request.headers.get("User-Agent", "-")
        _http_info["h_accept"] = request.headers.get("Accept", "")
        _http_info["h_content_type"] = request.headers.get("Content-Type", "")

        if "Origin" in request.headers:
            _http_info["h_origin"] = request.headers.get("Origin")

        _http_info["user_id"] = "-"
        if hasattr(request.state, "user_id"):
            _http_info["user_id"] = str(request.state.user_id)

        # Set http info to request state:
        request.state.http_info = _http_info
        response: Response = await call_next(request)
        return response


class ResponseHTTPInfoMiddleware(BaseHTTPMiddleware):
    """Response HTTP info middleware for FastAPI.
    Get HTTP info from response header and add it to `request.state.http_info`.

    Inherits:
        BaseHTTPMiddleware: Base HTTP middleware from Starlette.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        _http_info: dict[str, Any] = {}
        _start_time: int = time.perf_counter_ns()
        # Process request:
        response: Response = await call_next(request)
        # Response processed.
        _end_time: int = time.perf_counter_ns()
        _response_time: float = round((_end_time - _start_time) / 1_000_000, 1)

        if hasattr(request.state, "http_info") and isinstance(
            request.state.http_info, dict
        ):
            _http_info: dict[str, Any] = request.state.http_info

        _http_info["response_time"] = _response_time
        if "X-Process-Time" in response.headers:
            try:
                _x_process_time = response.headers.get("X-Process-Time")
                if _x_process_time:
                    _http_info["response_time"] = float(_x_process_time)

            except ValueError:
                logger.warning(
                    f"`X-Process-Time` header value '{response.headers.get('X-Process-Time')}' is invalid, "
                    "should be parseable to <float>!"
                )
        else:
            response.headers["X-Process-Time"] = str(_http_info["response_time"])

        if "X-Request-ID" not in response.headers:
            response.headers["X-Request-ID"] = _http_info["request_id"]

        if hasattr(request.state, "user_id"):
            _http_info["user_id"] = str(request.state.user_id)

        _http_info["status_code"] = response.status_code
        _http_info["content_length"] = 0
        if "Content-Length" in response.headers:
            try:
                _content_length = response.headers.get("Content-Length")
                if _content_length:
                    _http_info["content_length"] = int(_content_length)

            except ValueError:
                logger.warning(
                    f"`Content-Length` header value '{response.headers.get('Content-Length')}' is invalid, "
                    "should be parseable to <int>!"
                )

        request.state.http_info = _http_info
        return response


__all__ = [
    "RequestHTTPInfoMiddleware",
    "ResponseHTTPInfoMiddleware",
]
