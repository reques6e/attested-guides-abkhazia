from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy import Column, Integer, String
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, 
    DateTime, Float, ForeignKey, JSON, TEXT
)
from sqlalchemy.dialects.mysql import BIGINT

from core.database import Base, async_session_maker
from dao.base import BaseDAO


class Gids(Base):
    __tablename__ = 'gids'

    g_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(255), primary_key=True, index=True)
    fullName = Column(String(255))
    photoProfile = Column(TEXT)
    category = Column(String(255))
    license_number = Column(String(255))
    license_issuingAuthority = Column(String(255))
    license_issueDate = Column(DateTime)
    license_status = Column(String(255))
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
            Gids.license_number,
            Gids.license_issuingAuthority,
            Gids.license_issueDate,
            Gids.license_status,
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
                    'license': {
                        'number': row.license_number,
                        'issuingAuthority': row.issuingAuthority,
                        'issueDate': row.license_issueDate,
                        'status': row.license_status
                    },
                    # 'license_number': row.license_number,
                    # 'license_issuingAuthority': row.license_issuingAuthority,
                    # 'license_issueDate': row.license_issueDate,
                    # 'license_status': row.license_status,
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
            Gids.license_number,
            Gids.license_issuingAuthority,
            Gids.license_issueDate,
            Gids.license_status,
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
                'license': {
                    'number': user.license_number,
                    'issuingAuthority': user.license_issuingAuthority,
                    'issueDate': user.license_issueDate,
                    'status': user.license_status
                },
                # 'license_number': user.license_number,
                # 'license_issuingAuthority': user.license_issuingAuthority,
                # 'license_issueDate': user.license_issueDate,
                # 'license_status': user.license_status,
                'tags': user.tags,
                'contacts': user.contacts,
                'routes': user.routes,
                'additionalInfo': user.additionalInfo,
                'history': user.history
            }
        
    @classmethod
    async def create(
        cls, id: str, full_name: str, photo_profile: str, category: str, license_number: str, 
        license_issuingAuthority: str, license_issueDate: str, license_status: str,
        tags: dict, contacts: dict, routes: dict, additional_info: dict, history: dict) -> dict:
        """
        Создает нового экскурсовода
        """

        license_issueDate_str = license_issueDate.strftime('%Y-%m-%d %H:%M:%S')

        new_gid = Gids(
            id=id,
            fullName=full_name,
            photoProfile=photo_profile,
            category=category,
            license_number=license_number,
            license_issuingAuthority=license_issuingAuthority,
            license_issueDate=license_issueDate_str,
            license_status=license_status,
            tags=tags,
            contacts=contacts,
            routes=routes,
            additionalInfo=additional_info,
            history=history
        )

        async with async_session_maker() as session:
            session.add(new_gid)
            await session.commit()

        return {
            'id': new_gid.id,
            'fullName': new_gid.fullName,
            'photoProfile': new_gid.photoProfile,
            'category': new_gid.category,
            'license_number': new_gid.license_number,
            'license_issuingAuthority': new_gid.license_issuingAuthority,
            'license_issueDate': new_gid.license_issueDate,
            'license_status': new_gid.license_status,
            'tags': new_gid.tags,
            'contacts': new_gid.contacts,
            'routes': new_gid.routes,
            'additionalInfo': new_gid.additionalInfo,
            'history': new_gid.history
        }