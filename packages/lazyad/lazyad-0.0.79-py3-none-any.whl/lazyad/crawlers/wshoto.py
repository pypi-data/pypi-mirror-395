# 微盛，企业管家 https://platform.wshoto.com
from lazysdk import lazyrequests
import copy


default_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "platform.wshoto.com",
        "Origin": "https://platform.wshoto.com",
        "Pragma": "no-cache",
        "Referer": "https://platform.wshoto.com/index/dashboard",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0",
        "x-admin-header": "1",
        "x-clientType-header": "pc",
        "x-header-host": "platform.wshoto.com",
    }


def dashboard(
        authorization: str
):
    url = "https://platform.wshoto.com/bff/index/private/pc/dashboard?saMode=SECRET"
    headers = copy.deepcopy(default_headers)
    headers["Authorization"] = authorization
    return lazyrequests.lazy_requests(
        method="POST",
        url=url,
        headers=headers
    )