from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.config import settings

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.get(User, int(user_id))
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")


def require_admin(
    user: User = Depends(get_current_user),
):
    if user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return user