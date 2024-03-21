import hmac
import hashlib
from fastapi import Header, APIRouter,Body

router = APIRouter(prefix="/shopeeapi",tags=["ShopeeApi"])
@router.post('/get_sign')
async def get_sign(data:dict = Body(...)):

    base_string ="%s%s%s%s%s"%(data["partner_id"], data["path"],data["timest"],data["access_token"], data["shop_id"]) 

    sign = hmac.new(  bytes(data["partner_key"], 'UTF-8'),base_string.encode(),hashlib.sha256).hexdigest() 
    return {"sign":sign}

@router.post('/get_sign_refresh_token')
async def get_sign_refresh_token(data:dict = Body(...)):

    base_string ="%s%s%s"%(data["partner_id"], data["path"],data["timest"]) 

    sign = hmac.new(  bytes(data["partner_key"], 'UTF-8'),base_string.encode(),hashlib.sha256).hexdigest() 
    return {"sign":sign}



