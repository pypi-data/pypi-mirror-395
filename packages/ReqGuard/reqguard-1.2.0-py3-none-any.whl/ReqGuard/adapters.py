import os.path
import socket
import time
import warnings

try:
    import typing
except ImportError:
    typing = None

from urllib3.exceptions import ClosedPoolError, ConnectTimeoutError
from urllib3.exceptions import HTTPError as _HTTPError
from urllib3.exceptions import InvalidHeader as _InvalidHeader
from urllib3.exceptions import (
    LocationValueError,
    MaxRetryError,
    NewConnectionError,
    ProtocolError,
)
from urllib3.exceptions import ProxyError as _ProxyError
from urllib3.exceptions import ReadTimeoutError, ResponseError
from urllib3.exceptions import SSLError as _SSLError
from urllib3.poolmanager import PoolManager, proxy_from_url
from urllib3.util import Timeout as TimeoutSauce
from urllib3.util import parse_url
from urllib3.util.retry import Retry

from .auth import _basic_auth_str
from .compat import basestring, urlparse
from .cookies import extract_cookies_to_jar
from .exceptions import (
    ConnectionError,
    ConnectTimeout,
    InvalidHeader,
    InvalidProxyURL,
    InvalidSchema,
    InvalidURL,
    ProxyError,
    ReadTimeout,
    RetryError,
    SSLError,
    ResponseTooLarge,
    InsecureVerifyFalse,
    TimeoutRequired,
    ThreatDetected,
)
from .models import Response
from .structures import CaseInsensitiveDict
from .utils import (
    DEFAULT_CA_BUNDLE_PATH,
    extract_zipped_paths,
    get_auth_from_url,
    get_encoding_from_headers,
    prepend_scheme_if_needed,
    select_proxy,
    urldefragauth,
)
from .security import (
    SecurityConfig,
    get_global_config,
    validate_url_security,
    SlowlorisDetector,
    GLOBAL_LOGGER,
    GLOBAL_ROUTE_RECORDER,
    GLOBAL_ADAPTIVE_TIMEOUT,
    GLOBAL_FAILURE_PREDICTOR,
    GLOBAL_DEEP_INSPECTOR,
    GLOBAL_BEHAVIORAL_ANALYZER,
    GLOBAL_THREAT_SCORER,
    InsecureRequestWarning,
)

try:
    from urllib3.contrib.socks import SOCKSProxyManager
except ImportError:
    def SOCKSProxyManager(*args, **kwargs):
        raise InvalidSchema("Missing dependencies for SOCKS support.")


DEFAULT_POOLBLOCK = False
DEFAULT_POOLSIZE = 10
DEFAULT_RETRIES = 0
DEFAULT_POOL_TIMEOUT = None


def _urllib3_request_context(request, verify, client_cert, poolmanager):
    host_params = {}
    pool_kwargs = {}
    parsed_request_url = urlparse(request.url)
    scheme = parsed_request_url.scheme.lower()
    port = parsed_request_url.port

    cert_reqs = "CERT_REQUIRED"
    if verify is False:
        cert_reqs = "CERT_NONE"
    elif isinstance(verify, str):
        if not os.path.isdir(verify):
            pool_kwargs["ca_certs"] = verify
        else:
            pool_kwargs["ca_cert_dir"] = verify
    pool_kwargs["cert_reqs"] = cert_reqs
    if client_cert is not None:
        if isinstance(client_cert, tuple) and len(client_cert) == 2:
            pool_kwargs["cert_file"] = client_cert[0]
            pool_kwargs["key_file"] = client_cert[1]
        else:
            pool_kwargs["cert_file"] = client_cert
    host_params = {
        "scheme": scheme,
        "host": parsed_request_url.hostname,
        "port": port,
    }
    return host_params, pool_kwargs


