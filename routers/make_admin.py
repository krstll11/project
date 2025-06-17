from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
import models
from pyd.user_model import UserBase
from pyd.user_model import UserCreate
from check_user_role import require_admin
from routers.auth import get_password_hash  as hashed_password

router = APIRouter(
    prefix="/adminmaker",
    tags=["adminmaker"]
)


@router.post("/admin", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_admin(
    user: UserCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin("admin"))
):
    existing = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.nickname == user.nickname)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with such email or nickname already exists")

    new_user = models.User(
        email=user.email,
        nickname=user.nickname,
        role_id=1,
        password=hashed_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/mod", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_moderator(
    user: UserCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin("admin"))
):
    existing = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.nickname == user.nickname)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with such email or nickname already exists")

    new_user = models.User(
        email=user.email,
        nickname=user.nickname,
        role_id=3,
        password=hashed_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user