import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database import db
from security import decode_access_token

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id or not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    user["id"] = str(user.pop("_id"))
    return user