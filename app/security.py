from fastapi import  Header, HTTPException
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECURE_ACCESS_TOKEN: str 

async def verify_token(x_token: str = Header(...)):
    settings = Settings()
    print(settings.SECURE_ACCESS_TOKEN)
    if x_token != settings.SECURE_ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
