import requests
import json
from datetime import datetime
import pytz

# Đặt cấu hình API và Webhook
API_URL = 'https://sip.etelecom.vn:8900/api/call_logs/list'
WEBHOOK_URL = 'https://webhook.site/ea73131c-1058-4e41-8a44-f527ae51b7c3'

# Hàm convert thời gian từ chuỗi về Unix timestamp
def convert_to_unix_time(time_str):
    if time_str == "NOT_ANSWER":
        return "0"
    try:
        # Tách phần thời gian và múi giờ
        dt_str, tz_str = time_str.rsplit(' ', 1)
        
        # Chuyển đổi múi giờ từ 'GMT+07:00' thành offset phút
        tz_offset = int(tz_str.replace('GMT', '').replace(':00', '')) * 60
        
        # Xử lý thời gian
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        tz = pytz.FixedOffset(tz_offset)
        dt = tz.localize(dt)
        
        return str(int(dt.timestamp()))
    except ValueError:
        print(f"Error parsing time: {time_str}")
        return "0"

# Hàm convert call log item sang format webhook
def convert_cdr_item(cdr_item, tenant_id, tenant_name):
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
        "tenant_id": tenant_id,
        "tenant_name": tenant_name
    }

# Hàm lấy danh sách CDR từ API
def fetch_cdr_items(start_time, end_time, access_token):
    url = f"{API_URL}?pagination=1&pagesize=5&sort_by=DEFAULT&start_time={start_time}&end_time={end_time}"
    headers = {
        'Content-Type': 'application/json',
        'access_token': access_token
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print("Failed to fetch data from API:", response.status_code, response.text)
        return []

# Hàm lưu file JSON
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Hàm gửi dữ liệu tới webhook và kiểm tra lỗi
def send_to_webhook(data, webhook_url):
    response = requests.post(webhook_url, json=data)
    if response.status_code == 200:
        print(f"Successfully sent data to webhook.")
    else:
        print(f"Failed to send data to webhook: {response.status_code}, {response.text}")


# Hàm xử lý CDR
def process_cdr(start_time, end_time, access_token, tenant_id, tenant_name, webhook_url):
    raw_cdr_items = fetch_cdr_items(start_time, end_time, access_token)
    
    # Lưu raw call log
    save_to_file(raw_cdr_items, 'cdr_raw.json')
    
    # Convert từng item và lưu file đã convert
    converted_items = [convert_cdr_item(item, tenant_id, tenant_name) for item in raw_cdr_items]
    save_to_file(converted_items, 'cdr_converted.json')

    # Gửi tới webhook từng CDR đã convert
    for converted_item in converted_items:
        send_to_webhook(converted_item, webhook_url)

