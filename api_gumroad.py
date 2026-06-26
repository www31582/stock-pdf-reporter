import requests, json

# Try registering via Gumroad API
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
})

# Get CSRF token first
r = session.get('https://app.gumroad.com/signup', timeout=10)
print('Signup page status:', r.status_code)

# Try checking if email-based signup works via API
r2 = session.post('https://app.gumroad.com/api/v2/users', json={
    'user': {'email': 'aiquanttools_test@proton.me', 'password': 'TestPass123!'}
}, timeout=10)
print('API response:', r2.status_code)
try:
    data = r2.json()
    print(json.dumps(data, indent=2)[:500])
except:
    print('Not JSON:', r2.text[:200])