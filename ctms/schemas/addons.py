from datetime import date, datetime, timezone
from typing import Optional

from pydantic import UUID4, Field, validator

from .base import ComparableBase
from .email import EMAIL_ID_DESCRIPTION, EMAIL_ID_EXAMPLE


class AddOnsBase(ComparableBase):
    """
    The addons.mozilla.org (AMO) data for a contact.

    Extra info in Basket:
    * amo_deleted - True if the user was deleted in AMO. Basket also sets
        the amo_id to null on deletion.

    All are in basket's IGNORE_USER_FIELDS, and usually stripped from
    contact data on the return from Salesforce.
    """

    add_on_ids: Optional[str]
    display_name: Optional[str]
    email_opt_in: bool = False
    language: Optional[str]
    last_login: Optional[date]
    location: Optional[str]
    profile_url: Optional[str]
    user: bool = False
    user_id: Optional[str]
    username: Optional[str]

    class Config:
        orm_mode = True
        fields = {
            "add_on_ids": {
                "description": "Comma-separated list of add-ons for account, AMO_Add_On_ID_s__c in Salesforce",
                "example": "add-on-1,add-on-2",
            },
            "display_name": {
                "max_length": 255,
                "description": "Display name on AMO, AMO_Display_Name__c in Salesforce",
                "example": "Add-ons Author",
            },
            "email_opt_in": {
                "description": "Account has opted into emails, AMO_Email_Opt_In__c in Salesforce",
            },
            "language": {
                "max_length": 5,
                "description": "Account language, AMO_Language__c in Salesforce",
                "example": "en",
            },
            "last_login": {
                "description": "Last login date on addons.mozilla.org, AMO_Last_Login__c in Salesforce",
                "example": "2021-01-28",
            },
            "location": {
                "max_length": 255,
                "description": "Free-text location on AMO, AMO_Location__c in Salesforce",
                "example": "California",
            },
            "profile_url": {
                "max_length": 40,
                "description": "AMO profile URL, AMO_Profile_URL__c in Salesforce",
                "example": "firefox/user/98765",
            },
            "user": {
                "description": "True if user is from an Add-on sync, AMO_User__c in Salesforce",
                "example": True,
            },
            "user_id": {
                "max_length": 40,
                "description": "User ID on AMO, AMO_User_ID__c in Salesforce",
                "example": "98765",
            },
            "username": {
                "max_length": 100,
                "description": "Username on AMO, AMO_Username__c in Salesforce",
                "example": "AddOnAuthor",
            },
        }


# No need to change anything, just extend if you want to
AddOnsInSchema = AddOnsBase


class UpdatedAddOnsInSchema(AddOnsInSchema):
    update_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    class Config:
        fields = {
            "update_timestamp": {
                "description": "AMO data update timestamp",
                "example": "2021-01-28T21:26:57.511Z",
            }
        }


class AddOnsSchema(AddOnsBase):
    create_timestamp: Optional[datetime]
    update_timestamp: Optional[datetime]

    class Config:
        fields = {
            "create_timestamp": {
                "description": "AMO data creation timestamp",
                "example": "2020-12-05T19:21:50.908000+00:00",
            },
            "update_timestamp": {
                "description": "AMO data update timestamp",
                "example": "2021-02-04T15:36:57.511000+00:00",
            },
        }


class AddOnsTableSchema(AddOnsSchema):

    email_id: UUID4
    create_timestamp: datetime
    update_timestamp: datetime

    @validator("last_login", pre=True)
    def convert_from_empty(cls, value):  # pylint:disable = E0213
        if isinstance(value, str):
            if not value:
                return None
        return value

    class Config:
        extra = "forbid"
        fields = {
            "email": {
                "description": EMAIL_ID_DESCRIPTION,
                "example": EMAIL_ID_EXAMPLE,
            },
        }
