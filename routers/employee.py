from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth
from database import get_db
import model
import schema

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "/",
    response_model=schema.EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee"
)
def create_employee(
    emp_in: schema.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(auth.get_current_user)
):
    # Verify company exists
    comp = db.query(model.Company).filter(model.Company.id == emp_in.company_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    existing = db.query(model.Employee).filter(model.Employee.email == emp_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An employee with this email already exists"
        )

    new_emp = model.Employee(**emp_in.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp


@router.get(
    "/",
    response_model=List[schema.EmployeeResponse],
    summary="Get all employees"
)
def get_employees(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(auth.get_current_user)
):
    return db.query(model.Employee).all()


@router.get(
    "/{employee_id}",
    response_model=schema.EmployeeResponse,
    summary="Get employee by ID"
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(auth.get_current_user)
):
    emp = db.query(model.Employee).filter(model.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp


@router.get(
    "/company/{company_id}",
    response_model=List[schema.EmployeeResponse])
def get_employees_by_company(
    company_id: int,
    db: Session = Depends(get_db),
    
):
    comp = db.query(model.Company).filter(model.Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return comp.employees