"""
下载商品
"""

from asyncio import Semaphore, gather, get_event_loop
from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup

from aiocsv import AsyncWriter
import aiofiles
import os

from relax.util import get_header, get_settings


async def req(
    url: str,
    headers: dict,
    z: str,
    i_param: str,
    session: ClientSession,
    sem: Semaphore,
    folder_name: str,
):
    try:
        url = url.format(i_param)
        async with sem:
            async with session.get(url, headers=headers) as resp:
                file_name = os.path.join(folder_name, f"{z}.csv")
                async with aiofiles.open(
                    file_name, "w", encoding="utf-8-sig", newline=""
                ) as f:
                    txt = await resp.read()
                    data = BeautifulSoup(txt, "html.parser")
                    div1 = data.find("div", attrs={"id": "print"})
                    t1 = div1.find("div", attrs={"class": "title_text"}).text.strip()
                    t2s = div1.find_all("div", attrs={"class", "sub_title_text"})
                    t2 = t2s[0].text.strip()
                    t_last = t2s[1].text.strip()
                    t3s = div1.find("div", attrs={"class", "note_title_text"}).find_all(
                        "span"
                    )
                    t30, t31, t32 = (
                        t3s[0].text.strip(),
                        t3s[1].text.strip(),
                        t3s[2].text.strip(),
                    )
                    writer = AsyncWriter(f)
                    await writer.writerow([t1, "", "", "", "", "", "", ""])
                    await writer.writerow([t2, "", "", "", "", "", "", ""])
                    await writer.writerow([t30, "", "", "", t31, "", t32, ""])

                    table = data.find_all(
                        "table", attrs={"class": "c_table_1 printTable"}
                    )[0]
                    trs = table.find_all("tr")
                    cells = []
                    for tr in trs:
                        tds = tr.find_all("td")
                        cond = tds[0].text.strip()
                        if cond == "小计" or cond == "本账单合计":
                            cells.append(
                                [
                                    tds[0].text.strip(),
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    tds[1].text.strip(),
                                ]
                            )
                            continue
                        vs = []
                        for td in tds:
                            vs.append(td.text.strip())
                        cells.append(vs)
                    await writer.writerows(cells)
                    await writer.writerow(["", "", "", "", "", "", "", t_last])
                    return i_param
    except Exception as e:
        print(e)
        return -1


async def req_all_prod(url: str, headers: dict, lst: list, folder_name: str):
    sem = Semaphore(1)
    tasks = []
    exp_set = set()
    act_set = set()
    async with ClientSession(
        connector=TCPConnector(limit=3, verify_ssl="base_data/icbc.pem")
    ) as session:
        for z, i in lst:
            exp_set.add(i)
            tasks.append(req(url, headers, z, i, session, sem, folder_name))
        res = await gather(*tasks)
        act_set = set(res)
        if exp_set != act_set:
            fail = exp_set - act_set
            print(f"未成功({len(fail)}):{fail}")
    pass


if __name__ == "__main__":
    # lst = ['202306030001411469', '202306030001411187']
    lst = [["51016", "202306030001411469"]]
    headers = get_header()
    headers["Referer"] = "https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml"
    url = "https://sp.trade.icbc.com.cn/submit/seller/toProdDetail.jhtml?submitSeq={}"
    settings = get_settings()
    folder_name = os.path.join(
        settings["folder_name"], f'{settings["prod_folder_name"]}'
    )

    get_event_loop().run_until_complete(req_all_prod(url, headers, lst, folder_name))
    pass
