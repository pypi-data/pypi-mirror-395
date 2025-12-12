import hashlib
import hmac
import math
import random
import re
import socket
import struct
import threading
import time
import zlib
from collections import deque
from functools import wraps

try:
    import ipaddress
except ImportError:
    ipaddress = None

try:
    import json
except ImportError:
    import simplejson as json

try:
    from urllib.parse import urlparse, parse_qs, urlencode
except ImportError:
    from urlparse import urlparse, parse_qs
    from urllib import urlencode

from .exceptions import (
    SSRFDetected,
    DNSRebindingDetected,
    UnsafeRedirectError,
    ResponseTooLarge,
    SlowlorisDetected,
    RateLimitExceeded,
    InsecureVerifyFalse,
    BlockedDomain,
    BlockedPort,
    ProtocolSmugglingDetected,
    JSONBombDetected,
    ZipBombDetected,
    MemoryLimitExceeded,
    TimeoutRequired,
    UserAgentViolation,
    ThreatDetected,
    AnomalyDetected,
    FingerprintMismatch,
    CertificateTransparencyError,
    DataLeakageDetected,
    MaliciousPayloadDetected,
    BehaviorAnomalyDetected,
    EntropyAnomalyDetected,
    TimingAttackDetected,
    InjectionAttemptDetected,
    InsecureRequestWarning,
    SSRFWarning,
    SecurityWarning,
)


PRIVATE_IPV4_RANGES = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255"),
    ("127.0.0.0", "127.255.255.255"),
    ("169.254.0.0", "169.254.255.255"),
    ("0.0.0.0", "0.255.255.255"),
    ("100.64.0.0", "100.127.255.255"),
    ("192.0.0.0", "192.0.0.255"),
    ("192.0.2.0", "192.0.2.255"),
    ("198.18.0.0", "198.19.255.255"),
    ("198.51.100.0", "198.51.100.255"),
    ("203.0.113.0", "203.0.113.255"),
    ("224.0.0.0", "239.255.255.255"),
    ("240.0.0.0", "255.255.255.255"),
]

ALLOWED_PORTS = set([80, 443, 8080, 8443])

ALLOWED_SCHEMES = set(["http", "https"])

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]

SENSITIVE_HEADERS = [
    "authorization",
    "proxy-authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
    "x-csrf-token",
    "x-access-token",
    "x-secret-key",
    "x-private-key",
    "bearer",
    "token",
]

INJECTION_PATTERNS = [
    r"(?i)(\%27)|(\')|(\-\-)|(\%23)|(#)",
    r"(?i)((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))",
    r"(?i)\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
    r"(?i)((\%27)|(\'))union",
    r"(?i)exec(\s|\+)+(s|x)p\w+",
    r"(?i)<script[^>]*>",
    r"(?i)javascript:",
    r"(?i)on\w+\s*=",
    r"(?i)data:",
    r"(?i)vbscript:",
]

MALICIOUS_EXTENSIONS = [
    ".exe", ".dll", ".bat", ".cmd", ".ps1", ".sh", ".php",
    ".jsp", ".asp", ".aspx", ".cgi", ".pl", ".py", ".rb",
]

SENSITIVE_DATA_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    r"\b(?:\d[ -]*?){13,16}\b",
    r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",
    r"(?i)(password|passwd|pwd|secret|key|token|api_key|apikey|auth)",
    r"\b[A-Fa-f0-9]{32}\b",
    r"\b[A-Fa-f0-9]{40}\b",
    r"\b[A-Fa-f0-9]{64}\b",
]


def ip_to_int(ip_str):
    try:
        parts = ip_str.split(".")
        if len(parts) != 4:
            return 0
        result = 0
        for part in parts:
            result = result * 256 + int(part)
        return result
    except (ValueError, AttributeError):
        return 0


def is_private_ip(ip_str):
    if ipaddress is not None:
        try:
            ip = ipaddress.ip_address(ip_str if isinstance(ip_str, str) else ip_str.decode("utf-8"))
            return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved
        except (ValueError, AttributeError):
            pass
    
    ip_int = ip_to_int(ip_str)
    if ip_int == 0:
        return False
    
    for start, end in PRIVATE_IPV4_RANGES:
        start_int = ip_to_int(start)
        end_int = ip_to_int(end)
        if start_int <= ip_int <= end_int:
            return True
    return False


