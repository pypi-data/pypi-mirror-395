import base64
import hashlib
import hmac
from collections.abc import Sequence
from typing import TypeAlias
from urllib.parse import urlencode

Scalar: TypeAlias = str | int | float
QueryValue: TypeAlias = Scalar | Sequence[Scalar]
QueryDict: TypeAlias = dict[str, QueryValue]
QueryList: TypeAlias = list[tuple[str, QueryValue]]


supported_algorithms: list[str] = ["SHA256", "SHA512", "BLAKE2B", "BLAKE2S"]


supported_sign_formats: list[str] = ["base64", "hex"]


def create_url_signature_base64(message: str, secret_key: str, algorithm: str) -> str:
    hmo = hmac.new(
        secret_key.encode(),
        msg=message.encode(),
        digestmod=getattr(hashlib, algorithm.lower()),
    )
    digest = hmo.digest()
    return base64.urlsafe_b64encode(digest).decode("ascii")


def create_url_signature_hex(message: str, secret_key: str, algorithm: str) -> str:
    hmo = hmac.new(
        secret_key.encode(),
        msg=message.encode(),
        digestmod=getattr(hashlib, algorithm.lower()),
    )
    return hmo.hexdigest()


def create_url_signature(
    message: str, secret_key: str, algorithm: str, sign_format: str
) -> str:
    if sign_format == "base64":
        return create_url_signature_base64(message, secret_key, algorithm)
    elif sign_format == "hex":
        return create_url_signature_hex(message, secret_key, algorithm)
    else:
        raise ValueError(f"Unsupported signature format: {sign_format}")


def build_canonical_query_string(params: QueryDict | QueryList) -> str:
    """
    Build a canonical, URL-encoded query string from the given parameters.

    Keys are sorted lexicographically to ensure stable ordering. If a value is
    a sequence, multiple key/value pairs will be produced for that key.

    Args:
        params: Mapping of query parameter names to values. Values may be a
            single value or a sequence of values.

    Returns:
        URL-encoded query string with keys sorted.
    """
    if isinstance(params, dict):
        params = params.items()

    return urlencode(sorted(params), doseq=True)


def build_canonical_string(
    method: str,
    scheme: str,
    netloc: str,
    path: str,
    params: str | None,
    query: str | None,
    fragment: str | None,
) -> str:
    data = [method.upper(), scheme, netloc, path]
    if params:
        data.append(params)
    if query:
        data.append(query)
    if fragment:
        data.append(fragment)
    return "\n".join(data)
