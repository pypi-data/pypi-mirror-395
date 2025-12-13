# -*- coding: utf-8 -*-
"""
Core DataFrame utilities for StevenTricks.

這個模組只處理「跟 pandas DataFrame / Series 本身有關」的工具函式，
不依賴 StevenTricks 內其他自訂模組（例如 convert_utils）。

包含：
- findval：在整張表內搜尋特定值
- dateseries / periodictable：建立時間索引用的 Series / DataFrame
- replace_series：依字典做模糊或精準取代
- unique_series / cutoutliers_series / dateinterval_series / numinterval_series：常用欄位前處理
- dfrows_iter：依多欄位做笛卡兒積切表
- make_series：把某欄位取出並指定 index
- DataFrameMerger：在保持 index 的前提下，用「右表更新左表」的合併器
- replacebyseries：用一欄文字去刪掉另一欄中的子字串
"""

from __future__ import annotations

from datetime import datetime, date, timedelta
from itertools import product
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 基礎小工具
# ---------------------------------------------------------------------------

def findval(df: pd.DataFrame, val: Any) -> Iterable[Tuple[Any, str]]:
    """
    在整張 DataFrame 裡找出等於指定值的 cell，逐一回傳 (index, column)。

    用法：
        for idx, col in findval(df, 999):
            print(idx, col)
    """
    for col in df.columns:
        series = df.loc[df[col].isin([val]), col]
        for idx in series.index:
            yield idx, col


# ---------------------------------------------------------------------------
# 時間序列相關：dateseries / periodictable / dateinterval_series
# ---------------------------------------------------------------------------

def dateseries(
    seriesname: str = "",
    pendix: str = "",
    datemin: Any = "",
    datemax: Any = None,
    freq: str = "",
    defaultval: Any = None,
) -> pd.Series:
    """
    產生一串以日期為 index 的 Series，所有值都先填 defaultval。

    參數：
        seriesname : 此 Series 的基礎名稱。
        pendix     : 前綴字，會加在 seriesname 前面。
        datemin    : 起始日期（可為 str / datetime / date）。
        datemax    : 結束日期（預設為今天）。
        freq       : 頻率字串，例如 'D'、'W'、'MS'、'QS'、'YS'。
        defaultval : 預設填入的值。

    回傳：
        pandas.Series，index 為 DatetimeIndex。
    """
    if datemax is None:
        datemax = datetime.now().date()

    # 轉成 Timestamp
    datemin_ts = pd.to_datetime(datemin)
    datemax_ts = pd.to_datetime(datemax)

    if freq is None or freq == "":
        # 若沒指定頻率，就只產出 [datemin, datemax]
        idx = pd.to_datetime([datemin_ts, datemax_ts]).unique()
    else:
        idx = pd.date_range(start=datemin_ts, end=datemax_ts, freq=freq)
        # 確保結尾日期一定在 index 裡
        idx = idx.append(pd.DatetimeIndex([datemax_ts])).unique()

    return pd.Series(np.repeat(defaultval, idx.size), index=idx, name=pendix + seriesname)


def periodictable(
    perioddict: Optional[Dict[str, Dict[str, Any]]] = None,
    datemin: Optional[Any] = None,
) -> pd.DataFrame:
    """
    建立多條 dateseries 並以欄位方式合併成一張表。

    參數：
        perioddict:
            格式示意：
                {
                    "A": {"datemin": "2010-01-01", "datemax": "2020-12-31", "freq": "MS"},
                    "B": {"datemin": "2015-01-01", "freq": "Q"}
                }
            datemax 未指定時，預設為今天。
        datemin:
            若有給，會覆蓋每個 perioddict[key]["datemin"]。

    回傳：
        pd.DataFrame，各欄為一條 dateseries。
    """
    if perioddict is None:
        perioddict = {}

    series_list: List[pd.Series] = []
    today = datetime.now().date()

    for name, cfg in perioddict.items():
        cfg = dict(cfg)  # copy 一份避免 side-effect
        start = datemin if datemin is not None else cfg.get("datemin")
        if start is None:
            raise ValueError(f"perioddict['{name}'] 需要提供 'datemin'。")

        end = cfg.get("datemax", today)
        freq = cfg.get("freq", "D")
        s = dateseries(
            seriesname=name,
            pendix="",
            datemin=start,
            datemax=end,
            freq=freq,
            defaultval="wait",
        )
        series_list.append(s)

    if not series_list:
        return pd.DataFrame()

    return pd.concat(series_list, axis=1)


