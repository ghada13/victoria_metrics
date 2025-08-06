from fastapi import APIRouter, HTTPException
from datetime import datetime
from services.bulk_push_service import bulk_push_service
from models.push_egauge_schema import BulkPushRequest

router = APIRouter()


@router.post("/bulk-push")
async def bulk_push(payload: BulkPushRequest):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nPush request received at {current_date}")

    print(f"ranges nbr : {len(payload.ranges)}")
    print(f"rows nbr : {len(payload.ranges[0].rows)}")

    try:
        bulk_push_service(payload)
        return {"status": "success", "message": "Bulk push completed"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))