def resolve_and_check_ip(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        is_private = is_private_ip(ip)
        return ip, is_private
    except socket.gaierror:
        return "", False


def calculate_entropy(data):
    if not data:
        return 0.0
    
    if isinstance(data, bytes):
        data = data.decode("utf-8", errors="ignore")
    
    freq = {}
    for char in data:
        freq[char] = freq.get(char, 0) + 1
    
    length = float(len(data))
    entropy = 0.0
    for count in freq.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log(probability, 2)
    
    return entropy


def detect_injection(data):
    if not data:
        return False, None
    
    if isinstance(data, bytes):
        data = data.decode("utf-8", errors="ignore")
    
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, data):
            return True, pattern
    return False, None


def detect_sensitive_data(data):
    if not data:
        return []
    
    if isinstance(data, bytes):
        data = data.decode("utf-8", errors="ignore")
    
    matches = []
    for pattern in SENSITIVE_DATA_PATTERNS:
        found = re.findall(pattern, data)
        if found:
            matches.extend(found)
    return matches


def compute_request_hash(method, url, headers, body):
    hasher = hashlib.sha256()
    hasher.update(method.encode("utf-8") if isinstance(method, str) else method)
    hasher.update(url.encode("utf-8") if isinstance(url, str) else url)
    
    if headers:
        sorted_headers = sorted(headers.items()) if hasattr(headers, "items") else sorted(headers)
        for key, value in sorted_headers:
            if key.lower() not in SENSITIVE_HEADERS:
                hasher.update(str(key).encode("utf-8"))
                hasher.update(str(value).encode("utf-8"))
    
    if body:
        if isinstance(body, str):
            hasher.update(body.encode("utf-8"))
        elif isinstance(body, bytes):
            hasher.update(body)
    
    return hasher.hexdigest()


def generate_request_signature(secret_key, method, url, timestamp):
    message = "{0}:{1}:{2}".format(method, url, timestamp)
    if isinstance(message, str):
        message = message.encode("utf-8")
    if isinstance(secret_key, str):
        secret_key = secret_key.encode("utf-8")
    return hmac.new(secret_key, message, hashlib.sha256).hexdigest()


def verify_request_signature(secret_key, method, url, timestamp, signature, max_age=300):
    current_time = time.time()
    if abs(current_time - float(timestamp)) > max_age:
        return False
    expected = generate_request_signature(secret_key, method, url, timestamp)
    return hmac.compare_digest(expected, signature)


