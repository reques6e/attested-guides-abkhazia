from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException, status, Body
from fastapi.responses import JSONResponse

from .dao import *


router = APIRouter(
    prefix='/docs',
    tags=['Docs']
)

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    description='Документы'
)
async def get_documents() -> JSONResponse:
    return JSONResponse(
        content={
            'data': [
                {
                    'name': 'Аттестация экскурсоводов (гидов)',
                    'file': 'docs/files/file1.doc',
                    'type': 'doc'
                },
                {
                    'name': 'Утверждение стандартов безопасности',
                    'file': 'docs/files/file2.pdf',
                    'type': 'pdf'
                },
                {
                    'name': 'Курс повышения квалификации',
                    'file': 'docs/files/file3.xlsx',
                    'type': 'xlsx'
                }
            ]
        }
    )