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


class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    url = Column(TEXT)
    file_type = Column(String(10))


    def __repr__(self):
        return f'<Documents(id={self.id}, name={self.name}, url={self.url}, file_type={self.file_type})>'

class DocumentsDAO(BaseDAO):
    model = Documents

    @classmethod
    async def get_all(cls) -> dict | None:
        """
        Получает все файлы
        """
        query = select(
            Documents.id, 
            Documents.name, 
            Documents.url, 
            Documents.file_type,
        )

        async with async_session_maker() as session:
            result = await session.execute(query)
            users = result.fetchall()
            
            if not users:
                return None

            return [
                {
                    'id': row.id,
                    'name': row.name,
                    'url': row.url,
                    'file_type': row.file_type
                }
                for row in users
            ]
        
    @classmethod
    async def create(
        cls, 
        name: str, 
        url: str, 
        file_type: str 
    ) -> dict:
        """
        Создание документа
        """
        new_file = Documents(
            name=name,
            url=url,
            file_type=file_type
        )

        async with async_session_maker() as session:
            session.add(new_file)
            await session.commit()

        return {
            'id': new_file.id,
            'name': new_file.name,
            'url': new_file.url,
            'file_type': new_file.file_type
        }