from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
import models
from typing import List
from pyd.user_model import UserBase
from pyd.user_model import UserCreate
from check_user_role import require_admin
from routers.auth import get_password_hash  as hashed_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[UserBase])
def get_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    _=Depends(require_admin("admin"))
):
    offset = (page - 1) * limit
    return db.query(models.User).offset(offset).limit(limit).all()


@router.get("/{user_id}", response_model=UserBase)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_admin("admin"))):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
def create_user(
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
        role_id=2,
        password=hashed_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=UserBase)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin("admin"))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email = user_data.email
    user.nickname = user_data.nickname
    user.role_id = 3
    user.password = hashed_password(user_data.password)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin("admin"))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
