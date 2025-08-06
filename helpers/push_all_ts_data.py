import httpx
from core import config


async def push_all_ts_data(payload: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                config.VICTORIADB_PUSH_ENDPOINT,
                content=payload,
                headers={"Content-Type": "text/plain"},
                timeout=30,
            )
            response.raise_for_status()

            lines = len([line for line in payload.split("\n") if line.strip()])

        except httpx.HTTPError as e:
            print(f"Push failed: {e}")
            
            if e.response is not None:
                print(f"Response content: {e.response.text}")