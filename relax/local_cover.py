"""
根据product文件夹内的文件，制作封面列表
"""
from os import chdir, path as os_path, listdir
from re import search
from openpyxl import Workbook
from pandas import read_csv, ExcelWriter
from sys import path as sys_path


try:
    from relax.util import get_companys, get_cover_1, get_cover_2, get_year_month
    from relax.common import (
        stamp,
        get_page_size_list,
        get_row_height,
        get_one_page_size,
    )
except:
    from util import get_companys, get_cover_1, get_cover_2, get_year_month
    from common import stamp, get_page_size_list, get_row_height, get_one_page_size


def get_numb(raw: str):
    v = search(r"\d+", raw)
    return v.group()


def get_data(bill_no: str, xls_file_name: str) -> list[dict]:
    df = read_csv(xls_file_name, header=3)
    fm_list = []
    date = ""
    for _, row in df.iterrows():
        cond = row["序号"]
        no = bill_no
        if cond != "小计":
            date = row["收货日期"]
            if cond == "本账单合计":
                date = ""
                no = f"{bill_no}汇总"
            else:
                continue
        amt = row["金额"]
        row_obj = {"A": no, "B": date, "C": amt}
        fm_list.append(row_obj)
    return fm_list


def write_cover(
    size_data,
    xls_name: str,
    fm_list: list[dict],
    cover_file_name: str,
    cover_content_1: str,
    cover_content_2: str,
    company,
):
    writer = ExcelWriter(cover_file_name, engine="xlsxwriter")
    workbook1: Workbook = writer.book
    worksheet1 = workbook1.add_worksheet("Sheet1")
    worksheet1.center_horizontally()

    worksheet1.set_column("A:A", 23)
    worksheet1.set_column("B:B", 21)
    worksheet1.set_column("C:C", 23)

    worksheet1.set_row(0, 48)
    worksheet1.set_row(1, 18)
    worksheet1.set_row(2, 26)

    # 行1
    fmt_row1 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 14,
            "bold": True,
            "align": "centre",
            "valign": "vcentre",
        }
    )
    worksheet1.write(0, 1, cover_content_1, fmt_row1)

    # 行2
    fmt_row2 = workbook1.add_format(
        {
            "font_name": "宋体",
            "font_size": 8,
            "align": "left",
            "valign": "vcentre",
        }
    )
    worksheet1.write(1, 0, cover_content_2, fmt_row2)

    # 行3
    fmt_row3 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 11,
            "align": "centre",
            "valign": "vcentre",
            "border": 1,
        }
    )
    worksheet1.write(2, 0, "灶点号", fmt_row3)
    worksheet1.write(2, 1, "收货日期", fmt_row3)
    worksheet1.write(2, 2, "金额", fmt_row3)

    fmt_mid = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 11,
            "bold": True,
            "align": "centre",
            "valign": "vcentre",
            "border": 1,
        }
    )
    fmt_mid2 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 11,
            "bold": False,
            "align": "centre",
            "valign": "vcentre",
            "border": 1,
        }
    )

    row_height_list = [48, 18, 26]
    for i, v in enumerate(fm_list):
        index = i + 3
        row_height_list.append(26)
        worksheet1.set_row(index, 26)
        worksheet1.write(index, 0, v["A"], fmt_mid)
        worksheet1.write(index, 1, v["B"], fmt_mid2)
        worksheet1.write(index, 2, v["C"], fmt_mid)

    row_height_list.append(26)

    fmt_last = workbook1.add_format(
        {
            "font_name": "宋体",
            "font_size": 10,
            "align": "centre",
            "valign": "vcentre",
        }
    )
    count = len(fm_list) + 3
    worksheet1.set_row(count, 26)
    worksheet1.write(count, 2, "（盖章）", fmt_last)

    zd = xls_name.replace(".csv", "")
    page_size = get_one_page_size(size_data, zd)
    page_height = None
    page_size_index = 9
    if page_size == "A4":
        page_height = 768
        page_size_index = 9
        worksheet1.set_portrait()
    elif page_size == "A5":
        page_height = 360
        page_size_index = 11
        worksheet1.set_landscape()

    worksheet1.set_paper(page_size_index)
    is_enable = company["stamp"]["enable"]
    if is_enable:
        product_img_name = company["stamp"]["path"]
        stamp(
            worksheet1, row_height_list, product_img_name, page_size, "B", page_height
        )
        worksheet1.set_margins(
            left=1.78 / 2.5, right=1.78 / 2.5, top=1.91 / 2.5, bottom=0.5 / 2.5
        )

    writer.close()


def make_cover(
    size_data,
    xls_name,
    product_folder: str,
    cover_folder: str,
    cover_content_1: str,
    cover_content_2: str,
    company,
):
    bill_no = get_numb(xls_name)
    xls_file_name = os_path.join(product_folder, xls_name)
    fm_list = get_data(bill_no, xls_file_name)
    cover_file_name = os_path.join(cover_folder, f"{bill_no}.xlsx")
    write_cover(
        size_data,
        xls_name,
        fm_list,
        cover_file_name,
        cover_content_1,
        cover_content_2,
        company,
    )
    pass


def make_cover_list(
    product_folder: str,
    cover_folder: str,
    cover_content_1: str,
    cover_content_2: str,
    company,
):
    files = listdir(product_folder)
    size_data = get_page_size_list()
    for i in files:
        make_cover(
            size_data,
            i,
            product_folder,
            cover_folder,
            cover_content_1,
            cover_content_2,
            company,
        )


if __name__ == "__main__":
    p = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))
    print(p)
    sys_path.insert(0, p)
    chdir(p)
    from relax.util import get_settings

    settings = get_settings()

    product_folder = os_path.join(settings["folder_name"], settings["prod_folder_name"])
    cover_folder = os_path.join(settings["folder_name"], settings["cover_folder_name"])

    year, month = get_year_month("2023-10-03")
    cover_content_1 = get_cover_1(year, month)
    company = get_companys()["0"]
    cover_content_2 = get_cover_2(company["company"]["name"])

    size_data = get_page_size_list()
    make_cover(
        size_data,
        "81006.csv",
        product_folder,
        cover_folder,
        cover_content_1,
        cover_content_2,
        company,
    )
    pass
