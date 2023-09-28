import json
import os


def get_header():
    headers = {
        "Host": "sp.trade.icbc.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0; SE 2.X MetaSr 1.0) like Gecko",
    }
    with open("base_data/cookie.txt", mode="r", encoding="utf-8") as f:
        cookie = f.read()
    headers["Cookie"] = cookie
    return headers


def get_settings():
    with open(os.path.join("base_data", "base.json"), mode="r", encoding="utf8") as f:
        return json.load(f)
