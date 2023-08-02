import pandas as pd
from collections import OrderedDict
import os

# df = pd.read_csv('data/header.csv', dtype={"报账单号": "str", "报账单批次号": "str"})
# df.to_excel(f"data/header1.xlsx", index=False)


df = pd.read_csv('data/list.csv', dtype={"报账单号": "str", "报账单批次号": "str"})
df.to_excel(f"data/list1.xlsx", index=False)

