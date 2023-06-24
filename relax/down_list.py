'''
我的商城 > 销售交易管理 > 报账单管理
'''
import requests
import re
from bs4 import BeautifulSoup, Tag
import os
import csv
import time

from relax.util import get_header, get_settings


def get_page_count(url: str, params: dict, headers: dict):
    resp = requests.get(url, params=params, headers=headers, verify=False)
    txt = resp.text
    result = re.search(r'Paging.pageBar\("pageListDiv",(?P<count>.*?),', txt, re.S)
    if not result:
        return 0
    count = result.group('count')
    if not count:
        return 0
    return int(count)


def download_one_data(url: str, params: dict, headers: dict, file_name: str):
    resp = requests.get(url, params=params, headers=headers, verify=False)
    txt = resp.text

    soup = BeautifulSoup(txt, 'html.parser')
    table: Tag = soup.find('table', attrs={'class': 'c_table_1'})
    index: int = params['pageIndex']

    with open(file_name, mode='a', encoding='utf-8-sig', newline='') as f:
        cw = csv.writer(f)
        trs: list[Tag] = table.find_all("tr")
        if index == 1:
            ths: list[Tag] = trs[0].find_all("th")
            th_datas = []
            for i in ths:
                s = i.text.strip()
                th_datas.append(s)
            cw.writerow(th_datas)
        trs: list[Tag] = trs[1:]
        tr_rows = []
        for i in trs:
            tds: list[Tag] = i.find_all("td")
            tr_row = []
            for j in tds:
                s = j.text.strip()
                tr_row.append(s)
            tr_rows.append(tr_row)
        cw.writerows(tr_rows)


def download_list_data(
    url: str, params: dict, headers: dict, count: int, file_name: str
):
    size = count + 1
    for i in range(1, size):
        params['pageIndex'] = i
        download_one_data(url, params, headers, file_name)
        time.sleep(1)


if __name__ == '__main__':
    headers = get_header()
    settings = get_settings()
    headers['Referer'] = 'https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml'
    url = 'https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml'
    params = {
        "pageIndex": "1",
        "taskName": "",
        "startTime": settings['list_file_start'],
        "endTime": settings['list_file_end'],
        "submit.submitSeq": "",
        "submit.projectId": "",
        "submit.batchNo": "",
        "submit.submitStatus": "",
        "submit.year": "",
    }
    file_name = os.path.join(
        settings['folder_name'], f'{settings["list_file_name"]}.csv'
    )
    # 测试一条数据
    download_list_data(url, params, headers, 1, file_name)
