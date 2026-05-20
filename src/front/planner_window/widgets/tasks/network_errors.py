"""Типы сетевых ошибок httpx для безопасной обработки в UI задач."""

import httpx

# Исключения httpx, при которых UI задач не падает.
NETWORK_ERRORS = (
    httpx.TimeoutException,
    httpx.ReadTimeout,
    httpx.ConnectTimeout,
    httpx.ConnectError,
    httpx.NetworkError,
)
