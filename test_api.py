import urllib.request
import urllib.error
import json

url = 'https://i1h84q6gnj.execute-api.us-east-1.amazonaws.com/prod/chat'
api_key = '0JI8S0QKc48L7cT5rVGuyGYnZXJT7lP4IHQxqd9e'

def test_api_call(name, headers, method='POST', data=None):
    print("\n" + "=" * 50)
    print(f"TEST: {name}")
    print("=" * 50)
    payload = json.dumps(data).encode('utf-8') if data else None
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers=headers,
        method=method
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            print("STATUS CODE:", res.status)
            print("HEADERS:")
            for k, v in res.headers.items():
                if k.lower() in ['access-control-allow-origin', 'access-control-allow-headers', 'access-control-allow-methods', 'x-api-key']:
                    print(f"  {k}: {v}")
            body = res.read().decode('utf-8')
            print("RESPONSE BODY:")
            try:
                parsed = json.loads(body)
                print(json.dumps(parsed, indent=2))
            except:
                print(body)
            return True
    except urllib.error.HTTPError as e:
        print("STATUS CODE:", e.code)
        print("REASON:", e.reason)
        print("HEADERS:")
        for k, v in e.headers.items():
            if k.lower() in ['x-amzn-errortype', 'x-amz-apigw-id']:
                print(f"  {k}: {v}")
        body = e.read().decode('utf-8')
        print("RESPONSE BODY:", body)
        return False
    except Exception as e:
        print("ERROR:", str(e))
        return False

# 1. Test Valid Request (with API Key)
test_api_call(
    name="Valid Request (With API Key)",
    headers={'x-api-key': api_key, 'Content-Type': 'application/json'},
    method='POST',
    data={'prompt': 'Tell me a 3-word story.'}
)

# 2. Test Unauthenticated Request (No API Key)
test_api_call(
    name="Unauthenticated Request (No API Key)",
    headers={'Content-Type': 'application/json'},
    method='POST',
    data={'prompt': 'Hi'}
)

# 3. Test Invalid Key Request (Wrong API Key)
test_api_call(
    name="Invalid Key Request (Wrong API Key)",
    headers={'x-api-key': 'INVALID-KEY-12345', 'Content-Type': 'application/json'},
    method='POST',
    data={'prompt': 'Hi'}
)

# 4. Test CORS OPTIONS Preflight
test_api_call(
    name="CORS OPTIONS Preflight",
    headers={},
    method='OPTIONS'
)
