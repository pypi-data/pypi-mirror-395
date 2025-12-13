import urllib

import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, req):
        req.headers["authorization"] = "Bearer " + self.token
        return req


def build_request(site: str, url: str, params: dict, api_token: str):
    items = list(params.items()) if hasattr(params, "items") else list(params)
    items = sorted(items, key=lambda x: x[0].lower())
    url = f"{site}{url}?{urllib.parse.urlencode(items)}"
    response = requests.get(url, auth=BearerAuth(api_token), timeout=30)
    response.encoding = response.apparent_encoding
    response.raise_for_status()
    return response.json()["results"]


def request_category(category_id: int, start_date: str, end_date: str = "+15d", **kwargs):
    url = f"/export/categ/{category_id}.json"
    params = {"from": start_date, "to": end_date, "order": "start"}
    return build_request(url=url, params=params, **kwargs)


def request_event(event_id: str, **kwargs):
    url = f"/export/event/{event_id}.json"
    params = {"detail": "contributions"}
    return build_request(url=url, params=params, **kwargs)


def search(query: str, start_date: str, end_date: str = "+15d", **kwargs):
    url = f"/export/event/search/{query}.json"
    params = {"from": start_date, "to": end_date, "detail": "contributions"}
    return build_request(url=url, params=params, **kwargs)
