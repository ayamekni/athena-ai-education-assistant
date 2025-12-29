"""
Authentication Pydantic schemas
"""
from pydantic import BaseModel, EmailStr


class LoginInput(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshTokenInput(BaseModel):
    """Refresh token request schema"""
    refresh_token: str
