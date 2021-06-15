from datetime import datetime, timezone
from typing import Optional

from pydantic import UUID4, Field

from .base import ComparableBase
from .email import EMAIL_ID_DESCRIPTION, EMAIL_ID_EXAMPLE


class VpnWaitlistBase(ComparableBase):
    """
    The Mozilla VPN Waitlist schema.

    This was previously the Firefox Private Network (fpn) waitlist data,
    with a similar purpose.
    """

    geo: Optional[str]
    platform: Optional[str]

    class Config:
        orm_mode = True
        fields = {
            "geo": {
                "max_length": 100,
                "description": "VPN waitlist country, FPN_Waitlist_Geo__c in Salesforce",
                "example": "fr",
            },
            "platform": {
                "max_length": 100,
                "description": (
                    "VPN waitlist platforms as comma-separated list,"
                    " FPN_Waitlist_Platform__c in Salesforce"
                ),
                "example": "ios,mac",
            },
        }


# No need to change anything, just extend if you want to
VpnWaitlistInSchema = VpnWaitlistBase
VpnWaitlistSchema = VpnWaitlistBase


class UpdatedVpnWaitlistInSchema(VpnWaitlistInSchema):
    update_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Config:
        fields = {
            "update_timestamp": {
                "description": "VPN Waitlist data update timestamp",
                "example": "2021-01-28T21:26:57.511Z",
            }
        }


class VpnWaitlistTableSchema(VpnWaitlistBase):
    email_id: UUID4
    create_timestamp: datetime
    update_timestamp: datetime

    class Config:
        extra = "forbid"
        fields = {
            "email_id": {
                "description": EMAIL_ID_DESCRIPTION,
                "example": EMAIL_ID_EXAMPLE,
            },
            "create_timestamp": {
                "description": "VPN Waitlist data creation timestamp",
                "example": "2020-12-05T19:21:50.908000+00:00",
            },
            "update_timestamp": {
                "description": "VPN Waitlist data update timestamp",
                "example": "2021-02-04T15:36:57.511000+00:00",
            },
        }
