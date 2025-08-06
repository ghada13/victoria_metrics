import asyncio
import httpx
import os
from core import config
from services.load_egauge_data_service import load_egauge_data_service

def push_sample_data_to_file():
    file_path = "data.txt"

    # Load the data
    data_lines = load_egauge_data_service()
    print(f"Writing {len(data_lines)} lines to {file_path}")

    # Remove the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed existing {file_path}")

    # Write to new file
    with open(file_path, "w") as f:
        f.write("\n".join(data_lines))
        print(f"Successfully wrote to {file_path}")


async def push_all_ts_data(payload: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                config.VICTORIADB_PUSH_ENDPOINT,
                content=payload,
                headers={"Content-Type": "text/plain"},
                timeout=30,
                params={"db": "egauge_data"}
            )
            response.raise_for_status()

            lines = len([line for line in payload.split("\n") if line.strip()])
            print(f"Pushed all {lines} metrics successfully")

        except httpx.HTTPError as e:
            print(f"Push failed: {e}")
            if e.response is not None:
                print(f"Response content: {e.response.text}")


async def auto_bulk_push_service():
    all_lines = load_egauge_data_service()
    print(f"Loaded {len(all_lines)} metrics. Pushing...")

    payload = "\n".join(all_lines)
    await push_all_ts_data(payload)

    push_sample_data_to_file()

    return all_lines
