from fastapi import APIRouter, Depends, HTTPException

from database import db
from dependencies import get_current_user
from schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate):
    email = data.email.lower()
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=409, detail="Email already registered")

    user = {
        "name": data.name,
        "email": email,
        "password_hash": hash_password(data.password),
        "role": "agent",
    }
    result = await db.users.insert_one(user)
    return {
        "id": str(result.inserted_id),
        "name": user["name"],
        "email": email,
        "role": user["role"],
    }


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    user = await db.users.find_one({"email": data.email.lower()})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user["_id"]), user["role"])
    return {"access_token": token}


@router.get("/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    return current_user