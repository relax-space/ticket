'''
制作开电子票的模板
'''
import codecs
import pandas as pd
import os
import sys


def make_import_one(
    df_bases: pd.DataFrame,
    set1: set,
    prod_folder_name: str,
    import_folder_name: str,
    csvname: str,
):
    df = pd.read_csv(
        os.path.join(prod_folder_name, csvname), header=3, encoding='utf-8'
    )
    rows = []
    for i, row in df.iterrows():
        cond = row['序号']
        if pd.isna(cond):
            continue
        if not str.isdecimal(cond):
            continue
        new_row = []
        prod = row['商品名称']
        print(repr(prod))
        new_row.append(prod)
        new_row.append('')
        new_row.append(row['计量单位'])
        new_row.append(row['数量'])
        new_row.append('')
        new_row.append(row['金额'])

        df_base = df_bases.query('商品名称 == @prod')
        if df_base.empty:
            set1.add(prod)
            new_row.append('没有找到')
            new_row.append('')
            new_row.append('')
        else:
            new_row.append(df_base['税率'].fillna('0.0').values[0])
            new_row.append(df_base['税收编码'].fillna('').values[0])
            new_row.append(df_base['免税'].fillna('').values[0])
        rows.append(new_row)
    xlsxname = csvname.replace('csv', 'xlsx')
    pd.DataFrame(
        rows,
        columns=['商品名称*', '规格型号', '单位', '数量', '单价', '金额', '税率', '税收分类编码', '优惠政策名称'],
    ).to_excel(os.path.join(import_folder_name, xlsxname), startrow=2, index=False)


def make_import_list(
    base_file_name: str, prod_folder_name: str, import_folder_name: str
) -> set:
    df_bases = get_all_base(base_file_name)
    files = os.listdir(prod_folder_name)
    set1 = set()
    for i in files:
        make_import_one(df_bases, set1, prod_folder_name, import_folder_name, i)
    return set1


def get_all_base(base_file_name: str) -> pd.DataFrame:
    df = pd.read_excel(
        f'{base_file_name}.xlsx',
        usecols=['商品名称', '计量单位', '税率', '免税', '税收编码'],
        dtype={'税收编码': str, '税率': str},
    )
    return df


if __name__ == '__main__':
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    base_file_name = settings['base_file_name']
    prod_folder_name = os.path.join(
        settings['folder_name'], settings['prod_folder_name']
    )
    import_folder_name = os.path.join(
        settings['folder_name'], settings['import_folder_name']
    )
    df_bases = get_all_base(base_file_name)
    set1 = set()
    i = '11001.csv'
    make_import_one(df_bases, set1, prod_folder_name, import_folder_name, i)
    if len(set1) > 0:
        print(f'税率没有发现{set1}')
    pass
