import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.api import api_router
from ml import ocr

root_router = APIRouter()

app = FastAPI()

@root_router.get("/ping")
async def ping() -> str:
    return "pong"

@root_router.get("/healthcheck")
async def healthcheck() -> str:
    """
    Pre-loads the model and tokenizer.
    """
    ocr.load_model()
    ocr.load_tokenizer()
    return "ok"

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

