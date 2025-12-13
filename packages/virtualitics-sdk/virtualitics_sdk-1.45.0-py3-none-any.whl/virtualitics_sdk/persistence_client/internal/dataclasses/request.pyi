import httpx
from dataclasses import dataclass
from virtualitics_sdk.persistence_client.internal.auth.credential_provider import CredentialProvider as CredentialProvider
from virtualitics_sdk.persistence_client.internal.enums.method import Method as Method
from virtualitics_sdk.persistence_client.internal.enums.request_type import RequestType as RequestType, get_route_and_method_info as get_route_and_method_info

@dataclass
class PersistenceRequest:
    """Contains all the information needed to send a HTTP request to the persistence server."""
    method: Method
    route: str
    params: dict
    headers: dict
    data: dict
    files: dict
    json: dict
    credential_provider: CredentialProvider
    def send(self, client: httpx.Client) -> httpx.Response:
        """
        Sends the request to the persistence server. Puts in all necessary
        data for the request and uses the synchronous httpx client to send it over.
        :param client: the client that is stored by PersistenceClient to send requests
        """
    async def send_async(self, async_client: httpx.AsyncClient) -> httpx.Response:
        """
        Sends the request to the persistence server. Puts in all necessary
        data for the request and uses the async_client to send it over.
        :param async_client: the async client that is stored by PersistenceClient to send requests
        """
    request_type = ...
    def __init__(self, request_type: RequestType, credential_provider: CredentialProvider, request_data) -> None:
        """
        Extracts request_type, credential_provider, and request_data to build the 
        necessary fields to send an http request.
        :param request_type: Enum of the 6 possible API requests we can send to Persistence. Used for route and method
        :param credential_provider: Holds authentication information and uses to_http_headers to get headers for the request
        :param request_data: The parameters for the specific request
        """
