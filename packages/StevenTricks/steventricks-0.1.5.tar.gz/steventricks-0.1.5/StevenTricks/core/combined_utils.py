# -*- coding: utf-8 -*-
"""
高階資料處理流程（統整 convert_utils + df_utils）
================================================

設計目的：
    - 讓 core.convert_utils.py 與 core.df_utils.py 可以完全獨立，不互相 import。
    - 所有「同時需要用到 convert_utils + df_utils」的高階 function，都集中放在這一支。
    - 這支屬於『實務流程封裝』層，不放底層 utility，避免循環依賴。

典型功能：
    1. 數值欄位：先做安全轉數字（convert_utils.safe_numeric_convert），再剪尾（df_utils.cutoutliers_series）。
    2. 日期欄位：先做文字→日期轉換（convert_utils.stringtodate），再切 period（df_utils.dateinterval_series）。
    3. Segment 拆表：先做欄位清洗，再用 df_utils.dfrows_iter 依多維度切成多個子表。

注意：
    - 這裡只寫「需要同時用到兩個模組」的高階流程；
      單純的字串 / 型態轉換請直接用 convert_utils，
      單純的 DataFrame 操作請直接用 df_utils。
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import pandas as pd

# 這裡才允許同時 import，其他 core 檔案禁止互相 import
from .convert_utils import safe_numeric_convert, stringtodate
from .df_utils import (
    cutoutliers_series,
    dateinterval_series,
    dfrows_iter,
)


# ============================================================
# 一、數值欄位：轉型 + 剪尾的一條龍處理
# ============================================================

def clean_numeric_and_cut_outliers(
    df: pd.DataFrame,
    cols: Sequence[str],
    *,
    bottom: float = 0.01,
    up: float = 0.99,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    專門處理「一組數值欄位」的高階流程：

        1. 用 convert_utils.safe_numeric_convert 把 cols 轉成乾淨的 numeric
           （處理千分位、括號負號、全形字元等）
        2. 用 df_utils.cutoutliers_series 對每個欄位做剪尾，避免極端值干擾

    參數：
        df:
            原始 DataFrame。
        cols:
            要處理的欄位名稱列表。
        bottom, up:
            剪尾百分位數，例如 bottom=0.01, up=0.99 → 保留 1%～99% 區間。
        inplace:
            True  → 直接修改傳入 df 並回傳同一個物件。
            False → 複製一份後處理，不改動原 df。

    回傳：
        處理後的 DataFrame（若 inplace=True，實際是同一個物件）。
    """
    if not inplace:
        df = df.copy()

    # 第一步：型態轉換（這裡假設 safe_numeric_convert 會在 df 上就地修改）
    safe_numeric_convert(df, cols)

    # 第二步：剪尾
    for col in cols:
        if col not in df.columns:
            continue
        df[col] = cutoutliers_series(df[col], bottom=bottom, up=up)

    return df


# ============================================================
# 二、日期欄位：文字→日期→period 的一條龍處理
# ============================================================

def normalize_dates_and_make_period(
    df: pd.DataFrame,
    date_col: str,
    *,
    mode: int = 1,
    freq: str = "MS",
    new_col: Optional[str] = None,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    專門處理「一個日期欄位」的高階流程：

        1. 用 convert_utils.stringtodate 將文字日期轉成 datetime64[ns]
           （支援民國 / 西元等混合格式）
        2. 用 df_utils.dateinterval_series 依 freq 切出 period（例如每月、每季）

    參數：
        df:
            原始 DataFrame。
        date_col:
            要處理的日期欄位名稱。
        mode:
            傳給 stringtodate 的模式（1~4），依你 convert_utils 的定義來。
        freq:
            period 切分頻率，例：
                - "MS"：每月月初
                - "QS"：每季季初
                - "AS"：每年年初
        new_col:
            新欄位名稱；若為 None，預設為 f"{date_col}_period"。
        inplace:
            True  → 就地修改 df。
            False → 先 copy 再處理。

    回傳：
        處理後的 DataFrame。
    """
    if not inplace:
        df = df.copy()

    # 第一步：文字 → datetime
    stringtodate(df, [date_col], mode=mode)

    # 第二步：切 period
    period_series = dateinterval_series(df[date_col], freq=freq)
    if new_col is None:
        new_col = f"{date_col}_period"

    # 保留 index 對齊
    df[new_col] = period_series.reindex(df.index)

    return df


# ============================================================
# 三、Segment 拆表：清洗 + 切表的一條龍流程
# ============================================================

def segment_and_iterate(
    df: pd.DataFrame,
    segment_cols: Sequence[str],
    *,
    std_dict: Optional[Dict[str, Dict[Any, Any]]] = None,
    nodropcol_list: Sequence[str] = (),
    numeric_cols: Optional[Sequence[str]] = None,
    outlier_bottom: Optional[float] = None,
    outlier_up: Optional[float] = None,
) -> Iterable[Tuple[List[Any], pd.DataFrame]]:
    """
    高階版拆表流程：適合「Funding_Amt 月度拆解」這類需求。

    流程：
        1. （可選）先對 numeric_cols 做：
            - safe_numeric_convert（convert_utils）
            - cutoutliers_series（df_utils）剪尾
        2. 再呼叫 df_utils.dfrows_iter，依 segment_cols 做笛卡兒積拆表，
           每一組 key 對應一個子 DataFrame。

    參數：
        df:
            原始 DataFrame。
        segment_cols:
            要拿來做 segment 的欄位，例如：
                ["Product_Flag_new", "Cust_Flag", "Property_Location_Flag"]
        std_dict:
            傳給 dfrows_iter 的標準化字典（依你原本 df_utils 的定義）。
        nodropcol_list:
            在拆表時不被 drop 的欄位（例如主鍵）。
        numeric_cols:
            需要事先清洗的數值欄位；若為 None 則略過此步驟。
        outlier_bottom, outlier_up:
            若兩者皆為 None → 不剪尾；
            若有給值 → 對 numeric_cols 做剪尾，例如 0.01 / 0.99。

    回傳：
        一個 generator，yield 出：
            (key_list, sub_df)
        其中 key_list 順序與 segment_cols 一致。
    """
    # --- 1. 數值欄位前處理（如果有指定） ---
    if numeric_cols:
        # 先轉 numeric
        safe_numeric_convert(df, numeric_cols)

        # 再剪尾（若有指定 quantile）
        if outlier_bottom is not None and outlier_up is not None:
            for col in numeric_cols:
                if col not in df.columns:
                    continue
                df[col] = cutoutliers_series(
                    df[col],
                    bottom=outlier_bottom,
                    up=outlier_up,
                )

    # --- 2. 呼叫 dfrows_iter 做多維度拆表 ---
    # 注意：這裡直接沿用 df_utils.dfrows_iter 的介面定義，
    #       不去改動 df_utils 本體，只在這裡做高階封裝。
    std_dict = std_dict or {}
    for key_list, sub_df in dfrows_iter(
        df=df,
        colname_list=list(segment_cols),
        std_dict=std_dict,
        nodropcol_list=list(nodropcol_list),
    ):
        yield key_list, sub_df
