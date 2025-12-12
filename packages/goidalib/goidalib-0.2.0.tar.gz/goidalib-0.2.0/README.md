# This library is for GoidaHeta project. GoidaHeta currently in development.

### Using
```py
from goidalib import GoidaHetaAPIClient

api = GoidaHetaAPIClient(base_url="http://localhost:8000/api/v1/", token="your_token_here")

async def main():
    print(await api.logger.get_logs())

import asyncio
asyncio.run(main())```