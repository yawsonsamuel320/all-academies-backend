from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from models.user import User, UserType
import os
from bson import ObjectId

# OAuth2 scheme to extract token from request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Extracts and returns the authenticated user from the JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.find_one(User.id == ObjectId(user_id))
    if not user:
        raise credentials_exception

    return user

async def get_current_school_admin(user: User = Depends(get_current_user)) -> User:
    """Ensures that the authenticated user is a school admin"""
    if user.user_type != UserType.school_admin:
        raise HTTPException(status_code=403, detail="You do not have admin privileges")
    
    return user

async def get_current_contributor(user: User = Depends(get_current_user)) -> User:
    """Ensures that the authenticated user is a school admin"""
    if user.user_type != UserType.exam_contributor:
        raise HTTPException(status_code=403, detail="You do not have exam contributor privileges")
    
    return user

async def get_current_author(user: User = Depends(get_current_user)):
    if user.user_type != UserType.author:
        raise HTTPException(status_code=403, detail="Only authors can upload books")
    return user

async def get_current_contributor(user: User = Depends(get_current_user)):
    if user.user_type != UserType.exam_contributor:
        raise HTTPException(status_code=403, detail="Only contributors can upload assessments")
    return user