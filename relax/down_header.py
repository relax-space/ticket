"""
我的商城 > 销售交易管理 > 报账单详情
"""

from asyncio import Semaphore, gather, get_event_loop
from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup

from aiocsv import AsyncWriter
from aiofiles import open
from os import path as os_path

try:
    from relax.util import get_header, get_settings
except:
    from util import get_header, get_settings


async def req(
    url: str,
    headers: dict,
    i_param: dict,
    session: ClientSession,
    sem: Semaphore,
    file_name: str,
):
    try:
        url = url.format(i_param)
        async with sem:
            async with session.get(url, headers=headers) as resp:
                async with open(file_name, "a", encoding="utf-8-sig", newline="") as f:
                    txt = await resp.read()
                    data = BeautifulSoup(txt, "html.parser")
                    table = data.find_all(
                        "table", attrs={"class": "c_table_1 printTable"}
                    )[2]
                    trs = table.find_all("tr")[1:]
                    cells = [i_param]
                    for tr in trs:
                        tds = tr.find_all("td")
                        v = (
                            tds[1]
                            .text.strip()
                            .replace("\r\n", "")
                            .replace("\xa0", "")
                            .replace("\t", "")
                        )
                        cells.append(v)
                    writer = AsyncWriter(f)
                    await writer.writerow(cells)
                    return i_param
    except Exception as e:
        print(e)
        return -1


async def req_all_header(url: str, headers: dict, lst: list, file_name: str):
    sem = Semaphore(1)
    tasks = []
    exp_set = set()
    act_set = set()
    async with ClientSession(
        connector=TCPConnector(limit=3, verify_ssl="base_data/icbc.pem")
    ) as session:
        async with open(file_name, "w", encoding="utf-8-sig", newline="") as f:
            await f.truncate()
            writer = AsyncWriter(f)
            await writer.writerow(
                ["报账单号", "发票抬头", "纳税人识别码", "发票性质", "货物或应税劳务、服务名称", "发票备注", "邮寄地址"]
            )
        for i in lst:
            exp_set.add(i)
            tasks.append(req(url, headers, i, session, sem, file_name))
        res = await gather(*tasks)
        act_set = set(res)
        if exp_set != act_set:
            fail = exp_set - act_set
            print(f"未成功({len(fail)}):{fail}")
    pass


if __name__ == "__main__":
    # lst = ['202306030001411469', '202306030001411187']
    lst = ["202306030001411469"]
    headers = get_header()
    headers["Referer"] = "https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml"
    url = "https://sp.trade.icbc.com.cn/submit/seller/toDetail.jhtml?submitSeq={}&submit.year=0&flag=print"
    settings = get_settings()
    file_name = os_path.join(
        settings["folder_name"], f'{settings["header_file_name"]}.csv'
    )

    get_event_loop().run_until_complete(req_all_header(url, headers, lst, file_name))
    pass
