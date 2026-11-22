from fastapi import FastAPI
from routers import leads
from database import db
from routers import auth

app = FastAPI(title="LeadPilot AI API", version="0.1.0")
app.include_router(leads.router)
app.include_router(auth.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Namaste {name}"}


@app.get("/db-check")
async def db_check():
    await db.command("ping")
    return {"db": "connected"}
