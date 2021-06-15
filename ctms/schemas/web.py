from pydantic import BaseModel


class BadRequestResponse(BaseModel):
    """The client called the endpoint incorrectly."""

    detail: str

    class Config:
        fields = {
            "detail": {
                "description": "A human-readable summary of the client error.",
                "example": "No identifiers provided, at least one is needed.",
            }
        }


class NotFoundResponse(BaseModel):
    """No existing record was found for the indentifier."""

    detail: str

    class Config:
        fields = {
            "detail": {
                "description": "A human-readable summary of the client error.",
                "example": "Unknown contact_id",
            }
        }


class TokenResponse(BaseModel):
    """An OAuth2 Token response."""

    access_token: str
    token_type: str
    expires_in: int


class UnauthorizedResponse(BaseModel):
    """Client authorization failed."""

    detail: str

    class Config:
        fields = {
            "detail": {
                "description": "A human-readable summary of the client error.",
                "example": "Not authenticated",
            }
        }
