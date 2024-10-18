from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from .auth import authenticate_user, create_access_token, get_current_user, pwd_context
from models import User
from schemas import UserCreate, UserUpdate, UserInDB
from database import engine
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import secrets
from datetime import datetime, timedelta
from fastapi import BackgroundTasks

router = APIRouter()
app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@router.post("/register", response_model=User InDB, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    # Check if the user already exists
    existing_user = await engine.find_one(User, User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create a new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_active=True,  # Set to True for simplicity; implement email verification as needed
        is_verified=False
    )
    verification_link = f"http://localhost:8000/verify/{new_user.email}"  # Simplified link
    await send_verification_email(user.email, verification_link)
    
    await engine.save(new_user)
    return new_user

async def send_verification_email(email: str, verification_link: str):
    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'
    msg['To'] = email
    msg['Subject'] = 'Email Verification'

    body = f'Please verify your email by clicking on the following link: {verification_link}'
    msg.attach(MIMEText(body, 'plain'))

    # Use your SMTP server credentials
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)

@router.get("/verify/{email}")
async def verify_email(email: str):
    user = await engine.find_one(User, User.email == email)
    if user:
        user.is_verified = True
        await engine.save(user)
        return {"detail": "Email verified successfully"}
    raise HTTPException(status_code=404, detail="User  not found")

@router.get("/users/", response_model=list[User InDB])
async def read_users(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = await engine.find(User)
    return users

@router.get("/users/{user_id}", response_model=User InDB)
async def read_user(user_id: str, current_user: User = Depends(get_current_user)):
    user = await engine.find_one(User, User.id == user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return user

@router.put("/users/{user_id}", response_model=User InDB)
async def update_user(user_id: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    existing_user = await engine.find_one(User, User.id == user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    
    # Only allow the user to update their own profile or if they are an admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if user.password:
        existing_user.hashed_password = pwd_context.hash(user.password)
    existing_user.username = user.username or existing_user.username
    existing_user.email = user.email or existing_user.email
    existing_user.role = user.role or existing_user.role
    
    await engine.save(existing_user)
    return existing_user

@router.delete("/users/{user_id}", response_class=JSONResponse)
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    existing_user = await engine.find_one(User, User.id == user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    
    # Only allow the user to delete their own profile or if they are an admin
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await engine.delete(existing_user)
    return JSONResponse(status_code=200, content={"detail": "User deleted successfully"})

async def send_password_reset_email(email: str, reset_link: str):
    # Similar to the email verification function, implement email sending logic here.
    pass

@router.post("/password-reset/request")
async def password_reset_request(email: str, background_tasks: BackgroundTasks):
    user = await engine.find_one(User, User.email == email)
    if user:
        # Generate a reset token (in a real application, you'd want to store this securely)
        reset_token = secrets.token_urlsafe(16)
        reset_link = f"http://localhost:8000/password-reset/confirm/{reset_token}"
        background_tasks.add_task(send_password_reset_email, email, reset_link)
        return {"detail": "Password reset link sent to your email."}
    raise HTTPException(status_code=404, detail="User not found.")

@router.post("/password-reset/confirm/{token}")
async def password_reset_confirm(token: str, new_password: str):
    # In a real application, you would verify the token and associate it with a user.
    # For simplicity, we will skip this part.
    # Hash the new password
    hashed_password = pwd_context.hash(new_password)
    # Update the user's password (you need to find the user associated with the token)
    user = await engine.find_one(User, User.email == "user@example.com")  # Example lookup
    if user:
        user.hashed_password = hashed_password
        await engine.save(user)
        return {"detail": "Password updated successfully."}
    raise HTTPException(status_code=404, detail="User not found.")