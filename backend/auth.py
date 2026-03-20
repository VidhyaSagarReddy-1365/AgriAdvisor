# ============================================
# AgriAdvisor - Auth Utilities
# auth.py
# ============================================

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
from typing import Optional

# ============================================
# CONFIG
# ============================================

SECRET_KEY         = "agriadvisor-secret-key-change-this"
ALGORITHM          = "HS256"
TOKEN_EXPIRE_HOURS = 24

# ============================================
# PASSWORD HASHING
# ============================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)


def hash_password(plain: str) -> str:
    # Truncate to 72 bytes max — bcrypt limitation
    plain = plain[:72]
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    # Truncate same way before verifying
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)


# ============================================
# JWT TOKEN
# ============================================

def create_token(data: dict) -> str:
    payload      = data.copy()
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