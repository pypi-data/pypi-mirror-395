import httpx
from typing import Optional

class AuthAPI:
    def __init__(self, client: httpx.AsyncClient, token: str):
        self._client = client
        self.token = token

    async def generate_token(self, tg_id: int):
        params = {
            "token": self.token,
            "tg_id": tg_id,
        }
        response = await self._client.post("/auth/gen-token", params=params)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def get_user(self, tg_id: int):
        params = {
            "token": self.token,
            "tg_id": tg_id,
        }
        response = await self._client.get("/auth/get-user", params=params)
        response.raise_for_status()
        data = response.json()
        return data