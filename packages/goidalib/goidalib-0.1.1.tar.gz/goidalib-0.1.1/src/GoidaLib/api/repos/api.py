import httpx
from httpx_sse import aconnect_sse
from typing import Optional
from pydantic import BaseModel


class ReposAPI:
    def __init__(self, client: httpx.AsyncClient, token: str):
        self._client = client
        self.token = token

    async def add_repo(self, url: str):
        payload = {
            "url": url,
            "token": self.token
        }
        response = await self._client.post("/repos/add", params=payload)
        response.raise_for_status()
        data = response.json()
        return data

    async def remove_repo(self, url: str, reason: None | str = None):
        payload = {
            "url": url,
            "token": self.token,
        }
        if reason:
            payload["reason"] = reason
        
        response = await self._client.delete("/repos/remove", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def scan(self):
        payload = {
            "token": self.token
        }

        async with aconnect_sse(self._client, "GET", "/repos/scan", params=payload) as connection:
            print(connection.response.raise_for_status())
            data = []
            async for event in connection.aiter_sse():
                if event.data:
                    data.append(event.data)
            
            return data