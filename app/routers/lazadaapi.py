import hmac
import hashlib
import json
from fastapi import Header, APIRouter,Body
import urllib.parse

router = APIRouter(prefix="/lazadaapi",tags=["LazadaApi"])
@router.post('/get_sign')
async def get_sign(data:dict = Body(...)):

    sort_dict = sorted(data['parameters'])
    
    parameters_str = "%s%s" % (data['api'],
        str().join('%s%s' % (key, data['parameters'][key]) for key in sort_dict))
    h = hmac.new(data['secret'].encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)
    sign=h.hexdigest().upper()
    parameters_link = "%s?%s" % (data['api'],
        str().join('%s=%s&' % (key, urllib.parse.quote(data['parameters'][key])) for key in sort_dict))+"sign="+sign
    # url_link=
    return {"sign":h.hexdigest().upper(),
            "link":parameters_link}
