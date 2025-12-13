import requests
from authlib.integrations.requests_client import OAuth2Session
from pydantic import BaseModel


class Auth:

    def getSession(self) -> requests.Session:
        raise NotImplemented


class AccessTokenAuth(Auth):

    def __init__(self, token: str) -> None:
        super().__init__()

        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def getSession(self) -> requests.Session:
        return self.session


class OAuthClientAuth(Auth):

    def __init__(
        self,
        scope: str,
        clientId: str,
        clientSecret: str,
        tokenEndpoint: str,
    ) -> None:
        super().__init__()

        self.session = OAuth2Session(
            clientId,
            clientSecret,
            scope=scope,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        self.session.fetch_token(tokenEndpoint)

    def getSession(self) -> requests.Session:
        return self.session


class API:

    def __init__(
        self,
        fqdn: str,
        auth: Auth,
        insecure: bool = False,
    ) -> None:
        self.baseURL = f"http{"s" if not insecure else ""}://{fqdn}/api"

        self.session: requests.Session = auth.getSession()

    def __del__(self) -> None:
        self.session.close()

    @staticmethod
    def handleResponse(response: requests.Response) -> tuple[bool, dict]:
        if response.status_code in (200, 201):
            return True, response.json()["data"]
        elif response.status_code == 204:
            return True, {}
        else:
            raise RuntimeError(response.json())

    def get(self, endpoint: str) -> dict:
        response: requests.Response = self.session.get(f"{self.baseURL}/{endpoint}")
        return API.handleResponse(response)[1]

    def update(self, endpoint: str, data: BaseModel) -> dict:
        response: requests.Response = self.session.patch(
            f"{self.baseURL}/{endpoint}",
            json=data.model_dump(exclude_none=True, exclude_defaults=True),
        )
        return API.handleResponse(response)[1]

    def delete(self, endpoint: str, force: bool = False, cascade: bool = False) -> bool:
        if not force and cascade:
            raise ValueError("Cascade can only be true when force is also true")
        parameters = ""
        if force:
            parameters += "?force=true"
            if cascade:
                parameters += "&cascade=true"
        response: requests.Response = self.session.delete(
            f"{self.baseURL}/{endpoint}{parameters}",
        )
        return API.handleResponse(response)[0]

    def add(self, endpoint: str, data: BaseModel) -> dict:
        response: requests.Response = self.session.post(
            f"{self.baseURL}/{endpoint}",
            json=data.model_dump(exclude_none=True, exclude_defaults=True),
        )
        return API.handleResponse(response)[1]
