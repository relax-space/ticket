"""
制作开电子票的模板：电子税务局
"""
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
        os.path.join(prod_folder_name, csvname), header=3, encoding="utf-8"
    )
    rows = []
    rows.append(
        [
            """必填
(限100字符)""",
            """非必填
(限19字符)""",
            """非必填
(限40字符)""",
            """非必填
(限20字符)
""",
            """非必填
(限16字符)""",
            """非必填
(限16字符)	""",
            """必填
(限18字符)
(保留两位小数)""",
            """必填
(以小数后两位形式填写，如“0.13”代
表税率13%)""",
            """非必填
(限18字符)
保留两位小数""",
            """非必填
（限15字符)
""",
        ]
    )

    # columns = ['商品名称*', '规格型号', '单位', '数量', '单价', '金额', '税率', '税收分类编码', '优惠政策名称']
    columns = [
        "项目名称",
        "商品和服务税收分类编码",
        "规格型号",
        "单位",
        "商品数量",
        "商品单价",
        "金额",
        "税率",
        "折扣金额",
        "优惠政策类型",
    ]
    rows.append(columns)
    for i, row in df.iterrows():
        cond = row["序号"]
        if pd.isna(cond):
            continue
        if not str.isdecimal(cond):
            continue
        new_row = []
        prod = row["商品名称"]
        # df_base = df_bases.query('商品名称 == @prod')
        df_base = df_bases.loc[df_bases["商品名称"] == prod]
        new_row.append(prod)
        if df_base.empty:
            new_row.append("")
        else:
            new_row.append(df_base["税收编码"].fillna("").values[0])
        new_row.append("")
        new_row.append(row["计量单位"])
        new_row.append(row["数量"])
        new_row.append("")
        new_row.append(row["金额"])

        if df_base.empty:
            set1.add(prod)
            new_row.append("没有找到")
            new_row.append("")
            new_row.append("")
        else:
            new_row.append(df_base["税率"].fillna("0.0").values[0])
            new_row.append("")
            new_row.append(df_base["免税"].fillna("").values[0])
        rows.append(new_row)
    xlsxname = csvname.replace("csv", "xlsx")
    pd.DataFrame(
        rows,
        columns=[
            """填表说明：
1、项目名称：无需写商品和服务税收分类简称（*号以及中间内容）
2、导入前请在电子税务局【开票业务】-【开票信息维护】中对开具的项目信息进行维护，或在导入模板中填写“商品与服务税收分类编码”。如未做项目信息维护且未填商品编码，导入会不成功。当明细超过500条时，请在模板中填写商编。
3、数量、单价可任填其中一项，或者仅填金额；如果三项均填写，导入后系统将默认以填写的数量*单价=金额进行误差校验；
商品单价、商品数量：小数点后最多保留13位小数；
金额：小数点后最多保留2位小数；
4、系统会根据折扣金额自动生成折扣行，需填写正数折扣金额；折扣金额小数点后最多保留2位小数。
5、仅支持普通模式及货物运输服务业务导入项目明细且不支持普通模式及货物运输服务业务商编混开，暂不支持其他特定业务模式的项目明细信息导入。
6、目前因服务器承载原因，超过2000行后可能会导致系统异常无法开具发票，超过5000行后无法开具发票，请注意发票明细行数。""",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
    ).to_excel(os.path.join(import_folder_name, xlsxname), startrow=0, index=False)


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
        os.path.join("base_data", f"{base_file_name}.xlsx"),
        usecols=["商品名称", "计量单位", "税率", "免税", "税收编码"],
        dtype={"税收编码": str, "税率": str},
    )
    return df


if __name__ == "__main__":
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    os.chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    base_file_name = settings["base_file_name"]
    prod_folder_name = os.path.join(
        settings["folder_name"], settings["prod_folder_name"]
    )
    import_folder_name = os.path.join(
        settings["folder_name"], settings["import_folder_name"]
    )
    df_bases = get_all_base(base_file_name)
    set1 = set()
    i = "11001.csv"
    make_import_one(df_bases, set1, prod_folder_name, import_folder_name, i)
    if len(set1) > 0:
        print(f"税率没有发现{set1}")
    pass