class SecurityConfig(object):
    def __init__(
        self,
        verify_ssl=True,
        allow_verify_false=False,
        max_response_size=104857600,
        ssrf_protection=True,
        dns_rebinding_protection=True,
        safe_redirects=True,
        max_redirects=10,
        default_timeout=(10.0, 30.0),
        force_timeout=True,
        rate_limit=None,
        rate_limit_window=1.0,
        allowed_ports=None,
        blocked_ports=None,
        allowed_domains=None,
        blocked_domains=None,
        allowed_schemes=None,
        slowloris_min_speed=1024,
        slowloris_check_interval=5.0,
        max_memory=None,
        max_json_size=10485760,
        max_json_depth=100,
        user_agent=None,
        user_agent_lock=False,
        camouflage_mode=False,
        stealth_proxy=False,
        http2_enabled=True,
        http3_enabled=False,
        plugin_hooks=None,
        route_recording=False,
        adaptive_timeout=True,
        failure_prediction=True,
        meta_protocol_enabled=False,
        meta_protocol_key=None,
        threat_intelligence=True,
        behavioral_analysis=True,
        entropy_analysis=True,
        injection_detection=True,
        dlp_enabled=True,
        anomaly_detection=True,
        timing_attack_protection=True,
        certificate_transparency=True,
        request_signing=False,
        request_signing_key=None,
        fingerprint_validation=True,
        deep_inspection=True,
        correlation_engine=True,
        threat_scoring=True,
        auto_block_threats=True,
        threat_score_threshold=0.7,
        max_request_body_size=10485760,
        decompress_limit=104857600,
        header_size_limit=8192,
        url_length_limit=2048,
        parameter_count_limit=100,
        cookie_count_limit=50,
        connection_pool_size=10,
        retry_limit=3,
        backoff_factor=0.5,
    ):
        self.verify_ssl = verify_ssl
        self.allow_verify_false = allow_verify_false
        self.max_response_size = max_response_size
        self.ssrf_protection = ssrf_protection
        self.dns_rebinding_protection = dns_rebinding_protection
        self.safe_redirects = safe_redirects
        self.max_redirects = max_redirects
        self.default_timeout = default_timeout
        self.force_timeout = force_timeout
        self.rate_limit = rate_limit
        self.rate_limit_window = rate_limit_window
        self.allowed_ports = allowed_ports if allowed_ports is not None else ALLOWED_PORTS.copy()
        self.blocked_ports = blocked_ports if blocked_ports is not None else set()
        self.allowed_domains = allowed_domains
        self.blocked_domains = blocked_domains if blocked_domains is not None else set()
        self.allowed_schemes = allowed_schemes if allowed_schemes is not None else ALLOWED_SCHEMES.copy()
        self.slowloris_min_speed = slowloris_min_speed
        self.slowloris_check_interval = slowloris_check_interval
        self.max_memory = max_memory
        self.max_json_size = max_json_size
        self.max_json_depth = max_json_depth
        self.user_agent = user_agent
        self.user_agent_lock = user_agent_lock
        self.camouflage_mode = camouflage_mode
        self.stealth_proxy = stealth_proxy
        self.http2_enabled = http2_enabled
        self.http3_enabled = http3_enabled
        self.plugin_hooks = plugin_hooks if plugin_hooks is not None else {}
        self.route_recording = route_recording
        self.adaptive_timeout = adaptive_timeout
        self.failure_prediction = failure_prediction
        self.meta_protocol_enabled = meta_protocol_enabled
        self.meta_protocol_key = meta_protocol_key
        self.threat_intelligence = threat_intelligence
        self.behavioral_analysis = behavioral_analysis
        self.entropy_analysis = entropy_analysis
        self.injection_detection = injection_detection
        self.dlp_enabled = dlp_enabled
        self.anomaly_detection = anomaly_detection
        self.timing_attack_protection = timing_attack_protection
        self.certificate_transparency = certificate_transparency
        self.request_signing = request_signing
        self.request_signing_key = request_signing_key
        self.fingerprint_validation = fingerprint_validation
        self.deep_inspection = deep_inspection
        self.correlation_engine = correlation_engine
        self.threat_scoring = threat_scoring
        self.auto_block_threats = auto_block_threats
        self.threat_score_threshold = threat_score_threshold
        self.max_request_body_size = max_request_body_size
        self.decompress_limit = decompress_limit
        self.header_size_limit = header_size_limit
        self.url_length_limit = url_length_limit
        self.parameter_count_limit = parameter_count_limit
        self.cookie_count_limit = cookie_count_limit
        self.connection_pool_size = connection_pool_size
        self.retry_limit = retry_limit
        self.backoff_factor = backoff_factor


class RateLimiter(object):
    def __init__(self, max_requests, window=1.0):
        self.max_requests = max_requests
        self.window = window
        self.requests = deque()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            while self.requests and self.requests[0] < now - self.window:
                self.requests.popleft()
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False

    def wait(self):
        while not self.acquire():
            time.sleep(0.01)

    def get_remaining(self):
        with self.lock:
            now = time.time()
            while self.requests and self.requests[0] < now - self.window:
                self.requests.popleft()
            return max(0, self.max_requests - len(self.requests))

    def reset(self):
        with self.lock:
            self.requests.clear()


class AdaptiveTimeout(object):
    def __init__(
        self,
        initial_connect=5.0,
        initial_read=10.0,
        min_connect=1.0,
        max_connect=30.0,
        min_read=2.0,
        max_read=60.0,
    ):
        self.connect_timeout = initial_connect
        self.read_timeout = initial_read
        self.min_connect = min_connect
        self.max_connect = max_connect
        self.min_read = min_read
        self.max_read = max_read
        self.history = deque(maxlen=100)
        self.lock = threading.Lock()
        self.ewma_connect = initial_connect
        self.ewma_read = initial_read
        self.alpha = 0.3

    def get_timeout(self):
        with self.lock:
            return (self.connect_timeout, self.read_timeout)

    def record_response(self, connect_time, read_time, success):
        with self.lock:
            self.history.append((connect_time, read_time, success, time.time()))
            
            self.ewma_connect = self.alpha * connect_time + (1 - self.alpha) * self.ewma_connect
            self.ewma_read = self.alpha * read_time + (1 - self.alpha) * self.ewma_read
            
            if len(self.history) >= 10:
                recent = list(self.history)[-10:]
                success_rate = sum(1 for r in recent if r[2]) / len(recent)
                
                if success_rate < 0.5:
                    self.connect_timeout = min(self.connect_timeout * 1.5, self.max_connect)
                    self.read_timeout = min(self.read_timeout * 1.5, self.max_read)
                elif success_rate > 0.9:
                    self.connect_timeout = max(self.ewma_connect * 2, self.min_connect)
                    self.read_timeout = max(self.ewma_read * 1.5, self.min_read)
                else:
                    self.connect_timeout = max(self.ewma_connect * 1.2, self.min_connect)
                    self.read_timeout = max(self.ewma_read * 1.2, self.min_read)


