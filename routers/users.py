from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

import auth
from database import get_db
import model
import schema
import utils

router = APIRouter(
    prefix="/users",
    tags=["Authentication & Users"]
)



# -------------------- Registration --------------------
@router.post(
    "/register",
    response_model=schema.Userresponse,
    status_code=status.HTTP_201_CREATED,
   
)
def register_user(user_in: schema.Usercreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(model.User).filter (model.User.username == user_in.username
    ).first()

    if existing_user:
        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
      
    
    
        

    # Hash password
    hashed_password = utils.hash(user_in.password)

    # Create new user
    new_user = model.User(
        username=user_in.username,
       
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return (new_user)


# -------------------- Login with Username/Email & Password --------------------


# -------------------- OAuth2 Password Form Login (For Swagger UI Authorize button) --------------------
@router.post(
    "/login/form",
    response_model=schema.Token
    
)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter (model.User.username == form_data.username, 
    ).first()

    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = auth.create_access_token(data={"sub": str(user.id), "username": user.username})
    return schema.Token(access_token=access_token, token_type="bearer")
