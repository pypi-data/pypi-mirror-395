from datetime import datetime
from virtualitics_sdk.persistence_client.internal.auth.virtualitics_jwt import get_auth_headers_from_jwt as get_auth_headers_from_jwt, is_jwt_expired as is_jwt_expired
from virtualitics_sdk.persistence_client.internal.enums.authentication_mode import AuthenticationMode as AuthenticationMode

class CredentialProvider:
    """
    A CredentialProvider object is held by the PersistenceClient and authenticates
    each request that is sent by the client to the server
    """
    auth_mode: str
    jwt_string: str
    timestamp: datetime
    def __init__(self, jwt_string: str = None) -> None:
        """
        Pass in a JWT to use for authentication. In the future
        other constructors for other modes of authentication could
        be used.
        """
    def to_http_headers(self, request) -> dict[str, str]:
        """Takes the information stored in this object and builds the headers for the request"""
