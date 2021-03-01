from .addons import AddOnsSchema
from .api_client import ApiClientSchema
from .contact import ContactInSchema, ContactSchema, CTMSResponse, IdentityResponse
from .email import EmailInSchema, EmailSchema
from .fxa import FirefoxAccountsSchema
from .newsletter import NewsletterSchema
from .vpn import VpnWaitlistSchema
from .web import (
    BadRequestResponse,
    NotFoundResponse,
    TokenResponse,
    UnauthorizedResponse,
)
