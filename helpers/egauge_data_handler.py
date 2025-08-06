import json
from typing import Dict, List


def string_formatter(text: str, context: str = "tag") -> str:
    """
    Format text for InfluxDB line protocol based on context.
    context: "measurement", "tag", or "field"
    """
    if context == "measurement":
        return (
            text.replace(",", "\\,")
                .replace(" ", "_")
        )
    elif context == "tag":
        return (
            text.replace(",", "\\,")
                .replace(" ", "\\ ")
                .replace("=", "\\=")
        )
    elif context == "field":
        return (
            text.replace(",", "\\,")
                .replace(" ", "\\ ")
                .replace("=", "\\=")
        )
    else:
        raise ValueError(f"Unknown context: {context}")



def parse_value(number: str) -> float:
    normalized = number.replace(",", ".")
    float_number = float(normalized)
    return float_number


def create_single_line_protocol(register: Dict, data: str, timestamp_in_nanoseconds: int) -> str:
    measurement = string_formatter(register["name"], context="measurement")
    tags = (
        f"type={string_formatter(register['type'], context='tag')},"
        f"did={string_formatter(str(register['did']), context='tag')}"
    )
    data = parse_value(data)
    line_protocol = f"{measurement},{tags} value={data} {timestamp_in_nanoseconds}"
    return line_protocol



def timestamp_to_nanosecond(base_timestamp: int, range_index: int, delta: float) -> int:
    timestamp_in_nanosecond = (base_timestamp + range_index * delta) * 1_000_000_000
    return int(timestamp_in_nanosecond)


def convert_json_to_line_protocol(egauge_data: Dict) -> List[str]:
    all_registers = egauge_data["registers"]
    all_ranges = egauge_data["ranges"]
    all_line_protocols = []

    for range_item in all_ranges:
        base_timestamp = int(range_item["ts"])
        delta = float(range_item["delta"])

        for row_index, row in enumerate(range_item["rows"][1:], 1):
            row_ts_ns = timestamp_to_nanosecond(
                base_timestamp=base_timestamp,
                range_index=row_index,
                delta=delta
            )

            for register_index, register in enumerate(all_registers):
                lp = create_single_line_protocol(
                    register=register,
                    data=row[register_index],
                    timestamp_in_nanoseconds=row_ts_ns
                )
                all_line_protocols.append(lp)

    return all_line_protocols


def load_egauge_data_service() -> List[str]:
    with open("egauge_data.log") as log_file:
        all_json_data = json.load(log_file)

        print(f"loaded json! registers : {len(all_json_data.get('registers'))}, range blocks : {len(all_json_data.get('ranges'))}")
        all_line_protocol_data = convert_json_to_line_protocol(all_json_data)

        print(all_line_protocol_data[0])

        return all_line_protocol_data