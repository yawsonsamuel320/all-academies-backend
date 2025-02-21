from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.security import get_password_hash
from models.auth import LoginRequest, TokenResponse
from models.user import User, InviteStatus
from core.security import verify_password, create_access_token
from datetime import timedelta
from schemas.user import CompleteSignupRequest

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate a user and return an access token."""
    
    # Check if user exists
    user = await User.find_one(User.email == user_data.username)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/complete-signup")
async def complete_signup(request: CompleteSignupRequest):
    user = await User.find_one(User.email == request.email)

    if not user or user.school["status"] != InviteStatus.accepted:
        raise HTTPException(status_code=400, detail="Invalid registration attempt")

    # Update user details
    user.first_name = request.first_name
    user.last_name = request.last_name

    user.password_hash = get_password_hash(request.password)
    user.school["status"] = InviteStatus.registered

    # Set additional attributes from the request
    for attr, value in request.model_dump().items():
        if attr != "password":
            setattr(user, attr, value)

    await user.save()
    return {"message": "Signup complete, you can now log in"}


@router.post("/logout")
async def logout(response: Response):
    """Logs out the user by removing the authentication token."""
    response.delete_cookie("access_token")  # If stored in cookies
    return {"message": "Logged out successfully"}