def dateinterval_series(series: pd.Series, freq: str = "MS") -> pd.Series:
    """
    將一串日期 mapping 成「區間左端點」（例如每月、每季）。

    例：
        freq = "MS"  → 每月（Month Start）
        freq = "QS"  → 每季（Quarter Start）

    回傳：
        pd.Series，值為區間左端點（Python date 物件）。
    """
    if series.empty:
        return series.copy()

    s = pd.to_datetime(series)
    date_range = pd.date_range(start=s.min(), end=s.max(), freq=freq, inclusive="both")

    # 前後各多一個 bin，避免邊界問題
    date_range = date_range.union(
        pd.date_range(date_range[0] - date_range.freq, periods=1, freq=date_range.freq)
    )
    date_range = date_range.union(
        pd.date_range(date_range[-1] + date_range.freq, periods=1, freq=date_range.freq)
    )

    res = pd.cut(s, bins=date_range, include_lowest=True, right=False)
    return res.map(lambda x: x.left.date())


# ---------------------------------------------------------------------------
# Series 前處理：replace / unique / outlier / 數值區間
# ---------------------------------------------------------------------------

def replace_series(
    series: pd.Series,
    std_dict: Dict[Any, Any],
    na: bool = False,
    mode: str = "fuzz",
) -> pd.Series:
    """
    依照 std_dict 內容，將 series 的值替換成標準化 key。

    std_dict：
        {標準值: [同義字1, 同義字2, ...]} 或 {標準值: "單一同義字"}

    mode:
        - "exac": 同一組 value_list 裡的字串都必須在原字串中出現，才做替換。
        - "fuzz": 只要有一個同義字被搜尋到就替換。

    注意：
        - 會回傳「新的 Series」，不會在原地修改。
        - 若 na=True，未被任何 key 命中的值會被保留下來；否則會被丟棄。
    """
    s = series.copy()
    res_parts: List[pd.Series] = []

    for key, value_list in std_dict.items():
        if not isinstance(value_list, (list, tuple, set)):
            value_list = [value_list]

        # 把所有同義字組合成一個 regex pattern
        escaped = [re.escape(str(v)) for v in value_list]
        pattern = "|".join(escaped)

        # 只針對非 NA 的資料做字串比對
        s_str = s.dropna().astype(str)

        if mode == "exac":
            mask = s_str.map(
                lambda x: len(set(value_list)) == len(set(re.findall(pattern, x)))
            )
        elif mode == "fuzz":
            mask = s_str.map(lambda x: bool(re.search(pattern, x)))
        else:
            raise ValueError("mode 必須是 'exac' 或 'fuzz'")

        hit_idx = mask[mask].index
        if not len(hit_idx):
            continue

        replaced = pd.Series([key] * len(hit_idx), index=hit_idx, dtype=object)
        res_parts.append(replaced)

        # 從待處理集合中移除已經命中的 index
        s = s.drop(index=hit_idx)

        if s.empty:
            break

    if na and not s.empty:
        # 保留未被任何 key 命中的原值
        res_parts.append(s)

    if not res_parts:
        return s

    out = pd.concat(res_parts).sort_index()
    # 填回原 index（沒被處理到的若 na=False 就會是 NaN）
    out = out.reindex(series.index)
    return out


def unique_series(series: pd.Series, mode: str = "") -> np.ndarray:
    """
    取得 Series 的唯一值。

    mode:
        - "timestamp" / "datetime64[ns]" / "timedelta64": 只取「年份」作為 unique key。
        - 其他：直接依 Series 本身的值做 unique。
    """
    s = series.dropna()

    if mode in ["timestamp", "datetime64[ns]", "timedelta64"]:
        s = pd.to_datetime(s, errors="coerce").dropna()
        s = s.map(lambda x: str(x.year))

    return s.unique()


def cutoutliers_series(series: pd.Series, bottom: float = 0.05, up: float = 0.95) -> pd.Series:
    """
    用分位數剪掉極端值；被剪掉的值會變成 NaN。

    例：
        bottom=0.05, up=0.95 → 保留中間 90% 的值，其餘設為 NaN。
    """
    if series.empty:
        return series.copy()

    q_low = series.quantile(bottom)
    q_high = series.quantile(up)

    mask = (series >= q_low) & (series <= q_high)
    return series.where(mask)


def list_union(list_tup: Sequence[Sequence[Any]]) -> List[Any]:
    """
    對一串 list 做聯集並排序。

    例：
        list_union([[1, 2], [3, 2, 1]]) → [1, 2, 3]
    """
    return sorted(list(set().union(*list_tup)))


