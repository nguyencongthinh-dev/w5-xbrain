import urllib.request
import urllib.error
import json
import threading
import time

url = 'https://i1h84q6gnj.execute-api.us-east-1.amazonaws.com/prod/chat'
api_key = '0JI8S0QKc48L7cT5rVGuyGYnZXJT7lP4IHQxqd9e'

success_count = 0
failed_count = 0
lock = threading.Lock()

def call(req_id):
    global success_count, failed_count
    req = urllib.request.Request(
        url,
        data=json.dumps({'prompt': 'Hi'}).encode('utf-8'),
        headers={
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as res:
            if res.status == 200:
                with lock:
                    success_count += 1
    except urllib.error.HTTPError as e:
        with lock:
            failed_count += 1
        print(f"Request #{req_id} throttled: Status {e.code} ({e.reason})")
    except Exception as e:
        with lock:
            failed_count += 1

print("Firing 50 concurrent requests to trigger API Gateway throttling...")
threads = []
for i in range(1, 51):
    t = threading.Thread(target=call, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n" + "=" * 40)
print(f"Total Successful Requests: {success_count}")
print(f"Total Throttled/Failed Requests: {failed_count}")
print("=" * 40)
if failed_count > 0:
    print("[SUCCESS] Throttling verified! Some requests were successfully blocked by API Gateway.")
else:
    print("[WARNING] Throttling did not trigger. Try increasing the number of requests.")
