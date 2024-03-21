from fastapi import FastAPI,Depends,Header,HTTPException
import uvicorn
from .routers import datamining, facebookapi, googleapi,nhanhapi,connectdatabase,CukCukapi,lazadaapi,shopeeapi,nifi_expession,tiktokshop
from  .security import verify_token
from starlette.background import BackgroundTask
from starlette.types import Message
import logging




app = FastAPI(title='FastAPI',
    description='API'
    , dependencies=[Depends(verify_token)])

app.include_router(facebookapi.router)
app.include_router(googleapi.router)
app.include_router(nhanhapi.router)
app.include_router(connectdatabase.router)
app.include_router(CukCukapi.router)
app.include_router(datamining.router)
app.include_router(lazadaapi.router)
app.include_router(tiktokshop.router)
app.include_router(shopeeapi.router)
app.include_router(nifi_expession.router)
logging.basicConfig(filename='info.log', level=logging.DEBUG)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications 0.3!"}