def numinterval_series(
    series: pd.Series,
    std_list: Sequence[float],
    label: Optional[Sequence[str]] = None,
) -> pd.Series:
    """
    將數值欄位依 std_list 指定的分隔點切成區間。

    std_list:
        一組「切點」，例如 [0, 10, 20, 50]。
        函式會自動把實際最小值 / 最大值加進去（若超出範圍）。

    label:
        若為 None，預設用 "左~右" 表示，例如 "0.0~10.0"。

    回傳：
        pd.Series，值為區間或字串標籤。
    """
    if series.empty:
        return series.copy()

    bins = list(std_list)
    if series.min() < min(bins):
        bins = list_union([bins, [series.min()]])
    if series.max() > max(bins):
        bins = list_union([bins, [series.max()]])

    res = pd.cut(series, bins=bins, include_lowest=True, right=True, labels=label)

    if label is None:
        res = res.map(lambda x: f"{x.left}~{x.right}")

    return res


# ---------------------------------------------------------------------------
# DataFrame 切表與重組：dfrows_iter / make_series
# ---------------------------------------------------------------------------

def _dtypes_df(df: pd.DataFrame) -> pd.Series:
    """
    回傳每個欄位的 dtype（字串）。

    為了與舊版相容，獨立實作一次，不依賴 convert_utils.dtypes_df。
    """
    return df.dtypes.astype(str)


def dfrows_iter(
    df: pd.DataFrame,
    colname_list: Sequence[str],
    std_dict: Optional[Dict[str, Sequence[str]]] = None,
    nodropcol_list: Sequence[str] = (),
):
    """
    依照 colname_list 中指定的欄位，做笛卡兒積切表，逐一 yield (key_list, sub_df)。

    用途：
        - 想要針對某幾個欄位的所有組合，分別獨立做分析時使用。

    參數：
        df            : 原始 DataFrame。
        colname_list  : 要做切表的欄位名稱列表。
        std_dict      : （選用）用來調整 dtype 類別的 mapping，
                        例如：
                            {
                                "timestamp": ["datetime64", "datetime64[ns]"],
                            }
                        會影響 unique_series() 在日期欄位的行為。
        nodropcol_list: 在每個子表中「不要被 drop 掉」的欄位名稱。

    yield：
        [key_list, res_df]
            - key_list: 這個子表對應的各欄位取值（順序與 colname_list 相同）。
            - res_df  : 篩選後的子 DataFrame；預設會把切表欄位從欄位中移除，
                       除非該欄位有出現在 nodropcol_list。
    """
    if not colname_list:
        return

    df_converted = df.convert_dtypes()
    dtype_series = _dtypes_df(df_converted)

    # 若有提供 std_dict，允許用模糊比對方式重新歸類 dtype 名稱
    if std_dict:
        dtype_series = replace_series(dtype_series, std_dict, na=True, mode="fuzz")

    # 先為每個欄位取得 unique 值清單
    value_products: List[Iterable[Tuple[str, Any]]] = []
    for col in colname_list:
        if col not in df_converted.columns:
            continue
        dtype_name = dtype_series.get(col, "")
        uniq_vals = unique_series(df_converted[col], mode=str(dtype_name))
        # 封裝成 (欄位名稱, 值) 的配對，方便後面做 product
        value_products.append(product([col], uniq_vals))

    if not value_products:
        return

    # 對所有欄位做笛卡兒積
    for data_colkey in product(*value_products):
        key_list: List[Any] = []
        res_df = df_converted.copy()
        for col, key in data_colkey:
            dtype_name = str(dtype_series.get(col, ""))
            if dtype_name in ["timestamp", "datetime64[ns]", "timedelta64"]:
                # 日期類型 → 僅以年份做切分
                res_df = res_df.loc[
                    res_df[col].map(
                        lambda x: bool(
                            pd.notna(x)
                            and str(pd.to_datetime(x).year) == str(key)
                        )
                    ),
                    :
                ]
            else:
                res_df = res_df.loc[res_df[col] == key, :]

            if col not in nodropcol_list:
                res_df = res_df.drop(columns=[col])

            key_list.append(key)

        if res_df.empty:
            continue

        yield [key_list, res_df]


def make_series(df: pd.DataFrame, column_name: str, ind_name: str = "date") -> pd.Series:
    """
    從 DataFrame 中抽出特定欄位，並將 ind_name 指定的欄位作為 index。

    Parameters:
        df          : 原始資料。
        column_name : 欲抽取的欄位名稱。
        ind_name    : 要當作 index 的欄位名稱（預設 'date'）。

    Returns:
        pd.Series: index 為 ind_name，值為 column_name。
    """
    result = df[column_name].copy()
    result.index = df[ind_name]
    return result


# ---------------------------------------------------------------------------
# DataFrame 合併器：DataFrameMerger
# ---------------------------------------------------------------------------

