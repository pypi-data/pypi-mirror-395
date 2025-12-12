<h1 align="center">
    <strong>signed-urls</strong>
</h1>

<p align="center">
    <a href="https://github.com/alv2017/signed-urls" target="_blank">
        <!-- Last commit -->
        <img src="https://img.shields.io/github/last-commit/alv2017/signed-urls" alt="Latest Commit">
        <!-- GitHub Actions tests status -->
        <img src="https://img.shields.io/github/actions/workflow/status/alv2017/signed-urls/code-quality-check.yaml?branch=main&label=tests" alt="Tests Status">
        <!-- Codecov coverage -->
        <img src="https://img.shields.io/codecov/c/github/alv2017/signed-urls/main" alt="Code Coverage">
    </a>
    <br/>
    <a href="https://pypi.org/project/signed-urls" target="_blank">
        <img src="https://img.shields.io/pypi/v/signed-urls" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/signed-urls" alt="Python Version">
    <img src="https://img.shields.io/github/license/alv2017/signed-urls">
</p>

## Introduction

A signed URL is a URL that grants temporary, limited access to a resource, such as a file in cloud storage. 
It includes an expiration date and a digital signature in its query string, which authenticates the request 
and ensures the URL hasn't been altered. This allows users without direct credentials to perform a specific 
action, like downloading a file, for a limited time.  

### How signed URLs work?

1. A server creates a standard URL and adds parameters like an expiration time. 
2. The server generates a digital signature using a secret key and appends it to the URL.
3. The signed URL is shared with the user.
4. When the user accesses the URL, the resource server verifies the signature and checks the expiration time.
5. If the signature is valid and the URL hasn't expired, access to the resource is granted.

### Use cases

- Secure file downloads and uploads allowing temporary access.
- Granting temporary access to private resources without sharing credentials.
- Time-limited access to APIs for third-party applications.


## `signed-urls` package

The `signed-urls` package provides a simple way to generate and verify signed URLs.

### Installation

```commandline
pip install signed-urls
```

### Basic usage

```python
from signed_urls import sign_url, verify_signed_url

method = "GET"
secret_key = "Top-Secret-Key"
url = "https://example.com/resource/1?owner=alice"
hashing_algorithm = "SHA256"
sign_format = "base64"

# Generate a signed URL
signed_url = sign_url(
    method=method,
    url=url,
    secret_key=secret_key,
    ttl=300,
    algorithm=hashing_algorithm,
    sign_format=sign_format
)
    
# Verify the signed URL
is_valid = verify_signed_url(
    method=method,
    signed_url=signed_url,
    secret_key=secret_key,
    algorithm=hashing_algorithm,
    sign_format=sign_format
)

print(f"Is the signed URL valid? {is_valid}")
```
### Supported hashing algorithms

- SHA256
- SHA512
- BLAKE2B
- BLAKE2S

### Supported sign formats

- base64: creates signature as base64 ASCII string
- hex: creates signature as hexadecimal string