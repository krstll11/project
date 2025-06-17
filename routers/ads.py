from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from database import get_db
from sqlalchemy import or_
from pyd.ad_model import AdCreate
from pyd.base_models import AdBase  
import models
from check_user_role import require_admin
from .auth import get_current_user
from typing import List, Optional
router = APIRouter(
    prefix="/ads",
    tags=["ads"]
)


@router.get("/", response_model=list[AdBase])
def get_ads(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    minPrice: Optional[float] = Query(None, alias="minPrice", description="Минимальная цена"),
    maxPrice: Optional[float] = Query(None, alias="maxPrice", description="Максимальная цена"),
): 
    query = db.query(models.Ad).options(
        joinedload(models.Ad.category),
        joinedload(models.Ad.author)
    )
    

    if category:
        query = query.join(models.Ad.category).filter(models.Category.name == category)
    
    if maxPrice is not None:
        query = query.filter(models.Ad.price <= maxPrice)
    if minPrice is not None:
        query = query.filter(models.Ad.price >= minPrice)
        
    offset = (page - 1) * limit
    ads = query.offset(offset).limit(limit).all()
    
    return ads


@router.get("/{ad_id}", response_model=AdBase)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad


@router.post("/", response_model=AdBase, status_code=status.HTTP_201_CREATED)
def create_ad(ad: AdCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_ad = models.Ad(
        title=ad.title,
        description=ad.description,
        price=ad.price,
        author_id=current_user.id,
        category_id=ad.category_id
    )
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    
    if ad.author_id != current_user.id and current_user.role.name not in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this ad")

    db.delete(ad)
    db.commit()



@router.put("/{ad_id}", response_model=AdBase)
def update_ad(ad_id: int, ad_update: AdCreate, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    ad = db.query(models.Ad).filter(models.Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    ad.title = ad_update.title
    ad.description = ad_update.description
    ad.price = ad_update.price
    ad.category_id = ad_update.category_id

    
    if ad.author_id != current_user.id and current_user.role.name not in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this ad")
    
    db.commit()
    db.refresh(ad)
    return ad
