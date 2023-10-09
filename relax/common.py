from os import path as os_path
from pandas import read_excel


def get_page_size_list() -> list:
    df = read_excel(
        os_path.join("base_data", "size.xlsx"),
        usecols=["客户id", "筹措清单打印大小", "筹措清单份数", "备注"],
        dtype={"备注": str},
    )
    df[["备注"]] = df[["备注"]].astype(str)
    size_date = []
    for _, v in df.iterrows():
        zd = v["客户id"]
        page_size = v["筹措清单打印大小"]
        page_quantity = v["筹措清单份数"]
        remark: str = v["备注"].strip()
        # if not (remark == "nan" or remark == ""):
        #     continue
        if not (page_size == "A4" or page_size == "A5"):
            print(f"尺寸有误:{zd}")
            continue
        size_row = {
            "zd": zd,
            "page_size": page_size,
            "page_quantity": int(page_quantity),
        }
        size_date.append(size_row)
    return size_date


def get_ticket_size_list() -> list:
    df = read_excel(
        os_path.join("base_data", "size.xlsx"),
        usecols=["客户id", "发票打印大小", "发票份数", "备注"],
        dtype={"备注": str},
    )
    df[["备注"]] = df[["备注"]].astype(str)
    size_date = []
    for _, v in df.iterrows():
        zd = v["客户id"]
        page_size = v["发票打印大小"]
        page_quantity = v["发票份数"]
        remark: str = v["备注"].strip()
        # if not (remark == "nan" or remark == ""):
        #     continue
        if not (page_size == "A4" or page_size == "A5"):
            print(f"尺寸有误:{zd}")
            continue
        size_row = {
            "zd": zd,
            "page_size": page_size,
            "page_quantity": int(page_quantity),
        }
        size_date.append(size_row)
    return size_date


def get_one_page_size(size_data: list, zd: str) -> str:
    for row in size_data:
        if row["zd"] == int(zd):
            return row["page_size"]
    return None


def get_row_height(raw: str) -> int:
    height = 26
    raw_lenght = int(len(raw.encode("UTF8")) * 2 / 3)
    # 1行
    if raw_lenght <= 32:
        return height
    # 超过9个就换行
    break_count = 32
    row_count = int(raw_lenght / break_count)
    # 2行
    if row_count == 1:
        height += 7
        return height
    # 3行以上
    height = (row_count - 1) * 16

    if raw_lenght % break_count != 0:
        height += 16
    return height


def stamp(
    worksheet1, row_height_list: list, product_img_name, page_size, column, page_height
):
    if not page_height:
        return
    page_count = 1
    break_list = []
    part_height = 0
    part_height2 = 0
    total_height = 0
    rest_height = 0
    for height in row_height_list:
        total_height += height

    for i, height in enumerate(row_height_list, 1):
        part_height += height
        if part_height > page_height * page_count:
            part_height2 = part_height - height
            break_list.append(i - 1)
            page_count += 1
    rest_height = total_height - part_height2
    last_break = len(row_height_list)
    pic_row_index = 0
    if not break_list:
        if last_break < 7:
            pic_row_index = last_break - 1
        else:
            pic_row_index = last_break - 3
    else:
        if rest_height == 26:
            if break_list:
                break_list.pop()
            break_list.append(last_break - 2)
            pic_row_index = last_break - 1

        elif rest_height < 26 * 5:
            pic_row_index = last_break - 1
        else:
            pic_row_index = last_break - 3

    worksheet1.insert_image(
        f"{column}{pic_row_index}",
        product_img_name,
        {"x_scale": 4.2 / (4 * 4.62), "y_scale": 3 / (4 * 3.14), "y_offset": 2},
    )

    worksheet1.set_h_pagebreaks(break_list)
