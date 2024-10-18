from fastapi import FastAPI
from .routers import users, auth
from fastapi import FastAPI, Depends, HTTPException
from .auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def role_based_access_control(request, call_next):
    response = await call_next(request)
    if request.method in ["POST", "PUT", "DELETE"] and "Authorization" in request.headers:
        current_user = await get_current_user(request.headers["Authorization"].split(" ")[1])
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return response

@app.middleware("http")
async def log_requests(request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response: {response.status_code}")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)