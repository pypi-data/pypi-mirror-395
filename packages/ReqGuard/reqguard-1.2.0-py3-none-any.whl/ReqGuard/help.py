import platform
import ssl
import sys

try:
    import json
except ImportError:
    import simplejson as json

try:
    import idna
except ImportError:
    idna = None

try:
    import urllib3
except ImportError:
    urllib3 = None

from . import __version__ as requests_version

try:
    import charset_normalizer
except ImportError:
    charset_normalizer = None

try:
    import chardet
except ImportError:
    chardet = None

try:
    from urllib3.contrib import pyopenssl
except ImportError:
    pyopenssl = None
    OpenSSL = None
    cryptography = None
else:
    try:
        import cryptography
        import OpenSSL
    except ImportError:
        cryptography = None
        OpenSSL = None


def _implementation():
    implementation = platform.python_implementation()

    if implementation == "CPython":
        implementation_version = platform.python_version()
    elif implementation == "PyPy":
        pypy_version_info = getattr(sys, "pypy_version_info", (0, 0, 0))
        implementation_version = "{0}.{1}.{2}".format(
            pypy_version_info[0],
            pypy_version_info[1],
            pypy_version_info[2],
        )
        if len(pypy_version_info) > 3 and pypy_version_info[3] != "final":
            implementation_version = "".join([
                implementation_version, str(pypy_version_info[3])
            ])
    elif implementation == "Jython":
        implementation_version = platform.python_version()
    elif implementation == "IronPython":
        implementation_version = platform.python_version()
    else:
        implementation_version = "Unknown"

    return {"name": implementation, "version": implementation_version}


def info():
    try:
        platform_info = {
            "system": platform.system(),
            "release": platform.release(),
        }
    except OSError:
        platform_info = {
            "system": "Unknown",
            "release": "Unknown",
        }

    implementation_info = _implementation()
    urllib3_info = {"version": getattr(urllib3, "__version__", None)}
    charset_normalizer_info = {"version": None}
    chardet_info = {"version": None}
    
    if charset_normalizer:
        charset_normalizer_info = {"version": getattr(charset_normalizer, "__version__", None)}
    if chardet:
        chardet_info = {"version": getattr(chardet, "__version__", None)}

    pyopenssl_info = {
        "version": None,
        "openssl_version": "",
    }
    if OpenSSL:
        pyopenssl_info = {
            "version": getattr(OpenSSL, "__version__", None),
            "openssl_version": "{0:x}".format(getattr(OpenSSL.SSL, "OPENSSL_VERSION_NUMBER", 0)),
        }
    
    cryptography_info = {
        "version": getattr(cryptography, "__version__", "") if cryptography else "",
    }
    idna_info = {
        "version": getattr(idna, "__version__", "") if idna else "",
    }

    system_ssl = getattr(ssl, "OPENSSL_VERSION_NUMBER", None)
    system_ssl_info = {"version": "{0:x}".format(system_ssl) if system_ssl is not None else ""}

    return {
        "platform": platform_info,
        "implementation": implementation_info,
        "system_ssl": system_ssl_info,
        "using_pyopenssl": pyopenssl is not None,
        "using_charset_normalizer": chardet is None,
        "pyOpenSSL": pyopenssl_info,
        "urllib3": urllib3_info,
        "chardet": chardet_info,
        "charset_normalizer": charset_normalizer_info,
        "cryptography": cryptography_info,
        "idna": idna_info,
        "requests": {
            "version": requests_version,
        },
    }


def main():
    print(json.dumps(info(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
