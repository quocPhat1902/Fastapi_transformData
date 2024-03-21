from fastapi import Header, APIRouter,Depends,Body
from fastapi_versioning import version
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adreportrun import AdReportRun
from facebook_business.exceptions import FacebookRequestError
import time
import sys
import json
import warnings


warnings.filterwarnings('ignore')

router = APIRouter(prefix="/facebookapi",tags=["Facebook"])

@router.get('/get_facebook')
async def get_facebook():
    return "Facebook Say Hello"

@router.post('/ads_insights')
async def get_ads_insights(token: dict = Body(...)):
    FacebookAdsApi.init(token["my_app_id"], token["my_app_secret"], token["my_access_token"],api_version='v16.0')
    my_account = AdAccount(token["adaccount"])

    fields = [
    'account_id',
    'account_currency',
    'account_id',
    'account_name',
    'ad_id',
    'ad_name',
    'adset_id',
    'adset_name',
    'campaign_id',
    'campaign_name',
    'objective',
    'clicks',
    'date_start',
    'date_stop',
    'impressions',
    'reach',
    'social_spend',
    'spend',
    'actions',
    'action_values'
    ]

    params = {
        'level':'ad',
        'time_increment':'1',
        'time_range':{"since":token["time_range_1"],"until":token["time_range_2"]},
        'filtering':[{"field":"campaign.name","operator":"CONTAIN","value":"Hungnv_TK3__Car_VN__Tin nhắn__BST Lụa tới trái tim__Album__Mẫu tạo dáng_Tuan9____27.02.2023____"}]
    }


    if token["rp_type"] == "fb_Ads_Insights_Age":
        params['breakdowns'] = '["age"]'
    elif token["rp_type"] == "fb_Ads_Insights_Region":
        params['breakdowns'] = '["region"]'

    try:
        async_job = my_account.get_insights(fields=fields,params=params,is_async=True)
        async_job.api_get()
    except FacebookRequestError as error:
        return {"error_code":error.api_error_code(),
                "error_message":error.api_error_message()}
    fb_Ads_Insights = async_job["report_run_id"]
    data = {}
    data["fb_Ads_Insights"] = fb_Ads_Insights
    json_data = json.dumps(data)
    
    return json.loads(json_data)
