from lazysdk import lazyrequests
import showlog
import random
import time
import json


"""
2024-04-11 全面升级至3.0版本 https://developers.e.qq.com/v3.0/docs/api
"""


def make_nonce():
    """
    参考示例代码的生成一个随机数
    :return:
    """
    return str(time.time()) + str(random.randint(0, 999999))


def oauth_token2(
        app_id,
        app_secret,
        redirect_uri,
        grant_type='authorization_code',
        auth_code=None,
        refresh_token=None,
):
    """
    OAuth 2.0 授权
    获取/刷新token
    相关文档：https://developers.e.qq.com/docs/start/authorization
    :param auth_code:
    :param app_id:
    :param app_secret:
    :param grant_type: 请求的类型，可选值：authorization_code（授权码方式获取 token）、refresh_token（刷新 token）
    :param refresh_token:
    :param redirect_uri:
    :return:
    """
    redirect_uri = f'{redirect_uri}?app_id={app_id}'

    url = 'https://api.e.qq.com/oauth/token'
    params = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': grant_type
    }
    if auth_code:
        params['authorization_code'] = auth_code
    if refresh_token:
        params['refresh_token'] = refresh_token
    if redirect_uri:
        params['redirect_uri'] = redirect_uri

    for k in params:
        if type(params[k]) is not str:
            params[k] = json.dumps(params[k])

    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        params=params
    )


def oauth_token3(
        app_id,
        app_secret,
        redirect_uri=None,
        access_token=None,
        grant_type='authorization_code',
        auth_code=None,
        refresh_token=None,
):
    """
    获取/刷新token
    相关文档：https://developers.e.qq.com/v3.0/docs/api/oauth/token
    :param access_token:
    :param auth_code:
    :param app_id:
    :param app_secret:
    :param grant_type: 请求的类型，可选值：authorization_code（授权码方式获取 token）、refresh_token（刷新 token）
    :param refresh_token:
    :param redirect_uri: 回调地址
    :return:
    """
    params = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': grant_type
    }
    if access_token:
        # OAuth 相关接口无需提供 access_token、timestamp、nonce 等通用请求参数。
        params['access_token'] = access_token
        params['timestamp'] = int(time.time())
        params['nonce'] = make_nonce()
        url = 'https://api.e.qq.com/v3.0/oauth/token'
    else:
        url = 'https://api.e.qq.com/oauth/token'
    if auth_code:
        params['authorization_code'] = auth_code
    if refresh_token:
        params['refresh_token'] = refresh_token
    if redirect_uri:
        redirect_uri = f'{redirect_uri}?app_id={app_id}'
        params['redirect_uri'] = redirect_uri

    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        params=params
    )


def get_organization_account_relation(
        access_token: str,
        account_id=None,
        cursor=None,
        page: int = 1,
        page_size: int = 100,
        pagination_mode: str = "PAGINATION_MODE_CURSOR"
):
    """
    版本：3.0
    获取子账号列表
    这里获取子账户主要使用这个方法
    https://developers.e.qq.com/v3.0/docs/api/organization_account_relation/get
    :param access_token:
    :param account_id:
    :param cursor:
    :param page:
    :param page_size: 最小值 1，最大值 100
    :param pagination_mode: 分页方式，注意，为PAGINATION_MODE_NORMAL时，不能获取大于1000条的记录
    :return:
    """
    url = 'https://api.e.qq.com/v3.0/organization_account_relation/get'
    params = {
        'access_token': access_token,
        'timestamp': int(time.time()),
        'nonce': make_nonce(),
        "pagination_mode": pagination_mode,
        "page_size": page_size
    }
    if pagination_mode == "PAGINATION_MODE_NORMAL":
        params["page"] = page
    elif pagination_mode == "PAGINATION_MODE_CURSOR":
        params["cursor"] = cursor
    else:
        showlog.warning("pagination_mode参数错误")
        return

    if account_id:
        params["account_id"] = account_id
    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        params=params
    )


def get_advertiser_daily_budget(
        access_token: str,
        account_id
):
    """
    版本：3.0
    获取广告账户日预算
    https://developers.e.qq.com/v3.0/docs/api/advertiser_daily_budget/get
    :param access_token:
    :param account_id:
    :return:

    应答示例
    {
        "code": 0,
        "message": "",
        "message_cn": "",
        "data": {
            "account_id": "<ACCOUNT_ID>",
            "daily_budget": 20000,
            "min_daily_budget": 10000
        }
    }
    """
    url = 'https://api.e.qq.com/v3.0/advertiser_daily_budget/get'
    params = {
        'access_token': access_token,
        'timestamp': int(time.time()),
        'nonce': make_nonce(),

        "account_id": account_id,
        "fields": [
            "account_id",
            "daily_budget"
        ]
    }
    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        params=params
    )


def update_daily_budget(
        access_token: str,
        account_id: int = None,
        daily_budget: int = None,
        update_daily_budget_spec: list = None
):
    """
    版本：3.0
    批量修改广告主日限额
    https://developers.e.qq.com/v3.0/docs/api/advertiser/update_daily_budget
    :param access_token:
    :param account_id:
    :param daily_budget: 账户预算，单位为分
    :param update_daily_budget_spec: 任务列表，[{"account_id":"aaa","daily_budget": 100},{"account_id":"bbb","daily_budget": 100}]
    :return:

    应答示例
    {
        "code": 0,
        "message": "",
        "message_cn": "",
        "data": {
            "list": [
                {
                    "code": 0,
                    "message": "",
                    "message_cn": "",
                    "account_id": "<ACCOUNT_ID>"
                }
            ],
            "fail_id_list": []
        }
    }
    """
    url = 'https://api.e.qq.com/v3.0/advertiser/update_daily_budget'
    params = {
        'access_token': access_token,
        'timestamp': int(time.time()),
        'nonce': make_nonce()
    }
    data = dict()
    if update_daily_budget_spec:
        data["update_daily_budget_spec"] = update_daily_budget_spec
    else:
        data["update_daily_budget_spec"] = [
            {
                "account_id": account_id,
                "daily_budget": daily_budget
            }
        ]
    return lazyrequests.lazy_requests(
        method="POST",
        url=url,
        params=params,
        json=data
    )