class DataFrameMerger:
    """
    在「以 index 對齊」的前提下，用 right DataFrame 更新 left DataFrame。

    特性：
        - 支援覆寫或僅填補 NaN（overwrite=True / False）。
        - 自動處理 right 中的新欄位與新 index。
        - 會保留每次更新前後的歷程（history）。
    """

    def __init__(self, left: pd.DataFrame):
        # 初始化合併器，設定初始 DataFrame，並建立更新歷程記錄清單
        self.left = left.copy()
        self.history: List[Dict[str, pd.DataFrame]] = []

    def renew(self, right: pd.DataFrame, overwrite: bool = True) -> pd.DataFrame:
        """
        使用 right 更新目前的 left，並回傳更新後的 DataFrame。

        參數：
            right     : 新資料 DataFrame。
            overwrite : 若為 True，right 的值會覆蓋 left；
                        若為 False，只會在 left 該位置為 NaN 時才填入 right 的值。
        """
        # 判斷右邊資料是否為空
        if right is None or right.empty:
            print("Empty right, skip update.")
            return self.left

        # 若左邊資料為空，直接回傳右邊資料作為新狀態
        if self.left is None or self.left.empty:
            print("Empty left, initialize with right.")
            self.left = right.copy()
            self.history.append({
                "before": pd.DataFrame(),
                "right": right.copy(),
                "after": self.left.copy(),
            })
            return self.left

        # 若兩邊資料完全相同，無需處理
        if self.left.equals(right):
            print("left and right are identical, skip update.")
            return self.left

        # 建立左邊資料的副本作為更新基礎
        updated = self.left.copy()

        # 找出左右共同的欄位
        shared_cols = [col for col in right.columns if col in updated.columns]

        if shared_cols:
            if overwrite:
                # 若允許覆寫，直接使用 pandas 的 update 方法就地更新
                try:
                    updated.update(right[shared_cols])
                except ValueError as e:
                    # 若 index 不相容，退回用 reset_index 對齊 row 順序
                    print(f"update() ValueError, fallback to position-based update: {e}")
                    updated_reset = updated.reset_index(drop=True)
                    right_reset = right.reset_index(drop=True)
                    updated_reset.update(right_reset[shared_cols])
                    updated = updated_reset.set_index(self.left.index)
            else:
                # 若不允許覆寫，只更新 NaN 的欄位值
                for col in shared_cols:
                    common_index = updated.index.intersection(right.index)
                    for idx in common_index:
                        if pd.isna(updated.at[idx, col]) and not pd.isna(right.at[idx, col]):
                            updated.at[idx, col] = right.at[idx, col]

        # 處理 right 中的新欄位（left 中不存在）
        new_cols = [col for col in right.columns if col not in updated.columns]
        for col in new_cols:
            # 轉換型別以支援 NA（nullable）
            col_dtype = right[col].dtype
            if pd.api.types.is_integer_dtype(col_dtype):
                safe_dtype = "Int64"
            elif pd.api.types.is_bool_dtype(col_dtype):
                safe_dtype = "boolean"
            else:
                safe_dtype = col_dtype

            # 在 updated 中建立新欄位並初始化為 NA
            updated[col] = pd.Series(
                [pd.NA] * len(updated),
                index=updated.index,
                dtype=safe_dtype,
            )

            # 將新欄位在共有 index 中的資料從 right 填入 updated
            common_index = right.index.intersection(updated.index)
            updated.loc[common_index, col] = right.loc[common_index, col]

        # 新增 right 中在 left 中不存在的 index 對應的列
        new_rows = right.loc[~right.index.isin(updated.index)]
        if not new_rows.empty:
            updated = pd.concat([updated, new_rows], axis=0)

        # 儲存本次更新的歷史（包含更新前、更新使用的 right、更新後）
        self.history.append({
            "before": self.left.copy(),
            "right": right.copy(),
            "after": updated.copy(),
        })

        # 更新內部狀態
        self.left = updated
        return updated


# ---------------------------------------------------------------------------
# 其他小工具
# ---------------------------------------------------------------------------

def replacebyseries(
    toreplace: str = "",
    res: str = "",
    df: Optional[pd.DataFrame] = None,
) -> pd.Series:
    """
    以 df[toreplace] 欄位的值，去刪除 df[res] 欄位中的子字串。

    例：
        df["keyword"] = ["股份有限公司", "股份有限公司"]
        df["name"]    = ["台積電股份有限公司", "聯電股份有限公司"]

        replacebyseries("keyword", "name", df)
        → ["台積電", "聯電"]
    """
    if df is None or df.empty:
        return pd.Series(dtype=object)

    temp = df[[toreplace, res]].values
    return pd.Series(
        [str(name).replace(str(sub), "") for sub, name in temp],
        index=df.index,
    )


if __name__ == "__main__":
    pass
