import hmac
import time
from urllib.parse import parse_qs, urlparse

from signed_urls.utils import (
    build_canonical_query_string,
    build_canonical_string,
    create_url_signature,
    supported_algorithms,
    supported_sign_formats,
)
from signed_urls.validators import (
    validate_algorithm,
    validate_sign_format,
    validate_type,
    validate_url,
)


def verify_signed_url(
    method: str, signed_url: str, secret_key: str, algorithm: str, sign_format: str
) -> bool:
    """
    Verify a signed URL.

    Note:
    This function performs a basic validation of the url.
    URL correctness is the caller's responsibility.

    Args:
        method (str): HTTP method used to sign the request (e.g., 'GET').
        signed_url (str): The full URL containing the signature query parameter 'sig'.
        secret_key (str): Secret key used to create the HMAC signature.
        algorithm (str): Hash algorithm name passed to the signing helper. Choose from
            supported algorithms.
        sign_format (str): Signature encoding format, either 'base64' or 'hex'

    Returns:
        bool: True if the signature in the URL matches the expected signature computed
        from the canonicalized request and provided secret_key; False otherwise.
    """
    # Validate http method
    validate_type(value=method, expected_type=str, field_name="HTTP method")

    # Validate signed_url
    validate_url(url=signed_url)

    # Validate secret key
    validate_type(value=secret_key, expected_type=str, field_name="Secret key")

    # Validate algorithm
    validate_algorithm(algorithm=algorithm, supported_algorithms=supported_algorithms)

    # Validate sign_format
    validate_sign_format(
        sign_format=sign_format, supported_formats=supported_sign_formats
    )

    # Parse the signed URL
    parsed = urlparse(signed_url)
    query_params = parse_qs(parsed.query)

    # Extract the signature from the query parameters
    signature: str = query_params.pop("sig", [None])[0]

    # Signature must be present
    if not signature:
        raise ValueError("Invalid signed url: missing 'sig' parameter")

    # expiry timestamp
    exp = query_params.get("exp", [None])[0]
    if not exp:
        raise ValueError("Invalid signed url: missing 'exp' parameter")

    if not exp.isdigit():
        raise ValueError("Invalid signed url: 'exp' must be a valid timestamp")

    if int(exp) < int(time.time()):
        return False

    # Reconstruct the message to sign
    unsigned_query = build_canonical_query_string(query_params)

    message_to_sign = build_canonical_string(
        method=method,
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path,
        params=parsed.params,
        query=unsigned_query,
        fragment=parsed.fragment,
    )

    # Generate an expected signature using the secret key
    expected_signature = create_url_signature(
        message_to_sign, secret_key, algorithm=algorithm, sign_format=sign_format
    )

    # Compare the signature from the url with the expected signature
    return hmac.compare_digest(signature, expected_signature)
