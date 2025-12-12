import time
from urllib.parse import parse_qs, urlparse, urlunparse

from signed_urls.utils import (
    QueryDict,
    QueryList,
    build_canonical_query_string,
    build_canonical_string,
    create_url_signature,
    supported_algorithms,
    supported_sign_formats,
)
from signed_urls.validators import (
    validate_algorithm,
    validate_extra_query_parameters,
    validate_sign_format,
    validate_type,
    validate_url,
)


def sign_url(
    method: str,
    url: str,
    secret_key: str,
    ttl: int,
    algorithm: str = "SHA256",
    extra_qp: QueryDict | None = None,
    sign_format: str = "base64",
) -> str:
    """
    Sign a URL by adding an expiration timestamp and a signature.

    Builds a canonical string from the request components, computes a
    HMAC-based signature using `secret_key` and `algorithm`, and returns the
    URL with `exp` and `sig` query parameters appended.

    Note:
    This function does NOT perform semantic URL validation.
    Any non-empty string that can be parsed by urllib.parse.urlparse
    will be signed. URL correctness is the caller's responsibility.

    Args:
        method (str): HTTP method (e.g. 'GET', 'POST').
        url (str): The URL to sign.
        secret_key (str): Secret key used to create the signature.
        ttl (int): Time-to-live in seconds; expiration is current time + ttl.
            It can be positive or negative integer.
        extra_qp (dict | None): Additional query parameters to include in the
            signature and final URL.
        algorithm (str): Hash algorithm used for the signature (default: \'SHA256\').
        sign_format (str): Signature encoding format, either 'base64' or 'hex'

    Returns:
        str: The signed URL containing `exp` and `sig` query parameters.
    """
    # Validate http method
    validate_type(value=method, expected_type=str, field_name="HTTP method")

    # Validate url
    validate_url(url)

    # Validate secret key
    validate_type(value=secret_key, expected_type=str, field_name="Secret key")

    # Validate ttl
    validate_type(value=ttl, expected_type=int, field_name="TTL")

    # Validate algorithm
    validate_algorithm(algorithm=algorithm, supported_algorithms=supported_algorithms)

    # Validate sign_format
    validate_sign_format(
        sign_format=sign_format, supported_formats=supported_sign_formats
    )

    # Validate extra_qp: extra query parameters
    if extra_qp is not None:
        validate_extra_query_parameters(extra_qp)

    expire_ts = int(time.time()) + ttl
    parsed = urlparse(url)

    query = parsed.query
    query_params = parse_qs(query)
    query_params["exp"] = [str(expire_ts)]
    query_params.update(extra_qp or {})

    sorted_query_params: QueryList = sorted(query_params.items())

    canonical_query_string = build_canonical_query_string(sorted_query_params)

    message_to_sign = build_canonical_string(
        method=method,
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path,
        params=parsed.params,
        query=canonical_query_string,
        fragment=parsed.fragment,
    )

    signature: str = create_url_signature(
        message=message_to_sign,
        secret_key=secret_key,
        algorithm=algorithm,
        sign_format=sign_format,
    )

    sorted_query_params.append(("sig", [signature]))

    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            build_canonical_query_string(sorted_query_params),
            parsed.fragment,
        )
    )
