from fastapi import APIRouter, BackgroundTasks
import asyncio
from services.auto_bulk_push_service import auto_bulk_push_service

router = APIRouter()


#? use this to run the bulk push and wait for it till it finishes
@router.post("/auto-bulk-push")
async def bulk_push():
    data = await auto_bulk_push_service()
    # return {
    #     "status": "completed", 
    #     "message": "Bulk push completed",
    #     "data": data
    # }

    return {"data": data}