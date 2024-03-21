from fastapi import Header, APIRouter,Depends,Body,HTTPException
from requests import Request, Session
from requests.exceptions import HTTPError
import warnings
from urllib.parse import unquote
import json
import pandas as pd
import pandavro as pdx
import numpy as np
from urllib.request import urlopen
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder



router = APIRouter(prefix="/datamining",tags=["DataMining"])

@router.post('/fpgrowth_viewtogether')
async def fpgrowth_viewtogether(data:dict = Body(...)):
    try :
        a = urlopen(data["gcs.media.link"])
    except:
         raise HTTPException(
            status_code=402,
            detail="Link not found",
            headers={"X-Error": "Link not found"},
        )
    try :
        users_df_redux = pdx.from_avro(a)
        my_dict = users_df_redux['_source']

        raw_df = pd.DataFrame(my_dict.tolist())
        raw_df=raw_df.loc[(raw_df['previousLocation']!=0) & (raw_df['currentLocation']!=0)]


        prod_df = raw_df[['creationTimeUtc', 'sessionId', 'previousHandle', 'currentHandle']].melt(id_vars=['creationTimeUtc', 'sessionId'], value_name='product').sort_values(['sessionId', 'creationTimeUtc']).reset_index(drop=True)
        # .drop(['creationTimeUtc', 'variable'], axis=1)
        prod_df['variable'] = prod_df['variable'].str.replace('Handle','')
        lct_df = raw_df[['creationTimeUtc', 'sessionId', 'previousLocation', 'currentLocation']].melt(id_vars=['creationTimeUtc', 'sessionId'], value_name='location_code').sort_values(['sessionId', 'creationTimeUtc']).reset_index(drop=True)
        # .drop(['creationTimeUtc', 'variable', 'sessionId'], axis=1)
        lct_df['variable'] = lct_df['variable'].str.replace('Location','')
        # df = pd.concat([prod_df, lct_df], axis = 1)
        df = prod_df.merge(lct_df, how='inner', on=['creationTimeUtc', 'sessionId', 'variable'])
        df = df.loc[(df['location_code']==1)&(df['product']!="")]
        df = df.groupby(['sessionId','product'])['location_code'].agg('count').reset_index(name='quantity')

        # Get all the transactions as a list of lists
        all_transactions = [transaction[1]['product'].tolist() for transaction in list(df.groupby(['sessionId']))]

        # The following instructions transform the dataset into the required format 
        trans_encoder = TransactionEncoder() # Instanciate the encoder
        trans_encoder_matrix = trans_encoder.fit(all_transactions).transform(all_transactions)
        trans_encoder_matrix = pd.DataFrame(trans_encoder_matrix, columns=trans_encoder.columns_)
        # Build the model
        # call apriori function and pass minimum support here we are passing 0.1%. 
        frq_items = fpgrowth(trans_encoder_matrix, min_support = 0.0001, use_colnames = True, max_len=2)

        # Collect the inferred rules in a dataframe  
        rules = association_rules(frq_items, metric = "lift", min_threshold = 1)  
        rules = rules.sort_values(['confidence', 'lift'], ascending = [False, False])  
        rules['antecedents']=rules['antecedents'].apply(lambda x : list(x)[0])         
        rules['consequents']=rules['consequents'].apply(lambda x : list(x)[0])  
        rules=rules.replace(np.inf, 0)
    except: 
         raise HTTPException(
            status_code=403,
            detail="fpgrowth error",
            headers={"X-Error": "fpgrowth error"},
        )

    # rules=rules.head(10)  
    return (json.loads(json.dumps(rules.to_dict(orient='records'))))
