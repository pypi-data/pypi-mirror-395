from datetime import datetime


def parse_hl7_timestamps(ts: str) -> datetime:
    ts = ts.strip()
    format = None

    match len(ts):
        case 4:
            format = "%Y"
        case 6:
            format = "%Y%m"
        case 8:
            format = "%Y%m%d"
        case 10:
            format = "%Y%m%d%H"
        case 12:
            format = "%Y%m%d%H%M"
        case 14:
            format = "%Y%m%d%H%M%S"
        case 18:
            format = "%Y%m%d%H%M%S.%f"
        case _:
            raise ValueError(f"Invalid HL7 timestamp length {ts}")

    return datetime.strptime(ts, format)
