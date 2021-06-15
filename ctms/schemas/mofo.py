from typing import Optional

from .base import ComparableBase


class MozillaFoundationBase(ComparableBase):

    mofo_email_id: Optional[str]
    mofo_contact_id: Optional[str]
    mofo_relevant: bool = False

    class Config:
        orm_mode = True
        fields = {
            "mofo_email_id": {
                "max_length": 255,
                "description": "Foriegn key to email in MoFo contact database",
            },
            "mofo_contact_id": {
                "max_length": 255,
                "description": "Foriegn key to contact in MoFo contact database",
            },
            "mofo_relevant": {
                "description": "Mozilla Foundation is tracking this email",
            },
        }


MozillaFoundationSchema = MozillaFoundationBase
MozillaFoundationInSchema = MozillaFoundationBase
