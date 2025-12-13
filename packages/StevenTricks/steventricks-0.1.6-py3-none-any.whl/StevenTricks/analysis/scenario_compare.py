# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
scenario_compare
================

用途：
    - 把「同一張 raw data（通常是 Excel .xlsx）」在多個篩選條件（scenario）下的樞紐結果整併起來
    - 取代你手動拉出多張樞紐表，再用肉眼逐格比較的做法
    - 支援：
        1. 同一組維度（例如 location_grade × cust_flag），多個 scenario 的 Funding_Amt 對比
        2. 針對某一個 baseline scenario，自動算出其他 scenario 的差值 / 比例
        3. 從 .xlsx 讀 raw data
        4. 產出可以直接貼到 Excel（clipboard），或輸出成 .xlsx 檔

核心概念：
    你原本在 Excel 的 3 張樞紐：
        - 寬限期（含 DBR/ATD）
        - 寬限期（DBR）
        - 寬限期（ATD）
    在這裡會變成 3 個 scenario：
        - grace_all
        - grace_DBR
        - grace_ATD

    我們在 raw data 上針對每個 scenario 做 groupby(sum Funding_Amt)，
    然後把結果 join 成一張寬表 wide，再相對 baseline 做差值與比例。

使用方式（DataFrame 版）：
    from scenario_compare import summarize_scenarios

    res = summarize_scenarios(
        df,
        dims=["location_grade", "cust_flag"],
        value_col="Funding_Amt",
        scenarios={
            "grace_all": lambda d: d["Grace_Flag"] == 1,
            "grace_DBR": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "DBR"),
            "grace_ATD": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "ATD"),
        },
        base_scenario="grace_all",
    )

使用方式（直接吃 Excel）：
    from scenario_compare import summarize_scenarios_from_excel, copy_to_clipboard_for_excel

    res = summarize_scenarios_from_excel(
        excel_path="C:/your/path/raw_data.xlsx",
        sheet_name="Sheet1",
        dims=["location_grade", "cust_flag"],
        value_col="Funding_Amt",
        scenarios={
            "grace_all": lambda d: d["Grace_Flag"] == 1,
            "grace_DBR": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "DBR"),
            "grace_ATD": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "ATD"),
        },
        base_scenario="grace_all",
    )

    copy_to_clipboard_for_excel(res.wide_with_diff, index=False)
    # → 直接在 Excel 貼上就是一張分析表

"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Any

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 資料結構定義
# ---------------------------------------------------------------------------

@dataclass
class ScenarioMultiCompareResult:
    """
    summarize_scenarios / summarize_scenarios_from_excel 回傳的封裝結果。

    欄位說明：
        wide:
            index = dims（例如 location_grade, cust_flag）
            columns = 各 scenario 的彙總值（sum of value_col）

        wide_with_diff:
            reset_index 之後的 DataFrame：
                dims + [scenario1, scenario2, ...] + 差值 / 比例欄位
            若有設定 base_scenario，會多出：
                - {scenario}__minus__{base_scenario}
                - {scenario}__div__{base_scenario}

        long:
            把 wide 打平成長表：
                dims + ["scenario", value_col]

        long_diff:
            若有 base_scenario：
                dims + ["scenario", "base_scenario", "scenario_value",
                        "base_value", "diff", "abs_diff", "ratio"]

        top_abs_diff:
            若有 base_scenario：
                long_diff 按 abs_diff 由大到小排序的結果
    """
    wide: pd.DataFrame
    wide_with_diff: pd.DataFrame
    long: pd.DataFrame
    long_diff: Optional[pd.DataFrame]
    top_abs_diff: Optional[pd.DataFrame]


# ---------------------------------------------------------------------------
# 主邏輯：吃 DataFrame 的版本
# ---------------------------------------------------------------------------

