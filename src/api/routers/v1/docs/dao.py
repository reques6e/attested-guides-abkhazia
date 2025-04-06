from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException, status, Body
from fastapi.responses import JSONResponse

from .dao import *


router = APIRouter(
    prefix='/docs',
    tags=['Документы']
)