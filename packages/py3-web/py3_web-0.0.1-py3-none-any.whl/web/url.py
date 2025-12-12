import re
from typing import Any
from urllib import parse

import tldextract
from furl import furl
from typing_extensions import Literal
from w3lib.url import canonicalize_url


def get_furl_obj(url: str) -> furl:
    return furl(url)


def get_parse_result(url: str) -> parse.ParseResult:
    parse_result = parse.urlparse(url)
    return parse_result


def get_origin_path(url: str) -> str:
    """
    >>> get_origin_path("https://github.com/search?q=owner%3Amathewgeola+py3-web&type=repositories")
    'https://github.com/search'

    Args:
        url:

    Returns:

    """
    furl_obj = get_furl_obj(url)
    origin_path = str(furl_obj.origin) + str(furl_obj.path)
    return origin_path


def is_valid(url: str) -> bool:
    """
    >>> is_valid("https://www.baidu.com/")
    True

    Args:
        url:

    Returns:

    """
    try:
        parse_result = get_parse_result(url)
        scheme, netloc = parse_result.scheme, parse_result.netloc
        if not scheme:
            return False
        if not netloc:
            return False
        if scheme not in ("http", "https"):
            return False
        return True
    except ValueError:
        return False


def quote(
        url: str,
        safe: str | None = None,
        encoding: str = "utf-8",
        quote_type: Literal["encodeURI", "encodeURIComponent", "browser"] | None = "browser"
) -> str:
    """
    >>> quote("https://www.baidu.com/s?wd=你好")
    'https://www.baidu.com/s?wd=%E4%BD%A0%E5%A5%BD'

    Args:
        url:
        safe:
        encoding:
        quote_type:

    Returns:

    """
    if quote_type == "encodeURI":
        safe = ";/?:@&=+$,-_.!~*'()#"
    elif quote_type == "encodeURIComponent":
        safe = "-_.~"
    elif quote_type == "browser":
        safe = ";/?:@&=+$,-_.!~*'()"
        parsed = parse.urlparse(url)
        path = parse.quote(parsed.path, safe=safe)
        query_pairs = parse.parse_qsl(parsed.query, keep_blank_values=True)
        encoded_query = "&".join(
            f"{k}={parse.quote(v, safe='-_.~', encoding=encoding)}"
            for k, v in query_pairs
        )
        fragment = parse.quote(parsed.fragment, safe='-_.~', encoding=encoding)
        return parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            encoded_query,
            fragment
        ))
    else:
        if safe is None:
            safe = "/"

    return parse.quote(url, safe=safe, encoding=encoding)


def unquote(url: str, encoding: str = "utf-8") -> str:
    """
    >>> unquote("https://www.baidu.com/s?wd=%E4%BD%A0%E5%A5%BD")
    'https://www.baidu.com/s?wd=你好'

    Args:
        url:
        encoding:

    Returns:

    """
    return parse.unquote(url, encoding=encoding)


def encode(params: dict[str, Any]) -> str:
    """
    >>> encode({"a": "1", "b": "2"})
    'a=1&b=2'

    Args:
        params:

    Returns:

    """
    return parse.urlencode(params)


def decode(url: str) -> dict[str, str]:
    """
    >>> decode("xxx?a=1&b=2")
    {'a': '1', 'b': '2'}

    Args:
        url:

    Returns:

    """
    params = dict()

    lst = url.split("?", maxsplit=1)[-1].split("&")
    for i in lst:
        key, value = i.split("=", maxsplit=1)
        params[key] = unquote(value)

    return params


def join_url(base_url: str, url: str) -> str:
    """
    >>> join_url("https://www.baidu.com/", "/s?ie=UTF-8&wd=py3-web")
    'https://www.baidu.com/s?ie=UTF-8&wd=py3-web'

    Args:
        base_url:
        url:

    Returns:

    """
    return parse.urljoin(base_url, url)


def join_params(url: str, params: dict[str, Any]) -> str:
    """
    >>> join_params("https://www.baidu.com/s", {"wd": "你好"})
    'https://www.baidu.com/s?wd=%E4%BD%A0%E5%A5%BD'

    Args:
        url:
        params:

    Returns:

    """
    if not params:
        return url

    params = encode(params)
    separator = "?" if "?" not in url else "&"
    return url + separator + params


def get_params(url: str) -> dict[str, str]:
    """
    >>> get_params("https://www.baidu.com/s?wd=py3-web")
    {'wd': 'py3-web'}

    Args:
        url:

    Returns:

    """
    furl_obj = get_furl_obj(url)
    params = dict(furl_obj.query.params)
    return params


def get_param(url: str, key: str, default: Any | None = None) -> Any:
    """
    >>> get_param("https://www.baidu.com/s?wd=py3-web", "wd")
    'py3-web'

    Args:
        url:
        key:
        default:

    Returns:

    """
    params = get_params(url)
    param = params.get(key, default)
    return param


def get_url_params(url: str) -> tuple[str, dict[str, str]]:
    """
    >>> get_url_params("https://www.baidu.com/s?wd=py3-web")
    ('https://www.baidu.com/s', {'wd': 'py3-web'})

    Args:
        url:

    Returns:

    """
    root_url = ""
    params = dict()

    if "?" in url:
        root_url = url.split("?", maxsplit=1)[0]
        params = get_params(url)
    else:
        if re.search("[&=]", url) and not re.search("/", url):
            params = get_params(url)
        else:
            root_url = url

    return root_url, params


def get_domain(url: str) -> str:
    """
    >>> get_domain("https://image.baidu.com/search/index?word=py3-web")
    'baidu'

    Args:
        url:

    Returns:

    """
    er = tldextract.extract(url)
    domain = er.domain
    return domain


def get_subdomain(url: str) -> str:
    """
    >>> get_subdomain("https://image.baidu.com/search/index?word=py3-web")
    'image'

    Args:
        url:

    Returns:

    """
    er = tldextract.extract(url)
    subdomain = er.subdomain
    return subdomain


def canonicalize(url: str) -> str:
    """
    >>> canonicalize("https://www.baidu.com/s?wd=py3-web")
    'https://www.baidu.com/s?wd=py3-web'

    Args:
        url:

    Returns:

    """
    return canonicalize_url(url)
