from collections import defaultdict, deque
from time import monotonic
from threading import Lock
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from app.schemas.common import TokenResponse
from app.security import hash_password, verify_password, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
_attempts = defaultdict(deque)
_lock = Lock()

def check_rate_limit(key: str):
    now = monotonic()
    with _lock:
        bucket = _attempts[key]
        while bucket and now - bucket[0] > settings.login_rate_limit_window_seconds:
            bucket.popleft()
        if len(bucket) >= settings.login_rate_limit_attempts:
            raise HTTPException(status_code=429, detail="Too many login attempts; try again later")
        bucket.append(now)

@router.post("/register", response_model=UserResponse, status_code=201, summary="Register a user")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.role not in ("Admin", "Viewer"):
        raise HTTPException(status_code=422, detail="Role must be Admin or Viewer")
    if db.scalar(select(User).where(User.email == payload.email.lower())):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(name=payload.name, email=payload.email.lower(), hashed_password=hash_password(payload.password), role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse, summary="Log in and receive a JWT")
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    check_rate_limit(request.client.host if request.client else "unknown")
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}
