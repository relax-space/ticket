"""
制作开电子票的模板: 诺诺
"""
from pandas import DataFrame, read_csv, isna, read_excel
from os import path as os_path, listdir, chdir
from sys import path as sys_path


def make_import_one(
    df_bases: DataFrame,
    set1: set,
    prod_folder_name: str,
    import_folder_name: str,
    csvname: str,
):
    df = read_csv(os_path.join(prod_folder_name, csvname), header=3, encoding="utf-8")
    rows = []
    rows.append(
        [
            """必填
不超出92字符""",
            """不超出40字符""",
            """不超出20字符""",
            """数量、单价、金额：任选其中两项，或者仅填金额或者三项均填写；
导入红字信息表清单时数量和金额自动处理为负数
单价/数量：不得超过10位小数
金额：不得超过2位小数
""",
            "",
            "",
            """未填写，优先从已维护的商品信息中匹配

如果未维护该商品，通过大数据智能匹配获取""",
            """未填写，优先从已维护的商品信息中匹配

如果未维护该商品，通过大数据智能匹配获取""",
            """非必填，享受优惠政策时填写

比如：免税、不征税""",
        ]
    )

    columns = ["商品名称*", "规格型号", "单位", "数量", "单价", "金额", "税率", "税收分类编码", "优惠政策名称"]
    rows.append(columns)
    for i, row in df.iterrows():
        cond = row["序号"]
        if isna(cond):
            continue
        if not str.isdecimal(cond):
            continue
        new_row = []
        prod = row["商品名称"]
        # df_base = df_bases.query('商品名称 == @prod')
        df_base = df_bases.loc[df_bases["商品名称"] == prod]
        new_row.append(prod)
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
            new_row.append(df_base["税收编码"].fillna("").values[0])
            new_row.append(df_base["免税"].fillna("").values[0])
        rows.append(new_row)
    xlsxname = csvname.replace("csv", "xlsx")
    DataFrame(
        rows,
        columns=[
            """注意：
1、【金额是否含税】以导入时页面左上角设置为准    
2、【是否清单票】以导入时页面左上角设置为准""",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
    ).to_excel(os_path.join(import_folder_name, xlsxname), startrow=0, index=False)


def make_import_list(
    base_file_name: str, prod_folder_name: str, import_folder_name: str
) -> set:
    df_bases = get_all_base(base_file_name)
    files = listdir(prod_folder_name)
    set1 = set()
    for i in files:
        make_import_one(df_bases, set1, prod_folder_name, import_folder_name, i)
    return set1


def get_all_base(base_file_name: str) -> DataFrame:
    df = read_excel(
        os_path.join("base_data", f"{base_file_name}.xlsx"),
        usecols=["商品名称", "计量单位", "税率", "免税", "税收编码"],
        dtype={"税收编码": str, "税率": str},
    )
    return df


if __name__ == "__main__":
    p = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))
    sys_path.insert(0, p)
    chdir(p)
    from relax.util import get_settings

    settings = get_settings()
    base_file_name = settings["base_file_name"]
    prod_folder_name = os_path.join(
        settings["folder_name"], settings["prod_folder_name"]
    )
    import_folder_name = os_path.join(
        settings["folder_name"], settings["import_folder_name"]
    )
    df_bases = get_all_base(base_file_name)
    set1 = set()
    i = "11001.csv"
    make_import_one(df_bases, set1, prod_folder_name, import_folder_name, i)
    if len(set1) > 0:
        print(f"税率没有发现{set1}")
    pass
