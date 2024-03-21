# 
FROM python:3.9

# 
WORKDIR /fastapi

# 
COPY ./requirements.txt /fastapi/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /fastapi/requirements.txt
# 
COPY ./app /fastapi/app
EXPOSE 4000
# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000", "--workers", "4", "--timeout-keep-alive", "120"]
