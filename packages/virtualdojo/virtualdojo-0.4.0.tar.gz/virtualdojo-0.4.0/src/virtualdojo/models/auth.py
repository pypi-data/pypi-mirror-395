"""Authentication-related models."""

from typing import Optional

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Response from login endpoint."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800
    refresh_token: Optional[str] = None


class UserInfo(BaseModel):
    """User information response."""

    id: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    tenant_id: str
    profile_id: Optional[str] = None


class APIKeyResponse(BaseModel):
    """Response from API key creation."""

    id: str
    name: str
    key: str  # Only shown on creation
    created_at: str
    expires_at: Optional[str] = None


class APIKeyInfo(BaseModel):
    """API key information (without the actual key)."""

    id: str
    name: str
    created_at: str
    expires_at: Optional[str] = None
    is_active: bool = True