class RouteRecorder(object):
    def __init__(self, max_entries=10000):
        self.routes = deque(maxlen=max_entries)
        self.lock = threading.Lock()
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_bytes": 0,
            "avg_duration": 0.0,
        }

    def record(
        self,
        url,
        method,
        start_time,
        end_time,
        status_code,
        response_size,
        redirects,
        protocol,
        cipher=None,
        headers=None,
        error=None,
    ):
        with self.lock:
            duration = end_time - start_time
            entry = {
                "url": url,
                "method": method,
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
                "status_code": status_code,
                "response_size": response_size,
                "redirects": redirects,
                "protocol": protocol,
                "cipher": cipher,
                "error": str(error) if error else None,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.routes.append(entry)
            
            self.stats["total_requests"] += 1
            self.stats["total_bytes"] += response_size
            
            if status_code and status_code < 400:
                self.stats["successful_requests"] += 1
            else:
                self.stats["failed_requests"] += 1
            
            total = self.stats["total_requests"]
            self.stats["avg_duration"] = (
                (self.stats["avg_duration"] * (total - 1) + duration) / total
            )

    def export_json(self):
        with self.lock:
            return json.dumps(list(self.routes), indent=2)

    def get_stats(self):
        with self.lock:
            return dict(self.stats)

    def clear(self):
        with self.lock:
            self.routes.clear()
            self.stats = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_bytes": 0,
                "avg_duration": 0.0,
            }


class FailurePredictor(object):
    def __init__(self, history_size=1000):
        self.history = {}
        self.lock = threading.Lock()
        self.history_size = history_size

    def record(self, host, success, response_time, status_code=None):
        with self.lock:
            if host not in self.history:
                self.history[host] = {
                    "successes": 0,
                    "failures": 0,
                    "times": deque(maxlen=self.history_size),
                    "status_codes": deque(maxlen=self.history_size),
                    "last_failure": None,
                    "consecutive_failures": 0,
                }
            
            data = self.history[host]
            if success:
                data["successes"] += 1
                data["consecutive_failures"] = 0
            else:
                data["failures"] += 1
                data["last_failure"] = time.time()
                data["consecutive_failures"] += 1
            
            data["times"].append((response_time, time.time()))
            if status_code:
                data["status_codes"].append(status_code)

    def predict_failure(self, host):
        with self.lock:
            if host not in self.history:
                return 0.0
            
            data = self.history[host]
            total = data["successes"] + data["failures"]
            if total == 0:
                return 0.0
            
            base_failure_rate = data["failures"] / float(total)
            
            consecutive_penalty = min(data["consecutive_failures"] * 0.1, 0.5)
            
            time_factor = 0.0
            if data["last_failure"]:
                time_since_failure = time.time() - data["last_failure"]
                if time_since_failure < 60:
                    time_factor = 0.3 * (1 - time_since_failure / 60)
            
            latency_factor = 0.0
            if len(data["times"]) > 5:
                recent_times = [t[0] for t in list(data["times"])[-5:]]
                all_times = [t[0] for t in data["times"]]
                recent_avg = sum(recent_times) / len(recent_times)
                overall_avg = sum(all_times) / len(all_times)
                if overall_avg > 0 and recent_avg > overall_avg * 2:
                    latency_factor = min((recent_avg / overall_avg - 1) * 0.2, 0.3)
            
            failure_prob = base_failure_rate + consecutive_penalty + time_factor + latency_factor
            return min(failure_prob, 1.0)

    def should_retry(self, host):
        failure_prob = self.predict_failure(host)
        return failure_prob < 0.8

    def get_host_stats(self, host):
        with self.lock:
            if host not in self.history:
                return None
            return dict(self.history[host])


