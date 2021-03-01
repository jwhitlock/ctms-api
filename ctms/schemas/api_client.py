from pydantic import BaseModel, EmailStr


class ApiClientSchema(BaseModel):
    """An OAuth2 Client"""

    name: str
    email: EmailStr
    enabled: bool
