from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import os
import json

load_dotenv()

env = os.getenv('ENVIRONMENT', 'dev')
SCHEMA_PATH = Path(__file__).parent / "openapi.json"

app = FastAPI(
    title='Test API',
    description='API ',
    openapi_url="/openapi.json"
)
app.openapi_schema = json.loads(SCHEMA_PATH.read_text())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.api_local.router import router
app.include_router(router, prefix=f"/{env.lower() or 'v1'}")


@app.get("/")
def read_root():
    return {"Message": "Api deployed"}


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)

