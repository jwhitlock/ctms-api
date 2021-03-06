from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID, uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field, HttpUrl


class FirefoxAccountsSchema(BaseModel):
    """The Firefox Account schema."""

    fxa_id: Optional[str] = Field(
        default=None,
        description="Firefox Accounts foreign ID, FxA_Id__c in Salesforce",
        max_length=50,
        example="6eb6ed6ac3b64259968aa490c6c0b9df",  # pragma: allowlist secret
    )
    primary_email: Optional[EmailStr] = Field(
        default=None,
        description="FxA Email, can be foreign ID, FxA_Primary_Email__c in Salesforce",
        example="my-fxa-acct@example.com",
    )
    created_date: Optional[str] = Field(
        default=None,
        description="Source is unix timestamp, FxA_Created_Date__c in Salesforce",
        example="2021-01-29T18:43:49.082375+00:00",
    )
    lang: Optional[str] = Field(
        default=None,
        max_length=255,
        description="FxA Locale (from browser Accept-Language header), FxA_Language__c in Salesforce",
        example="en,en-US",
    )
    first_service: Optional[str] = Field(
        default=None,
        max_length=50,
        description="First service that an FxA user used, FirstService__c in Salesforce",
        example="sync",
    )
    account_deleted: bool = Field(
        default=False,
        description=(
            "Set to True when FxA account deleted or dupe,"
            " FxA_Account_Deleted__c in Salesforce"
        ),
    )

    class Config:
        orm_mode = True
