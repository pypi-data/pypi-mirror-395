import httpx
from typing import Optional
from httpx_sse import aconnect_sse

class LoggerAPI:
    def __init__(self, client: httpx.AsyncClient, token: str):
        self._client = client
        self.token = token

    async def get_logs(self):
        payload = {
            "token": self.token
        }
        # async with aconnect_sse(self._client, "GET","/logger/logs", params=payload) as event_source:
        #     async for event in event_source.aiter_sse():
        #         print(event)
        response = await self._client.get("/logger/logs", params=payload)
        response.raise_for_status()
        data = response.text
        return data