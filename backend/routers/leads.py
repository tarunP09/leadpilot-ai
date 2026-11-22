from bson import ObjectId
from fastapi import APIRouter, HTTPException

from database import db
from schemas.lead import LeadCreate, LeadResponse

router = APIRouter(prefix="/leads", tags=["Leads"])


def serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(lead: LeadCreate):
    result = await db.leads.insert_one(lead.model_dump())
    return {**lead.model_dump(), "id": str(result.inserted_id)}


@router.get("", response_model=list[LeadResponse])
async def list_leads():
    docs = await db.leads.find().to_list(length=100)
    return [serialize(d) for d in docs]


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: str):
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead id")
    doc = await db.leads.find_one({"_id": ObjectId(lead_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Lead not found")
    return serialize(doc)