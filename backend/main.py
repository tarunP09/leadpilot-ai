from fastapi import FastAPI

from database import db

app = FastAPI(title="LeadPilot AI API", version="0.1.0")


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