class BehavioralAnalyzer(object):
    def __init__(self, baseline_window=100):
        self.baseline = {}
        self.lock = threading.Lock()
        self.baseline_window = baseline_window
        self.anomaly_threshold = 3.0

    def record_behavior(self, host, metrics):
        with self.lock:
            if host not in self.baseline:
                self.baseline[host] = {
                    "response_times": deque(maxlen=self.baseline_window),
                    "response_sizes": deque(maxlen=self.baseline_window),
                    "status_codes": deque(maxlen=self.baseline_window),
                    "header_counts": deque(maxlen=self.baseline_window),
                }
            
            data = self.baseline[host]
            if "response_time" in metrics:
                data["response_times"].append(metrics["response_time"])
            if "response_size" in metrics:
                data["response_sizes"].append(metrics["response_size"])
            if "status_code" in metrics:
                data["status_codes"].append(metrics["status_code"])
            if "header_count" in metrics:
                data["header_counts"].append(metrics["header_count"])

    def detect_anomaly(self, host, metrics):
        with self.lock:
            if host not in self.baseline:
                return False, []
            
            data = self.baseline[host]
            anomalies = []
            
            if "response_time" in metrics and len(data["response_times"]) >= 10:
                times = list(data["response_times"])
                mean = sum(times) / len(times)
                variance = sum((x - mean) ** 2 for x in times) / len(times)
                std = math.sqrt(variance) if variance > 0 else 1
                if std > 0:
                    z_score = (metrics["response_time"] - mean) / std
                    if abs(z_score) > self.anomaly_threshold:
                        anomalies.append(("response_time", z_score))
            
            if "response_size" in metrics and len(data["response_sizes"]) >= 10:
                sizes = list(data["response_sizes"])
                mean = sum(sizes) / len(sizes)
                variance = sum((x - mean) ** 2 for x in sizes) / len(sizes)
                std = math.sqrt(variance) if variance > 0 else 1
                if std > 0:
                    z_score = (metrics["response_size"] - mean) / std
                    if abs(z_score) > self.anomaly_threshold:
                        anomalies.append(("response_size", z_score))
            
            return len(anomalies) > 0, anomalies


class ThreatIntelligence(object):
    def __init__(self):
        self.threat_db = {}
        self.lock = threading.Lock()
        self.threat_signatures = []
        self.ip_reputation = {}
        self.domain_reputation = {}

    def add_threat_signature(self, signature, severity, description):
        with self.lock:
            self.threat_signatures.append({
                "signature": signature,
                "severity": severity,
                "description": description,
                "compiled": re.compile(signature, re.IGNORECASE) if isinstance(signature, str) else signature,
            })

    def check_threat(self, data):
        if not data:
            return False, None
        
        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="ignore")
        
        with self.lock:
            for threat in self.threat_signatures:
                if threat["compiled"].search(data):
                    return True, threat
        return False, None

    def set_ip_reputation(self, ip, score, reason=None):
        with self.lock:
            self.ip_reputation[ip] = {
                "score": score,
                "reason": reason,
                "updated": time.time(),
            }

    def get_ip_reputation(self, ip):
        with self.lock:
            return self.ip_reputation.get(ip, {"score": 0.5, "reason": None})

    def set_domain_reputation(self, domain, score, reason=None):
        with self.lock:
            self.domain_reputation[domain] = {
                "score": score,
                "reason": reason,
                "updated": time.time(),
            }

    def get_domain_reputation(self, domain):
        with self.lock:
            return self.domain_reputation.get(domain, {"score": 0.5, "reason": None})


class CorrelationEngine(object):
    def __init__(self, window_size=100):
        self.events = deque(maxlen=window_size)
        self.lock = threading.Lock()
        self.rules = []
        self.alert_callbacks = []

    def add_event(self, event_type, source, data):
        with self.lock:
            event = {
                "type": event_type,
                "source": source,
                "data": data,
                "timestamp": time.time(),
            }
            self.events.append(event)
            self._check_correlations(event)

    def add_rule(self, rule_name, condition_func, action_func):
        self.rules.append({
            "name": rule_name,
            "condition": condition_func,
            "action": action_func,
        })

    def _check_correlations(self, new_event):
        recent_events = list(self.events)
        for rule in self.rules:
            try:
                if rule["condition"](new_event, recent_events):
                    rule["action"](new_event, recent_events)
            except Exception:
                pass

    def add_alert_callback(self, callback):
        self.alert_callbacks.append(callback)


class ThreatScorer(object):
    def __init__(self):
        self.weights = {
            "ssrf_attempt": 1.0,
            "injection_attempt": 0.9,
            "sensitive_data_leak": 0.8,
            "anomaly_detected": 0.6,
            "high_entropy": 0.4,
            "malicious_extension": 0.7,
            "rate_limit_exceeded": 0.3,
            "timing_anomaly": 0.5,
            "behavioral_anomaly": 0.6,
            "unknown_threat": 0.5,
        }
        self.lock = threading.Lock()

    def calculate_score(self, threats):
        if not threats:
            return 0.0
        
        with self.lock:
            total_score = 0.0
            for threat_type, severity in threats:
                weight = self.weights.get(threat_type, self.weights["unknown_threat"])
                total_score += weight * severity
            
            return min(total_score, 1.0)

    def set_weight(self, threat_type, weight):
        with self.lock:
            self.weights[threat_type] = weight


