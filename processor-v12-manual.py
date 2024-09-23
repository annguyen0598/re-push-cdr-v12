import json
from datetime import datetime
import pytz

# Dữ liệu CDR mẫu (nhập trực tiếp)
cdr_data = [
{
            "id": "887991905386762240",
            "call_id": "0l6jp55ep8u12fshcmk8",
            "caller": "3003",
            "caller_domain": "etelecom-vn-2023-prod.eb2b.vn",
            "caller_display_name": "",
            "callee": "0773821705",
            "callee_domain": "etelecom-vn-2023-prod.eb2b.vn",
            "final_dest": "",
            "fail_code": 0,
            "start_time": "2024-09-16 16:22:48 GMT+07:00",
            "answer_time": "NOT_ANSWER",
            "end_time": "2024-09-16 16:22:58 GMT+07:00",
            "ringing_time": "2024-09-16 16:22:48 GMT+07:00",
            "duration": "0",
            "session_id": "887991905378373632",
            "related_callid_1": "0",
            "related_callid_2": "",
            "ring_duration": "10",
            "talk_duration": "0",
            "caller_endpoint": "EXTENSION_NUMBER",
            "callee_endpoint": "EXTENSION_NUMBER",
            "direction": "OUTBOUND_CALL",
            "end_reason": "CALLER_DISCONNECT",
            "status": "NONE",
            "outcid": "2607422273982216036",
            "didcid": "",
            "call_cost": "0.000000"
        }
]

# Hàm convert thời gian từ chuỗi về Unix timestamp
def convert_to_unix_time(time_str):
    if time_str == "NOT_ANSWER":
        return "0"
    try:
        dt_str, tz_str = time_str.rsplit(' ', 1)
        tz_offset = int(tz_str.replace('GMT', '').replace(':00', '')) * 60
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        tz = pytz.FixedOffset(tz_offset)
        dt = tz.localize(dt)
        return str(int(dt.timestamp()))
    except ValueError:
        print(f"Error parsing time: {time_str}")
        return "0"

# Hàm convert call log item sang format webhook
def convert_cdr_item(cdr_item):
    return {
        "answered_time": convert_to_unix_time(cdr_item.get("answer_time")),
        "call_id": cdr_item.get("call_id", ""),
        "call_status": cdr_item.get("status", ""),
        "call_targets": [
            {
                "add_time": convert_to_unix_time(cdr_item.get("start_time")),
                "answered_time": convert_to_unix_time(cdr_item.get("answer_time")),
                "end_reason": cdr_item.get("end_reason", "").lower(),
                "ended_time": convert_to_unix_time(cdr_item.get("end_time")),
                "fail_code": cdr_item.get("fail_code", 0),
                "ring_duration": int(cdr_item.get("ring_duration", 0)),
                "ring_time": convert_to_unix_time(cdr_item.get("ringing_time")),
                "status": "NOANSWER" if cdr_item.get("status", "") == "NONE" else "ANSWERED",
                "talk_duration": int(cdr_item.get("talk_duration", 0)),
                "target_number": cdr_item.get("callee", ""),
                "trunk_name": "TRUNK_SBC_01"
            }
        ],
        "callee": cdr_item.get("callee", ""),
        "callee_domain": cdr_item.get("callee_domain", ""),
        "caller": cdr_item.get("caller", ""),
        "caller_display_name": cdr_item.get("caller_display_name", ""),
        "caller_domain": cdr_item.get("caller_domain", ""),
        "cdr_id": cdr_item.get("id", ""),
        "did_cid": cdr_item.get("didcid", ""),
        "direction": "out" if cdr_item.get("direction") == "OUTBOUND_CALL" else "in",
        "ended_reason": cdr_item.get("end_reason", "").lower(),
        "ended_time": convert_to_unix_time(cdr_item.get("end_time")),
        "event_type": "call_cdr",
        "fail_code": cdr_item.get("fail_code", "0"),
        "final_dest": cdr_item.get("final_dest", ""),
        "outbound_caller_id": cdr_item.get("outcid", ""),
        "request_description": "",
        "request_id": "0",
        "ring_duration": cdr_item.get("ring_duration", "0"),
        "ring_time": convert_to_unix_time(cdr_item.get("ringing_time")),
        "session_id": cdr_item.get("session_id", ""),
        "start_time": convert_to_unix_time(cdr_item.get("start_time")),
        "talk_duration": cdr_item.get("talk_duration", "0"),
        "tenant_id": "747778467130511360",
        "tenant_name": "etelecom-vn-2023-prod"
    }

# Chuyển đổi tất cả các CDR
converted_items = [convert_cdr_item(item) for item in cdr_data]

# Lưu file JSON
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# In ra dữ liệu đã chuyển đổi
def print_converted_items(items):
    print(json.dumps(items, indent=4))

# Lưu file JSON đã chuyển đổi
save_to_file(converted_items, 'cdr_converted.json')

# In ra dữ liệu đã chuyển đổi
print_converted_items(converted_items)