def summarize_scenarios(
    df: pd.DataFrame,
    *,
    dims: List[str],
    value_col: str,
    scenarios: Dict[str, Callable[[pd.DataFrame], pd.Series]],
    base_scenario: Optional[str] = None,
) -> ScenarioMultiCompareResult:
    """
    對同一張 raw data，根據多個 scenario 做 groupby(sum)，
    整併成一張寬表，並可針對某個 base_scenario 計算差值與比例。

    參數
    ----
    df : pd.DataFrame
        原始明細資料（你原來拿去拉樞紐的那張總表）
    dims : list[str]
        當作樞紐 row / column 的維度欄位，例如 ["location_grade", "cust_flag"]
    value_col : str
        要彙總的數值欄位，例如 "Funding_Amt"
    scenarios : dict[str, callable]
        每個 key 是 scenario 名稱（會變成輸出表的欄名），
        value 是一個函式：mask = func(df) -> bool Series，
        定義這個 scenario 的篩選條件。

    base_scenario : str 或 None
        若提供，代表要針對這個 scenario 做 baseline，
        對「其他所有 scenario」計算：
            - diff = scenario - base_scenario
            - ratio = scenario / base_scenario

    回傳
    ----
    ScenarioMultiCompareResult
    """
    if not dims:
        raise ValueError("dims 不可為空，至少要有一個分群欄位（例如 ['location_grade']）")

    if not scenarios:
        raise ValueError("scenarios 不可為空，至少需要一個 scenario 定義")

    scenario_names = list(scenarios.keys())

    if base_scenario is not None and base_scenario not in scenario_names:
        raise ValueError(f"base_scenario={base_scenario!r} 不在 scenarios 裡：{scenario_names!r}")

    # 1) 分別針對每個 scenario 做 groupby(sum)
    pieces = []
    for name, func in scenarios.items():
        mask = func(df)
        sub = df[mask]

        if sub.empty:
            # 這個 scenario 完全沒有資料 → 給一個空的 Series，就會在 concat 時產生全 0
            agg = pd.Series(dtype="float64", name=name)
        else:
            agg = (
                sub.groupby(dims, dropna=False)[value_col]
                   .sum()
                   .rename(name)
            )
        pieces.append(agg)

    # 2) 把所有 scenario 的 Series 以 index=dims 為主拼起來 → 寬表
    wide = pd.concat(pieces, axis=1).fillna(0.0)
    # wide 的 index 是 dims（MultiIndex 或單一 Index），columns 是 scenario 名稱

    # 3) 打平成 long（方便你做任何排序 / filter）
    long = (
        wide
        .stack()  # index => (dims..., scenario)，value => value_col
        .rename(value_col)
        .reset_index()
    )
    # 最後一個 level 的名稱自動是 "level_{k}"，我們改成 "scenario"
    scenario_level_name = f"level_{len(dims)}"
    if scenario_level_name in long.columns:
        long = long.rename(columns={scenario_level_name: "scenario"})
    else:
        if "scenario" not in long.columns:
            raise RuntimeError("無法辨識 scenario 欄位，請檢查 dims 設定。")

    # 4) 建 wide_with_diff：把 index reset，並加上差值 / 比例（若有 base_scenario）
    wide_with_diff = wide.reset_index()

    long_diff: Optional[pd.DataFrame] = None
    top_abs_diff: Optional[pd.DataFrame] = None

    if base_scenario is not None:
        if base_scenario not in wide.columns:
            raise RuntimeError(f"在 wide 表裡找不到 base_scenario 欄位：{base_scenario!r}")

        base_col = base_scenario

        # 4a) 在 wide_with_diff 上加上每個 scenario vs base 的差值 / 比例
        for name in scenario_names:
            if name == base_col:
                continue

            diff_col = f"{name}__minus__{base_col}"
            ratio_col = f"{name}__div__{base_col}"

            wide_with_diff[diff_col] = wide_with_diff[name] - wide_with_diff[base_col]

            # 安全處理 base=0 的情況
            def _safe_div(x, y):
                return np.nan if y == 0 else x / y

            wide_with_diff[ratio_col] = [
                _safe_div(x, y)
                for x, y in zip(wide_with_diff[name], wide_with_diff[base_col])
            ]

        # 4b) 做一張「所有 scenario 相對 base 的差距長表」，方便做排名
        long_diff_rows = []
        for name in scenario_names:
            if name == base_col:
                continue

            subset = wide_with_diff[dims + [base_col, name]].copy()
            subset["scenario"] = name
            subset["base_scenario"] = base_col

            subset["diff"] = subset[name] - subset[base_col]
            subset["abs_diff"] = subset["diff"].abs()

            # 注意：這裡的 ratio 是 scenario / base
            def _safe_ratio_row(row):
                denom = row[base_col]
                return np.nan if denom == 0 else row[name] / denom

            subset["ratio"] = subset.apply(_safe_ratio_row, axis=1)

            # 統一數值欄名
            subset = subset.rename(columns={name: "scenario_value", base_col: "base_value"})

            long_diff_rows.append(subset)

        if long_diff_rows:
            long_diff = pd.concat(long_diff_rows, ignore_index=True)
            top_abs_diff = long_diff.sort_values("abs_diff", ascending=False)
        else:
            long_diff = pd.DataFrame()
            top_abs_diff = pd.DataFrame()

    return ScenarioMultiCompareResult(
        wide=wide,
        wide_with_diff=wide_with_diff,
        long=long,
        long_diff=long_diff,
        top_abs_diff=top_abs_diff,
    )

# 放在 scenario_compare.py 裡（summarize_scenarios 後面）

