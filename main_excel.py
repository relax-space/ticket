from relax.local_cover import make_cover_list
from relax.down_prod import req_all_prod
from relax.local_import import make_import_list
from relax.util import get_header, get_settings
import os
import sys

from relax.cookie_check import check
from relax.down_list import get_page_count, download_list_data
import asyncio
import pandas as pd
from relax.down_header import req_all_header
from relax.local_header import merge


# check cookie
def step_1(headers: dict):
    headers['Referer'] = 'https://loginaep.mall.icbc.com.cn/'
    url = 'https://sp.trade.icbc.com.cn/index.jhtml'
    is_success = check(url, headers=headers)
    return is_success


# download list
def step_2(headers: dict, settings: dict):
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
    count = get_page_count(url, params=params, headers=headers)
    if not count:
        print('获取分页数量失败')
        return
    print('获取分页数量成功')
    file_name = os.path.join(
        settings['folder_name'], f'{settings["list_file_name"]}.csv'
    )
    download_list_data(url, params, headers, count, file_name)


# download header
async def step_3(headers: dict, settings: dict, lst: list):
    headers['Referer'] = 'https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml'
    url = 'https://sp.trade.icbc.com.cn/submit/seller/toDetail.jhtml?submitSeq={}&submit.year=0&flag=print'
    file_name = os.path.join(
        settings['folder_name'], f'{settings["header_file_name"]}.csv'
    )
    await req_all_header(url, headers, lst, file_name)
    print(f'下载{settings["header_file_name"]}.csv完成')


# download products
async def step_4(headers: dict, settings: dict, lst: list):
    headers['Referer'] = 'https://sp.trade.icbc.com.cn/submit/seller/toSubmitList.jhtml'
    url = 'https://sp.trade.icbc.com.cn/submit/seller/toProdDetail.jhtml?submitSeq={}'
    folder_name = os.path.join(
        settings['folder_name'], f'{settings["prod_folder_name"]}'
    )
    await req_all_prod(url, headers, lst, folder_name)
    print(f'下载{settings["header_file_name"]}.csv完成')


# merge
def step_5(settings: dict):
    list_file_name = os.path.join(
        settings['folder_name'], f'{settings["list_file_name"]}.csv'
    )
    header_file_name = os.path.join(
        settings['folder_name'], f'{settings["header_file_name"]}.csv'
    )
    list_header_name = os.path.join(
        settings['folder_name'], f'{settings["list_header_name"]}.xlsx'
    )
    merge(list_file_name, header_file_name, list_header_name)
    pass


# make cover
def step_6(settings: dict):
    product_folder = os.path.join(settings['folder_name'], settings['prod_folder_name'])
    cover_folder = os.path.join(settings['folder_name'], settings['cover_folder_name'])
    cover_content_1 = settings['cover_content_1']
    cover_content_2 = settings['cover_content_2']
    make_cover_list(product_folder, cover_folder, cover_content_1, cover_content_2)


# make import list
def step_7(settings: dict):
    base_file_name = settings['base_file_name']
    prod_folder_name = os.path.join(
        settings['folder_name'], settings['prod_folder_name']
    )
    import_folder_name = os.path.join(
        settings['folder_name'], settings['import_folder_name']
    )
    return make_import_list(base_file_name, prod_folder_name, import_folder_name)


def get_csv_list(settings: dict):
    file_name = os.path.join(
        settings['folder_name'], f'{settings["list_file_name"]}.csv'
    )
    datas = pd.read_csv(file_name, usecols=['报账单号'])
    lst = datas['报账单号'].values.tolist()
    return lst


def get_csv_two_list(settings: dict):
    file_name = os.path.join(
        settings['folder_name'], f'{settings["list_file_name"]}.csv'
    )
    datas = pd.read_csv(file_name, usecols=['灶点编码', '报账单号'])
    lst = datas.values.tolist()
    return lst


async def main_async(headers: dict):
    settings = get_settings()
    prod_folder = os.path.join(settings['folder_name'], settings['prod_folder_name'])
    if not os.path.isdir(prod_folder):
        os.makedirs(prod_folder)
    cover_folder = os.path.join(settings['folder_name'], settings['cover_folder_name'])
    if not os.path.isdir(cover_folder):
        os.makedirs(cover_folder)
    import_folder = os.path.join(
        settings['folder_name'], settings['import_folder_name']
    )
    if not os.path.isdir(import_folder):
        os.makedirs(import_folder)

    # step_5(settings)
    # print(f'5.合并完成：{settings["prod_folder_name"]}')

    # step_6(settings)
    # print(f'6.制作封面完成：{settings["cover_folder_name"]}')

    set1 = step_7(settings)
    if len(set1) > 0:
        print(f'税率没有发现{set1}')
    print(f'7.导入列表完成：{settings["import_folder_name"]}')

    print('全部任务已完成')

    pass


if __name__ == '__main__':
    p = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, p)
    os.chdir(p)
    headers = get_header()

    asyncio.get_event_loop().run_until_complete(main_async(headers))
    pass
