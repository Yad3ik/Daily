"""Shared network error types for task UI (front-only guards)."""

import httpx

NETWORK_ERRORS = (
    httpx.TimeoutException,
    httpx.ReadTimeout,
    httpx.ConnectTimeout,
    httpx.ConnectError,
    httpx.NetworkError,
)