def two_period_change_pivot(
    df: pd.DataFrame,
    *,
    dim: str,
    value_col: str,
    time_col: str,
    base_period,
    comp_period,
) -> pd.DataFrame:
    """
    在單一欄位 dim 上，計算「base_period vs comp_period」的樞紐表。

    回傳欄位：
        index: dim 的各個類別
        columns:
            - amt_base
            - amt_comp
            - delta_amt
            - delta_share_in_node  （尚未知道「整棵樹」的占比，只先算 node 內部）

    注意：這個函式只處理「兩期加總＋差額」，不處理 driver_tree 的選維度邏輯。
    """
    scenarios = {
        "amt_base": lambda d: d[time_col] == base_period,
        "amt_comp": lambda d: d[time_col] == comp_period,
    }

    # 用 summarize_scenarios 做真正的 groupby+pivot
    res = summarize_scenarios(
        df=df,
        dims=[dim],
        value_col=value_col,
        scenarios=scenarios,
        base_scenario=None,   # 這裡不需要指定 baseline，自己算 delta
    )

    # res.wide 的 index 是 dim，columns = ["amt_base", "amt_comp"]
    pivot = res.wide.copy()

    pivot["delta_amt"] = pivot["amt_comp"] - pivot["amt_base"]

    node_delta = float(pivot["delta_amt"].sum())
    denom = abs(node_delta) if node_delta != 0 else 1e-9
    pivot["delta_share_in_node"] = pivot["delta_amt"] / denom

    return pivot

# ---------------------------------------------------------------------------
# 入口 1：從 Excel 讀 raw data 再跑 summarize_scenarios
# ---------------------------------------------------------------------------

def summarize_scenarios_from_excel(
    excel_path: str | Path,
    sheet_name: str | int = 0,
    *,
    dims: List[str],
    value_col: str,
    scenarios: Dict[str, Callable[[pd.DataFrame], pd.Series]],
    base_scenario: Optional[str] = None,
    read_excel_kwargs: Optional[Dict[str, Any]] = None,
) -> ScenarioMultiCompareResult:
    """
    從 .xlsx 讀 raw data，再呼叫 summarize_scenarios。

    參數
    ----
    excel_path : str | Path
        Excel 檔案路徑，例如：
            "C:/Users/steven/Desktop/raw_data.xlsx"
    sheet_name : str | int
        工作表名稱或索引（跟 pandas.read_excel 的用法一樣）。
    dims, value_col, scenarios, base_scenario :
        與 summarize_scenarios 相同。
    read_excel_kwargs : dict 或 None
        額外傳給 pandas.read_excel 的參數，例如：
            {"dtype": {"location_grade": "string", "cust_flag": "string"}}

    回傳
    ----
    ScenarioMultiCompareResult
    """
    excel_path = Path(excel_path)
    if not excel_path.exists():
        raise FileNotFoundError(f"找不到 Excel 檔案：{excel_path}")

    kwargs = read_excel_kwargs or {}
    df = pd.read_excel(excel_path, sheet_name=sheet_name, **kwargs)

    return summarize_scenarios(
        df,
        dims=dims,
        value_col=value_col,
        scenarios=scenarios,
        base_scenario=base_scenario,
    )


# ---------------------------------------------------------------------------
# 輸出工具：貼到 Excel / 匯出成 .xlsx
# ---------------------------------------------------------------------------

def copy_to_clipboard_for_excel(df: pd.DataFrame, *, index: bool = False) -> None:
    """
    把 DataFrame 複製到系統剪貼簿，直接在 Excel 貼上。

    使用方式：
        copy_to_clipboard_for_excel(res.wide_with_diff, index=False)
    """
    df.to_clipboard(index=index, excel=True)
    print(f"[已複製到剪貼簿] 欄數={df.shape[1]}, 列數={df.shape[0]}，可直接在 Excel 貼上。")


def export_result_to_excel(
    result: ScenarioMultiCompareResult,
    out_path: str | Path,
    *,
    include_long: bool = True,
    include_long_diff: bool = True,
) -> None:
    """
    把分析結果輸出成 .xlsx 檔，包含多個 sheet。

    sheet 規劃：
        - "wide":            result.wide
        - "wide_with_diff":  result.wide_with_diff
        - （選擇性）"long":        result.long
        - （選擇性）"long_diff":   result.long_diff
        - （選擇性）"top_abs_diff":result.top_abs_diff
    """
    out_path = Path(out_path)
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        result.wide.to_excel(writer, sheet_name="wide")
        result.wide_with_diff.to_excel(writer, sheet_name="wide_with_diff", index=False)

        if include_long:
            result.long.to_excel(writer, sheet_name="long", index=False)

        if include_long_diff and result.long_diff is not None:
            result.long_diff.to_excel(writer, sheet_name="long_diff", index=False)
        if include_long_diff and result.top_abs_diff is not None:
            result.top_abs_diff.to_excel(writer, sheet_name="top_abs_diff", index=False)

    print(f"[已輸出] {out_path}")


