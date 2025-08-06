from fastapi import APIRouter, Query, HTTPException
from services.bulk_query_service import bulk_query_service

router = APIRouter()

@router.get("/bulk-query")
async def bulk_query(
    metric_name: str = Query(..., description="Metric name to query"),
    start: int = Query(..., description="Start timestamp (Unix)"),
    end: int = Query(..., description="End timestamp (Unix)"),
    step: str = Query("1h", description="Step duration (e.g. 15s, 1m)")
):
    try:
        return await bulk_query_service(metric_name, start, end, step)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
