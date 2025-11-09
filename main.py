from fastapi import FastAPI
from routes import file_router
from db import engine, Base
from models import Files # needed to for that Base statement


app = FastAPI()

app.include_router(file_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message":"Server running"}
