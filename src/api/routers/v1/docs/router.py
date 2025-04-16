from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException, status, Body
from fastapi.responses import JSONResponse

from .dao import DocumentsDAO

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
    result = await DocumentsDAO.get_all()
    return JSONResponse(
        content={
            'data': result
        }
    )

@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    description='Создать документ'
)
async def create_document(
    name: str = Body(..., description='Название файла'),
    url: str = Body(..., description='Ссылка на файл'),
    file_type: str = Body(None, description='Тип файла')
) -> JSONResponse:
    allowed_file_types = ['doc', 'pdf', 'xlsx']
    if file_type is None:
        parsed_url = urlparse(url)
        path = parsed_url.path
        file_extension = path.split('.')[-1] if '.' in path else None
        file_type = file_extension.lower() if file_extension else None

    if file_type not in allowed_file_types:
        return JSONResponse(
            content='Невозможно загрузить выбранный тип файла',
            status_code=400
        )

    if await DocumentsDAO.create(
        name=name,
        url=url,
        file_type=file_type
    ):
        return JSONResponse(
            content={'message': 'Файл успешно создан', 'file_type': file_type},
            status_code=201
        )
    else:
        return JSONResponse(
            content={'message': 'Файл не был создан'},
            status_code=500
        )