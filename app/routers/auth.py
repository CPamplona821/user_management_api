from fastapi import APIRouter, Depends, UserInDB
from .auth import get_current_user
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/users/", response_class=JSONResponse)
async def read_users(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
    # Implement retrieving all user profiles for admins
    pass