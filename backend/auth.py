# ============================================
# AgriAdvisor - Auth Utilities
# auth.py
# ============================================

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

# ============================================
# CONFIG
# ============================================

SECRET_KEY         = os.getenv("SECRET_KEY", "fallback-secret-change-this")
ALGORITHM          = "HS256"
TOKEN_EXPIRE_HOURS = 24

# ============================================
# PASSWORD HASHING
# ============================================

pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto"
)


def hash_password(plain: str) -> str:
    plain = plain[:72]
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)


# ============================================
# JWT TOKEN
# ============================================

def create_token(data: dict) -> str:
    payload        = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")


# ============================================
# DEPENDENCY — protect routes
# ============================================

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated.")
    token = authorization.split(" ")[1]
    return decode_token(token)