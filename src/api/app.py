import uvicorn
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import create_tables

from routers.v1.router import router as _v1Router
# from .routers.v2.router import router as _v2Router


api = FastAPI(
    title='API By Reques6e',
    version='0.0.1',
    redoc_url=None
)

allow_origins=[
    'http://localhost:5000',  
    'http://127.0.0.1:5000'
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  
    allow_credentials=True,
    allow_methods=['*'],  
    allow_headers=['*'], 
)

api.include_router(_v1Router)
# api.include_router(_v2Router)

if __name__ == '__main__':
    asyncio.run(create_tables())
    uvicorn.run(
        app='app:api', 
        host='0.0.0.0', 
        port=5008,
        reload=True # В проде офнуть нужно
    )