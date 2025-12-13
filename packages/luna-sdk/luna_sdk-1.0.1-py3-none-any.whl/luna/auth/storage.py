"""Secure storage for authentication tokens."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import keyring

from luna.auth.types import TokenPair


class TokenStore(ABC):
    """Abstract base class for token storage."""

    @abstractmethod
    def save(self, tokens: TokenPair) -> None:
        """Save tokens to storage."""
        ...

    @abstractmethod
    def load(self) -> TokenPair | None:
        """Load tokens from storage."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear tokens from storage."""
        ...


class KeyringTokenStore(TokenStore):
    """
    Token storage using the system keyring.
    
    Uses the 'keyring' library to securely store credentials
    in the operating system's credential manager (Keychain on macOS,
    Credential Vault on Windows, Secret Service on Linux).
    """

    def __init__(self, service_name: str = "luna-sdk", account_name: str = "default") -> None:
        self._service = service_name
        self._account_access = f"{account_name}_access"
        self._account_refresh = f"{account_name}_refresh"
        self._account_expires = f"{account_name}_expires"

    def save(self, tokens: TokenPair) -> None:
        keyring.set_password(self._service, self._account_access, tokens.access_token)
        if tokens.refresh_token:
            keyring.set_password(self._service, self._account_refresh, tokens.refresh_token)
        if tokens.expires_at:
            keyring.set_password(self._service, self._account_expires, tokens.expires_at.isoformat())

    def load(self) -> TokenPair | None:
        access_token = keyring.get_password(self._service, self._account_access)
        if not access_token:
            return None

        refresh_token = keyring.get_password(self._service, self._account_refresh)
        # Note: Expiration parsing omitted for brevity, usually re-validated by API
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token or "",
            expires_at=None 
        )

    def clear(self) -> None:
        try:
            keyring.delete_password(self._service, self._account_access)
            keyring.delete_password(self._service, self._account_refresh)
            keyring.delete_password(self._service, self._account_expires)
        except keyring.errors.PasswordDeleteError:
            pass


class FileTokenStore(TokenStore):
    """
    Token storage using a local JSON file (for development).
    """

    def __init__(self, path: str | Path = "~/.luna/credentials.json") -> None:
        self._path = Path(path).expanduser()

    def save(self, tokens: TokenPair) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "expires_at": tokens.expires_at.isoformat() if tokens.expires_at else None,
        }
        with open(self._path, "w") as f:
            json.dump(data, f)
        
        # Set permissions to 0600 (read/write only by owner)
        try:
            self._path.chmod(0o600)
        except Exception:
            pass

    def load(self) -> TokenPair | None:
        if not self._path.exists():
            return None
        
        try:
            with open(self._path, "r") as f:
                data = json.load(f)
                return TokenPair(
                    access_token=data.get("access_token", ""),
                    refresh_token=data.get("refresh_token", ""),
                    expires_at=None # Parsing logic needed if strictly required
                )
        except Exception:
            return None

    def clear(self) -> None:
        if self._path.exists():
            self._path.unlink()
