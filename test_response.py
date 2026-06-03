import urllib.request
import urllib.error
import json
import sys

# Reconfigure stdout to use UTF-8 encoding on Windows to print Vietnamese characters
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = 'https://i1h84q6gnj.execute-api.us-east-1.amazonaws.com/prod/chat'
api_key = '0JI8S0QKc48L7cT5rVGuyGYnZXJT7lP4IHQxqd9e'

req = urllib.request.Request(
    url,
    data=json.dumps({'prompt': 'Bạn làm được gì? Hãy kể chi tiết và liệt kê rõ ràng.'}).encode('utf-8'),
    headers={
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    },
    method='POST'
)

print("Sending request to verify long response generation...")
try:
    with urllib.request.urlopen(req) as res:
        print("Status Code:", res.status)
        body = res.read().decode('utf-8')
        data = json.loads(body)
        response_text = data.get("response")
        print("\nAI Response:")
        print(response_text)
        
        # Write to file to ensure we can inspect it safely
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(response_text)
        print("\nLogged response to output.txt")
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))
