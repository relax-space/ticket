"""
打印封面和商品
1. 获取灶点、尺寸和数量
2. 分别写入到不同的文件夹
"""

import os
import sys
import shutil
from relax.common import get_page_size_list


def make_print_file(size_date, folder, print_folder, order_mark, postfix):
    for v in size_date:
        zd = int(v["zd"])
        page_size = v["page_size"]
        page_quantity = v["page_quantity"]
        cover = os.path.join(folder, f"{zd}.{postfix}")
        if os.path.isfile(cover):
            for i in range(page_quantity):
                name = f"{zd}.{postfix}"
                print_name = f"{zd}-{i}{order_mark}-{page_size}.{postfix}"
                if postfix == "pdf":
                    print_name = f"{zd}-0{order_mark}{i}-{page_size}.{postfix}"
                shutil.copyfile(
                    os.path.join(folder, name),
                    os.path.join(print_folder, page_size, print_name),
                )
    pass


if __name__ == "__main__":
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    prod_xlsx_folder = os.path.join(
        settings["folder_name"], settings["prod_xlsx_folder_name"]
    )
    if not os.path.isdir(prod_xlsx_folder):
        raise Exception("请先下载产品")
    cover_folder = os.path.join(settings["folder_name"], settings["cover_folder_name"])
    if not os.path.isdir(cover_folder):
        raise Exception("请先下载封面")

    print_folder = os.path.join(
        settings["folder_name"],
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
    pass
