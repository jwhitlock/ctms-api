from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr, Field, HttpUrl

from .addons import AddOnsSchema
from .email import EmailInSchema, EmailSchema
from .fxa import FirefoxAccountsSchema
from .newsletter import NewsletterSchema
from .vpn import VpnWaitlistSchema


class ContactSchema(BaseModel):
    """A complete contact."""

    amo: Optional[AddOnsSchema] = None
    email: EmailSchema
    fxa: Optional[FirefoxAccountsSchema] = None
    newsletters: List[NewsletterSchema] = Field(
        default=[],
        description="List of newsletters for which the contact is or was subscribed",
        example=([{"name": "firefox-welcome"}, {"name": "mozilla-welcome"}]),
    )
    vpn_waitlist: Optional[VpnWaitlistSchema] = None

    def as_identity_response(self) -> "IdentityResponse":
        """Return the identities of a contact"""
        return IdentityResponse(
            amo_user_id=getattr(self.amo, "user_id", None),
            basket_token=getattr(self.email, "basket_token", None),
            email_id=getattr(self.email, "email_id", None),
            fxa_id=getattr(self.fxa, "fxa_id", None),
            fxa_primary_email=getattr(self.fxa, "primary_email", None),
            mofo_id=getattr(self.email, "mofo_id", None),
            primary_email=getattr(self.email, "primary_email", None),
            sfdc_id=getattr(self.email, "sfdc_id", None),
        )


class ContactInSchema(BaseModel):
    """A contact as provided by callers."""

    amo: Optional["AddOnsSchema"] = None
    email: "EmailInSchema"
    fxa: Optional["FirefoxAccountsSchema"] = None
    newsletters: List["NewsletterSchema"] = Field(
        default=[],
        description="List of newsletters for which the contact is or was subscribed",
        example=([{"name": "firefox-welcome"}, {"name": "mozilla-welcome"}]),
    )
    vpn_waitlist: Optional["VpnWaitlistSchema"] = None


class CTMSResponse(BaseModel):
    """
    Response for /ctms/<email_id>

    Similar to ContactSchema, but groups are required and includes status: OK
    """

    amo: AddOnsSchema
    email: EmailSchema
    fxa: FirefoxAccountsSchema
    newsletters: List[NewsletterSchema]
    status: Literal["ok"] = Field(
        default="ok", description="Request was successful", example="ok"
    )
    vpn_waitlist: VpnWaitlistSchema


class IdentityResponse(BaseModel):
    """The identity keys for a contact."""

    email_id: UUID
    primary_email: EmailStr
    basket_token: UUID
    sfdc_id: Optional[str] = None
    mofo_id: Optional[str] = None
    amo_user_id: Optional[str] = None
    fxa_id: Optional[str] = None
    fxa_primary_email: Optional[EmailStr] = None
