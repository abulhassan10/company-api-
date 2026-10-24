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
    existing_user = db.query(model.User).filter(
        or_(model.User.username == user_in.username, model.User.email == user_in.email)
    ).first()

    if existing_user:
        if existing_user.username == user_in.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    
    
        

    # Hash password
    hashed_password = utils.hash(user_in.password)

    # Create new user
    new_user = model.User(
        username=user_in.username,
        email=user_in.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return (new_user)


# -------------------- Login with Username/Email & Password --------------------
@router.post(
    "/login",
    response_model=schema.Token,
    summary="Login with Username/Email and Password"
)
def login_with_password(credentials: schema.LoginPasswordRequest, db: Session = Depends(get_db)):
    # Find user by username or email
    user = db.query(model.User).filter(
        or_(model.User.username == credentials.username, model.User.email == credentials.username)
    ).first()

    if not user or not utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )

    # Generate JWT token
    token_data = {"user_id": user.id, "username": user.username}
    access_token = auth.create_access_token(data=token_data)

    return schema.Token(access_token=access_token, token_type="bearer")


# -------------------- OAuth2 Password Form Login (For Swagger UI Authorize button) --------------------
@router.post(
    "/login/form",
    response_model=schema.Token,
    include_in_schema=False
)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(
        or_(model.User.username == form_data.username, model.User.email == form_data.username)
    ).first()

    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = auth.create_access_token(data={"sub": str(user.id), "username": user.username})
    return schema.Token(access_token=access_token, token_type="bearer")
