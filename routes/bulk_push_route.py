from fastapi import APIRouter, HTTPException
from datetime import datetime
import httpx
from services.bulk_push_service import bulk_push_service
from models.push_egauge_schema import BulkPushRequest

router = APIRouter()

async def get_vm_time() -> int:
    url = "http://148.253.86.63:8428/api/v1/query?query=time()"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        # Récupérer le timestamp serveur VictoriaMetrics (en secondes)
        vm_time = int(float(data['data']['result'][0]['value'][1]))
        return vm_time

@router.post("/bulk-push")
async def bulk_push(payload: BulkPushRequest):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nPush request received at {current_date}")

    print(f"ranges nbr : {len(payload.ranges)}")
    print(f"rows nbr : {len(payload.ranges[0].rows)}")

    try:
        vm_time = await get_vm_time()
        local_time = int(datetime.utcnow().timestamp())
        time_diff = vm_time - local_time
        print(f"VM server time: {vm_time}, local time: {local_time}, time diff: {time_diff}s")

        # Ajuster le timestamp dans chaque range
        for range_obj in payload.ranges:
            original_ts = range_obj.ts
            range_obj.ts += time_diff
            print(f"Adjusted range ts from {original_ts} to {range_obj.ts}")

        # Appeler le service avec le payload modifié
        bulk_push_service(payload)

        return {"status": "success", "message": "Bulk push completed with time adjustment"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

