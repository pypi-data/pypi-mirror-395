import httpx
from typing import Optional

from .api.auth.api import AuthAPI
from .api.modules.api import ModulesAPI
from .api.checker.api import CheckerAPI
from .api.logger.api import LoggerAPI
from .api.repos.api import ReposAPI

class GoidaHetaAPIClient:
    API_PREFIX = "/api/v1"
    def __init__(self, base_url: str, token: str = ""):
        cleaned_url = base_url.rstrip('/')
        if not cleaned_url.endswith(self.API_PREFIX):
            self.base_url = cleaned_url + self.API_PREFIX
        else:
            self.base_url = cleaned_url
        self.client = httpx.AsyncClient(base_url=self.base_url)
        self.token = token
        if not self.token:
            raise ValueError("Token required!")
        self.auth = AuthAPI(self.client, token=self.token)
        self.checker = CheckerAPI(self.client, token=self.token)
        self.modules = ModulesAPI(self.client, token=self.token)
        self.logger = LoggerAPI(self.client, token=self.token)
        self.repos = ReposAPI(self.client,token=self.token)