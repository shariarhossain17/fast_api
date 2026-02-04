import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

load_dotenv()


app=FastAPI(title=os.getenv("APP_NAME","FASTAPI"))


@app.get("/ping")
def ping():
    return {"status":"ok","message":"pong"}
