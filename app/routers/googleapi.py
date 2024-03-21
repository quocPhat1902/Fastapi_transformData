from fastapi import Header, APIRouter,Body
import time
import jwt
import requests
import json
router = APIRouter(prefix="/googleapi",tags=["Google"])

@router.get('/')
async def get_google():
    return "Google Say Hello"
@router.post('/get_token')
async def get_token(data:dict = Body(...)):
    
    
    iat = time.time()
    exp = iat + 3600
    try:
        payload = {'iss': data[ 'client_email'],
                'sub': data[ 'client_email'],
                'scope': data['scope'],
                'aud': data[ 'token_uri'],
                'iat': iat,
                'exp': exp}
    except:
        payload = {'iss': data[ 'client_email'],
                'sub': data[ 'client_email'],
                'scope': 'https://www.googleapis.com/auth/cloud-platform',
                'aud': data[ 'token_uri'],
                'iat': iat,
                'exp': exp}
    signed_jwt = jwt.encode(
        payload, 
        data[ 'private_key'],
        algorithm='RS256')
    signed_jwt = signed_jwt.decode('UTF-8')

    url = "https://oauth2.googleapis.com/token?grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion="
    response = requests.post(url+signed_jwt)

    return(json.loads(response.content.decode('UTF-8')))

@router.post('/ga_jolt_spec')
async def ga_jolt_spec(data:dict = Body(...)):
    metric=data["reportRequests"][0]['metrics']
    dimensions=data["reportRequests"][0]['dimensions']
    value=[]
    dim=[]
    for m in metric:
        value.append(m['expression'])
    for d in dimensions:
        value.append(d['name'])
        dim.append(d['name'])

    json_data={ "operation": "shift",
                "spec":{}}
    for i in range(len(value)):
        a={"*":{"@":value[i].replace('ga:','[&1].')}}
        json_data["spec"].update({value[i]:a})
    json_1=json.dumps(json_data)

    str_a='),@('.join(dim).replace('ga:','1,')
    str_a="=join('',@("+ str_a +'))'
    json_2={ "operation": "modify-overwrite-beta",
            "spec":{"*":{"id":str_a}}}
    json_2=json.dumps(json_2)

    res='['+json_1+','+json_2+']'
    return(json.loads(json.loads(json.dumps(res))))
