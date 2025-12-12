import asyncio

import httpx

from deprecat.backends.utils import get_logger

logger = get_logger(__name__)


async def mock_request():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://example.com")
            response.raise_for_status()

            data = response.text
            logger.info(f"[RESP]: {data}")

            return
    except httpx.HTTPStatusError as e:
        logger.error(f"Error fetching / processing the data: {e}")
        return


if __name__ == "__main__":
    asyncio.run(mock_request())
