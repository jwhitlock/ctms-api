"""
Implement OAuth2 client credentials.

A backend client POSTs to the /token endpoint, sending client_id and
client_secret, either as form fields in the body, or in the Authentication
header. A JWT token is returned, that expires after a short time. To renew,
the client POSTs to /token again.

See:
* https://github.com/tiangolo/fastapi/issues/774
* https://github.com/tiangolo/fastapi/blob/c09e950bd2efb81f82931469bee6856c72e54357/fastapi/security/oauth2.py
* https://tools.ietf.org/html/rfc6749
"""
from datetime import datetime, timedelta
from typing import Dict, Optional

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi.security.oauth2 import OAuth2, OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password):
    return pwd_context.hash(plain_password)


def create_access_token(
    data: dict,
    expires_delta: timedelta,
    secret_key: str,
    algorithm: str,
    now: Optional[datetime] = None,
) -> str:
    """Create a JWT string to act as an OAuth2 access token."""
    to_encode = data.copy()
    expire = (now or datetime.utcnow()) + expires_delta
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_name_from_token(token: str, secret_key: str, algorithm: str):
    """Get the API client name from a token.

    Returns None if the token is invalid, or payload is expired or invalid.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithm)
    except JWTError:
        return None
    return payload["sub"]


class OAuth2ClientCredentialsRequestForm:
    """
    This is a dependency class, use it like:
        @app.post("/login")
        def login(form_data: OAuth2ClientCredentialsRequestForm = Depends()):
            data = form_data.parse()
            print(data.client_id)
            for scope in data.scopes:
                print(scope)
            return data

    It creates the following Form request parameters in your endpoint:
    grant_type: the OAuth2 spec says it is required and MUST be the fixed string "client_credentials".
        Nevertheless, this dependency class is permissive and allows not passing it.
    scope: Optional string. Several scopes (each one a string) separated by spaces. Currently unused.
    client_id: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    client_secret: optional string. OAuth2 recommends sending the client_id and client_secret (if any)
        using HTTP Basic auth, as: client_id:client_secret
    """

    def __init__(
        self,
        grant_type: str = Form(None, regex="client_credentials"),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


class OAuth2ClientCredentials(OAuth2):
    """Implement OAuth2 client_credentials workflow."""

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes}
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
