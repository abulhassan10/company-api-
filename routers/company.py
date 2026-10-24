from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth 
from database import get_db
import model
import schema

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post(
    "/",
    response_model=schema.CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new company"
)
def create_company(
    company_in: schema.CompanyCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(auth.get_current_user)
):
    existing = db.query(model.Company).filter(model.Company.email == company_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A company with this email already exists"
        )
    new_company = model.Company(**company_in.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


@router.get(
    "/",
    response_model=List[schema.CompanyResponse],
    summary="Get all companies"
)
def get_companies(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(auth.get_current_user)
):
    return db.query(model.Company).all()


@router.get(
    "/{company_id}",
    response_model=schema.CompanyResponse,
    summary="Get company by ID"
)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(auth.get_current_user)
):
    comp = db.query(model.Company).filter(model.Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return comp
