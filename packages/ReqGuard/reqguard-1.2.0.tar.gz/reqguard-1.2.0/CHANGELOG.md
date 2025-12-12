# Changelog

## [1.2.0] - 2024-12

### Security Features
- SSL/TLS verification warnings
- Response size limits (100MB default)
- SSRF protection (blocks private IPs)
- Mandatory timeout enforcement
- Rate limiting
- DNS rebinding protection
- Port restrictions
- Protocol smuggling protection
- Scheme validation
- Domain allowlist/blocklist
- JSON bomb protection
- Zip bomb protection
- Slowloris detection
- Redirect security
- Header sanitization
- Memory limits
- Adaptive timeouts
- Failure prediction
- Camouflage mode
- Plugin system
- Route recording
- Secure logging
- Threat intelligence
- Behavioral analysis
- Correlation engine
- Threat scoring
- Deep inspection
- Entropy analysis
- Injection detection
- Sensitive data detection
- Request signing
- Certificate transparency

### Authentication
- HTTPBasicAuth
- HTTPDigestAuth
- HTTPBearerAuth
- APIKeyAuth
- HMACAuth
- OAuth2Auth

### Protocol Support
- HTTP/1.1
- HTTP/2
- HTTP/3 ready

### Initial Release
- Full backward compatibility with requests library
- Python 3.6-3.14 support
