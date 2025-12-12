# StevenTricks/__init__.py

"""StevenTricks: Steven 的個人工具箱。"""

from . import core, io, db, analysis, dev

__all__ = ["core", "io", "db", "analysis", "dev", "__version__"]


__version__ = "0.1.0"  # prepare_release.py 會改這個


from StevenTricks.core.convert_utils import stringtodate
"""
df = stringtodate(df, "Appl_Date")  # 民國/西元混合日期 → datetime64[ns]

df["Cust_Name"] = df["Cust_Name"].map(
    lambda x: safe_replace(x, "股份有限公司", "")
)

"""

"""
from StevenTricks.core.df_utils import safe_numeric_convert

cols = ["Income", "Loan_Amt", "Balance"]
df = safe_numeric_convert(df, cols)

"""