class DeepInspector(object):
    def __init__(self, config=None):
        self.config = config
        self.inspection_results = {}
        self.lock = threading.Lock()

    def inspect_request(self, method, url, headers, body):
        results = {
            "threats": [],
            "anomalies": [],
            "warnings": [],
            "score": 0.0,
        }
        
        if body:
            is_injection, pattern = detect_injection(body)
            if is_injection:
                results["threats"].append(("injection_attempt", 0.9))
        
        if body:
            sensitive = detect_sensitive_data(body)
            if sensitive:
                results["threats"].append(("sensitive_data_leak", 0.8))
                results["warnings"].append("Sensitive data detected in request body")
        
        if body:
            entropy = calculate_entropy(body)
            if entropy > 6.0:
                results["anomalies"].append(("high_entropy", entropy))
        
        if url:
            parsed = urlparse(url)
            path = parsed.path.lower()
            for ext in MALICIOUS_EXTENSIONS:
                if path.endswith(ext):
                    results["threats"].append(("malicious_extension", 0.7))
                    break
        
        if headers:
            header_size = sum(len(str(k)) + len(str(v)) for k, v in headers.items()) if hasattr(headers, "items") else 0
            if self.config and header_size > self.config.header_size_limit:
                results["warnings"].append("Header size exceeds limit")
        
        if url and self.config and len(url) > self.config.url_length_limit:
            results["warnings"].append("URL length exceeds limit")
        
        scorer = ThreatScorer()
        results["score"] = scorer.calculate_score(results["threats"])
        
        return results

    def inspect_response(self, status_code, headers, body, content_type=None):
        results = {
            "threats": [],
            "anomalies": [],
            "warnings": [],
            "score": 0.0,
        }
        
        if body and content_type and "json" in content_type.lower():
            try:
                if self.config and len(body) > self.config.max_json_size:
                    results["warnings"].append("JSON size exceeds limit")
            except Exception:
                pass
        
        if body:
            sensitive = detect_sensitive_data(body if isinstance(body, str) else body.decode("utf-8", errors="ignore"))
            if sensitive:
                results["warnings"].append("Sensitive data in response")
        
        scorer = ThreatScorer()
        results["score"] = scorer.calculate_score(results["threats"])
        
        return results


