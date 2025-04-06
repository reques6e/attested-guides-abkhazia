from pydantic import BaseModel
from datetime import datetime

class GidCreateRequest(BaseModel):
    id: str
    full_name: str
    photo_profile: str
    category: str
    license_number: str
    license_issuingAuthority: str
    license_issueDate: datetime
    license_status: str
    tags: dict
    contacts: dict
    routes: dict
    additional_info: dict
    history: dict