#!/usr/bin/env python3
"""
AWS API Gateway & Lambda Throttling Test Tool (MH5 Verification)
This script fires 5 concurrent requests to the deployed /chat API Gateway endpoint.
Since the backend Lambda has Reserved Concurrency set to 1, some of these requests
are expected to fail with HTTP 429 (Too Many Requests) or HTTP 502 (Bad Gateway).

No external dependencies are required. Uses Python's built-in urllib.request and threading libraries.
"""

import json
import urllib.request
import urllib.error
import threading
import sys
import time

def send_request(url, api_key, request_id, results):
    payload = json.dumps({
        "prompt": f"Tell me a short 3-word story. Request #{request_id}"
    }).encode("utf-8")
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    start_time = time.time()
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.status
            body = response.read().decode("utf-8")
            elapsed = time.time() - start_time
            results[request_id] = {
                "success": True,
                "status": status,
                "elapsed": elapsed,
                "body": json.loads(body)
            }
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start_time
        body = e.read().decode("utf-8") if e.fp else ""
        results[request_id] = {
            "success": False,
            "status": e.code,
            "elapsed": elapsed,
            "error": str(e),
            "body": body
        }
    except Exception as e:
        elapsed = time.time() - start_time
        results[request_id] = {
            "success": False,
            "status": 0,
            "elapsed": elapsed,
            "error": str(e)
        }

def main():
    print("=" * 60)
    print(" AWS W5 THROTTLING TEST TOOL (Reserved Concurrency = 1)")
    print("=" * 60)
    
    url = input("Enter API Gateway URL: ").strip()
    if not url:
        print("API URL is required.")
        sys.exit(1)
        
    api_key = input("Enter API Key (x-api-key): ").strip()
    if not api_key:
        print("API Key is required.")
        sys.exit(1)
        
    print("\nSending 5 concurrent requests...")
    threads = []
    results = {}
    
    for i in range(1, 6):
        t = threading.Thread(target=send_request, args=(url, api_key, i, results))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n" + "=" * 30 + " RESULTS " + "=" * 30)
    throttled_count = 0
    success_count = 0
    
    for req_id in sorted(results.keys()):
        res = results[req_id]
        status = res["status"]
        elapsed = f"{res['elapsed']:.2f}s"
        
        if res["success"]:
            success_count += 1
            print(f"Request #{req_id}: SUCCESS | Status: {status} | Time: {elapsed}")
            print(f"  Response: {res['body'].get('response', '').strip()}")
        else:
            print(f"Request #{req_id}: FAILED  | Status: {status} | Time: {elapsed}")
            print(f"  Error: {res.get('error', '')}")
            if res.get("body"):
                print(f"  Response Body: {res['body']}")
            
            # API Gateway or Lambda Throttling
            if status in [429, 502, 500]:
                throttled_count += 1
                
    print("=" * 69)
    print(f"Total Successful: {success_count}/5")
    print(f"Total Throttled/Failed: {5 - success_count}/5")
    
    if throttled_count > 0:
        print("\n[SUCCESS] Verification Complete! Checked that requests were throttled due to Reserved Concurrency = 1 limit.")
    else:
        print("\n[WARNING] No requests were throttled. Ensure Lambda Reserved Concurrency is set to 1 and try again.")
    print("=" * 69)

if __name__ == "__main__":
    main()