class CamouflageEngine(object):
    def __init__(self):
        self.current_ua_index = random.randint(0, len(USER_AGENTS) - 1)
        self.last_rotation = time.time()
        self.rotation_interval = 300
        self.lock = threading.Lock()

    def get_headers(self):
        with self.lock:
            now = time.time()
            if now - self.last_rotation > self.rotation_interval:
                self.current_ua_index = random.randint(0, len(USER_AGENTS) - 1)
                self.last_rotation = now
            
            accept_languages = ["en-US,en;q=0.9", "en-GB,en;q=0.9", "en;q=0.8"]
            
            headers = {
                "User-Agent": USER_AGENTS[self.current_ua_index],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": random.choice(accept_languages),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            }
            return headers

    def rotate_ua(self):
        with self.lock:
            self.current_ua_index = random.randint(0, len(USER_AGENTS) - 1)
            self.last_rotation = time.time()


class MetaProtocol(object):
    def __init__(self, key=None):
        if key is None:
            key = hashlib.sha256(str(time.time()).encode()).digest()
        self.key = key if isinstance(key, bytes) else key.encode("utf-8")

    def encode(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        
        encoded = bytearray()
        key_len = len(self.key)
        for i, b in enumerate(data):
            if isinstance(b, int):
                encoded.append(b ^ self.key[i % key_len])
            else:
                encoded.append(ord(b) ^ self.key[i % key_len])
        return bytes(encoded)

    def decode(self, data):
        return self.encode(data)


class SlowlorisDetector(object):
    def __init__(self, min_speed=1024, check_interval=5.0):
        self.min_speed = min_speed
        self.check_interval = check_interval
        self.bytes_received = 0
        self.start_time = None
        self.last_check = None
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            self.start_time = time.time()
            self.last_check = self.start_time
            self.bytes_received = 0

    def add_bytes(self, count):
        with self.lock:
            self.bytes_received += count
            now = time.time()
            if now - self.last_check >= self.check_interval:
                elapsed = now - self.start_time
                if elapsed > 0:
                    speed = self.bytes_received / elapsed
                    if speed < self.min_speed:
                        raise SlowlorisDetected(
                            "Slowloris detected: {0:.2f} bytes/sec < {1}".format(speed, self.min_speed)
                        )
                self.last_check = now


class PluginManager(object):
    def __init__(self):
        self.hooks = {
            "pre_request": [],
            "post_request": [],
            "pre_send": [],
            "post_receive": [],
            "on_error": [],
            "on_redirect": [],
            "header_validator": [],
            "auth_handler": [],
            "threat_handler": [],
            "response_validator": [],
        }
        self.middlewares = []
        self.validators = []
        self.interceptors = []
        self.lock = threading.Lock()

    def register_hook(self, hook_name, callback):
        with self.lock:
            if hook_name in self.hooks:
                self.hooks[hook_name].append(callback)

    def unregister_hook(self, hook_name, callback):
        with self.lock:
            if hook_name in self.hooks and callback in self.hooks[hook_name]:
                self.hooks[hook_name].remove(callback)

    def execute_hooks(self, hook_name, *args, **kwargs):
        result = None
        hooks = None
        with self.lock:
            hooks = list(self.hooks.get(hook_name, []))
        
        for callback in hooks:
            try:
                result = callback(*args, **kwargs)
            except Exception:
                pass
        return result

    def add_middleware(self, middleware):
        with self.lock:
            self.middlewares.append(middleware)

    def add_validator(self, validator):
        with self.lock:
            self.validators.append(validator)

    def add_interceptor(self, interceptor):
        with self.lock:
            self.interceptors.append(interceptor)

    def run_middlewares(self, request):
        middlewares = None
        with self.lock:
            middlewares = list(self.middlewares)
        
        for middleware in middlewares:
            request = middleware(request)
        return request

    def run_validators(self, request):
        validators = None
        with self.lock:
            validators = list(self.validators)
        
        for validator in validators:
            if not validator(request):
                return False
        return True

    def run_interceptors(self, headers):
        interceptors = None
        with self.lock:
            interceptors = list(self.interceptors)
        
        for interceptor in interceptors:
            headers = interceptor(headers)
        return headers


class SecureLogger(object):
    def __init__(self, enabled=True, max_entries=10000):
        self.enabled = enabled
        self.logs = deque(maxlen=max_entries)
        self.lock = threading.Lock()

    def log(
        self,
        method,
        url,
        status_code,
        response_size,
        duration,
        ip=None,
        headers=None,
        threats=None,
    ):
        if not self.enabled:
            return
        
        with self.lock:
            entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "method": method,
                "url": self._sanitize_url(url),
                "status_code": status_code,
                "response_size": response_size,
                "duration_ms": round(duration * 1000, 2),
            }
            if ip:
                entry["ip"] = ip
            if headers:
                entry["headers"] = sanitize_headers_for_logging(headers)
            if threats:
                entry["threats"] = threats
            self.logs.append(entry)

    def _sanitize_url(self, url):
        parsed = urlparse(url)
        if parsed.password:
            return url.replace(parsed.password, "[REDACTED]")
        return url

    def get_logs(self):
        with self.lock:
            return list(self.logs)

    def clear(self):
        with self.lock:
            self.logs.clear()

    def export_json(self):
        with self.lock:
            return json.dumps(list(self.logs), indent=2)


def validate_url_security(url, config):
    parsed = urlparse(url)
    
    scheme = parsed.scheme.lower() if parsed.scheme else ""
    if scheme not in config.allowed_schemes:
        raise SSRFDetected("Scheme not allowed: {0}".format(scheme))
    
    if "@" in (parsed.netloc or ""):
        raise ProtocolSmugglingDetected("Protocol smuggling detected: @ in URL")
    
    hostname = parsed.hostname
    if not hostname:
        raise SSRFDetected("No hostname in URL")
    
    if config.blocked_domains and hostname in config.blocked_domains:
        raise BlockedDomain("Domain blocked: {0}".format(hostname))
    
    if config.allowed_domains and hostname not in config.allowed_domains:
        raise BlockedDomain("Domain not in allowlist: {0}".format(hostname))
    
    port = parsed.port
    if port is None:
        port = 443 if scheme == "https" else 80
    
    if port in config.blocked_ports:
        raise BlockedPort("Port blocked: {0}".format(port))
    
    if config.allowed_ports and port not in config.allowed_ports:
        raise BlockedPort("Port not allowed: {0}".format(port))
    
    if config.url_length_limit and len(url) > config.url_length_limit:
        raise SSRFDetected("URL length exceeds limit")
    
    if config.ssrf_protection:
        ip, is_private = resolve_and_check_ip(hostname)
        if is_private:
            raise SSRFDetected("SSRF detected: private IP {0}".format(ip))


def validate_redirect_security(original_url, redirect_url, config):
    original_parsed = urlparse(original_url)
    redirect_parsed = urlparse(redirect_url)
    
    if original_parsed.scheme == "https" and redirect_parsed.scheme == "http":
        raise UnsafeRedirectError("HTTPS to HTTP downgrade detected")
    
    redirect_scheme = redirect_parsed.scheme.lower() if redirect_parsed.scheme else ""
    if redirect_scheme not in config.allowed_schemes:
        raise UnsafeRedirectError("Redirect to unsafe scheme: {0}".format(redirect_scheme))
    
    if config.ssrf_protection:
        hostname = redirect_parsed.hostname
        if hostname:
            ip, is_private = resolve_and_check_ip(hostname)
            if is_private:
                raise SSRFDetected("SSRF via redirect: private IP {0}".format(ip))


def check_dns_rebinding(hostname, original_ip):
    try:
        current_ip = socket.gethostbyname(hostname)
        if current_ip != original_ip:
            if is_private_ip(current_ip):
                raise DNSRebindingDetected(
                    "DNS rebinding detected: {0} resolved to {1}".format(hostname, current_ip)
                )
    except socket.gaierror:
        pass


def sanitize_headers_for_logging(headers):
    sanitized = {}
    if not headers:
        return sanitized
    
    items = headers.items() if hasattr(headers, "items") else headers
    for key, value in items:
        if key.lower() in SENSITIVE_HEADERS:
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    return sanitized


def validate_json_safety(data, max_size=None, max_depth=100):
    if max_size and len(data) > max_size:
        raise JSONBombDetected("JSON size exceeds limit: {0} > {1}".format(len(data), max_size))
    
    def check_depth(obj, depth=0):
        if depth > max_depth:
            raise JSONBombDetected("JSON depth exceeds limit: {0}".format(max_depth))
        if isinstance(obj, dict):
            max_child = depth
            for v in obj.values():
                child_depth = check_depth(v, depth + 1)
                if child_depth > max_child:
                    max_child = child_depth
            return max_child
        elif isinstance(obj, list):
            max_child = depth
            for item in obj:
                child_depth = check_depth(item, depth + 1)
                if child_depth > max_child:
                    max_child = child_depth
            return max_child
        return depth
    
    parsed = json.loads(data)
    check_depth(parsed)
    return parsed


def check_decompression_bomb(data, max_ratio=100, max_size=None):
    if not data:
        return data
    
    compressed_size = len(data)
    
    try:
        decompressed = zlib.decompress(data, 16 + zlib.MAX_WBITS)
        decompressed_size = len(decompressed)
        
        if max_size and decompressed_size > max_size:
            raise ZipBombDetected("Decompressed size exceeds limit")
        
        if compressed_size > 0:
            ratio = decompressed_size / float(compressed_size)
            if ratio > max_ratio:
                raise ZipBombDetected("Compression ratio too high: {0}".format(ratio))
        
        return decompressed
    except zlib.error:
        return data


DEFAULT_CONFIG = SecurityConfig()
GLOBAL_RATE_LIMITER = None
GLOBAL_ADAPTIVE_TIMEOUT = AdaptiveTimeout()
GLOBAL_ROUTE_RECORDER = RouteRecorder()
GLOBAL_FAILURE_PREDICTOR = FailurePredictor()
GLOBAL_CAMOUFLAGE = CamouflageEngine()
GLOBAL_PLUGIN_MANAGER = PluginManager()
GLOBAL_LOGGER = SecureLogger()
GLOBAL_THREAT_INTELLIGENCE = ThreatIntelligence()
GLOBAL_BEHAVIORAL_ANALYZER = BehavioralAnalyzer()
GLOBAL_CORRELATION_ENGINE = CorrelationEngine()
GLOBAL_THREAT_SCORER = ThreatScorer()
GLOBAL_DEEP_INSPECTOR = DeepInspector()


def set_global_config(config):
    global DEFAULT_CONFIG, GLOBAL_RATE_LIMITER, GLOBAL_DEEP_INSPECTOR
    DEFAULT_CONFIG = config
    if config.rate_limit:
        GLOBAL_RATE_LIMITER = RateLimiter(config.rate_limit, config.rate_limit_window)
    GLOBAL_DEEP_INSPECTOR = DeepInspector(config)


def get_global_config():
    return DEFAULT_CONFIG
