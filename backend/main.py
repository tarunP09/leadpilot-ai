from fastapi import FastAPI

app = FastAPI(title="LeadPilot AI API", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Namaste {name}"}