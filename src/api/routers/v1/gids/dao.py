from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy import Column, Integer, String
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, 
    DateTime, Float, ForeignKey, JSON, TEXT
)
from sqlalchemy.dialects.mysql import BIGINT

from core.database import Base, async_session_maker
from dao.base import BaseDAO

from .models import ContactPoint, HistoryItem, AdditionalInfo, License, Contact

class Gids(Base):
    __tablename__ = 'gids'

    g_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(255), primary_key=True, index=True)
    fullName = Column(String(255))
    photoProfile = Column(TEXT)
    category = Column(String(255))
    license = Column(JSON)
    tags = Column(JSON)
    contacts = Column(JSON)
    routes = Column(JSON)
    additionalInfo = Column(JSON)
    history = Column(JSON)

    def __repr__(self):
        return f"<Gid(id={self.id}, fullName={self.fullName}, phone={self.contacts['phone']})>"

class GidsDAO(BaseDAO):
    model = Gids

    @classmethod
    async def get_all(cls) -> dict | None:
        """
        Получает всех экскурсоводов
        """
        query = select(
            Gids.id, 
            Gids.fullName, 
            Gids.photoProfile, 
            Gids.category,
            Gids.license,
            Gids.tags,
            Gids.contacts,
            Gids.routes,
            Gids.additionalInfo,
            Gids.history,
        )

        async with async_session_maker() as session:
            result = await session.execute(query)
            users = result.fetchall()
            
            if not users:
                return None

            return [
                {
                    'id': row.id,
                    'fullName': row.fullName,
                    'photoProfile': row.photoProfile,
                    'category': row.category,
                    'license': row.license,
                    'tags': row.tags,
                    'contacts': row.contacts,
                    'routes': row.routes,
                    'additionalInfo': row.additionalInfo,
                    'history': row.history
                }
                for row in users
            ]

    @classmethod
    async def get_by_id(cls, gid_id: str) -> dict | None:
        """
        Получает экскурсовода по ID
        """
        query = select(
            Gids.id, 
            Gids.fullName, 
            Gids.photoProfile, 
            Gids.category,
            Gids.license,
            Gids.tags,
            Gids.contacts,
            Gids.routes,
            Gids.additionalInfo,
            Gids.history,
        ).where(Gids.id == gid_id)

        async with async_session_maker() as session:
            result = await session.execute(query)
            user = result.fetchone()

            if not user:
                return None

            return {
                'id': user.id,
                'fullName': user.fullName,
                'photoProfile': user.photoProfile,
                'category': user.category,
                'license': user.license,
                'tags': user.tags,
                'contacts': user.contacts,
                'routes': user.routes,
                'additionalInfo': user.additionalInfo,
                'history': user.history
            }
        
    @classmethod
    async def create(
        cls, 
        id: str, 
        full_name: str, 
        photo_profile: str, 
        category: str, 
        license: License, 
        tags: List[str], 
        contacts: Contact, 
        routes: List[ContactPoint], 
        additional_info: AdditionalInfo, 
        history: List[HistoryItem]
    ) -> dict:
        """
        Создает нового экскурсовода
        """
        license_dict = license.dict()
        if 'issueDate' in license_dict and isinstance(license_dict['issueDate'], datetime):
            license_dict['issueDate'] = license_dict['issueDate'].strftime('%Y-%m-%d %H:%M:%S')

        new_gid = Gids(
            id=id,
            fullName=full_name,
            photoProfile=photo_profile,
            category=category,
            license=license_dict, 
            tags=tags,
            contacts=contacts.dict(),
            routes=[route.dict() for route in routes],
            additionalInfo=additional_info.dict(),
            history=[item.dict() for item in history]
        )

        async with async_session_maker() as session:
            session.add(new_gid)
            await session.commit()

        return {
            'id': new_gid.id,
            'fullName': new_gid.fullName,
            'photoProfile': new_gid.photoProfile,
            'category': new_gid.category,
            'license': new_gid.license,
            'tags': new_gid.tags,
            'contacts': new_gid.contacts,
            'routes': new_gid.routes,
            'additionalInfo': new_gid.additionalInfo,
            'history': new_gid.history
        }