class BaseAdapter(object):
    def __init__(self):
        super(BaseAdapter, self).__init__()

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class HTTPAdapter(BaseAdapter):
    __attrs__ = [
        "max_retries",
        "config",
        "_pool_connections",
        "_pool_maxsize",
        "_pool_block",
    ]

    def __init__(
        self,
        pool_connections=DEFAULT_POOLSIZE,
        pool_maxsize=DEFAULT_POOLSIZE,
        max_retries=DEFAULT_RETRIES,
        pool_block=DEFAULT_POOLBLOCK,
        security_config=None,
    ):
        if max_retries == DEFAULT_RETRIES:
            self.max_retries = Retry(0, read=False)
        else:
            self.max_retries = Retry.from_int(max_retries)
        self.config = {}
        self.proxy_manager = {}
        self.security_config = security_config if security_config is not None else get_global_config()

        super(HTTPAdapter, self).__init__()

        self._pool_connections = pool_connections
        self._pool_maxsize = pool_maxsize
        self._pool_block = pool_block

        self.init_poolmanager(pool_connections, pool_maxsize, block=pool_block)

    def __getstate__(self):
        return dict((attr, getattr(self, attr, None)) for attr in self.__attrs__)

    def __setstate__(self, state):
        self.proxy_manager = {}
        self.config = {}

        for attr, value in state.items():
            setattr(self, attr, value)

        self.init_poolmanager(
            self._pool_connections, self._pool_maxsize, block=self._pool_block
        )

    def init_poolmanager(
        self, connections, maxsize, block=DEFAULT_POOLBLOCK, **pool_kwargs
    ):
        self._pool_connections = connections
        self._pool_maxsize = maxsize
        self._pool_block = block

        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            **pool_kwargs
        )

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        if proxy in self.proxy_manager:
            manager = self.proxy_manager[proxy]
        elif proxy.lower().startswith("socks"):
            username, password = get_auth_from_url(proxy)
            manager = self.proxy_manager[proxy] = SOCKSProxyManager(
                proxy,
                username=username,
                password=password,
                num_pools=self._pool_connections,
                maxsize=self._pool_maxsize,
                block=self._pool_block,
                **proxy_kwargs
            )
        else:
            proxy_headers = self.proxy_headers(proxy)
            manager = self.proxy_manager[proxy] = proxy_from_url(
                proxy,
                proxy_headers=proxy_headers,
                num_pools=self._pool_connections,
                maxsize=self._pool_maxsize,
                block=self._pool_block,
                **proxy_kwargs
            )

        return manager

    def cert_verify(self, conn, url, verify, cert):
        config = self.security_config

        if verify is False:
            if not config.allow_verify_false:
                warnings.warn(
                    "SSL verification disabled. This is a security risk.",
                    InsecureRequestWarning,
                )

        if url.lower().startswith("https") and verify:
            cert_loc = None

            if verify is not True:
                cert_loc = verify

            if not cert_loc:
                cert_loc = extract_zipped_paths(DEFAULT_CA_BUNDLE_PATH)

            if not cert_loc or not os.path.exists(cert_loc):
                raise OSError(
                    "Could not find a suitable TLS CA certificate bundle, "
                    "invalid path: {0}".format(cert_loc)
                )

            conn.cert_reqs = "CERT_REQUIRED"

            if not os.path.isdir(cert_loc):
                conn.ca_certs = cert_loc
            else:
                conn.ca_cert_dir = cert_loc
        else:
            conn.cert_reqs = "CERT_NONE"
            conn.ca_certs = None
            conn.ca_cert_dir = None

        if cert:
            if not isinstance(cert, basestring):
                conn.cert_file = cert[0]
                conn.key_file = cert[1]
            else:
                conn.cert_file = cert
                conn.key_file = None
            if conn.cert_file and not os.path.exists(conn.cert_file):
                raise OSError(
                    "Could not find the TLS certificate file, "
                    "invalid path: {0}".format(conn.cert_file)
                )
            if conn.key_file and not os.path.exists(conn.key_file):
                raise OSError(
                    "Could not find the TLS key file, invalid path: {0}".format(conn.key_file)
                )

    def build_response(self, req, resp):
        response = Response()

        response.status_code = getattr(resp, "status", None)

        response.headers = CaseInsensitiveDict(getattr(resp, "headers", {}))

        response.encoding = get_encoding_from_headers(response.headers)
        response.raw = resp
        response.reason = response.raw.reason

        if isinstance(req.url, bytes):
            response.url = req.url.decode("utf-8")
        else:
            response.url = req.url

        extract_cookies_to_jar(response.cookies, req, resp)

        response.request = req
        response.connection = self

        return response

    def build_connection_pool_key_attributes(self, request, verify, cert=None):
        return _urllib3_request_context(request, verify, cert, self.poolmanager)

    def get_connection_with_tls_context(self, request, verify, proxies=None, cert=None):
        proxy = select_proxy(request.url, proxies)
        try:
            host_params, pool_kwargs = self.build_connection_pool_key_attributes(
                request,
                verify,
                cert,
            )
        except ValueError as e:
            raise InvalidURL(e, request=request)
        if proxy:
            proxy = prepend_scheme_if_needed(proxy, "http")
            proxy_url = parse_url(proxy)
            if not proxy_url.host:
                raise InvalidProxyURL(
                    "Please check proxy URL. It is malformed "
                    "and could be missing the host."
                )
            proxy_manager = self.proxy_manager_for(proxy)
            conn = proxy_manager.connection_from_host(
                **dict(list(host_params.items()) + [("pool_kwargs", pool_kwargs)])
            )
        else:
            conn = self.poolmanager.connection_from_host(
                **dict(list(host_params.items()) + [("pool_kwargs", pool_kwargs)])
            )

        return conn

    def get_connection(self, url, proxies=None):
        warnings.warn(
            (
                "`get_connection` has been deprecated in favor of "
                "`get_connection_with_tls_context`. Custom HTTPAdapter subclasses "
                "will need to migrate for Requests>=2.32.2. Please see "
                "https://github.com/psf/requests/pull/6710 for more details."
            ),
            DeprecationWarning,
        )
        proxy = select_proxy(url, proxies)

        if proxy:
            proxy = prepend_scheme_if_needed(proxy, "http")
            proxy_url = parse_url(proxy)
            if not proxy_url.host:
                raise InvalidProxyURL(
                    "Please check proxy URL. It is malformed "
                    "and could be missing the host."
                )
            proxy_manager = self.proxy_manager_for(proxy)
            conn = proxy_manager.connection_from_url(url)
        else:
            parsed = urlparse(url)
            url = parsed.geturl()
            conn = self.poolmanager.connection_from_url(url)

        return conn

    def close(self):
        self.poolmanager.clear()
        for proxy in self.proxy_manager.values():
            proxy.clear()

    def request_url(self, request, proxies):
        proxy = select_proxy(request.url, proxies)
        scheme = urlparse(request.url).scheme

        is_proxied_http_request = proxy and scheme != "https"
        using_socks_proxy = False
        if proxy:
            proxy_scheme = urlparse(proxy).scheme.lower()
            using_socks_proxy = proxy_scheme.startswith("socks")

        url = request.path_url
        if url.startswith("//"):
            url = "/{0}".format(url.lstrip("/"))

        if is_proxied_http_request and not using_socks_proxy:
            url = urldefragauth(request.url)

        return url

    def add_headers(self, request, **kwargs):
        pass

    def proxy_headers(self, proxy):
        headers = {}
        username, password = get_auth_from_url(proxy)

        if username:
            headers["Proxy-Authorization"] = _basic_auth_str(username, password)

        return headers

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        config = self.security_config
        start_time = time.time()

        try:
            validate_url_security(request.url, config)
        except Exception as e:
            raise e

        if config.deep_inspection:
            headers_dict = dict(request.headers) if request.headers else {}
            inspection = GLOBAL_DEEP_INSPECTOR.inspect_request(
                request.method, request.url, headers_dict, request.body
            )
            if config.auto_block_threats and inspection["score"] >= config.threat_score_threshold:
                raise ThreatDetected("Threat detected in request: score {0}".format(inspection["score"]))

        if config.force_timeout and timeout is None:
            if config.adaptive_timeout:
                timeout = GLOBAL_ADAPTIVE_TIMEOUT.get_timeout()
            else:
                timeout = config.default_timeout

        try:
            conn = self.get_connection_with_tls_context(
                request, verify, proxies=proxies, cert=cert
            )
        except LocationValueError as e:
            raise InvalidURL(e, request=request)

        self.cert_verify(conn, request.url, verify, cert)
        url = self.request_url(request, proxies)
        self.add_headers(
            request,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies=proxies,
        )

        chunked = not (request.body is None or "Content-Length" in request.headers)

        if isinstance(timeout, tuple):
            try:
                connect, read = timeout
                timeout = TimeoutSauce(connect=connect, read=read)
            except ValueError:
                raise ValueError(
                    "Invalid timeout {0}. Pass a (connect, read) timeout tuple, "
                    "or a single float to set both timeouts to the same value.".format(timeout)
                )
        elif isinstance(timeout, TimeoutSauce):
            pass
        else:
            timeout = TimeoutSauce(connect=timeout, read=timeout)

        try:
            resp = conn.urlopen(
                method=request.method,
                url=url,
                body=request.body,
                headers=request.headers,
                redirect=False,
                assert_same_host=False,
                preload_content=False,
                decode_content=False,
                retries=self.max_retries,
                timeout=timeout,
                chunked=chunked,
            )

        except (ProtocolError, OSError) as err:
            raise ConnectionError(err, request=request)

        except MaxRetryError as e:
            if isinstance(e.reason, ConnectTimeoutError):
                if not isinstance(e.reason, NewConnectionError):
                    raise ConnectTimeout(e, request=request)

            if isinstance(e.reason, ResponseError):
                raise RetryError(e, request=request)

            if isinstance(e.reason, _ProxyError):
                raise ProxyError(e, request=request)

            if isinstance(e.reason, _SSLError):
                raise SSLError(e, request=request)

            raise ConnectionError(e, request=request)

        except ClosedPoolError as e:
            raise ConnectionError(e, request=request)

        except _ProxyError as e:
            raise ProxyError(e)

        except (_SSLError, _HTTPError) as e:
            if isinstance(e, _SSLError):
                raise SSLError(e, request=request)
            elif isinstance(e, ReadTimeoutError):
                raise ReadTimeout(e, request=request)
            elif isinstance(e, _InvalidHeader):
                raise InvalidHeader(e, request=request)
            else:
                raise

        end_time = time.time()
        duration = end_time - start_time
        connect_time = duration / 2
        read_time = duration / 2

        response = self.build_response(request, resp)

        if config.max_response_size:
            content_length = response.headers.get("content-length")
            if content_length:
                try:
                    if int(content_length) > config.max_response_size:
                        raise ResponseTooLarge(
                            "Response size {0} exceeds limit {1}".format(content_length, config.max_response_size)
                        )
                except ValueError:
                    pass

        hostname = urlparse(request.url).hostname
        GLOBAL_FAILURE_PREDICTOR.record(
            hostname, response.status_code < 400, duration, response.status_code
        )

        if config.adaptive_timeout:
            GLOBAL_ADAPTIVE_TIMEOUT.record_response(connect_time, read_time, response.status_code < 400)

        if config.behavioral_analysis:
            GLOBAL_BEHAVIORAL_ANALYZER.record_behavior(hostname, {
                "response_time": duration,
                "response_size": int(response.headers.get("content-length", 0)),
                "status_code": response.status_code,
                "header_count": len(response.headers),
            })

        if config.route_recording:
            GLOBAL_ROUTE_RECORDER.record(
                url=request.url,
                method=request.method,
                start_time=start_time,
                end_time=end_time,
                status_code=response.status_code,
                response_size=int(response.headers.get("content-length", 0)),
                redirects=[],
                protocol="HTTP/1.1",
            )

        GLOBAL_LOGGER.log(
            method=request.method,
            url=request.url,
            status_code=response.status_code,
            response_size=int(response.headers.get("content-length", 0)),
            duration=duration,
        )

        return response
