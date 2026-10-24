from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# -------------------- Company Schemas --------------------
class Companycreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    city: str


class companyresponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    address: str
    city: str

    class Config:
        from_attributes = True


CompanyCreate = Companycreate
CompanyResponse = companyresponse


# -------------------- Employee Schemas --------------------
class Employeecreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    position: str
    company_id: int


class employeeresponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    position: str
    company_id: int

    class Config:
        from_attributes = True


EmployeeCreate = Employeecreate
EmployeeResponse = employeeresponse


# -------------------- User & Auth Schemas --------------------
class Usercreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    


class Userresponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    

    class Config:
        from_attributes = True


UserCreate = Usercreate
UserResponse = Userresponse


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None


class LoginPasswordRequest(BaseModel):
    username: str
    password: str



