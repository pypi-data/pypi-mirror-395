import json

def parse_jwt(jwt_string: str) -> json:
    """Converts JWT to unverified json data"""
def get_auth_headers_from_jwt(jwt_string: str) -> dict:
    """
    Pulls the user_id and org_id from the jwt. We dont
    need to verify since the server also has the JWT and
    will verify that the token hasnt been modified
    """
def is_jwt_expired(token_string: str) -> bool:
    """Checks if a JWT has expired without verifying its signature."""
