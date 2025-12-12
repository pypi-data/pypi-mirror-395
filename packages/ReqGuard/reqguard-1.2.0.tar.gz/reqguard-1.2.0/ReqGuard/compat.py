import sys

_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3

try:
    import simplejson as json
    has_simplejson = True
except ImportError:
    import json
    has_simplejson = False

if has_simplejson:
    from simplejson import JSONDecodeError
else:
    try:
        from json import JSONDecodeError
    except ImportError:
        class JSONDecodeError(ValueError):
            def __init__(self, msg, doc="", pos=0):
                self.msg = msg
                self.doc = doc
                self.pos = pos
                super(JSONDecodeError, self).__init__(msg)

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from collections.abc import Callable, Mapping, MutableMapping
except ImportError:
    from collections import Callable, Mapping, MutableMapping

try:
    from http import cookiejar as cookielib
except ImportError:
    import cookielib

try:
    from http.cookies import Morsel
except ImportError:
    from Cookie import Morsel

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from urllib.parse import (
        quote,
        quote_plus,
        unquote,
        unquote_plus,
        urldefrag,
        urlencode,
        urljoin,
        urlparse,
        urlsplit,
        urlunparse,
    )
except ImportError:
    from urllib import (
        quote,
        quote_plus,
        unquote,
        unquote_plus,
        urlencode,
    )
    from urlparse import (
        urldefrag,
        urljoin,
        urlparse,
        urlsplit,
        urlunparse,
    )

try:
    from urllib.request import (
        getproxies,
        getproxies_environment,
        parse_http_list,
        proxy_bypass,
        proxy_bypass_environment,
    )
except ImportError:
    from urllib import (
        getproxies,
        proxy_bypass,
    )
    from urllib2 import parse_http_list
    
    def getproxies_environment():
        return getproxies()
    
    def proxy_bypass_environment(host):
        return proxy_bypass(host)

try:
    import importlib
    def _resolve_char_detection():
        chardet = None
        for lib in ("chardet", "charset_normalizer"):
            if chardet is None:
                try:
                    chardet = importlib.import_module(lib)
                except ImportError:
                    pass
        return chardet
    chardet = _resolve_char_detection()
except ImportError:
    chardet = None

try:
    from urllib3 import __version__ as urllib3_version
    try:
        is_urllib3_1 = int(urllib3_version.split(".")[0]) == 1
    except (TypeError, AttributeError, ValueError):
        is_urllib3_1 = True
except ImportError:
    urllib3_version = "0.0.0"
    is_urllib3_1 = True

builtin_str = str
str = str
bytes = bytes
basestring = (str, bytes)
numeric_types = (int, float)
integer_types = (int,)

if is_py2:
    builtin_str = str
    str = unicode
    bytes = str
    basestring = basestring
    numeric_types = (int, long, float)
    integer_types = (int, long)
