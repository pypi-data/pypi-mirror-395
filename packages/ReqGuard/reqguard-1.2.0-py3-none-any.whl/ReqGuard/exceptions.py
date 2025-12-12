from urllib3.exceptions import HTTPError as BaseHTTPError

from .compat import JSONDecodeError as CompatJSONDecodeError


class RequestException(IOError):
    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = self.response.request
        super(RequestException, self).__init__(*args, **kwargs)


class InvalidJSONError(RequestException):
    pass


class JSONDecodeError(InvalidJSONError, CompatJSONDecodeError):
    def __init__(self, *args, **kwargs):
        CompatJSONDecodeError.__init__(self, *args)
        InvalidJSONError.__init__(self, *self.args, **kwargs)

    def __reduce__(self):
        return CompatJSONDecodeError.__reduce__(self)


class HTTPError(RequestException):
    pass


class ConnectionError(RequestException):
    pass


class ProxyError(ConnectionError):
    pass


class SSLError(ConnectionError):
    pass


class Timeout(RequestException):
    pass


class ConnectTimeout(ConnectionError, Timeout):
    pass


class ReadTimeout(Timeout):
    pass


class URLRequired(RequestException):
    pass


class TooManyRedirects(RequestException):
    pass


class MissingSchema(RequestException, ValueError):
    pass


class InvalidSchema(RequestException, ValueError):
    pass


class InvalidURL(RequestException, ValueError):
    pass


class InvalidHeader(RequestException, ValueError):
    pass


class InvalidProxyURL(InvalidURL):
    pass


class ChunkedEncodingError(RequestException):
    pass


class ContentDecodingError(RequestException, BaseHTTPError):
    pass


class StreamConsumedError(RequestException, TypeError):
    pass


class RetryError(RequestException):
    pass


class UnrewindableBodyError(RequestException):
    pass


class SSRFDetected(RequestException):
    pass


class DNSRebindingDetected(RequestException):
    pass


class UnsafeRedirectError(RequestException):
    pass


class ResponseTooLarge(RequestException):
    pass


class SlowlorisDetected(RequestException):
    pass


class RateLimitExceeded(RequestException):
    pass


class InsecureVerifyFalse(RequestException):
    pass


class BlockedDomain(RequestException):
    pass


class BlockedPort(RequestException):
    pass


class ProtocolSmugglingDetected(RequestException):
    pass


class JSONBombDetected(RequestException):
    pass


class ZipBombDetected(RequestException):
    pass


class MemoryLimitExceeded(RequestException):
    pass


class TimeoutRequired(RequestException):
    pass


class UserAgentViolation(RequestException):
    pass


class ThreatDetected(RequestException):
    pass


class AnomalyDetected(RequestException):
    pass


class FingerprintMismatch(RequestException):
    pass


class CertificateTransparencyError(RequestException):
    pass


class DataLeakageDetected(RequestException):
    pass


class MaliciousPayloadDetected(RequestException):
    pass


class BehaviorAnomalyDetected(RequestException):
    pass


class EntropyAnomalyDetected(RequestException):
    pass


class TimingAttackDetected(RequestException):
    pass


class InjectionAttemptDetected(RequestException):
    pass


class RequestsWarning(Warning):
    pass


class FileModeWarning(RequestsWarning, DeprecationWarning):
    pass


class RequestsDependencyWarning(RequestsWarning):
    pass


class InsecureRequestWarning(RequestsWarning):
    pass


class SSRFWarning(RequestsWarning):
    pass


class SecurityWarning(RequestsWarning):
    pass
