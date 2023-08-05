import os
import sys
import pandas as pd


def write_one(prod_folder, prod_xlsx_folder, xlsx_name):
    writer = pd.ExcelWriter(
        os.path.join(prod_xlsx_folder, f'{xlsx_name}.xlsx'), engine='xlsxwriter'
    )
    workbook1 = writer.book
    worksheet1 = workbook1.add_worksheet('Sheet1')
    worksheet1.center_horizontally()

    fmt_row1 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 14,
            'bold': True,
            'align': 'centre',
            'valign': 'vcentre',
        }
    )

    fmt_row2 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 10,
            'align': 'centre',
            'valign': 'vcentre',
        }
    )

    fmt_row3 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 8,
            'align': 'left',
            'valign': 'vcentre',
        }
    )

    fmt_row4 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 8,
            'align': 'centre',
            'valign': 'vcentre',
            'border': 1,
        }
    )

    fmt_row5 = workbook1.add_format(
        {
            "font_name": u"Arial",
            'font_size': 8,
            'bold': True,
            'align': 'centre',
            'valign': 'vcentre',
            'border': 1,
        }
    )

    fmt_row6 = workbook1.add_format(
        {
            "font_name": u"宋体",
            'font_size': 10,
            'align': 'centre',
            'valign': 'vcentre',
        }
    )

    adjust_width = 0.13

    worksheet1.set_column(0, 0, 3.29 - adjust_width)
    worksheet1.set_column(1, 1, 7 - adjust_width)
    worksheet1.set_column('C:C', 15.57 - adjust_width)
    worksheet1.set_column('D:D', 27 - adjust_width)
    worksheet1.set_column('E:E', 9.86 - adjust_width)
    worksheet1.set_column('F:F', 6.57 - adjust_width)
    worksheet1.set_column('G:G', 5.14 - adjust_width)
    worksheet1.set_column('H:H', 9.86 - adjust_width)

    df = pd.read_csv(
        os.path.join(prod_folder, f'{xlsx_name}.csv'),
        names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    )
    df = df.astype(str)

    for i, row in df.iterrows():
        if i == 0:
            worksheet1.set_row(i, 48)
            worksheet1.merge_range(i, 0, i, 7, row['A'], fmt_row1)
        elif i == 1:
            worksheet1.set_row(i, 21)
            worksheet1.merge_range(i, 0, i, 7, row['A'], fmt_row2)
        elif i == 2:
            worksheet1.set_row(i, 18)
            worksheet1.merge_range(i, 0, i, 3, row['A'], fmt_row3)
            worksheet1.merge_range(i, 4, i, 5, row['E'], fmt_row3)
            worksheet1.merge_range(i, 6, i, 7, row['G'], fmt_row3)
        elif i == 3:
            worksheet1.set_row(i, 25.5)
            worksheet1.write(i, 0, row['A'], fmt_row4)
            worksheet1.write(i, 1, row['B'], fmt_row4)
            worksheet1.write(i, 2, row['C'], fmt_row4)
            worksheet1.write(i, 3, row['D'], fmt_row4)
            worksheet1.write(i, 4, row['E'], fmt_row4)
            worksheet1.write(i, 5, row['F'], fmt_row4)
            worksheet1.write(i, 6, row['G'], fmt_row4)
            worksheet1.write(i, 7, row['H'], fmt_row4)
        elif row['A'] == '小计':
            worksheet1.set_row(i, 22.5)
            worksheet1.merge_range(i, 0, i, 6, row['A'], fmt_row5)
            worksheet1.write(i, 7, row['H'], fmt_row5)
        elif row['A'] == '本账单合计':
            worksheet1.set_row(i, 24.75)
            worksheet1.merge_range(i, 0, i, 6, row['A'], fmt_row5)
            worksheet1.write(i, 7, row['H'], fmt_row5)
        elif row['H'] == '（盖章）':
            worksheet1.set_row(i, 18.75)
            worksheet1.write(i, 7, row['H'], fmt_row6)
        else:
            worksheet1.set_row(i, 25.5)
            worksheet1.write(i, 0, row['A'], fmt_row4)
            worksheet1.write(i, 1, row['B'], fmt_row4)
            worksheet1.write(i, 2, row['C'], fmt_row4)
            worksheet1.write(i, 3, row['D'], fmt_row4)
            worksheet1.write(i, 4, row['E'], fmt_row4)
            worksheet1.write(i, 5, row['F'], fmt_row4)
            worksheet1.write(i, 6, row['G'], fmt_row4)
            worksheet1.write(i, 7, row['H'], fmt_row4)
        pass

    writer.close()


def write_all(prod_folder, prod_xlsx_folder):
    files = os.listdir(prod_folder)
    for i in files:
        short_i = str.replace(i, '.csv', '')
        write_one(prod_folder, prod_xlsx_folder, short_i)


pass

if __name__ == '__main__':
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    prod_folder = os.path.join(settings['folder_name'], settings['prod_folder_name'])
    prod_xlsx_folder = os.path.join(
        settings['folder_name'], settings['prod_xlsx_folder_name']
    )
    if not os.path.isdir(prod_folder):
        os.makedirs(prod_folder)
    if not os.path.isdir(prod_xlsx_folder):
        os.makedirs(prod_xlsx_folder)
    write_one(prod_folder, prod_xlsx_folder, '11001')
    pass
