'''
根据product文件夹内的文件，制作封面列表
'''
import os
import re
from openpyxl import Workbook
import pandas as pd

from relax.util import get_settings


def get_numb(raw: str):
    v = re.search(r'\d+', raw)
    return v.group()


def get_data(bill_no: str, xls_file_name: str) -> list[dict]:
    df = pd.read_csv(xls_file_name, header=3)
    fm_list = []
    date = ''
    for _, row in df.iterrows():
        cond = row['序号']
        no = bill_no
        if cond != '小计':
            date = row['收货日期']
            if cond == '本账单合计':
                date = ''
                no = f'{bill_no}汇总'
            else:
                continue
        amt = row['金额']
        row_obj = {'A': no, 'B': date, 'C': amt}
        fm_list.append(row_obj)
    return fm_list


def write_cover(
    fm_list: list[dict],
    cover_file_name: str,
    cover_content_1: str,
    cover_content_2: str,
):
    writer = pd.ExcelWriter(cover_file_name, engine='xlsxwriter')
    workbook1: Workbook = writer.book
    worksheet1 = workbook1.add_worksheet('Sheet1')

    worksheet1.set_column('A:A', 23)
    worksheet1.set_column('B:B', 21)
    worksheet1.set_column('C:C', 23)

    worksheet1.set_row(0, 48)
    worksheet1.set_row(1, 18)
    worksheet1.set_row(2, 25.5)

    # 行1
    fmt_row1 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 14,
            'bold': True,
            'align': 'centre',
            'valign': 'vcentre',
        }
    )
    worksheet1.write(0, 1, cover_content_1, fmt_row1)

    # 行2
    fmt_row2 = workbook1.add_format(
        {
            "font_name": u"宋体",
            'font_size': 8,
            'align': 'left',
            'valign': 'vcentre',
        }
    )
    worksheet1.write(1, 0, cover_content_2, fmt_row2)

    # 行3
    fmt_row3 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 11,
            'align': 'centre',
            'valign': 'vcentre',
            'border': 1,
        }
    )
    worksheet1.write(2, 0, '序号', fmt_row3)
    worksheet1.write(2, 1, '收货日期', fmt_row3)
    worksheet1.write(2, 2, '金额', fmt_row3)

    fmt_mid = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 11,
            'bold': True,
            'align': 'centre',
            'valign': 'vcentre',
            'border': 1,
        }
    )
    fmt_mid2 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 11,
            'bold': False,
            'align': 'centre',
            'valign': 'vcentre',
            'border': 1,
        }
    )
    for i, v in enumerate(fm_list):
        index = i + 3
        worksheet1.set_row(index, 25.5)
        worksheet1.write(index, 0, v['A'], fmt_mid)
        worksheet1.write(index, 1, v['B'], fmt_mid2)
        worksheet1.write(index, 2, v['C'], fmt_mid)

    fmt_last = workbook1.add_format(
        {
            "font_name": u"宋体",
            'font_size': 10,
            'align': 'centre',
            'valign': 'vcentre',
        }
    )
    count = len(fm_list) + 3
    worksheet1.set_row(count, 25.5)
    worksheet1.write(count, 2, '（盖章）', fmt_last)
    writer.close()


def make_cover(
    xls_name,
    product_folder: str,
    cover_folder: str,
    cover_content_1: str,
    cover_content_2: str,
):
    bill_no = get_numb(xls_name)
    xls_file_name = os.path.join(product_folder, xls_name)
    fm_list = get_data(bill_no, xls_file_name)
    cover_file_name = os.path.join(cover_folder, f'{bill_no}.xlsx')
    write_cover(fm_list, cover_file_name, cover_content_1, cover_content_2)
    pass


def make_cover_list(
    product_folder: str,
    cover_folder: str,
    cover_content_1: str,
    cover_content_2: str,
):
    files = os.listdir(product_folder)
    for i in files:
        make_cover(i, product_folder, cover_folder, cover_content_1, cover_content_2)


if __name__ == '__main__':
    settings = get_settings()

    product_folder = os.path.join(settings['folder_name'], settings['prod_folder_name'])
    cover_folder = os.path.join(settings['folder_name'], settings['cover_folder_name'])
    cover_content_1 = settings['cover_content_1']
    cover_content_2 = settings['cover_content_2']
    make_cover_list(product_folder, cover_folder, cover_content_1, cover_content_2)
    pass
