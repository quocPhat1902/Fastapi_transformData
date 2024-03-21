import hmac
import hashlib
from datetime import datetime
import requests
import json
from fastapi import Header, APIRouter,Body


router = APIRouter(prefix="/cukcukapi",tags=["MisaCukCuk"])
@router.post('/get_token')
async def get_token(data:dict = Body(...)):

    loginttime=datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    secret = data["secret"]
    AppId=data["appId"]
    Domain=data["domain"]
    message = '''{"AppID":"'''+AppId+'''","Domain":"'''+Domain+'''","LoginTime":"%s"}'''%loginttime
    hash = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    message='''{"AppID":"'''+AppId+'''","Domain":"'''+Domain+'''","LoginTime":"'''+loginttime+'''","SignatureInfo":"%s"}'''%hash
    url="https://graphapi.cukcuk.vn/api/account/login"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    x = requests.post(url,json=json.loads(message),headers=headers)
    return(x.json())


