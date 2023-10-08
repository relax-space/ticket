import json
import os
from datetime import date, datetime, timedelta
import time

import requests


def get_header():
    headers = {
        "Host": "sp.trade.icbc.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0; SE 2.X MetaSr 1.0) like Gecko",
    }
    return headers


def get_settings():
    with open(os.path.join("base_data", "base.json"), mode="r", encoding="utf8") as f:
        return json.load(f)


def get_companys():
    with open(
        os.path.join("base_data", "company.json"), mode="r", encoding="utf8"
    ) as f:
        return json.load(f)


def str_to_int(strObj: str) -> int:
    if strObj.isdigit():
        return int(strObj)
    else:
        return 0


def fill_zero_2(i) -> str:
    return f"{i:0>2}"


def get_current_date(retry=3) -> date:
    while retry > 0:
        try:
            resp = requests.get("https://www.baidu.com")
            if resp.status_code == 200:
                ts = resp.headers["date"]
                time_array = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
                stamp = time.mktime(time_array) + 8 * 60 * 60
                return datetime.fromtimestamp(stamp).date()
        except Exception as e:
            retry -= 1
            time.sleep(0.5)
    else:
        return None


def check_file_date(file_name) -> int:
    stamp = os.path.getmtime(file_name)
    file_date = datetime.fromtimestamp(stamp).date()
    now_date = date.today()
    res = now_date - file_date
    return res.days


def get_cover_1(year, month) -> str:
    c = f"{year}年{month}月驻琼部队副食品区域集中筹措物资【封面】"
    return c


def get_cover_1_bydate(date_str: str) -> str:
    year, month = get_year_month(date_str)
    c = f"{year}年{month}月驻琼部队副食品区域集中筹措物资【封面】"
    return c


def get_cover_2(company_name) -> str:
    c = f"供应商：{company_name}".ljust(27, " ") + "每日汇总表"
    return c


def get_year_month(date_str: str) -> tuple[int, int]:
    s = datetime.strptime(date_str, "%Y-%m-%d")
    s = datetime(s.year, s.month, 1) - timedelta(days=1)
    return s.year, s.month
