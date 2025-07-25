from fastapi import FastAPI
from app.api.endpoints import router
from app.core.db import async_engine  # Your async engine from app/core/db.py
from sqlmodel import SQLModel
import asyncio

app = FastAPI(title="Async Media Generator")
app.include_router(router)

# Add a startup event to create tables
@app.on_event("startup")
async def on_startup():
    # This creates all tables if they don't exist already (dev only!)
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
