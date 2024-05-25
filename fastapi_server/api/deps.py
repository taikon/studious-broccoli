from fastapi import Depends, HTTPException
from core.config import settings
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

get_bearer_token = HTTPBearer()

async def authorize(
    authorization: HTTPAuthorizationCredentials = Depends(get_bearer_token)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid authorization")

    access_token = authorization.credentials
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid authorization")

    if access_token != settings.ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid access token")

    return True

