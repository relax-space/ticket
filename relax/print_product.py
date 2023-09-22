'''
打印封面和商品
1. 获取灶点、尺寸和数量
2. 分别写入到不同的文件夹
'''

import os
import sys
import shutil
from relax.common import get_page_size_list


def make_print_file(
    cover_folder,
    prod_xlsx_folder,
    print_folder,
):
    size_date = get_page_size_list()

    for v in size_date:
        zd = v['zd']
        page_size = v['page_size']
        page_quantity = v['page_quantity']
        cover = os.path.join(cover_folder, f'{zd}.xlsx')
        if os.path.isfile(cover):
            for i in range(page_quantity):
                name = f'{zd}.xlsx'
                cover_name = f'{zd}-{i}.xlsx'
                prod_name = f'{zd}-{i}p.xlsx'
                shutil.copyfile(
                    os.path.join(cover_folder, name),
                    os.path.join(print_folder, page_size, cover_name),
                )
                shutil.copyfile(
                    os.path.join(prod_xlsx_folder, name),
                    os.path.join(print_folder, page_size, prod_name),
                )

    pass


if __name__ == '__main__':
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    prod_xlsx_folder = os.path.join(
        settings['folder_name'], settings['prod_xlsx_folder_name']
    )
    if not os.path.isdir(prod_xlsx_folder):
        raise Exception('请先下载产品')
    cover_folder = os.path.join(settings['folder_name'], settings['cover_folder_name'])
    if not os.path.isdir(cover_folder):
        raise Exception('请先下载封面')

    print_folder = os.path.join(
        settings['folder_name'],
        settings['print_folder_name'],
    )
    print_folder_A4 = os.path.join(
        print_folder,
        settings['print_folder_A4'],
    )
    if not os.path.isdir(print_folder_A4):
        os.makedirs(print_folder_A4)

    print_folder_A5 = os.path.join(
        print_folder,
        settings['print_folder_A5'],
    )
    if not os.path.isdir(print_folder_A5):
        os.makedirs(print_folder_A5)

    make_print_file(cover_folder, prod_xlsx_folder, print_folder)
    pass
