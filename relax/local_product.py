from pandas import read_csv, ExcelWriter
from os import path as os_path, listdir, chdir, makedirs
from sys import path as sys_path


try:
    from relax.common import (
        stamp,
        get_page_size_list,
        get_row_height,
        get_one_page_size,
    )
    from relax.util import get_companys
except:
    from common import (
        stamp,
        get_page_size_list,
        get_row_height,
        get_one_page_size,
    )
    from util import get_companys


def write_one(size_data, prod_folder, prod_xlsx_folder, company, xlsx_name):
    writer = ExcelWriter(
        os_path.join(prod_xlsx_folder, f"{xlsx_name}.xlsx"), engine="xlsxwriter"
    )
    workbook1 = writer.book
    worksheet1 = workbook1.add_worksheet("Sheet1")
    worksheet1.center_horizontally()

    fmt_row1 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 14,
            "bold": True,
            "align": "centre",
            "valign": "vcentre",
        }
    )

    fmt_row2 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 10,
            "align": "centre",
            "valign": "vcentre",
        }
    )

    fmt_row3 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "left",
            "valign": "vcentre",
        }
    )

    fmt_row4 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "align": "centre",
            "valign": "vcentre",
            "border": 1,
        }
    )

    fmt_row5 = workbook1.add_format(
        {
            "font_name": "Arial",
            "font_size": 8,
            "bold": True,
            "align": "centre",
            "valign": "vcentre",
            "border": 1,
        }
    )

    fmt_row6 = workbook1.add_format(
        {
            "font_name": "宋体",
            "font_size": 10,
            "align": "centre",
            "valign": "vcentre",
        }
    )

    adjust_width = 0.13

    worksheet1.set_column(0, 0, 3.29 - adjust_width)
    worksheet1.set_column(1, 1, 7 - adjust_width)
    worksheet1.set_column("C:C", 15.57 - adjust_width)
    worksheet1.set_column("D:D", 27 - adjust_width)
    worksheet1.set_column("E:E", 9.86 - adjust_width)
    worksheet1.set_column("F:F", 6.57 - adjust_width)
    worksheet1.set_column("G:G", 5.14 - adjust_width)
    worksheet1.set_column("H:H", 9.86 - adjust_width)

    df = read_csv(
        os_path.join(prod_folder, f"{xlsx_name}.csv"),
        names=["A", "B", "C", "D", "E", "F", "G", "H"],
    )
    df = df.astype(str)
    row_height_list = []
    for i, row in df.iterrows():
        if i == 0:
            row_height_list.append(48)
            worksheet1.set_row(i, 48)
            worksheet1.merge_range(i, 0, i, 7, row["A"], fmt_row1)
        elif i == 1:
            row_height_list.append(21)
            worksheet1.set_row(i, 21)
            worksheet1.merge_range(i, 0, i, 7, row["A"], fmt_row2)
        elif i == 2:
            row_height_list.append(18)
            worksheet1.set_row(i, 18)
            worksheet1.merge_range(i, 0, i, 3, row["A"], fmt_row3)
            worksheet1.merge_range(i, 4, i, 5, row["E"], fmt_row3)
            worksheet1.merge_range(i, 6, i, 7, row["G"], fmt_row3)
        elif i == 3:
            row_height_list.append(26)
            worksheet1.set_row(i, 26)
            worksheet1.write(i, 0, row["A"], fmt_row4)
            worksheet1.write(i, 1, row["B"], fmt_row4)
            worksheet1.write(i, 2, row["C"], fmt_row4)
            worksheet1.write(i, 3, row["D"], fmt_row4)
            worksheet1.write(i, 4, row["E"], fmt_row4)
            worksheet1.write(i, 5, row["F"], fmt_row4)
            worksheet1.write(i, 6, row["G"], fmt_row4)
            worksheet1.write(i, 7, row["H"], fmt_row4)
        elif row["A"] == "小计":
            row_height_list.append(26)
            worksheet1.set_row(i, 26)
            worksheet1.merge_range(i, 0, i, 6, row["A"], fmt_row5)
            worksheet1.write(i, 7, row["H"], fmt_row5)
        elif row["A"] == "本账单合计":
            row_height_list.append(26)
            worksheet1.set_row(i, 26)
            worksheet1.merge_range(i, 0, i, 6, row["A"], fmt_row5)
            worksheet1.write(i, 7, row["H"], fmt_row5)
        elif row["H"] == "（盖章）":
            row_height_list.append(26)
            worksheet1.set_row(i, 26)
            worksheet1.write(i, 7, row["H"], fmt_row6)
        else:
            row_height = get_row_height(row["D"])
            row_height_list.append(row_height)
            worksheet1.set_row(i, row_height)
            worksheet1.write(i, 0, row["A"], fmt_row4)
            worksheet1.write(i, 1, row["B"], fmt_row4)
            worksheet1.write(i, 2, row["C"], fmt_row4)
            worksheet1.write(i, 3, row["D"], fmt_row4)
            worksheet1.write(i, 4, row["E"], fmt_row4)
            worksheet1.write(i, 5, row["F"], fmt_row4)
            worksheet1.write(i, 6, row["G"], fmt_row4)
            worksheet1.write(i, 7, row["H"], fmt_row4)
        pass

    page_size = get_one_page_size(size_data, xlsx_name)

    page_height = None
    page_size_index = 9
    if page_size == "A4":
        page_height = 768
        page_size_index = 9
        worksheet1.set_portrait()
    elif page_size == "A5":
        page_height = 340
        page_size_index = 11
        worksheet1.set_landscape()

    worksheet1.set_paper(page_size_index)
    is_enable = company["stamp"]["enable"]
    if is_enable:
        product_img_name = company["stamp"]["path"]
        stamp(
            worksheet1, row_height_list, product_img_name, page_size, "D", page_height
        )

        worksheet1.set_margins(
            left=1.78 / 2.5, right=1.78 / 2.5, top=1.91 / 2.5, bottom=0.5 / 2.5
        )

    writer.close()


def write_all(prod_folder, prod_xlsx_folder, company):
    files = listdir(prod_folder)
    size_data = get_page_size_list()
    for i in files:
        short_i = str.replace(i, ".csv", "")
        write_one(size_data, prod_folder, prod_xlsx_folder, company, short_i)


pass

if __name__ == "__main__":
    p = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))
    sys_path.insert(0, p)
    chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    prod_folder = os_path.join(settings["folder_name"], settings["prod_folder_name"])
    prod_xlsx_folder = os_path.join(
        settings["folder_name"], settings["prod_xlsx_folder_name"]
    )
    if not os_path.isdir(prod_folder):
        makedirs(prod_folder)
    if not os_path.isdir(prod_xlsx_folder):
        makedirs(prod_xlsx_folder)

    company = get_companys()["0"]
    size_data = get_page_size_list()
    write_one(size_data, prod_folder, prod_xlsx_folder, company, "11015")
    pass
