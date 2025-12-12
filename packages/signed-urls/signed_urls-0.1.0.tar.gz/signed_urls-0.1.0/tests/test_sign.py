from inspect import signature
from unittest.mock import patch
from urllib.parse import parse_qs, urlencode, urlparse

import pytest

from signed_urls.sign import sign_url
from signed_urls.utils import supported_sign_formats
from tests.data import (
    FIXED_TIME,
    non_encodable_extra_qp,
    request_methods,
    secret_key,
    unsupported_algorithms,
)

test_method = "GET"
test_url = "https://example.com/path?foo=1&foo=2&foo=3&baz=qux"
test_secret_key = secret_key
test_ttl = 300
test_algorithm = "SHA256"

methods_to_test = request_methods


# 0. The default value of sign_format is 'base64'


def test_sign_url_default_sign_format_is_base64():
    fn_signature = signature(sign_url)
    assert fn_signature.parameters["sign_format"].default == "base64"


# 1. Basic Functionality


def test_sign_url_returns_string():
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
    )
    assert isinstance(signed_url, str)


@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_returns_string_sf_parametrized(sign_format):
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        sign_format=sign_format,
    )
    assert isinstance(signed_url, str)


def test_sign_url_with_extra_query_parameters_returns_string():
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        extra_qp={"keyid": "key001", "user": "alice"},
    )
    assert isinstance(signed_url, str)


@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_with_extra_query_parameters_returns_string_sf_parametrized(
    sign_format,
):
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        extra_qp={"keyid": "key001", "user": "alice"},
        sign_format=sign_format,
    )
    assert isinstance(signed_url, str)


def test_sign_url_preserves_original_url_data():
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
    )
    url_data = urlparse(test_url)
    url_query_params = parse_qs(url_data.query)
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)

    # signed url preserves the original url data
    assert url_data.scheme == signed_url_data.scheme
    assert url_data.netloc == signed_url_data.netloc
    assert url_data.path == signed_url_data.path
    assert url_data.fragment == signed_url_data.fragment

    # signed url preserves the original query parameters
    for k, v in url_query_params.items():
        assert k in signed_query_params
        assert signed_query_params[k] == v


@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_preserves_original_url_data_sf_parametrized(sign_format):
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        sign_format=sign_format,
    )
    url_data = urlparse(test_url)
    url_query_params = parse_qs(url_data.query)
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)

    # signed url preserves the original url data
    assert url_data.scheme == signed_url_data.scheme
    assert url_data.netloc == signed_url_data.netloc
    assert url_data.path == signed_url_data.path
    assert url_data.fragment == signed_url_data.fragment

    # signed url preserves the original query parameters
    for k, v in url_query_params.items():
        assert k in signed_query_params
        assert signed_query_params[k] == v


def test_sign_url_with_extra_query_parameters_preserves_original_url_data():
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        extra_qp={"keyid": "key001", "user": "alice"},
    )
    url_data = urlparse(test_url)
    url_query_params = parse_qs(url_data.query)
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)

    # signed url preserves the original url data
    assert url_data.scheme == signed_url_data.scheme
    assert url_data.netloc == signed_url_data.netloc
    assert url_data.path == signed_url_data.path
    assert url_data.fragment == signed_url_data.fragment

    # signed url preserves the original query parameters
    for k, v in url_query_params.items():
        assert k in signed_query_params
        assert signed_query_params[k] == v


@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_with_extra_query_parameters_preserves_original_url_data_sf_parametrized(  # noqa: E501
    sign_format,
):
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        extra_qp={"keyid": "key001", "user": "alice"},
        sign_format=sign_format,
    )
    url_data = urlparse(test_url)
    url_query_params = parse_qs(url_data.query)
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)

    # signed url preserves the original url data
    assert url_data.scheme == signed_url_data.scheme
    assert url_data.netloc == signed_url_data.netloc
    assert url_data.path == signed_url_data.path
    assert url_data.fragment == signed_url_data.fragment

    # signed url preserves the original query parameters
    for k, v in url_query_params.items():
        assert k in signed_query_params
        assert signed_query_params[k] == v


def test_sign_url_contains_exp_and_sig():
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
    )
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)
    expire_ts = signed_query_params["exp"][0]

    assert "exp" in signed_query_params
    assert "sig" in signed_query_params

    # successful conversion to int
    assert expire_ts.isdigit()


@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_contains_exp_and_sig_sf_parametrized(sign_format):
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        sign_format=sign_format,
    )
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)
    expire_ts = signed_query_params["exp"][0]

    assert "exp" in signed_query_params
    assert "sig" in signed_query_params

    # successful conversion to int
    assert expire_ts.isdigit()


def test_sign_url_with_extra_query_parameters_contains_extra_qp_exp_and_sig():
    extra_qp = {
        "keyid": "key001",
        "user": "alice",
        "chapter": [1, 2],
        "job": "тест",
        "id": 1,
    }
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        extra_qp=extra_qp,
    )
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)

    extra_qp_normalized = parse_qs(urlencode(extra_qp, doseq=True))

    # 'exp' and 'sig' are present
    assert "exp" in signed_query_params
    assert "sig" in signed_query_params

    # extra query parameters are present
    for k, v in extra_qp_normalized.items():
        assert k in signed_query_params
        assert signed_query_params[k] == v

    # successful conversion to int
    try:
        int(signed_query_params["exp"][0])
    except ValueError:
        pytest.fail("exp parameter is not a valid integer timestamp")


