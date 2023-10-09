"""
合并list 和 header
"""


from sys import path as sys_path
from pandas import read_csv
from os import path as os_path, chdir


def merge(list_file_name: str, header_file_name: str, list_header_name: str):
    df1 = read_csv(list_file_name, dtype={"报账单号": "str", "报账单批次号": "str"})
    df2 = read_csv(header_file_name, dtype={"报账单号": "str"})
    df = df1.merge(df2, how="inner", on=["报账单号"])
    df = df.sort_values(by="灶点编码")
    df["序号"] = range(1, len(df) + 1)
    df.to_excel(list_header_name, index=False)


if __name__ == "__main__":
    p = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))
    sys_path.insert(0, p)
    chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    list_file_name = os_path.join(
        settings["folder_name"], f'{settings["list_file_name"]}.csv'
    )
    header_file_name = os_path.join(
        settings["folder_name"], f'{settings["header_file_name"]}.csv'
    )
    list_header_name = os_path.join(
        settings["folder_name"], f'{settings["list_header_name"]}.xlsx'
    )
    merge(list_file_name, header_file_name, list_header_name)
