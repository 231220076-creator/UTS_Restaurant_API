from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routes.resource import router as resource_router
from routes.transaction import router as transaction_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database restoran berhasil diinisialisasi!")
    yield


app = FastAPI(
    title="Restaurant Management API",
    description="REST API Manajemen Restoran",
    version="1.0.0",
    lifespan=lifespan
)

# Menghubungkan endpoint menu restoran
app.include_router(resource_router)
app.include_router(transaction_router)

@app.get("/")
async def home():
    return {
        "message": "Restaurant Management API Berhasil Berjalan!"
    }