@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_with_extra_query_parameters_contains_extra_qp_exp_and_sig_sf_parametrized(  # noqa: E501
    sign_format,
):
    extra_qp = {
        "keyid": "key001",
        "user": "alice",
        "chapter": [1, 2],
        "job": "тест",
        "id": 1,
    }
    signed_url = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        extra_qp=extra_qp,
        sign_format=sign_format,
    )
    signed_url_data = urlparse(signed_url)
    signed_query_params = parse_qs(signed_url_data.query)

    extra_qp_normalized = parse_qs(urlencode(extra_qp, doseq=True))

    # 'exp' and 'sig' are present
    assert "exp" in signed_query_params
    assert "sig" in signed_query_params

    # extra query parameters are present
    for k, v in extra_qp_normalized.items():
        assert k in signed_query_params
        assert signed_query_params[k] == v

    # successful conversion to int
    try:
        int(signed_query_params["exp"][0])
    except ValueError:
        pytest.fail("exp parameter is not a valid integer timestamp")


# 2. The signing process is deterministic


@patch("signed_urls.sign.time.time", return_value=FIXED_TIME)
def test_sign_url_is_deterministic(mocked_time):  # noqa: ARG001
    signed_url_1 = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
    )
    signed_url_2 = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
    )
    exp_1 = parse_qs(urlparse(signed_url_1).query)["exp"][0]
    exp_2 = parse_qs(urlparse(signed_url_2).query)["exp"][0]
    assert exp_1 == exp_2


@pytest.mark.parametrize("sign_format", supported_sign_formats)
@patch("signed_urls.sign.time.time", return_value=FIXED_TIME)
def test_sign_url_is_deterministic_sf_parametrized(mocked_time, sign_format):  # noqa: ARG001
    signed_url_1 = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        sign_format=sign_format,
    )
    signed_url_2 = sign_url(
        method=test_method,
        url=test_url,
        secret_key=test_secret_key,
        ttl=test_ttl,
        algorithm=test_algorithm,
        sign_format=sign_format,
    )
    assert signed_url_1 == signed_url_2


# 3. Failure Cases


def test_sign_url_when_url_is_empty_raises_value_error():
    with pytest.raises(ValueError, match="URL cannot be empty"):
        sign_url(
            method=test_method,
            url="",
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=test_algorithm,
        )


@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_when_url_is_empty_raises_value_error_sf_paramterized(sign_format):
    with pytest.raises(ValueError, match="URL cannot be empty"):
        sign_url(
            method=test_method,
            url="",
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=test_algorithm,
            sign_format=sign_format,
        )


@pytest.mark.parametrize("reserved_keyword", ["exp", "sig"])
def test_sign_url_when_extra_qp_contains_exp_raises_value_error(reserved_keyword):
    with pytest.raises(
        ValueError,
        match="Extra query parameters cannot contain reserved keys 'exp' or 'sig'.",
    ):
        sign_url(
            method=test_method,
            url=test_url,
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=test_algorithm,
            extra_qp={reserved_keyword: "some_value", "user": "alice"},
        )


@pytest.mark.parametrize("reserved_keyword", ["exp", "sig"])
@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_when_extra_qp_contains_exp_raises_value_error_sf_parametrized(
    reserved_keyword, sign_format
):
    with pytest.raises(
        ValueError,
        match="Extra query parameters cannot contain reserved keys 'exp' or 'sig'.",
    ):
        sign_url(
            method=test_method,
            url=test_url,
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=test_algorithm,
            extra_qp={reserved_keyword: "some_value", "user": "alice"},
            sign_format=sign_format,
        )


@pytest.mark.parametrize("algorithm", unsupported_algorithms)
def test_sign_url_with_unsupported_algorithm_raises_value_error(algorithm):
    with pytest.raises(ValueError, match=f"Unsupported algorithm: {algorithm}"):
        sign_url(
            method=test_method,
            url=test_url,
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=algorithm,
        )


@pytest.mark.parametrize("algorithm", unsupported_algorithms)
@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_with_unsupported_algorithm_raises_value_error_sf_parametrized(
    algorithm, sign_format
):
    with pytest.raises(ValueError, match=f"Unsupported algorithm: {algorithm}"):
        sign_url(
            method=test_method,
            url=test_url,
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=algorithm,
            sign_format=sign_format,
        )


@pytest.mark.parametrize("non_encodable_extra_qp", non_encodable_extra_qp)
def test_sign_url_with_non_encodable_extra_qp_raises_type_error(non_encodable_extra_qp):
    with pytest.raises(
        TypeError, match="Extra query parameter contains non-encodable value"
    ):
        sign_url(
            method=test_method,
            url=test_url,
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=test_algorithm,
            extra_qp=non_encodable_extra_qp,
        )


@pytest.mark.parametrize("non_encodable_extra_qp", non_encodable_extra_qp)
@pytest.mark.parametrize("sign_format", supported_sign_formats)
def test_sign_url_with_non_encodable_extra_qp_raises_type_error_sf_parametrized(
    non_encodable_extra_qp, sign_format
):
    with pytest.raises(
        TypeError, match="Extra query parameter contains non-encodable value"
    ):
        sign_url(
            method=test_method,
            url=test_url,
            secret_key=test_secret_key,
            ttl=test_ttl,
            algorithm=test_algorithm,
            extra_qp=non_encodable_extra_qp,
            sign_format=sign_format,
        )
