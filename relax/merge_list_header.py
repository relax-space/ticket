'''
合并list 和 header
'''


import pandas as pd
import os
from relax.util import get_settings


def merge(list_file_name: str, header_file_name: str, list_header_name: str):
    df1 = pd.read_csv(list_file_name, dtype={"报账单号": "str", "报账单批次号": "str"})
    df2 = pd.read_csv(header_file_name, dtype={"报账单号": "str"})
    df = df1.merge(df2, how='inner', on=["报账单号"])
    df.to_excel(list_header_name, index=False)


if __name__ == '__main__':
    settings = get_settings()
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
