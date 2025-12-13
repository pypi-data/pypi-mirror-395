# This library is for GoidaHeta project. GoidaHeta currently in development.

### Example usage:
```py
from goidalib import GoidaHetaAPIClient

api = GoidaHetaAPIClient(base_url="http://localhost:8000", token="your_token_here")

async def main():
    print(await api.auth.get_me())

import asyncio
asyncio.run(main())
```