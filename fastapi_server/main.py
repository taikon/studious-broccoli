import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.api import api_router

root_router = APIRouter()

app = FastAPI()

@root_router.get("/ping")
async def ping() -> str:
    return "pong"

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(api_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run(
        app='main:app', 
        host='0.0.0.0', 
        port=8000, 
        reload=True, 
        log_level="debug"
    )

