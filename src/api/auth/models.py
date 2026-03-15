from string import digits, punctuation

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator, model_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    password2: str
    gender: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, password: str) -> str:
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long",
            )
        if not any(c in digits for c in password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one digit",
            )
        if not any(c in punctuation for c in password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one special character",
            )
        return password

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
            )
        return self
