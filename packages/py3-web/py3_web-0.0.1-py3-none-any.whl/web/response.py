import re
from typing import Any

import bs4
import execute
import httpx
import orjson
import parsel
import requests


def jsonp_to_json(jsonp: str) -> dict[str, Any]:
    func_name = re.match(r"^(?P<func_name>.*?)\({.*}\)\S*$", jsonp, re.DOTALL).groupdict()["func_name"]
    js_code = f"function {func_name}(o){{return o}};function sdk(){{return JSON.stringify({jsonp})}};"
    json_str = execute.js.execute_javascript_by_py_mini_racer(js_code, func_name="sdk")
    json_obj = orjson.loads(json_str)
    return json_obj


def to_text(response: httpx.Response | requests.Response) -> Any:
    return response.text


def to_json(response: httpx.Response | requests.Response) -> Any:
    return orjson.loads(response.text)


def to_sel(response: httpx.Response | requests.Response) -> parsel.Selector:
    return parsel.Selector(response.text)


def to_soup(response: httpx.Response | requests.Response) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(response.text, "html.parser")
