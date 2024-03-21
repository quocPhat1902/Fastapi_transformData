from sqlite3 import connect
from fastapi import Header, APIRouter,Body,HTTPException
from fastapi_versioning import version
from pymysql.err import IntegrityError
import json
import pymysql
import json
import pandas as pd

import io


from datetime import datetime
from pymysql.err import IntegrityError


router = APIRouter(prefix="/database",tags= ["Database"])

# Custom JSON encoder that handles datetime objects
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            if obj == b'\x01':
                return 1
            elif obj == b'\x00':
                return 0
            else:
                return obj.decode('utf-8')
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@router.post('/get_data_mysql')
async def mysqlconnect(data :dict = Body(...)):
# To connect MySQL database
    conn = pymysql.connect(
        host=data['DatabaseHost'],
        port=data['DatabasePort'],
        user=data['DatabaseUser'], 
        password =data['DatabasePassword'],
        db=data['DatabaseName'],
        charset='utf8mb4'
        # cursorclass=pymysql.cursors.DictCursor
        )
    try:
        cur = conn.cursor()
    except Exception as e:
       raise HTTPException(status_code=402, detail=e)
    
    sql=''
    if data['count_row']=="true":
        if(data['LoadFullData']=="true"):
            sql=""" select count(1) as count_row from `{0}` ;""".format(data['TableName'])
        elif(data['AppendByColumnName'] !="null"):
            sql=""" select count(1) as count_row from `{0}`
            ORDER BY `{1}` ASC  ;""".format(data['TableName'],data['AppendByColumnName'])
        elif(data['RawQuery']!="null"):
            sql=data['RawQuery']
    else:
        if(data['LoadFullData']=="true"):
            sql=""" select * from `{0}` LIMIT {1} OFFSET {2};""".format(data['TableName'],data['limit'],data['offset'])
        elif(data['AppendByColumnName'] !="null"):
            sql=""" select * from `{0}`
            ORDER BY `{1}` ASC  LIMIT {2} OFFSET {3};""".format(data['TableName'],data['AppendByColumnName'],data['limit'],data['offset'])
        elif(data['RawQuery']!="null"):
            sql=data['RawQuery']
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
       raise HTTPException(status_code=402, detail=e)
    # result = cur.fetchall()
   
    if(df.empty):
        raise HTTPException(status_code=401, detail="Table is NULL")
    if cur and conn:                        
        cur.close() 
        conn.close() 
    try:
        json_result = df.to_json(orient='records')
        result_json = json.dumps(json_result,ensure_ascii=False,cls=CustomEncoder)
    except:
         raise HTTPException(status_code=403, detail="Transform data error!!!")
    return json.loads(json.loads(result_json))


