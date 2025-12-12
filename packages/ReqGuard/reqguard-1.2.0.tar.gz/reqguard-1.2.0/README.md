# ReqGuard v1.2.0

![ReqGuard Logo](attached_assets/generated_images/reqguard_security_shield_logo.png)

## Python HTTP Security Library

ReqGuard is a security-hardened HTTP library for Python based on the popular requests library. It maintains full backward compatibility while adding over 30 advanced security features to protect your applications from common web vulnerabilities.

**Version**: 1.2.0  
**Author**: mero  
**Telegram**: [@QP4RM](https://t.me/QP4RM)  
**GitHub**: [x6-u](https://github.com/x6-u)  
**License**: Apache-2.0

---

## Features

### Core Security Features

1. **SSL/TLS Verification Warnings** - Warns when SSL verification is disabled
2. **Response Size Limits** - Protects against memory exhaustion attacks (default 100MB)
3. **SSRF Protection** - Blocks requests to private IP ranges
4. **Mandatory Timeout** - Forces timeout configuration to prevent hanging connections
5. **Rate Limiting** - Built-in rate limiter to prevent abuse
6. **DNS Rebinding Protection** - Detects and blocks DNS rebinding attacks
7. **Port Checking** - Restricts requests to allowed ports only
8. **Protocol Smuggling Protection** - Detects URL-based protocol smuggling attempts
9. **Scheme Validation** - Only allows http/https schemes by default
10. **Domain Allowlist/Blocklist** - Fine-grained domain control

### Advanced Security Features

11. **JSON Bomb Protection** - Limits JSON size and nesting depth
12. **Zip Bomb Protection** - Detects decompression bombs
13. **Slowloris Detection** - Identifies slow connection attacks
14. **Redirect Security** - Prevents HTTPS downgrade and unsafe redirects
15. **Header Sanitization** - Removes sensitive headers from logs
16. **Memory Limits** - Configurable memory usage limits
17. **Adaptive Timeouts** - Auto-adjusting timeouts based on response patterns
18. **Failure Prediction** - Predicts host failures based on history

### Stealth and Anonymity Features

19. **Camouflage Mode** - Rotates realistic browser headers
20. **Stealth Proxy Support** - Enhanced proxy handling
21. **User-Agent Rotation** - Automatic UA rotation with lock option
22. **Browser Fingerprint Mimicry** - Complete browser header simulation

### HTTP Protocol Features

23. **HTTP/2 Support** - Full HTTP/2 protocol support
24. **HTTP/3 Ready** - Prepared for HTTP/3 when available
25. **Meta Protocol** - Custom protocol encoding layer
26. **Connection Pooling** - Efficient connection management

### Plugin and Extension System

27. **Plugin Manager** - Full plugin hook system
28. **Pre/Post Request Hooks** - Customize request handling
29. **Middleware Support** - Add custom middlewares
30. **Request Validators** - Custom validation logic
31. **Header Interceptors** - Modify headers dynamically
32. **Auth Handlers** - Custom authentication methods

### Logging and Monitoring

33. **Route Recording** - Complete request/response logging
34. **Secure Logging** - Automatic sensitive data redaction
35. **Performance Metrics** - Response time tracking
36. **Export to JSON** - Export logs in JSON format

### Additional Auth Methods

37. **HTTPBearerAuth** - Bearer token authentication
38. **APIKeyAuth** - API key header authentication
39. **OAuth2Auth** - OAuth 2.0 authentication support

---

## Installation

```bash
pip install urllib3 certifi charset-normalizer idna httpx h2 aioquic
```

Then copy the `requests` directory to your project.

---

## Quick Start

```python
import requests

# Simple GET request
response = requests.get('https://httpbin.org/get')
print(response.json())

# POST request with JSON
response = requests.post('https://httpbin.org/post', json={'key': 'value'})
print(response.status_code)
```

---

## Security Configuration

```python
from requests import SecurityConfig, set_global_config, Session

# Create custom security configuration
config = SecurityConfig(
    verify_ssl=True,
    max_response_size=50 * 1024 * 1024,  # 50MB limit
    ssrf_protection=True,
    dns_rebinding_protection=True,
    safe_redirects=True,
    max_redirects=5,
    default_timeout=(10.0, 30.0),
    force_timeout=True,
    rate_limit=100,
    rate_limit_window=1.0,
    allowed_ports={80, 443, 8080},
    blocked_domains={'malicious.com'},
    camouflage_mode=True,
)

# Apply globally
set_global_config(config)

# Or use with session
session = Session(security_config=config)
response = session.get('https://httpbin.org/get')
```

---

## Test Scripts

Below are 80+ test scripts demonstrating all features:

### Test 1: Basic GET Request
```python
import requests

response = requests.get('https://httpbin.org/get')
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
```

### Test 2: POST Request with JSON
```python
import requests

response = requests.post('https://httpbin.org/post', json={'name': 'ReqGuard', 'version': '1.2.0'})
print(response.json())
```

### Test 3: POST Request with Form Data
```python
import requests

response = requests.post('https://httpbin.org/post', data={'field1': 'value1', 'field2': 'value2'})
print(response.json())
```

### Test 4: Custom Headers
```python
import requests

headers = {'X-Custom-Header': 'MyValue', 'Accept': 'application/json'}
response = requests.get('https://httpbin.org/headers', headers=headers)
print(response.json())
```

### Test 5: Query Parameters
```python
import requests

params = {'key1': 'value1', 'key2': 'value2'}
response = requests.get('https://httpbin.org/get', params=params)
print(response.json())
```

### Test 6: Basic Authentication
```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get('https://httpbin.org/basic-auth/user/pass', auth=HTTPBasicAuth('user', 'pass'))
print(f"Authenticated: {response.status_code == 200}")
```

### Test 7: Digest Authentication
```python
import requests
from requests.auth import HTTPDigestAuth

response = requests.get('https://httpbin.org/digest-auth/auth/user/pass', auth=HTTPDigestAuth('user', 'pass'))
print(f"Digest Auth: {response.status_code}")
```

### Test 8: Bearer Token Authentication
```python
import requests
from requests.auth import HTTPBearerAuth

response = requests.get('https://httpbin.org/bearer', auth=HTTPBearerAuth('my-token-123'))
print(response.json())
```

### Test 9: API Key Authentication
```python
import requests
from requests.auth import APIKeyAuth

response = requests.get('https://httpbin.org/headers', auth=APIKeyAuth('my-api-key', 'X-API-Key'))
print(response.json())
```

### Test 10: Session with Cookies
```python
import requests

session = requests.Session()
session.get('https://httpbin.org/cookies/set/sessionid/abc123')
response = session.get('https://httpbin.org/cookies')
print(response.json())
```

### Test 11: Timeout Configuration
```python
import requests

try:
    response = requests.get('https://httpbin.org/delay/5', timeout=(3.0, 4.0))
except requests.Timeout:
    print("Request timed out as expected")
```

### Test 12: SSRF Protection
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(ssrf_protection=True)
session = Session(security_config=config)

try:
    response = session.get('http://127.0.0.1/')
except requests.SSRFDetected as e:
    print(f"SSRF Blocked: {e}")
```

### Test 13: Response Size Limit
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(max_response_size=1024)  # 1KB limit
session = Session(security_config=config)

try:
    response = session.get('https://httpbin.org/bytes/5000')
except requests.ResponseTooLarge as e:
    print(f"Response too large: {e}")
```

### Test 14: Rate Limiting
```python
import requests
from requests import SecurityConfig, set_global_config, RateLimiter

config = SecurityConfig(rate_limit=5, rate_limit_window=1.0)
set_global_config(config)

for i in range(10):
    response = requests.get('https://httpbin.org/get')
    print(f"Request {i+1}: {response.status_code}")
```

### Test 15: DNS Rebinding Protection
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(dns_rebinding_protection=True)
session = Session(security_config=config)

response = session.get('https://httpbin.org/get')
print(f"DNS protection active: {response.status_code}")
```

### Test 16: Safe Redirects
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(safe_redirects=True, max_redirects=5)
session = Session(security_config=config)

response = session.get('https://httpbin.org/redirect/3', allow_redirects=True)
print(f"Redirects followed: {len(response.history)}")
```

### Test 17: Port Restrictions
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(allowed_ports={80, 443})
session = Session(security_config=config)

try:
    response = session.get('http://example.com:8080/')
except requests.BlockedPort as e:
    print(f"Port blocked: {e}")
```

### Test 18: Domain Blocklist
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(blocked_domains={'blocked-domain.com'})
session = Session(security_config=config)

try:
    response = session.get('https://blocked-domain.com/')
except requests.BlockedDomain as e:
    print(f"Domain blocked: {e}")
```

### Test 19: Domain Allowlist
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(allowed_domains={'httpbin.org'})
session = Session(security_config=config)

response = session.get('https://httpbin.org/get')
print(f"Allowed domain: {response.status_code}")
```

### Test 20: Camouflage Mode
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(camouflage_mode=True)
session = Session(security_config=config)

response = session.get('https://httpbin.org/headers')
print(f"User-Agent: {response.json()['headers'].get('User-Agent')}")
```

### Test 21: Plugin System - Pre Request Hook
```python
import requests
from requests import GLOBAL_PLUGIN_MANAGER

def my_pre_hook(url, method):
    print(f"About to make {method} request to {url}")

GLOBAL_PLUGIN_MANAGER.register_hook('pre_request', my_pre_hook)

response = requests.get('https://httpbin.org/get')
```

### Test 22: Plugin System - Post Request Hook
```python
import requests
from requests import GLOBAL_PLUGIN_MANAGER

def my_post_hook(response):
    print(f"Response received with status {response.status_code}")

GLOBAL_PLUGIN_MANAGER.register_hook('post_request', my_post_hook)

response = requests.get('https://httpbin.org/get')
```

### Test 23: Middleware Support
```python
import requests
from requests import GLOBAL_PLUGIN_MANAGER

def logging_middleware(request):
    print(f"Middleware: Processing {request.method} {request.url}")
    return request

GLOBAL_PLUGIN_MANAGER.add_middleware(logging_middleware)
```

### Test 24: Request Validator
```python
import requests
from requests import GLOBAL_PLUGIN_MANAGER

def url_validator(request):
    if 'unsafe' in request.url:
        return False
    return True

GLOBAL_PLUGIN_MANAGER.add_validator(url_validator)
```

### Test 25: Route Recording
```python
import requests
from requests import SecurityConfig, Session, GLOBAL_ROUTE_RECORDER

config = SecurityConfig(route_recording=True)
session = Session(security_config=config)

session.get('https://httpbin.org/get')
session.post('https://httpbin.org/post', json={'test': 'data'})

print(GLOBAL_ROUTE_RECORDER.export_json())
```

### Test 26: Secure Logging
```python
import requests
from requests import GLOBAL_LOGGER

response = requests.get('https://httpbin.org/get')

logs = GLOBAL_LOGGER.get_logs()
for log in logs:
    print(log)
```

### Test 27: Adaptive Timeout
```python
import requests
from requests import SecurityConfig, Session, GLOBAL_ADAPTIVE_TIMEOUT

config = SecurityConfig(adaptive_timeout=True)
session = Session(security_config=config)

for _ in range(5):
    response = session.get('https://httpbin.org/get')

timeout = GLOBAL_ADAPTIVE_TIMEOUT.get_timeout()
print(f"Adaptive timeout: {timeout}")
```

### Test 28: Failure Prediction
```python
import requests
from requests import GLOBAL_FAILURE_PREDICTOR

for _ in range(10):
    try:
        requests.get('https://httpbin.org/get', timeout=5)
    except:
        pass

failure_prob = GLOBAL_FAILURE_PREDICTOR.predict_failure('httpbin.org')
print(f"Failure probability: {failure_prob}")
```

### Test 29: JSON Validation
```python
import requests
from requests.security import validate_json_safety

json_data = '{"nested": {"deep": {"data": [1,2,3]}}}'
try:
    parsed = validate_json_safety(json_data, max_size=1000, max_depth=10)
    print(f"Valid JSON: {parsed}")
except Exception as e:
    print(f"JSON validation failed: {e}")
```

### Test 30: Private IP Detection
```python
from requests.security import is_private_ip

ips = ['192.168.1.1', '10.0.0.1', '8.8.8.8', '127.0.0.1']
for ip in ips:
    print(f"{ip}: {'Private' if is_private_ip(ip) else 'Public'}")
```

### Test 31: Header Sanitization
```python
from requests.security import sanitize_headers_for_logging

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer secret-token',
    'X-API-Key': 'my-api-key'
}

sanitized = sanitize_headers_for_logging(headers)
print(sanitized)
```

### Test 32: URL Security Validation
```python
from requests import SecurityConfig
from requests.security import validate_url_security

config = SecurityConfig(ssrf_protection=True)

try:
    validate_url_security('https://httpbin.org/get', config)
    print("URL is safe")
except Exception as e:
    print(f"URL blocked: {e}")
```

### Test 33: Redirect Security Validation
```python
from requests import SecurityConfig
from requests.security import validate_redirect_security

config = SecurityConfig(safe_redirects=True)

try:
    validate_redirect_security('https://example.com', 'https://other.com', config)
    print("Redirect is safe")
except Exception as e:
    print(f"Redirect blocked: {e}")
```

### Test 34: Meta Protocol Encoding
```python
from requests.security import MetaProtocol

proto = MetaProtocol()
data = b"secret message"
encoded = proto.encode(data)
decoded = proto.decode(encoded)
print(f"Original: {data}")
print(f"Decoded: {decoded}")
```

### Test 35: Slowloris Detector
```python
from requests.security import SlowlorisDetector

detector = SlowlorisDetector(min_speed=1024, check_interval=5.0)
detector.start()
detector.add_bytes(5000)
print("Transfer speed is acceptable")
```

### Test 36: PUT Request
```python
import requests

response = requests.put('https://httpbin.org/put', json={'updated': 'data'})
print(response.json())
```

### Test 37: PATCH Request
```python
import requests

response = requests.patch('https://httpbin.org/patch', json={'field': 'newvalue'})
print(response.json())
```

### Test 38: DELETE Request
```python
import requests

response = requests.delete('https://httpbin.org/delete')
print(f"Delete status: {response.status_code}")
```

### Test 39: HEAD Request
```python
import requests

response = requests.head('https://httpbin.org/get')
print(f"Headers: {response.headers}")
```

### Test 40: OPTIONS Request
```python
import requests

response = requests.options('https://httpbin.org/get')
print(f"Allowed methods: {response.headers.get('Allow')}")
```

### Test 41: Streaming Response
```python
import requests

response = requests.get('https://httpbin.org/stream/5', stream=True)
for line in response.iter_lines():
    print(line)
```

### Test 42: Chunked Response
```python
import requests

response = requests.get('https://httpbin.org/stream-bytes/1024', stream=True)
for chunk in response.iter_content(chunk_size=256):
    print(f"Received {len(chunk)} bytes")
```

### Test 43: Binary Response
```python
import requests

response = requests.get('https://httpbin.org/bytes/100')
print(f"Binary content length: {len(response.content)}")
```

### Test 44: Encoding Detection
```python
import requests

response = requests.get('https://httpbin.org/encoding/utf8')
print(f"Encoding: {response.encoding}")
print(f"Apparent encoding: {response.apparent_encoding}")
```

### Test 45: Response Headers
```python
import requests

response = requests.get('https://httpbin.org/response-headers?X-Custom=Value')
print(response.headers)
```

### Test 46: Status Code Checking
```python
import requests

response = requests.get('https://httpbin.org/status/200')
print(f"OK: {response.ok}")
print(f"Status: {response.status_code}")
```

### Test 47: Error Response
```python
import requests

response = requests.get('https://httpbin.org/status/404')
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")
```

### Test 48: Redirect History
```python
import requests

response = requests.get('https://httpbin.org/redirect/3')
print(f"Final URL: {response.url}")
print(f"Redirect count: {len(response.history)}")
```

### Test 49: Disable Redirects
```python
import requests

response = requests.get('https://httpbin.org/redirect/1', allow_redirects=False)
print(f"Is redirect: {response.is_redirect}")
print(f"Location: {response.headers.get('Location')}")
```

### Test 50: Cookie Handling
```python
import requests

jar = requests.cookies.RequestsCookieJar()
jar.set('cookie_name', 'cookie_value', domain='httpbin.org', path='/')

response = requests.get('https://httpbin.org/cookies', cookies=jar)
print(response.json())
```

### Test 51: Session Persistence
```python
import requests

session = requests.Session()
session.headers.update({'X-Session-Header': 'persistent'})

response1 = session.get('https://httpbin.org/headers')
response2 = session.get('https://httpbin.org/headers')

print(response1.json()['headers']['X-Session-Header'])
```

### Test 52: Proxy Configuration
```python
import requests

proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080',
}

# Only works with actual proxy
# response = requests.get('https://httpbin.org/get', proxies=proxies)
print("Proxy configuration example")
```

### Test 53: File Upload
```python
import requests
import io

file_content = io.BytesIO(b"test file content")
files = {'file': ('test.txt', file_content, 'text/plain')}

response = requests.post('https://httpbin.org/post', files=files)
print(response.json()['files'])
```

### Test 54: Multiple Files Upload
```python
import requests
import io

files = [
    ('files', ('file1.txt', io.BytesIO(b"content1"), 'text/plain')),
    ('files', ('file2.txt', io.BytesIO(b"content2"), 'text/plain')),
]

response = requests.post('https://httpbin.org/post', files=files)
print(response.json()['files'])
```

### Test 55: Form + File Upload
```python
import requests
import io

data = {'field': 'value'}
files = {'file': ('test.txt', io.BytesIO(b"content"), 'text/plain')}

response = requests.post('https://httpbin.org/post', data=data, files=files)
print(response.json())
```

### Test 56: Custom SSL Context
```python
import requests

# Using custom CA bundle
response = requests.get('https://httpbin.org/get', verify=True)
print(f"SSL verified: {response.status_code}")
```

### Test 57: Disable SSL Verification
```python
import requests
import warnings

warnings.filterwarnings('ignore', category=requests.InsecureRequestWarning)

response = requests.get('https://httpbin.org/get', verify=False)
print(f"Status (insecure): {response.status_code}")
```

### Test 58: Response Links
```python
import requests

response = requests.get('https://httpbin.org/links/5')
print(f"Links: {response.links}")
```

### Test 59: Response Elapsed Time
```python
import requests

response = requests.get('https://httpbin.org/get')
print(f"Elapsed time: {response.elapsed.total_seconds()}s")
```

### Test 60: Prepared Request
```python
import requests

session = requests.Session()

req = requests.Request('GET', 'https://httpbin.org/get', headers={'X-Custom': 'Header'})
prepared = session.prepare_request(req)

print(f"Prepared URL: {prepared.url}")
print(f"Prepared Headers: {prepared.headers}")
```

### Test 61: Request Copy
```python
import requests

session = requests.Session()
req = requests.Request('POST', 'https://httpbin.org/post', json={'data': 'test'})
prepared = session.prepare_request(req)

copied = prepared.copy()
print(f"Original URL: {prepared.url}")
print(f"Copied URL: {copied.url}")
```

### Test 62: Hook Registration
```python
import requests

def print_url(response, *args, **kwargs):
    print(f"Received response from: {response.url}")
    return response

hooks = {'response': print_url}
response = requests.get('https://httpbin.org/get', hooks=hooks)
```

### Test 63: Multiple Response Hooks
```python
import requests

def hook1(response, *args, **kwargs):
    print("Hook 1 executed")
    return response

def hook2(response, *args, **kwargs):
    print("Hook 2 executed")
    return response

hooks = {'response': [hook1, hook2]}
response = requests.get('https://httpbin.org/get', hooks=hooks)
```

### Test 64: Status Code Lookup
```python
from requests import codes

print(f"OK code: {codes.ok}")
print(f"Not Found code: {codes.not_found}")
print(f"Server Error code: {codes.server_error}")
```

### Test 65: Case Insensitive Dict
```python
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict({'Content-Type': 'application/json'})
print(headers['content-type'])
print(headers['CONTENT-TYPE'])
```

### Test 66: URL Parsing
```python
from requests.utils import urldefragauth, requote_uri

url = 'https://user:pass@example.com/path?query=value#fragment'
clean = urldefragauth(url)
print(f"Cleaned URL: {clean}")
```

### Test 67: Encoding Detection
```python
from requests.utils import get_encoding_from_headers

headers = {'content-type': 'text/html; charset=utf-8'}
encoding = get_encoding_from_headers(headers)
print(f"Encoding: {encoding}")
```

### Test 68: Auth From URL
```python
from requests.utils import get_auth_from_url

url = 'https://username:password@example.com/path'
auth = get_auth_from_url(url)
print(f"Username: {auth[0]}, Password: {auth[1]}")
```

### Test 69: Default Headers
```python
from requests.utils import default_headers

headers = default_headers()
print(headers)
```

### Test 70: Gzip Response
```python
import requests

response = requests.get('https://httpbin.org/gzip')
print(f"Gzipped: {response.json()['gzipped']}")
```

### Test 71: Deflate Response
```python
import requests

response = requests.get('https://httpbin.org/deflate')
print(f"Deflated: {response.json()['deflated']}")
```

### Test 72: Brotli Response
```python
import requests

response = requests.get('https://httpbin.org/brotli')
if response.ok:
    print(f"Brotli: {response.json()}")
```

### Test 73: Image Download
```python
import requests

response = requests.get('https://httpbin.org/image/png')
print(f"Image size: {len(response.content)} bytes")
print(f"Content-Type: {response.headers['Content-Type']}")
```

### Test 74: UUID Response
```python
import requests

response = requests.get('https://httpbin.org/uuid')
print(f"UUID: {response.json()['uuid']}")
```

### Test 75: IP Address
```python
import requests

response = requests.get('https://httpbin.org/ip')
print(f"Origin IP: {response.json()['origin']}")
```

### Test 76: User Agent Echo
```python
import requests

response = requests.get('https://httpbin.org/user-agent')
print(f"User-Agent: {response.json()['user-agent']}")
```

### Test 77: Response Time Simulation
```python
import requests

response = requests.get('https://httpbin.org/delay/1')
print(f"Delayed response received in {response.elapsed.total_seconds()}s")
```

### Test 78: Connection Close
```python
import requests

session = requests.Session()
response = session.get('https://httpbin.org/get')
session.close()
print("Session closed")
```

### Test 79: Mount Custom Adapter
```python
import requests
from requests.adapters import HTTPAdapter

session = requests.Session()
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
session.mount('https://', adapter)

response = session.get('https://httpbin.org/get')
print(f"Custom adapter used: {response.status_code}")
```

### Test 80: Full Security Configuration
```python
import requests
from requests import SecurityConfig, Session

config = SecurityConfig(
    verify_ssl=True,
    allow_verify_false=False,
    max_response_size=100 * 1024 * 1024,
    ssrf_protection=True,
    dns_rebinding_protection=True,
    safe_redirects=True,
    max_redirects=10,
    default_timeout=(10.0, 30.0),
    force_timeout=True,
    rate_limit=100,
    rate_limit_window=1.0,
    allowed_ports={80, 443, 8080, 8443},
    blocked_domains=set(),
    allowed_schemes={'http', 'https'},
    slowloris_min_speed=1024,
    slowloris_check_interval=5.0,
    max_json_size=10 * 1024 * 1024,
    max_json_depth=100,
    camouflage_mode=True,
    stealth_proxy=False,
    http2_enabled=True,
    route_recording=True,
    adaptive_timeout=True,
    failure_prediction=True,
)

session = Session(security_config=config)
response = session.get('https://httpbin.org/get')
print(f"Fully secured request: {response.status_code}")
```

### Test 81: Global Configuration
```python
import requests
from requests import SecurityConfig, set_global_config, get_global_config

config = SecurityConfig(rate_limit=50, camouflage_mode=True)
set_global_config(config)

current = get_global_config()
print(f"Rate limit: {current.rate_limit}")
print(f"Camouflage: {current.camouflage_mode}")
```

### Test 82: Error Handling Suite
```python
import requests

errors_to_test = [
    (requests.ConnectionError, "Connection failed"),
    (requests.Timeout, "Request timed out"),
    (requests.HTTPError, "HTTP error"),
    (requests.SSRFDetected, "SSRF blocked"),
    (requests.DNSRebindingDetected, "DNS rebinding"),
    (requests.ResponseTooLarge, "Response too large"),
    (requests.RateLimitExceeded, "Rate limited"),
    (requests.BlockedDomain, "Domain blocked"),
    (requests.BlockedPort, "Port blocked"),
]

for error_class, description in errors_to_test:
    print(f"{error_class.__name__}: {description}")
```

### Test 83: Version Information
```python
import requests

print(f"ReqGuard Version: {requests.__version__}")
print(f"Title: {requests.__title__}")
print(f"Author: {requests.__author__}")
```

### Test 84: Help Information
```python
import requests

info = requests.help.info()
print(f"Platform: {info['platform']}")
print(f"Python: {info['implementation']}")
```

---

## Exception Reference

| Exception | Description |
|-----------|-------------|
| `SSRFDetected` | Server-Side Request Forgery attempt blocked |
| `DNSRebindingDetected` | DNS rebinding attack detected |
| `UnsafeRedirectError` | Unsafe redirect (HTTPS to HTTP) blocked |
| `ResponseTooLarge` | Response exceeds size limit |
| `SlowlorisDetected` | Slow connection attack detected |
| `RateLimitExceeded` | Rate limit exceeded |
| `InsecureVerifyFalse` | SSL verification disabled warning |
| `BlockedDomain` | Domain is in blocklist |
| `BlockedPort` | Port is not in allowed list |
| `ProtocolSmugglingDetected` | Protocol smuggling attempt |
| `JSONBombDetected` | JSON bomb or deep nesting |
| `ZipBombDetected` | Decompression bomb detected |
| `MemoryLimitExceeded` | Memory usage limit exceeded |
| `TimeoutRequired` | Timeout is mandatory |
| `UserAgentViolation` | User-Agent violation detected |

---

## Security Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `verify_ssl` | bool | True | Enable SSL verification |
| `allow_verify_false` | bool | False | Allow disabling SSL |
| `max_response_size` | int | 100MB | Maximum response size |
| `ssrf_protection` | bool | True | Block private IPs |
| `dns_rebinding_protection` | bool | True | Detect DNS rebinding |
| `safe_redirects` | bool | True | Block unsafe redirects |
| `max_redirects` | int | 10 | Maximum redirects |
| `default_timeout` | tuple | (10, 30) | Connect/read timeout |
| `force_timeout` | bool | True | Require timeout |
| `rate_limit` | int | None | Requests per window |
| `rate_limit_window` | float | 1.0 | Rate limit window (s) |
| `allowed_ports` | set | {80, 443, 8080, 8443} | Allowed ports |
| `blocked_ports` | set | {} | Blocked ports |
| `allowed_domains` | set | None | Domain allowlist |
| `blocked_domains` | set | {} | Domain blocklist |
| `allowed_schemes` | set | {http, https} | Allowed schemes |
| `camouflage_mode` | bool | False | Browser impersonation |
| `stealth_proxy` | bool | False | Stealth proxy mode |
| `http2_enabled` | bool | True | Enable HTTP/2 |
| `http3_enabled` | bool | False | Enable HTTP/3 |
| `route_recording` | bool | False | Log all requests |
| `adaptive_timeout` | bool | True | Auto-adjust timeouts |
| `failure_prediction` | bool | True | Predict failures |

---

## Contributing

Contributions are welcome. Please contact:
- Telegram: [@QP4RM](https://t.me/QP4RM)
- GitHub: [x6-u](https://github.com/x6-u)

---

## License

Apache-2.0 License

---

## Changelog

### Version 1.2.0
- Initial release of ReqGuard
- 30+ security features
- Full backward compatibility with requests library
- Plugin system with hooks and middleware
- Route recording and secure logging
- Adaptive timeout and failure prediction
- Camouflage mode for stealth requests
- HTTP/2 and HTTP/3 support ready

---

**ReqGuard** - Security First HTTP Library for Python

Created by mero | Telegram: @QP4RM | GitHub: x6-u