# ---------------------------------------------------------------------------
# （選用）直接當成 script 執行的範例：
#   改路徑、改欄位名稱、改 scenarios，然後在 PyCharm 右鍵 Run 即可。
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # === 1. 設定 Excel 檔案與工作表 ===
    EXCEL_PATH = "/Users/stevenhsu/Desktop/raw_data.xlsx"  # ← 換成你自己的路徑
    SHEET_NAME = 0  # 或 "Sheet1"

    # === 2. 設定樞紐的維度與金額欄位 ===
    DIMS = ["location_grade", "cust_flag"]  # 列 × 欄的邏輯
    VALUE_COL = "Funding_Amt"

    # === 3. 設定 scenario（對應你原本要拉的各種樞紐表） ===
    # 這裡只是照你寬限期 × DBR/ATD 的例子，欄位名稱請對應你實際的 raw data
    SCENARIOS = {
        "grace_all": lambda d: d["Grace_Flag"] == 1,
        "grace_DBR": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "DBR"),
        "grace_ATD": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "ATD"),
    }

    BASE_SCENARIO = "grace_all"  # 其他 scenario 都會相對它算差值 / 比例

    # === 4. 讀 Excel + 分析 ===
    res = summarize_scenarios_from_excel(
        excel_path=EXCEL_PATH,
        sheet_name=SHEET_NAME,
        dims=DIMS,
        value_col=VALUE_COL,
        scenarios=SCENARIOS,
        base_scenario=BASE_SCENARIO,
    )

    # === 5. 直接輸出兩種方式（二選一 or 都用） ===

    # 5-1. 複製 wide_with_diff 到剪貼簿，去 Excel 貼上
    copy_to_clipboard_for_excel(res.wide_with_diff, index=False)

    # 5-2. 輸出成 .xlsx 檔（方便留檔）
    OUT_XLSX = "/Users/stevenhsu/Desktop/scenario_compare_result.xlsx"
    export_result_to_excel(res, OUT_XLSX)


"""
你實際要做什麼？

把上面整段存成一個檔案，例如：StevenTricks/analysis/scenario_compare.py。

改 __main__ 底下這幾個變數：

EXCEL_PATH：你的 raw data .xlsx 路徑。

SHEET_NAME：工作表。

DIMS：你樞紐的「列 × 欄」（這次是 ["location_grade", "cust_flag"]）。

VALUE_COL：通常是 "Funding_Amt"。

SCENARIOS：把你原本要拉的各種樞紐條件（寬限期、寬限期+DBR、寬限期+ATD…）寫進去。

在 PyCharm 對 scenario_compare.py 右鍵 Run。

跑完後：

res.wide_with_diff 已經被複製到剪貼簿 → 直接去 Excel 貼。

或到桌面看 scenario_compare_result.xlsx，裡面有完整分析表＋差距排名。

"""


"""
怎麼用在你現在的「寬限期 × DBR / ATD」問題上？

假設 raw data 欄位：

Grace_Flag：是否有寬限期 (1/0)

Eval_Type："DBR" / "ATD"

location_grade：地區等級（你樞紐的列）

cust_flag：客群旗標（你樞紐的欄）

Funding_Amt：金額

在你的分析 script / PyCharm console：

from scenario_compare import summarize_scenarios, copy_to_clipboard_for_excel

dims = ["location_grade", "cust_flag"]
value_col = "Funding_Amt"

scenarios = {
    "grace_all": lambda d: d["Grace_Flag"] == 1,
    "grace_DBR": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "DBR"),
    "grace_ATD": lambda d: (d["Grace_Flag"] == 1) & (d["Eval_Type"] == "ATD"),
}

res = summarize_scenarios(
    df,
    dims=dims,
    value_col=value_col,
    scenarios=scenarios,
    base_scenario="grace_all",   # 其他 scenario 相對「全部寬限期」做比較
)

# 1) 一張「整併後的樞紐」：location_grade × cust_flag × (3 個 scenario + 差值 + 比例)
copy_to_clipboard_for_excel(res.wide_with_diff, index=False)
# → 直接切到 Excel 貼上，就是一張可閱讀的分析表

# 2) 「差距最大的格子」排名（跨所有 scenario vs base）
top20 = res.top_abs_diff.head(20)
copy_to_clipboard_for_excel(top20, index=False)


這樣：

你不用再手動拉三張樞紐表。

每個 location_grade × cust_flag 的「grace_all / grace_DBR / grace_ATD」金額、
vs. baseline 的差距與比例一次看完。

想貼到 Excel 就 copy_to_clipboard_for_excel(...)，貼上就好。

如果之後你有「12 個 scenario」（= 12 張樞紐表要比），
只要 scenarios 多加幾個條目即可，整套流程不用改。

"""