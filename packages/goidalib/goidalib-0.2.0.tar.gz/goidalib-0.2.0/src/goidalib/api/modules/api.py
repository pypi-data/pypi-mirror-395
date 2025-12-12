import httpx
from typing import Optional

class ModulesAPI:
    def __init__(self, client: httpx.AsyncClient, token: str):
        self._client = client
        self.token = token
    
    async def get_rate(self, module_id: str):
        """Get rate for module with given id"""
        payload = {
            "module_id": module_id
        }
        response = await self._client.get("/modules/rate", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def search(self, query: str):
        """Search modules by query"""
        payload = {
            "query": query
        }
        response = await self._client.get("/modules/search", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def modules(self):
        """Get all modules(ADMIN ONLY)"""
        payload = {
            "token": self.token
        }
        response = await self._client.get("/modules/modules", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def module(self, module_id: int):
        """Get info about module by module_id"""
        response = await self._client.get(f"/modules/{module_id}")
        response.raise_for_status()
        data = response.json()
        return data

    async def rnd(self, count: int):
        """Get random module"""
        payload = {
            "count": count
        }
        response = await self._client.get("/modules/rnd", params=payload)
        response.raise_for_status()
        data = response.json()
        return data
    
    async def rate_module(self, module_id: int, rating: str):
        """Rate module(like or dislike)"""
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