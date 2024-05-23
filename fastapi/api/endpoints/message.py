from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post("/message")
async def create_message(
    *,
    message: Message
):
    return {"message": message.message}

