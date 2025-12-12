import httpx
from typing import Optional

class ModulesAPI:
    def __init__(self, client: httpx.AsyncClient, token: str):
        self._client = client
        self.token = token
    
    async def get_rate(self, module_link: str):
        response = await self._client.get("/modules/rate")
        response.raise_for_status()
        data = response.json()
        return data
    
    async def search(self, query: str):
        payload = {
            "query": query
        }
        response = await self._client.get("/modules/search", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def modules(self):
        payload = {
            "token": self.token
        }
        response = await self._client.get("/modules/modules", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def module(self, module_id: int):
        response = await self._client.get(f"/modules/{module_id}")
        response.raise_for_status()
        data = response.json()
        return data

    async def rnd(self, count: int):
        payload = {
            "count": count
        }
        response = await self._client.get("/modules/rnd", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def rate_module(self, module_id: int, rating: str):
        val = rating.lower()
        if val not in ["like", "dislike"]:
            raise ValueError(detail="Only like or dislike allowed")
        
        payload = {
            "module_link": module_id,
            "rating": val,
            "token": self.token
        }
        
        response = await self._client.post("/modules/modules", params=payload)
        response.raise_for_status()
        data = response.json()
        return data