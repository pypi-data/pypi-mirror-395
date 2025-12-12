from collections.abc import Iterable


def validate_type(value, expected_type: type, field_name: str = "") -> None:
    if not field_name:
        field_name = "Value"
    if not isinstance(value, expected_type):
        raise TypeError(f"{field_name} must be of type {expected_type.__name__}")


def validate_extra_query_parameters(extra_qp: dict) -> None:
    validate_type(
        value=extra_qp, expected_type=dict, field_name="Extra query parameters"
    )
    # extra query parameters can not contain reserved keys 'exp' or 'sig'
    if "exp" in extra_qp or "sig" in extra_qp:
        raise ValueError(
            "Extra query parameters cannot contain reserved keys 'exp' or 'sig'."
        )

    # reject non-encodable values in extra query parameters
    allowed_scalars = (str, int, float, bool)
    err_msg = "Extra query parameter contains non-encodable value: {key}: {value}"
    for key, value in extra_qp.items():
        if isinstance(value, allowed_scalars):
            continue
        elif isinstance(value, (list, tuple)):
            if not all(isinstance(item, allowed_scalars) for item in value):
                raise TypeError(err_msg.format(key=key, value=value))
        else:
            raise TypeError(err_msg.format(key=key, value=value))


def validate_url(url: str) -> None:
    from urllib.parse import urlparse

    validate_type(value=url, expected_type=str, field_name="URL")
    url = url.strip()
    if len(url) == 0:
        raise ValueError("URL cannot be empty")
    parsed = urlparse(url)
    if not parsed.scheme:
        raise ValueError(f"Invalid URL format: missing scheme: {url}")
    if not parsed.netloc:
        raise ValueError(f"Invalid URL format: missing network location: {url}")


def validate_algorithm(algorithm: str, supported_algorithms: Iterable) -> None:
    validate_type(value=algorithm, expected_type=str, field_name="Algorithm")
    if algorithm not in supported_algorithms:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def validate_sign_format(sign_format: str, supported_formats: Iterable) -> None:
    validate_type(value=sign_format, expected_type=str, field_name="Signature format")
    if sign_format not in supported_formats:
        raise ValueError(f"Unsupported signature format: {sign_format}")
