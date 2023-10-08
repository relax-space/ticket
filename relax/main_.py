import os
import sys
import asyncio
import pandas as pd

from relax.count_ import add_count

try:
    from relax.common import get_page_size_list, get_ticket_size_list
    from relax.local_cover import make_cover_list
    from relax.down_prod import req_all_prod
    from relax.local_import import make_import_list
    from relax.local_product import write_all
    from relax.print_product import make_print_file
    from relax.util import (
        get_companys,
        get_cover_1,
        get_cover_2,
        get_header,
        get_settings,
        get_year_month,
    )

    from relax.cookie_check import check
    from relax.down_list import get_page_count, download_list_data

    from relax.down_header import req_all_header
    from relax.local_header import merge
except:
    pass


# check cookie
def step_1(headers: dict):
    headers["Referer"] = "https://loginaep.mall.icbc.com.cn/"
    url = "https://sp.trade.icbc.com.cn/index.jhtml"
    is_success = check(url, headers=headers)
    return is_success


# download list
def step_2(headers: dict, search_date: str, output_path):
    headers["Referer"] = "https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml"
    url = "https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml"
    params = {
        "pageIndex": "1",
        "taskName": "",
        "startTime": search_date,
        "endTime": search_date,
        "submit.submitSeq": "",
        "submit.projectId": "",
        "submit.batchNo": "",
        "submit.submitStatus": "",
        "submit.year": "",
    }
    count = get_page_count(url, params=params, headers=headers)
    if not count:
        print("获取分页数量失败")
        return
    print(f"获取分页数量成功:{count}")
    file_name = os.path.join(output_path, f'{settings["list_file_name"]}.csv')
    download_list_data(url, params, headers, count, file_name)


# download header
async def step_3(headers: dict, settings: dict, lst: list, output_path):
    headers["Referer"] = "https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml"
    url = "https://sp.trade.icbc.com.cn/submit/seller/toDetail.jhtml?submitSeq={}&submit.year=0&flag=print"
    file_name = os.path.join(output_path, f'{settings["header_file_name"]}.csv')
    await req_all_header(url, headers, lst, file_name)


# download products
async def step_4(headers: dict, settings: dict, lst: list, output_path):
    headers["Referer"] = "https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml"
    url = "https://sp.trade.icbc.com.cn/submit/seller/toProdDetail.jhtml?submitSeq={}"
    folder_name = os.path.join(output_path, f'{settings["prod_folder_name"]}')
    await req_all_prod(url, headers, lst, folder_name)


# merge
def step_5(settings: dict, output_path):
    list_file_name = os.path.join(output_path, f'{settings["list_file_name"]}.csv')
    header_file_name = os.path.join(output_path, f'{settings["header_file_name"]}.csv')
    list_header_name = os.path.join(output_path, f'{settings["list_header_name"]}.xlsx')
    merge(list_file_name, header_file_name, list_header_name)
    pass


# make cover
def step_6(settings: dict, company: dict, search_date, output_path):
    product_folder = os.path.join(output_path, settings["prod_folder_name"])
    cover_folder = os.path.join(output_path, settings["cover_folder_name"])
    year, month = get_year_month(search_date)
    cover_content_1 = get_cover_1(year, month)
    cover_content_2 = get_cover_2(company["company"]["name"])
    make_cover_list(
        product_folder, cover_folder, cover_content_1, cover_content_2, company
    )


def step_7(settings: dict, company: dict, output_path):
    prod_folder = os.path.join(output_path, settings["prod_folder_name"])
    prod_xlsx_folder = os.path.join(output_path, settings["prod_xlsx_folder_name"])
    write_all(prod_folder, prod_xlsx_folder, company)


# make import list
def step_8(settings: dict, output_path):
    base_file_name = settings["base_file_name"]
    prod_folder_name = os.path.join(output_path, settings["prod_folder_name"])
    import_folder_name = os.path.join(output_path, settings["import_folder_name"])
    return make_import_list(base_file_name, prod_folder_name, import_folder_name)


def step_9(settings: dict, output_path):
    prod_xlsx_folder = os.path.join(output_path, settings["prod_xlsx_folder_name"])
    if not os.path.isdir(prod_xlsx_folder):
        raise Exception("请先下载产品")
    cover_folder = os.path.join(output_path, settings["cover_folder_name"])
    if not os.path.isdir(cover_folder):
        raise Exception("请先下载封面")

    print_folder = os.path.join(
        output_path,
        settings["print_folder_name"],
    )
    print_folder_A4 = os.path.join(
        print_folder,
        settings["print_folder_A4"],
    )
    if not os.path.isdir(print_folder_A4):
        os.makedirs(print_folder_A4)

    print_folder_A5 = os.path.join(
        print_folder,
        settings["print_folder_A5"],
    )
    if not os.path.isdir(print_folder_A5):
        os.makedirs(print_folder_A5)
    size_list = get_page_size_list()
    make_print_file(size_list, cover_folder, print_folder, "i", "xlsx")
    make_print_file(size_list, prod_xlsx_folder, print_folder, "j", "xlsx")


