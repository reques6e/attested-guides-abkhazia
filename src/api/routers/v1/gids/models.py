from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class License(BaseModel):
    number: str | None
    issuingAuthority: str | None
    issueDate: datetime | None
    status: str | None

class ContactPoint(BaseModel):
    id: int | None
    name: str | None
    groupNumber: str | None
    points: List[str] | None

class Contact(BaseModel):
    phone: str | None
    email: Optional[str] = ''
    address: Optional[str] = ''

class AdditionalInfo(BaseModel):
    inn: str | None
    examType: str | None
    entityType: str | None

class HistoryItem(BaseModel):
    date: str | None
    action: str | None

class GidCreateRequest(BaseModel):
    id: str
    fullName: str = Field(..., alias='fullName')
    photoProfile: str = Field(..., alias='photoProfile')
    category: str | None
    license: License
    tags: List[str]
    contacts: Contact
    routes: List[ContactPoint]
    additionalInfo: AdditionalInfo = Field(..., alias='additionalInfo')
    history: List[HistoryItem]

    class Config:
        allow_population_by_field_name = True