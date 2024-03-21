from fastapi import Header, APIRouter,Depends,Body
from requests import Request, Session
from requests.exceptions import HTTPError
import warnings
from urllib.parse import unquote
import json
warnings.filterwarnings('ignore')

router = APIRouter(prefix="/nhanhapi",tags=["Nhanh"])

@router.post('/get_data')
async def get_data(token: dict = Body(...)):
    p_url = unquote(token["p_url"])
    data_filter=unquote(token["data"])
    
    files = {'appId': (None, token["appId"]),
    'businessId': (None, token["businessId"]),
    'accessToken': (None,token["accessToken"]),
    'version': (None, token["version"]),
    'data':(None,data_filter)}
    try:
        request = Request('POST', url = p_url, files = files).prepare()
        s = Session()
        responses = s.send(request)
        responses.raise_for_status()
        return json.loads(responses.text)
    except HTTPError as err: 
        return {"code": err.response.status_code,
                "message":err.response.text}
    
    