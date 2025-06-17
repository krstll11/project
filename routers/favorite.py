from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from pyd.favorite_model import FavoriteCreate
from pyd.base_models import FavoriteBase
from typing import List
from .auth import get_current_user
import models

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)

@router.get("/", response_model=List[FavoriteBase])
def get_my_favorites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    favorites = db.query(models.Favorite).options(
        joinedload(models.Favorite.ad)
    ).filter(models.Favorite.user_id == current_user.id).all()
    return favorites


@router.post("/{favorite_id}", response_model=FavoriteBase, status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing = db.query(models.Favorite).filter_by(
        ad_id=favorite_id,
        user_id=current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")

    db_favorite = models.Favorite(
        ad_id=favorite_id,
        user_id=current_user.id
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    favorite = db.query(models.Favorite).filter(
        models.Favorite.id == favorite_id,
        models.Favorite.user_id == current_user.id
    ).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