def step_10(settings: dict, output_path):
    ticket_folder = os.path.join(output_path, settings["ticket_folder_name"])
    if not os.path.isdir(ticket_folder):
        raise Exception("请先下载发票")

    print_folder = os.path.join(
        output_path,
        settings["print_folder_name"],
    )
    print_folder_A4 = os.path.join(
        print_folder,
        settings["print_folder_A4"],
    )
    if not os.path.isdir(print_folder_A4):
        os.makedirs(print_folder_A4)

    print_folder_A5 = os.path.join(
        print_folder,
        settings["print_folder_A5"],
    )
    if not os.path.isdir(print_folder_A5):
        os.makedirs(print_folder_A5)
    size_list = get_ticket_size_list()
    make_print_file(size_list, ticket_folder, print_folder, "h", "pdf")


def get_csv_list(settings: dict, output_path):
    file_name = os.path.join(output_path, f'{settings["list_file_name"]}.csv')
    datas = pd.read_csv(file_name, usecols=["报账单号"])
    lst = datas["报账单号"].values.tolist()
    return lst


def get_csv_two_list(settings: dict, output_path):
    file_name = os.path.join(output_path, f'{settings["list_file_name"]}.csv')
    datas = pd.read_csv(file_name, usecols=["灶点编码", "报账单号"])
    lst = datas.values.tolist()
    return lst


def init(settings, output_path) -> dict:
    prod_folder = os.path.join(output_path, settings["prod_folder_name"])
    if not os.path.isdir(prod_folder):
        os.makedirs(prod_folder)
    cover_folder = os.path.join(output_path, settings["cover_folder_name"])
    if not os.path.isdir(cover_folder):
        os.makedirs(cover_folder)
    import_folder = os.path.join(output_path, settings["import_folder_name"])
    if not os.path.isdir(import_folder):
        os.makedirs(import_folder)
    prod_xlsx_folder = os.path.join(output_path, settings["prod_xlsx_folder_name"])
    if not os.path.isdir(prod_xlsx_folder):
        os.makedirs(prod_xlsx_folder)

    ticket_folder = os.path.join(output_path, settings["ticket_folder_name"])
    if not os.path.isdir(ticket_folder):
        os.makedirs(ticket_folder)

    print_folder = os.path.join(
        output_path,
        settings["print_folder_name"],
    )
    print_folder_A4 = os.path.join(
        print_folder,
        settings["print_folder_A4"],
    )
    if not os.path.isdir(print_folder_A4):
        os.makedirs(print_folder_A4)

    print_folder_A5 = os.path.join(
        print_folder,
        settings["print_folder_A5"],
    )
    if not os.path.isdir(print_folder_A5):
        os.makedirs(print_folder_A5)
    return settings


async def main_async(
    headers: dict, company: dict, settings: dict, search_date: str, is_download: bool
):
    output_path = company["company"]["output_path"]
    init(settings, output_path)
    if is_download:
        # is_success = step_1(headers)
        # if not is_success:
        #     print("valid fail")
        #     return "1.验证失败"
        # print("1.验证完成")

        # step_2(headers, search_date, output_path)
        # print(f'2.下载完成：{settings["list_file_name"]}.csv')

        # lst = None
        # lst = get_csv_list(settings, output_path)
        # # lst = ["202309030001518570"]
        # await step_3(
        #     headers,
        #     settings,
        #     lst,
        #     output_path,
        # )
        # print(f'3.下载完成：{settings["header_file_name"]}.csv')

        # lst = get_csv_two_list(settings, output_path)
        # # lst = [["51016", "202309030001518570"]]
        # await step_4(headers, settings, lst, output_path)
        # print(f'4.下载完成：{settings["prod_folder_name"]}')
        add_count()

    step_5(settings, output_path)
    print(f'5.合并完成：{settings["prod_folder_name"]}')

    step_6(settings, company, search_date, output_path)
    print(f'6.制作封面完成：{settings["cover_folder_name"]}')

    step_7(settings, company, output_path)
    print(f'7.商品/*.xlsx完成：{settings["prod_xlsx_folder_name"]}')

    set1 = step_8(settings, output_path)
    if len(set1) > 0:
        print(f"税率没有发现{set1}")
    print(f'8.导入列表完成：{settings["import_folder_name"]}')

    step_9(settings, output_path)
    print(f"9.打印列表A4A5完成：{settings['print_folder_name']}")

    step_10(settings, output_path)
    print(f"10.打印列表A4A5完成：{settings['print_folder_name']}")

    print("全部任务已完成")
    return None

    pass


if __name__ == "__main__":
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.common import get_page_size_list, get_ticket_size_list
    from relax.local_cover import make_cover_list
    from relax.down_prod import req_all_prod
    from relax.local_import import make_import_list
    from relax.local_product import write_all
    from relax.print_product import make_print_file
    from relax.util import (
        get_companys,
        get_cover_1,
        get_cover_2,
        get_header,
        get_settings,
        get_year_month,
    )

    from relax.cookie_check import check
    from relax.down_list import get_page_count, download_list_data

    from relax.down_header import req_all_header
    from relax.local_header import merge

    headers = get_header()
    settings = get_settings()
    # 0 食安， 1：农惠民
    company = get_companys()["0"]
    search_date = "2023-10-03"
    cookie = "1111"
    headers.update({"Cookie": cookie})

    asyncio.get_event_loop().run_until_complete(
        main_async(headers, company, settings, search_date, True)
    )
    pass
