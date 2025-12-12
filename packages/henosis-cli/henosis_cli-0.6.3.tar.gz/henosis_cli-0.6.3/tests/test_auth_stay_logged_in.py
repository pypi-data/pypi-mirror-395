from __future__ import annotations

"""Programmatic tests for the "stay logged in" auth flow.

These tests exercise the FastAPI auth endpoints directly using httpx + TestClient
to validate that:

1. /api/login with remember_me=true issues both access and refresh cookies.
2. /api/check-auth succeeds with a valid access token.
3. When the access token is considered invalid/expired, the unified auth
   dependency can still authenticate the user via the refresh token by
   calling /api/check-auth.
4. /api/refresh issues a new access token and optionally rotates the refresh
   token when near expiry.

The goal is to give us a tight, repeatable loop for debugging "stay logged in"
semantics independent of the CLI.
"""

from typing import Dict

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _extract_auth_cookies(resp) -> Dict[str, str]:
    jar = {}
    for c in resp.cookies.jar:
        if c.name in ("access_token_cookie", "refresh_token_cookie"):
            jar[c.name] = c.value
    return jar


def test_login_with_remember_me_issues_refresh_cookie():
    """Login with remember_me=true should set both access and refresh cookies."""
    # NOTE: assumes a test user exists in the DB. Adjust creds or create a fixture
    # user as needed for your environment.
    username = "testuser"
    password = "testpassword"

    resp = client.post(
        "/api/login",
        json={
            "username": username,
            "password": password,
            "remember_me": True,
            "device_id": "test-device",
            "device_name": "pytest device",
        },
    )
    assert resp.status_code == 200, resp.text
    cookies = _extract_auth_cookies(resp)
    assert "access_token_cookie" in cookies, "login did not set access token cookie"
    assert "refresh_token_cookie" in cookies, "login did not set refresh token cookie when remember_me=true"


def test_check_auth_works_with_access_token_only():
    """/api/check-auth should authenticate when the access token cookie is valid."""
    username = "testuser"
    password = "testpassword"

    login = client.post(
        "/api/login",
        json={"username": username, "password": password, "remember_me": False},
    )
    assert login.status_code == 200, login.text
    cookies = _extract_auth_cookies(login)
    assert "access_token_cookie" in cookies

    r = client.get("/api/check-auth", cookies=cookies)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("authenticated") is True
    assert data.get("user") == username


def test_check_auth_falls_back_to_refresh_when_access_missing():
    """/api/check-auth should authenticate via refresh when access cookie is missing.

    We simulate an expired/missing access token by deleting it from the cookie jar
    and then calling /api/check-auth with only the refresh cookie.
    """
    username = "testuser"
    password = "testpassword"

    login = client.post(
        "/api/login",
        json={"username": username, "password": password, "remember_me": True},
    )
    assert login.status_code == 200, login.text
    cookies = _extract_auth_cookies(login)
    assert "refresh_token_cookie" in cookies

    # Drop the access token to simulate expiry/missing
    cookies.pop("access_token_cookie", None)

    r = client.get("/api/check-auth", cookies=cookies)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("authenticated") is True
    assert data.get("user") == username


def test_refresh_endpoint_issues_new_access_token():
    """/api/refresh should return a new access token when given a valid refresh cookie."""
    username = "testuser"
    password = "testpassword"

    login = client.post(
        "/api/login",
        json={"username": username, "password": password, "remember_me": True},
    )
    assert login.status_code == 200, login.text
    cookies = _extract_auth_cookies(login)
    assert "refresh_token_cookie" in cookies

    r = client.post("/api/refresh", cookies={"refresh_token_cookie": cookies["refresh_token_cookie"]})
    assert r.status_code == 200, r.text
    # TestClient automatically updates its cookie jar; but we can also inspect Set-Cookie headers if needed
    new_cookies = _extract_auth_cookies(r)
    assert "access_token_cookie" in new_cookies or "access_token_cookie" in client.cookies
