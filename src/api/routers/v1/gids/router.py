from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException, status, Body
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from core.auth import verify_user

from .dao import GidsDAO
from .models import GidCreateRequest


router = APIRouter(
    prefix='/gids',
    tags=['Gids']
)

db = {
    'U191KK': {
        'id': 'U191KK',
        'fullName': 'Абанос Астамур Русланович',
        'photoProfile': 'https://img.freepik.com/free-photo/close-up-shot-serious-looking-handsome-adult-european-man-with-red-hair-beard-staring-with-focused-determined-expression-standing-strict-pose-gray-wall_176420-27574.jpg?t=st=1743933775~exp=1743937375~hmac=962096c06812fd48366a04e537080bd062975393b7bbb4e4ffa8a6d8f81c2b19&w=996',
        'category': 'Первая категория',
        'license': {
            'number': '№ 8368 от 03.10.2022 г.',
            'issuingAuthority': 'Министерство туризма Республики Абхазия',
            'issueDate': '05.10.2022',
            'status': 'Отозвана'
        },
        'tags': ['Исторические экскурсии', 'Природные маршруты'],
        'contacts': {
            'phone': '7940-997-09-79',
            'email': '',
            'address': ''
        },
        'routes': [
            {
                'id': 1,
                'name': 'Основной маршрут',
                'groupNumber': '№ в группе: 1',
                'points': [
                    'пос. Гячрыпш',
                    'г. Гагра',
                    'г. Пицунда',
                    'оз. Рица',
                    'г. Н. Афон',
                    'пос. Гячрыпш'
                ]
            }
        ],
        'additionalInfo': {
            'inn': '123456789012',
            'examType': 'Очный (теория + практика)',
            'entityType': 'Физическое лицо'
        },
        'history': [
            { 'date': '12.07.2023', 'action': 'Добавлен в реестр' },
            { 'date': '15.08.2023', 'action': 'Номер телефона обновлён' },
            { 'date': '20.09.2023', 'action': 'ФИО было обновлено' },
            { 'date': '01.10.2023', 'action': 'Добавлен новый маршрут' }
        ]
    }
}

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    description='Гид/Экскурсовод'
)
async def get_gid(
    id: str = Query(..., description='ID Пользователя')
) -> JSONResponse:
    try:
        gid_data = await GidsDAO.get_by_id(gid_id=id)
        
        for key, value in gid_data.items():
            if isinstance(value, datetime):
                gid_data[key] = value.isoformat()
            elif isinstance(value, dict):  
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, datetime):
                        value[sub_key] = sub_value.isoformat()

    except Exception:
        gid_data = {
            'error': 'not_found'
        }

    return JSONResponse(
        content=gid_data # db[id]
    )


@router.get(
    path='/all',
    status_code=status.HTTP_200_OK,
    description='Гиды/Экскурсоводы'
)
async def get_gids() -> JSONResponse:
    response = await GidsDAO.get_all()

    gids = [
        {
            'id': value['id'],
            'name': value['fullName'],
            'phone': value['contacts']['phone']
        }
        for value in response
    ]
    return JSONResponse(content=gids)


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    description='Создать экскурсовода',
    dependencies=[Depends(verify_user)]
)
async def create_gid(gid: GidCreateRequest) -> JSONResponse:
    """Создание нового экскурсовода"""
    try:
        created_gid = await GidsDAO.create(
            id=gid.id,
            full_name=gid.fullName,
            photo_profile=gid.photoProfile,
            category=gid.category,
            license=gid.license, 
            tags=gid.tags,
            contacts=gid.contacts,
            routes=gid.routes,
            additional_info=gid.additionalInfo,
            history=gid.history
        )
        return JSONResponse(content=created_gid, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при создании экскурсовода'
        )