from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import UUID4, Field, HttpUrl

from .base import ComparableBase
from .email import EMAIL_ID_DESCRIPTION, EMAIL_ID_EXAMPLE


class NewsletterBase(ComparableBase):
    """The newsletter subscriptions schema."""

    name: str
    subscribed: bool = True
    format: Literal["H", "T"] = "H"
    lang: Optional[str] = "en"
    source: Optional[HttpUrl]
    unsub_reason: Optional[str]

    def __lt__(self, other):
        return self.name < other.name

    class Config:
        orm_mode = True
        fields = {
            "name": {
                "description": "Basket slug for the newsletter",
                "example": "mozilla-welcome",
            },
            "subscribed": {
                "description": "True if subscribed, False when formerly subscribed",
            },
            "format": {"description": "Newsletter format, H=HTML, T=Plain Text"},
            "lang": {
                "min_length": 2,
                "max_length": 5,
                "description": "Newsletter language code, usually 2 lowercase letters",
            },
            "source": {
                "description": "Source URL of subscription",
                "example": "https://www.mozilla.org/en-US/",
            },
            "unsub_reason": {
                "description": "Reason for unsubscribing",
            },
        }


# No need to change anything, just extend if you want to
NewsletterInSchema = NewsletterBase
NewsletterSchema = NewsletterBase


class UpdatedNewsletterInSchema(NewsletterInSchema):
    update_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Config:
        fields = {
            "update_timestamp": {
                "description": "Newsletter subscription data update timestamp",
                "example": "2021-01-28T21:26:57.511Z",
            }
        }


class NewsletterTableSchema(NewsletterBase):
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
                "description": "Newsletter subscription data creation timestamp",
                "example": "2020-12-05T19:21:50.908000+00:00",
            },
            "update_timestamp": {
                "description": "Newsletter subscription data update timestamp",
                "example": "2021-01-28T21:26:57.511Z",
            },
        }
