import httpx
from typing import Optional

class CheckerAPI:
    def __init__(self, client: httpx.AsyncClient, token: str):
        self._client = client
        self.token = token

    async def verdict(self, source: str, hash: str, status: str, reason: Optional[str] = None):
        payload = {
            "token": self.token,
            "source": source,
            "hash": hash,
            "status": status,
            "reason": reason,
        }
        response = await self._client.post("/checker/verdict", params=payload)
        response.raise_for_status()
        data = response.json()
        return data