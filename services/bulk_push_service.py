from models.push_egauge_schema import BulkPushRequest
from helpers.egauge_data_handler import convert_json_to_line_protocol
from helpers.push_all_ts_data import push_all_ts_data
import asyncio
from services.create_egauge_row_length_service import create_egauge_row_length_service

def bulk_push_service(payload: BulkPushRequest):
    # Convert Pydantic model to raw dict for helper
    payload_dict = payload.dict()

    # Convert JSON structure to Influx Line Protocol
    lines = convert_json_to_line_protocol(payload_dict)

    # Join into a newline-delimited string
    final_payload = "\n".join(lines)

    # Push to TSDB asynchronously
    asyncio.create_task(push_all_ts_data(final_payload))

    #! --------------- to push egauge row length metrics
    try:
        lp_line = create_egauge_row_length_service(len(payload.ranges[0].rows))
        print(f"generated row metric : {lp_line}")

        asyncio.create_task(push_all_ts_data(lp_line))
    except Exception as e:
        print(e)
