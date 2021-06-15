from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import UUID

from pydantic import UUID4, Field, validator

from .base import ComparableBase

EMAIL_ID_DESCRIPTION = "ID for email"
EMAIL_ID_EXAMPLE = "332de237-cab7-4461-bcc3-48e68f42bd5c"


class EmailBase(ComparableBase):
    """Data that is included in input/output/db of a primary_email and such."""

    primary_email: str
    basket_token: Optional[UUID]
    double_opt_in: bool = False
    sfdc_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    mailing_country: Optional[str]
    email_format: Literal["H", "T", "N", ""] = "H"
    email_lang: Optional[str] = "en"
    has_opted_out_of_email: bool = False
    unsubscribe_reason: Optional[str]

    class Config:
        orm_mode = True
        fields = {
            "primary_email": {
                "description": "Contact email address, Email in Salesforce",
                "example": "contact@example.com",
            },
            "basket_token": {
                "description": "Basket token, Token__c in Salesforce",
                "example": "c4a7d759-bb52-457b-896b-90f1d3ef8433",
            },
            "double_opt_in": {
                "description": "User has clicked a confirmation link",
                "example": True,
            },
            "sfdc_id": {
                "max_length": 255,
                "description": "Salesforce legacy ID, Id in Salesforce",
                "example": "001A000023aABcDEFG",
            },
            "first_name": {
                "max_length": 255,
                "description": "First name of contact, FirstName in Salesforce",
                "example": "Jane",
            },
            "last_name": {
                "max_length": 255,
                "description": "Last name of contact, LastName in Salesforce",
                "example": "Doe",
            },
            "mailing_country": {
                "max_length": 255,
                "description": "Mailing country code, 2 lowercase letters, MailingCountryCode in Salesforce",
                "example": "us",
            },
            "email_format": {
                "description": "Email format, H=HTML, T=Plain Text, N and Empty=No selection, Email_Format__c in Salesforce",
            },
            "email_lang": {
                "max_length": 5,
                "description": "Email language code, usually 2 lowercase letters, Email_Language__c in Salesforce",
            },
            "has_opted_out_of_email": {
                "description": "User has opted-out, HasOptedOutOfEmail in Salesforce",
            },
            "unsubscribe_reason": {
                "description": "Reason for unsubscribing, in basket IGNORE_USER_FIELDS, Unsubscribe_Reason__c in Salesforce",
            },
        }


class EmailSchema(EmailBase):
    email_id: UUID4
    create_timestamp: Optional[datetime]
    update_timestamp: Optional[datetime]

    class Config:
        fields = {
            "email_id": {
                "description": EMAIL_ID_DESCRIPTION,
                "example": EMAIL_ID_EXAMPLE,
            },
            "create_timestamp": {
                "description": "Contact creation date, CreatedDate in Salesforce",
                "example": "2020-03-28T15:41:00.000Z",
            },
            "update_timestamp": {
                "description": "Contact last modified date, LastModifiedDate in Salesforce",
                "example": "2021-01-28T21:26:57.511Z",
            },
        }


class EmailTableSchema(EmailSchema):
    create_timestamp: datetime
    update_timestamp: datetime

    class Config:
        extra = "forbid"


class EmailInSchema(EmailBase):
    """Nearly identical to EmailPutSchema but the email_id is not required."""

    email_id: Optional[UUID4]

    class Config:
        fields = {
            "email_id": {
                "description": EMAIL_ID_DESCRIPTION,
                "example": EMAIL_ID_EXAMPLE,
            },
        }


class EmailPutSchema(EmailBase):
    """Nearly identical to EmailInSchema but the email_id is required."""

    email_id: UUID4

    class Config:
        fields = {
            "email_id": {
                "description": EMAIL_ID_DESCRIPTION,
                "example": EMAIL_ID_EXAMPLE,
            },
        }


class EmailPatchSchema(EmailInSchema):
    """Nearly identical to EmailInSchema but nothing is required."""

    primary_email: Optional[str]

    @validator("primary_email")
    @classmethod
    def prevent_none(cls, value):
        assert value is not None, "primary_email may not be None"
        return value


class UpdatedEmailPutSchema(EmailPutSchema):
    update_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        fields = {
            "update_timestamp": {
                "description": "Contact last modified date, LastModifiedDate in Salesforce",
                "example": "2021-01-28T21:26:57.511Z",
            },
        }
