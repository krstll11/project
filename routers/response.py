from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from database import get_db
from pyd.response_model import ResponseCreate
from pyd.base_models import ResponseBase
import models
from typing import List, Optional
from .auth import get_current_user
from check_user_role import require_admin

router = APIRouter(
    prefix="/responses",
    tags=["responses"]
)

@router.get("/", response_model=List[ResponseBase])
def get_responses(
    db: Session = Depends(get_db),
    ad_id: Optional[int] = Query(None, description="Фильтр по объявлению"),
    user_id: Optional[int] = Query(None, description="Фильтр по пользователю")
):
    query = db.query(models.Response).options(
        joinedload(models.Response.ad),
        joinedload(models.Response.user)
    )

    if ad_id is not None:
        query = query.filter(models.Response.ad_id == ad_id)

    if user_id is not None:
        query = query.filter(models.Response.user_id == user_id)

    responses = query.all()
    return responses


@router.get("/{response_id}", response_model=ResponseBase)
def get_response(response_id: int, db: Session = Depends(get_db)):
    response = db.query(models.Response).filter(models.Response.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@router.post("/", response_model=ResponseBase, status_code=status.HTTP_201_CREATED)
def create_response(
    response: ResponseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_response = models.Response(
        message=response.message,
        ad_id=response.ad_id,
        user_id=current_user.id
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


@router.put("/{response_id}", response_model=ResponseBase)
def update_response(
    response_id: int,
    response_data: ResponseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    response = db.query(models.Response).filter(models.Response.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    if response.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this response")

    response.message = response_data.message
    response.ad_id = response_data.ad_id
    db.commit()
    db.refresh(response)
    return response


@router.delete("/{response_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_response(
    response_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    response = db.query(models.Response).filter(models.Response.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    if response.user_id != current_user.id and not current_user.role.name in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this response")

    db.delete(response)
    db.commit()
