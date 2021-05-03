from datetime import datetime, timezone
from typing import Optional

from pydantic import UUID4, Field

from .base import ComparableBase
from .email import EMAIL_ID_DESCRIPTION, EMAIL_ID_EXAMPLE


class FirefoxAccountsBase(ComparableBase):
    """The Firefox Account schema."""

    fxa_id: Optional[str] = None
    primary_email: Optional[str] = None
    created_date: Optional[str] = None
    lang: Optional[str] = None
    first_service: Optional[str] = None
    account_deleted: bool = False

    class Config:
        orm_mode = True
        fields = {
            "fxa_id": {
                "description": "Firefox Accounts foreign ID, FxA_Id__c in Salesforce",
                "max_length": 50,
                "example": "6eb6ed6ac3b64259968aa490c6c0b9df",  # pragma: allowlist secret
            },
            "primary_email": {
                "description": "FxA Email, can be foreign ID, FxA_Primary_Email__c in Salesforce",
                "example": "my-fxa-acct@example.com",
            },
            "created_date": {
                "description": "Source is unix timestamp, FxA_Created_Date__c in Salesforce",
                "example": "2021-01-29T18:43:49.082375+00:00",
            },
            "lang": {
                "description": "FxA Locale (from browser Accept-Language header), FxA_Language__c in Salesforce",
                "example": "en,en-US",
            },
            "first_service": {
                "description": "First service that an FxA user used, FirstService__c in Salesforce",
                "max_length": 50,
                "example": "sync",
            },
            "account_deleted": {
                "description": "Set to True when FxA account deleted or dupe, FxA_Account_Deleted__c in Salesforce",
            },
        }


# No need to change anything, just extend if you want to
FirefoxAccountsInSchema = FirefoxAccountsBase
FirefoxAccountsSchema = FirefoxAccountsBase


class UpdatedFirefoxAccountsInSchema(FirefoxAccountsInSchema):
    update_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Config:
        fields = {
            "update_timestamp": {
                "description": "FxA data update timestamp",
                "example": "2021-01-28T21:26:57.511Z",
            }
        }


class FirefoxAccountsTableSchema(FirefoxAccountsBase):
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
                "description": "FxA data creation timestamp",
                "example": "2020-12-05T19:21:50.908000+00:00",
            },
            "update_timestamp": {
                "description": "FxA data update timestamp",
                "example": "2021-02-04T15:36:57.511000+00:00",
            },
        }
