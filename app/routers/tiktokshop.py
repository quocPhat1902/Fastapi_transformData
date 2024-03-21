import hmac
import hashlib
import json
from fastapi import Header, APIRouter,Body
from fastapi.responses import JSONResponse
import urllib.parse

router = APIRouter(prefix="/tiktokshop",tags=["TikTokShopApi"])
@router.post('/get_sign')
async def get_sign(data:dict = Body(...),):

    sort_dict = sorted(data['parameters'])
    
    parameters_str =data['secret']+ "%s%s" % (data['api'],
        str().join('%s%s' % (key, str(data['parameters'][key])) for key in sort_dict))+data['secret']
   
    sign = hmac.new(data['secret'].encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest()
    parameters_link = "%s?%s" % (data['api'],
         str().join('%s=%s&' % (key, urllib.parse.quote(str(data['parameters'][key]))) for key in sort_dict))+"sign="+sign
    content = {"parameters":data['parameters']}
    headers = {"link":parameters_link, "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
