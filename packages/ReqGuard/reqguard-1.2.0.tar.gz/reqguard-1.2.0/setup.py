#!/usr/bin/env python
import os
import sys
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "ReqGuard", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

requires = [
    "urllib3>=1.21.1,<3",
    "certifi>=2017.4.17",
    "charset-normalizer>=2,<4",
    "idna>=2.5,<4",
]

extras_require = {
    "http2": ["httpx>=0.23.0", "h2>=4.0.0"],
    "http3": ["aioquic>=0.9.0"],
    "security": ["cryptography>=2.5"],
    "socks": ["PySocks>=1.5.6,!=1.5.7"],
}

extras_require["all"] = list(set(sum(extras_require.values(), [])))

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"": ["LICENSE", "NOTICE"]},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=requires,
    extras_require=extras_require,
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Security",
    ],
    project_urls={
        "Documentation": "https://github.com/x6-u/ReqGuard",
        "Source": "https://github.com/x6-u/ReqGuard",
        "Telegram": "https://t.me/QP4RM",
    },
    keywords=[
        "http",
        "https",
        "security",
        "ssrf",
        "protection",
        "rate-limiting",
        "dns-rebinding",
        "threat-detection",
        "web-security",
        "api-security",
    ],
)
