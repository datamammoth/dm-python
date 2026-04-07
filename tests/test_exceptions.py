"""Tests for exception mapping."""

from datamammoth.exceptions import (
    AuthError,
    DataMammothError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    ValidationError,
    map_error,
)


def test_map_401():
    err = map_error(401, {"error": {"code": "INVALID_KEY", "message": "Bad key"}})
    assert isinstance(err, AuthError)
    assert err.status == 401


def test_map_403():
    err = map_error(403, {"error": {"code": "FORBIDDEN", "message": "No access"}})
    assert isinstance(err, PermissionError)
    assert err.status == 403


def test_map_404():
    err = map_error(404, {"error": {"code": "NOT_FOUND", "message": "Gone"}})
    assert isinstance(err, NotFoundError)


def test_map_422():
    err = map_error(
        422,
        {
            "error": {
                "code": "VALIDATION",
                "message": "Invalid",
                "details": {"errors": {"name": "required"}},
            }
        },
    )
    assert isinstance(err, ValidationError)
    assert err.field_errors == {"name": "required"}


def test_map_429():
    err = map_error(
        429,
        {"error": {"code": "RATE_LIMITED", "message": "Slow down"}},
        retry_after=10,
    )
    assert isinstance(err, RateLimitError)
    assert err.retry_after == 10


def test_map_500():
    err = map_error(500, {"error": {"code": "INTERNAL", "message": "Server error"}})
    assert isinstance(err, ServerError)


def test_map_unknown():
    err = map_error(418, {"error": {"code": "TEAPOT", "message": "I'm a teapot"}})
    assert isinstance(err, DataMammothError)
    assert err.status == 418


def test_error_str():
    err = DataMammothError("TEST", "test message", 400)
    assert "[TEST] test message" in str(err)


def test_empty_body():
    err = map_error(500, {})
    assert isinstance(err, ServerError)
    assert err.code == "UNKNOWN_ERROR"
