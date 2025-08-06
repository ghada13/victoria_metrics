import httpx
from core import config

async def bulk_query_service(metric_name: str, start: int, end: int, step: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                config.VICTORIADB_BULK_QUERY_ENDPOINT,
                params={
                    "query": metric_name,
                    "start": start,
                    "end": end,
                    "step": step,
                },
            )
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
        
    except httpx.RequestError as e:
        return {"status": "error", "details": str(e)}
