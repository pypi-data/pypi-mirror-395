import warnings

import urllib3

from .exceptions import RequestsDependencyWarning

try:
    from charset_normalizer import __version__ as charset_normalizer_version
except ImportError:
    charset_normalizer_version = None

try:
    from chardet import __version__ as chardet_version
except ImportError:
    chardet_version = None


def check_compatibility(urllib3_version, chardet_version, charset_normalizer_version):
    urllib3_version = urllib3_version.split(".")
    if urllib3_version == ["dev"]:
        return

    if len(urllib3_version) == 2:
        urllib3_version.append("0")

    major, minor, patch = urllib3_version
    major, minor, patch = int(major), int(minor), int(patch)
    if major < 1:
        return
    if major == 1 and minor < 21:
        return

    if chardet_version:
        parts = chardet_version.split(".")[:3]
        if len(parts) >= 3:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if charset_normalizer_version:
        parts = charset_normalizer_version.split(".")[:3]
        if len(parts) >= 3:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])


def _check_cryptography(cryptography_version):
    try:
        cryptography_version = list(map(int, cryptography_version.split(".")))
    except ValueError:
        return

    if cryptography_version < [1, 3, 4]:
        warning = "Old version of cryptography ({0}) may cause slowdown.".format(
            cryptography_version
        )
        warnings.warn(warning, RequestsDependencyWarning)


try:
    check_compatibility(
        urllib3.__version__, chardet_version, charset_normalizer_version
    )
except (AssertionError, ValueError):
    warnings.warn(
        "urllib3 ({0}) or chardet ({1})/charset_normalizer ({2}) doesn't match a supported "
        "version!".format(
            urllib3.__version__, chardet_version, charset_normalizer_version
        ),
        RequestsDependencyWarning,
    )

try:
    try:
        import ssl
    except ImportError:
        ssl = None

    if ssl and not getattr(ssl, "HAS_SNI", False):
        try:
            from urllib3.contrib import pyopenssl
            pyopenssl.inject_into_urllib3()
            from cryptography import __version__ as cryptography_version
            _check_cryptography(cryptography_version)
        except ImportError:
            pass
except ImportError:
    pass

try:
    from urllib3.exceptions import DependencyWarning
    warnings.simplefilter("ignore", DependencyWarning)
except ImportError:
    pass

import logging
from logging import NullHandler

from . import packages, utils
from .__version__ import (
    __author__,
    __author_email__,
    __build__,
    __cake__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from .api import delete, get, head, options, patch, post, put, request
from .exceptions import (
    ConnectionError,
    ConnectTimeout,
    FileModeWarning,
    HTTPError,
    JSONDecodeError,
    ReadTimeout,
    RequestException,
    Timeout,
    TooManyRedirects,
    URLRequired,
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
from .models import PreparedRequest, Request, Response
from .sessions import Session, session
from .status_codes import codes
from .security import (
    SecurityConfig,
    RateLimiter,
    AdaptiveTimeout,
    RouteRecorder,
    FailurePredictor,
    CamouflageEngine,
    MetaProtocol,
    PluginManager,
    SecureLogger,
    SlowlorisDetector,
    ThreatIntelligence,
    BehavioralAnalyzer,
    CorrelationEngine,
    ThreatScorer,
    DeepInspector,
    set_global_config,
    get_global_config,
    validate_url_security,
    validate_redirect_security,
    check_dns_rebinding,
    sanitize_headers_for_logging,
    validate_json_safety,
    is_private_ip,
    resolve_and_check_ip,
    calculate_entropy,
    detect_injection,
    detect_sensitive_data,
    compute_request_hash,
    generate_request_signature,
    verify_request_signature,
    check_decompression_bomb,
    GLOBAL_RATE_LIMITER,
    GLOBAL_ADAPTIVE_TIMEOUT,
    GLOBAL_ROUTE_RECORDER,
    GLOBAL_FAILURE_PREDICTOR,
    GLOBAL_CAMOUFLAGE,
    GLOBAL_PLUGIN_MANAGER,
    GLOBAL_LOGGER,
    GLOBAL_THREAT_INTELLIGENCE,
    GLOBAL_BEHAVIORAL_ANALYZER,
    GLOBAL_CORRELATION_ENGINE,
    GLOBAL_THREAT_SCORER,
    GLOBAL_DEEP_INSPECTOR,
)

logging.getLogger(__name__).addHandler(NullHandler())

warnings.simplefilter("default", FileModeWarning, append=True)
