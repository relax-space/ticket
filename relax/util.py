def get_header():
    headers = {
        'Host': 'sp.trade.icbc.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0; SE 2.X MetaSr 1.0) like Gecko',
    }
    with open('relax/cookie.txt', mode='r', encoding='utf-8') as f:
        cookie = f.read()
    headers['Cookie'] = cookie
    return headers


def get_settings():
    settings = {
        'folder_name': 'data',
        'list_file_name': 'list',
        'list_file_start': '2023-08-03',
        'list_file_end': '2023-08-03',
        'header_file_name': 'header',
        'prod_folder_name': 'product',
        'prod_xlsx_folder_name': 'product_xlsx',
        'list_header_name': 'list_header',
        'cover_folder_name': 'cover',
        'cover_content_1': '2023年7月驻琼部队副食品区域集中筹措物资【封面】',
        'cover_content_2': '供应商：海南食安万商电子商务有限公司                       每日汇总表',
        'base_file_name': 'base',
        'import_folder_name': 'import_list',
    }
    return settings
