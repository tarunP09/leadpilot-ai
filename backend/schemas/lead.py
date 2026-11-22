from typing import Optional

from pydantic import BaseModel, EmailStr


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    status: str = "new"
    source: Optional[str] = None


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None


class LeadResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    status: str
    source: Optional[str] = None