from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import user as user_service
from app.core.security import create_access_token
from app.schemas import auth as auth_schema

router = APIRouter()

@router.post("/register", response_model=auth_schema.User)
def register(user: auth_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return user_service.create_user(db, user)

@router.post("/login", response_model=auth_schema.Token)
def login(
    credentials: auth_schema.UserLogin,  # JSON 요청을 처리하기 위한 새로운 스키마 사용
    db: Session = Depends(get_db)
):
    user = user_service.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"} 