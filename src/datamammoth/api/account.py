"""Account API — user profile, API keys, sessions, notifications, activity."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth.models.account import (
    Activity,
    ApiKey,
    Notification,
    Session,
    TwoFactorStatus,
    UserProfile,
)


class AccountAPI:
    """Synchronous account API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── Profile ──────────────────────────────────────────────────────

    def me(self) -> UserProfile:
        """Get the authenticated user's profile."""
        return UserProfile(**self._client.get("/me"))

    def update_profile(
        self,
        name: Optional[str] = None,
        company: Optional[str] = None,
        phone: Optional[str] = None,
        country: Optional[str] = None,
        timezone: Optional[str] = None,
        language: Optional[str] = None,
    ) -> UserProfile:
        """Update the user profile."""
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if company is not None:
            body["company"] = company
        if phone is not None:
            body["phone"] = phone
        if country is not None:
            body["country"] = country
        if timezone is not None:
            body["timezone"] = timezone
        if language is not None:
            body["language"] = language
        return UserProfile(**self._client.patch("/me", json=body))

    def change_password(
        self, current_password: str, new_password: str
    ) -> dict:
        """Change the account password."""
        return self._client.post(
            "/me/change-password",
            json={
                "current_password": current_password,
                "new_password": new_password,
            },
        )

    # ── Two-Factor Auth ──────────────────────────────────────────────

    def two_factor_status(self) -> TwoFactorStatus:
        """Get 2FA status."""
        return TwoFactorStatus(**self._client.get("/me/2fa"))

    def enable_two_factor(self, method: str = "totp") -> TwoFactorStatus:
        """Enable 2FA and get provisioning URI + backup codes."""
        return TwoFactorStatus(
            **self._client.post("/me/2fa", json={"method": method, "action": "enable"})
        )

    def disable_two_factor(self, code: str) -> TwoFactorStatus:
        """Disable 2FA with a verification code."""
        return TwoFactorStatus(
            **self._client.post("/me/2fa", json={"code": code, "action": "disable"})
        )

    # ── API Keys ─────────────────────────────────────────────────────

    def api_keys(self) -> List[ApiKey]:
        """List API keys."""
        data = self._client.get("/me/api-keys")
        return [ApiKey(**k) for k in data]

    def create_api_key(
        self,
        name: str,
        scopes: Optional[List[str]] = None,
        expires_at: Optional[str] = None,
    ) -> dict:
        """Create a new API key. Returns the key (only shown once)."""
        body: Dict[str, Any] = {"name": name}
        if scopes:
            body["scopes"] = scopes
        if expires_at:
            body["expires_at"] = expires_at
        return self._client.post("/me/api-keys", json=body)

    def delete_api_key(self, key_id: str) -> None:
        """Revoke an API key."""
        self._client.delete(f"/me/api-keys/{key_id}")

    # ── Sessions ─────────────────────────────────────────────────────

    def sessions(self) -> List[Session]:
        """List active sessions."""
        data = self._client.get("/me/sessions")
        return [Session(**s) for s in data]

    def revoke_session(self, session_id: str) -> None:
        """Revoke (terminate) a session."""
        self._client.delete(f"/me/sessions/{session_id}")

    # ── Notifications ────────────────────────────────────────────────

    def notifications(
        self,
        page: int = 1,
        per_page: int = 20,
        unread_only: bool = False,
    ) -> List[Notification]:
        """List notifications."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if unread_only:
            params["filter[read]"] = "false"
        data = self._client.get("/me/notifications", params=params)
        return [Notification(**n) for n in data]

    def mark_notifications_read(self) -> dict:
        """Mark all notifications as read."""
        return self._client.post("/me/notifications", json={"action": "mark_all_read"})

    # ── Activity ─────────────────────────────────────────────────────

    def activity(
        self,
        page: int = 1,
        per_page: int = 20,
    ) -> List[Activity]:
        """List account activity log."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        data = self._client.get("/me/activity", params=params)
        return [Activity(**a) for a in data]


class AsyncAccountAPI:
    """Asynchronous account API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def me(self) -> UserProfile:
        return UserProfile(**await self._client.get("/me"))

    async def update_profile(
        self,
        name: Optional[str] = None,
        company: Optional[str] = None,
        phone: Optional[str] = None,
        country: Optional[str] = None,
        timezone: Optional[str] = None,
        language: Optional[str] = None,
    ) -> UserProfile:
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if company is not None:
            body["company"] = company
        if phone is not None:
            body["phone"] = phone
        if country is not None:
            body["country"] = country
        if timezone is not None:
            body["timezone"] = timezone
        if language is not None:
            body["language"] = language
        return UserProfile(**await self._client.patch("/me", json=body))

    async def change_password(self, current_password: str, new_password: str) -> dict:
        return await self._client.post(
            "/me/change-password",
            json={
                "current_password": current_password,
                "new_password": new_password,
            },
        )

    async def two_factor_status(self) -> TwoFactorStatus:
        return TwoFactorStatus(**await self._client.get("/me/2fa"))

    async def enable_two_factor(self, method: str = "totp") -> TwoFactorStatus:
        return TwoFactorStatus(
            **await self._client.post("/me/2fa", json={"method": method, "action": "enable"})
        )

    async def disable_two_factor(self, code: str) -> TwoFactorStatus:
        return TwoFactorStatus(
            **await self._client.post("/me/2fa", json={"code": code, "action": "disable"})
        )

    async def api_keys(self) -> List[ApiKey]:
        data = await self._client.get("/me/api-keys")
        return [ApiKey(**k) for k in data]

    async def create_api_key(
        self,
        name: str,
        scopes: Optional[List[str]] = None,
        expires_at: Optional[str] = None,
    ) -> dict:
        body: Dict[str, Any] = {"name": name}
        if scopes:
            body["scopes"] = scopes
        if expires_at:
            body["expires_at"] = expires_at
        return await self._client.post("/me/api-keys", json=body)

    async def delete_api_key(self, key_id: str) -> None:
        await self._client.delete(f"/me/api-keys/{key_id}")

    async def sessions(self) -> List[Session]:
        data = await self._client.get("/me/sessions")
        return [Session(**s) for s in data]

    async def revoke_session(self, session_id: str) -> None:
        await self._client.delete(f"/me/sessions/{session_id}")

    async def notifications(
        self,
        page: int = 1,
        per_page: int = 20,
        unread_only: bool = False,
    ) -> List[Notification]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if unread_only:
            params["filter[read]"] = "false"
        data = await self._client.get("/me/notifications", params=params)
        return [Notification(**n) for n in data]

    async def mark_notifications_read(self) -> dict:
        return await self._client.post("/me/notifications", json={"action": "mark_all_read"})

    async def activity(self, page: int = 1, per_page: int = 20) -> List[Activity]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        data = await self._client.get("/me/activity", params=params)
        return [Activity(**a) for a in data]
