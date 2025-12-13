# -*- coding: utf-8 -*-
"""
core.convert_utils
==================

型態與格式轉換工具（不依賴 df_utils，只依賴標準庫 + pandas/numpy）。

設計原則
--------
- 負責把「髒資料」轉成乾淨的 Python / pandas 型態：
    * 文字 → 數字（處理千分位、括號負號、全形字元等）
    * 文字 → 日期（西元 / 民國混合）
    * 文字 / 字典的輔助查找
- 盡量不處理 DataFrame 結構（切片、groupby 等），那些放在 df_utils。
- DataFrame 層級的函式僅限「欄位型態清洗」這一種用途（例如 safe_numeric_convert）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Hashable, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union
import re
import random
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


NumberLike = Union[int, float, np.number]
Scalar = Union[str, NumberLike, None]


# ============================================================
# 基礎字串工具
# ============================================================

def safe_replace(obj: Any, old: str, new: str) -> Any:
    """
    安全版本 str.replace：
        - 若 obj 為字串 → 呼叫 obj.replace(old, new)
        - 否則 → 原樣回傳（不丟錯）

    這個函式常用於欄位清洗前的預處理。
    """
    if isinstance(obj, str):
        return obj.replace(old, new)
    return obj


def findbylist(keywords: Iterable[str], text: Optional[str]) -> List[str]:
    """
    回傳 keywords 中「有出現在 text 裡」的所有字串，保持原順序。

    例：
        findbylist(["房貸", "車貸"], "本月房貸新增放款增加")
        → ["房貸"]
    """
    if not isinstance(text, str):
        return []
    return [k for k in keywords if k and k in text]


# ============================================================
# 數字轉換相關
# ============================================================

_NEG_PAREN_RE = re.compile(r"^\((?P<num>.+)\)$")
_THOUSAND_SEP_RE = re.compile(r"[,_]")

def _normalize_numeric_str(s: Any) -> Optional[str]:
    """
    將各種「看起來像數字」的字串轉成乾淨的標準形式（尚未轉成 float/int）。
    處理：
        - 去除前後空白
        - 全形轉半形 (NFKC)
        - 處理括號負號：(123) → -123
        - 去除千分位逗號 / 底線
    """
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return None
    if isinstance(s, (int, np.integer, float, np.floating)):
        return str(s)
    if not isinstance(s, str):
        s = str(s)

    s = unicodedata.normalize("NFKC", s.strip())
    if s == "":
        return None

    # 括號負號
    m = _NEG_PAREN_RE.match(s)
    if m:
        inner = m.group("num")
        inner = _THOUSAND_SEP_RE.sub("", inner)
        return "-" + inner

    # 一般情況：去除千分位
    s = _THOUSAND_SEP_RE.sub("", s)

    return s or None


def tonumeric_int(value: Any, *, errors: str = "raise", default: Optional[int] = None) -> Optional[int]:
    """
    嘗試把 value 轉成 int。

    處理：
        - None / 空字串 → None
        - 允許千分位、括號負號、全形數字
        - 若是浮點字串，會先轉 float 再取 int（截尾）

    參數：
        errors:
            - "raise"：轉換失敗時丟 ValueError
            - "coerce"：轉換失敗時回傳 default（預設 None）
        default:
            errors="coerce" 時的回傳值。

    回傳：
        int 或 None
    """
    s = _normalize_numeric_str(value)
    if s is None:
        return None

    try:
        # 先試直接 int
        return int(s)
    except (TypeError, ValueError):
        try:
            f = float(s)
            return int(f)
        except (TypeError, ValueError):
            if errors == "coerce":
                return default
            raise


def TenPercentile_to_int(
    value: Any,
    *,
    errors: str = "raise",
    default: Optional[Union[int, float]] = None,
    allow_float: bool = False,
) -> Optional[Union[int, float]]:
    """
    比 tonumeric_int 更彈性的數值轉換工具（原舊版名稱保留）。

    功能：
        - 將字串轉成數字，處理：
            * 千分位 / 底線
            * 括號負號
            * 全形字元
        - 預設回傳 int；若 allow_float=True，回傳 float。

    參數：
        errors:
            - "raise"：失敗時丟 ValueError
            - "coerce"：失敗時回傳 default
        default:
            errors="coerce" 時的預設回傳值。
        allow_float:
            True  → 回傳 float
            False → 回傳 int（透過 tonumeric_int）

    回傳：
        int / float / None
    """
    s = _normalize_numeric_str(value)
    if s is None:
        return None

    try:
        if allow_float:
            return float(s)
        return tonumeric_int(s, errors=errors, default=default if isinstance(default, int) else None)
    except ValueError:
        if errors == "coerce":
            return default
        raise


# ============================================================
# DataFrame 數值欄位清洗
# ============================================================

def safe_numeric_convert(
    df: pd.DataFrame,
    cols: Sequence[Hashable],
    *,
    allow_float: bool = True,
    errors: str = "coerce",
) -> pd.DataFrame:
    """
    對 DataFrame 中一組欄位做「安全數值轉換」。

    處理內容：
        - 全形→半形
        - 去除前後空白
        - 括號負號 (123) → -123
        - 去除千分位逗號 / 底線
        - 轉成 float（或 int）

    參數：
        df:
            要處理的 DataFrame。
        cols:
            欄位名稱列表。
        allow_float:
            True  → 轉成 float（預設）
            False → 轉成 int。
        errors:
            - "raise"：遇到無法轉換的值丟錯
            - "coerce"：無法轉換的值改為 NaN（float 模式）或 None（int 模式）

    回傳：
        原 df（就地修改）並返回，方便串接。
    """
    for col in cols:
        if col not in df.columns:
            continue

        if allow_float:
            df[col] = df[col].map(lambda x: TenPercentile_to_int(x, allow_float=True, errors=errors))
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = df[col].map(lambda x: tonumeric_int(x, errors=errors))
            # int 欄位會因為 None 而變成 float，交由使用者後續決定是否填補
    return df


def isinstance_dfiter(obj: Any) -> bool:
    """
    檢查物件是否「可迭代但不是 DataFrame」。
    這是舊版程式碼遺留的工具函式，這裡保留以維持相容性。

    回傳：
        True  → obj 是 iterable 且不是 pandas.DataFrame
        False → 否則
    """
    if isinstance(obj, pd.DataFrame):
        return False
    try:
        iter(obj)
        return True
    except TypeError:
        return False


# ============================================================
# dtype 輔助工具
# ============================================================

def dtypes_df(df: pd.DataFrame) -> pd.Series:
    """
    回傳每一欄位的 dtype 名稱（字串），index 為欄位名。

    例：
        >>> dtypes_df(df)
        col1    int64
        col2    float64
        col3    object
        dtype: object
    """
    return df.dtypes.astype(str)


# ============================================================
# 中文 / 數字混合處理
# ============================================================

def ChineseStr_bool(text: Any) -> bool:
    """
    檢查字串裡是否含有「中文」字元（CJK Unified Ideographs）。
    非字串則回傳 False。
    """
    if not isinstance(text, str):
        return False
    for ch in text:
        # CJK Unified Ideographs: 4E00–9FFF
        if "\u4e00" <= ch <= "\u9fff":
            return True
    return False


def numfromright(text: Any) -> str:
    """
    從右往左抓連續的「數字相關字元」，直到遇到第一個非數字相關的字元為止。

    數字相關字元包含：0-9, +, -, ., 逗號, 底線。

    例：
        numfromright("總計：1,234.56 元") → "1234.56"
    """
    if not isinstance(text, str):
        text = str(text)

    text = unicodedata.normalize("NFKC", text)
    valid_chars = set("0123456789+-.,_")
    buf: List[str] = []
    for ch in reversed(text):
        if ch in valid_chars:
            buf.append(ch)
        elif buf:
            break
    return "".join(reversed(buf))


# ============================================================
# 中文數字對應表（若未正式啟用，可當作保留欄位）
# ============================================================

CJK_NUM_MAP: Dict[str, int] = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "兩": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}

CJK_UNIT_MAP: Dict[str, int] = {
    "十": 10,
    "百": 100,
    "千": 1000,
    "萬": 10_000,
    "亿": 100_000_000,
    "億": 100_000_000,
    "兆": 1_000_000_000_000,
}


def chinese_number_to_int(text: Any, *, errors: str = "raise", default: Optional[int] = None) -> Optional[int]:
    """
    將中文數字（含萬 / 億 / 兆）轉換為 int 的簡易實作。

    只處理整數部分，未處理小數「點五」之類寫法。
    若字串中有非中文數字，則嘗試抽出右側數字片段再轉換。

    例：
        chinese_number_to_int("三萬二千")   → 32000
        chinese_number_to_int("一億兩千萬") → 120000000
    """
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return None
    if isinstance(text, (int, np.integer)):
        return int(text)
    if isinstance(text, (float, np.floating)):
        return int(text)

    s = str(text)
    s = unicodedata.normalize("NFKC", s.strip())
    if s == "":
        return None

    # 若不含中文數字，嘗試一般數值轉換
    if not any(ch in CJK_NUM_MAP or ch in CJK_UNIT_MAP for ch in s):
        try:
            return tonumeric_int(s, errors=errors, default=default)
        except ValueError:
            if errors == "coerce":
                return default
            raise

    total = 0
    section = 0  # 每個「萬」以下的小節
    num = 0      # 當前數字

    for ch in s:
        if ch in CJK_NUM_MAP:
            num = CJK_NUM_MAP[ch]
        elif ch in CJK_UNIT_MAP:
            unit = CJK_UNIT_MAP[ch]
            if unit >= 10_000:
                section = (section + num) * unit
                total += section
                section = 0
                num = 0
            else:
                section += (num or 1) * unit
                num = 0
        else:
            # 遇到非中文數字字元就忽略
            continue

    total += section + num
    return total


# ============================================================
# 日期轉換（文字 → datetime64[ns]）
# ============================================================

# =========================
# 日期格式樣板
# =========================

# 西元格式：
#   YYYYMMDD, YYYY/MM/DD, YYYY-MM-DD, YYYYMM, YYYY-MM
_DATE_PATTERNS_GREGORIAN = [
    "%Y%m%d",
    "%Y/%m/%d",
    "%Y-%m-%d",
    "%Y%m",
    "%Y-%m",
]

# 民國格式：
#   YYYMMDD, YYY/MM/DD, YYY-MM-DD
#   注意：實際轉換時會再加上 +1911 的邏輯
_DATE_PATTERNS_ROC = [
    "%Y%m%d",
    "%Y/%m/%d",
    "%Y-%m-%d",
]


def _parse_single_date(text: Any, mode: int = 1) -> Optional[pd.Timestamp]:
    """
    將單一輸入值轉成 `pd.Timestamp`。

    支援格式：
        - 西元：
            - YYYYMMDD
            - YYYY/MM/DD
            - YYYY-MM-DD
            - YYYYMM
            - YYYY-MM
        - 民國（自動 +1911）：
            - YYYMMDD
            - YYY/MM/DD
            - YYY-MM-DD
        - mode=5 另有專用「壓縮民國年月日」規則（見下方說明）

    參數
    ----------
    text : Any
        單一日期值，可為字串、數字、Timestamp、numpy.datetime64 等。
    mode : int, 預設 1
        解析策略：
            1 → 自動判斷西元 / 民國：
                 - 部分依字串長度與開頭判斷
                 - 預設流程為「先試西元 → 再試民國」
            2 → 民國優先：
                 - 先以民國格式嘗試
                 - 失敗再以西元格式嘗試
            3 → 僅西元：
                 - 只套用西元格式，不做 +1911 調整
            4 → 僅民國：
                 - 只套用民國格式，年份 <1911 時才 +1911
                 - 不 fallback 至西元
            5 → 壓縮民國年月日：
                 - 專門處理舊制民國日期（例如：`0820412`）
                 - 規則：
                     * 去掉小數點後內容、空白、`-`
                     * 長度必須介於 6～7 碼，不符則回傳 None
                     * 前面位數視為民國年，後四碼為 MMDD
                     * 年份 +1911
                     * 月 / 日為 "00" 時，補為 "01"
                 - 解析失敗回傳 None，不再嘗試其他模式

    回傳
    ----------
    `pd.Timestamp` 或 `None`
        解析成功則回傳 Timestamp；無法解析則回傳 None。
    """
    # 明確處理 None / NaN
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return None

    # 若本身已有時間型態，直接轉或回傳
    if isinstance(text, pd.Timestamp):
        return text
    if isinstance(text, (np.datetime64,)):
        return pd.Timestamp(text)

    s = str(text).strip()
    if s == "":
        return None

    # 正規化全形／半形等差異
    s = unicodedata.normalize("NFKC", s)

    # -------------------------------------------------
    # mode 5：舊制壓縮民國年月日（模仿原 strtodate 行為，不再 fallback）
    # -------------------------------------------------
    if mode == 5:
        # 去除小數、空白與 "-"
        raw = s.split(".")[0]
        raw = raw.replace(" ", "").replace("-", "")

        # 長度限制：6～7 碼；否則直接視為無效
        if not (6 <= len(raw) <= 7):
            return None

        # 不足位數前補零，統一視為 7 碼：YYYMMDD
        raw = raw.zfill(7)
        y_part = raw[:-4]
        m_part = raw[-4:-2]
        d_part = raw[-2:]

        # 年份 +1911；若無法轉 int 直接失敗
        try:
            year = int(y_part) + 1911
        except ValueError:
            return None

        # 月 / 日為 "00" 則補 "01"
        if m_part == "00":
            m_part = "01"
        if d_part == "00":
            d_part = "01"

        # 組合為 YYYY-MM-DD；若無法解析則回傳 None
        try:
            return pd.Timestamp(f"{year}-{m_part}-{d_part}")
        except ValueError:
            return None

    # -------------------------------------------------
    # ★ 明顯是「民國年月日」格式：110/06/01 或 110-06-01
    #   - 年份為 2～3 位數
    #   - 中間用 / 或 - 當分隔
    #   在 mode 1 / 2 / 4（允許民國）時，先直接套 ROC 規則。
    #   這一段是專門解決你現在看到的 110/06/01 → None 的問題。
    # -------------------------------------------------
    roc_slash = re.match(r"^(\d{2,3})[/-](\d{1,2})[/-](\d{1,2})$", s)
    if roc_slash and mode in (1, 2, 4):
        y_str, m_str, d_str = roc_slash.groups()
        try:
            year = int(y_str) + 1911
            month = int(m_str)
            day = int(d_str)
            return pd.Timestamp(year=year, month=month, day=day)
        except ValueError:
            # 非法日期（例如 110/13/40）就交給後面原流程處理
            pass

    # -------------------------------------------------
    # 共用 helper：依格式列表逐一嘗試
    # -------------------------------------------------
    def try_patterns(patterns, roc: bool = False) -> Optional[pd.Timestamp]:
        """
        依指定格式列表逐一嘗試解析字串 s。

        patterns :
            一組 datetime format 字串（例如：["%Y%m%d", "%Y/%m/%d"]）
        roc :
            True  → 視為民國年，若 year < 1911 則 +1911。
            False → 視為西元，不做年分修正。
        """
        for p in patterns:
            try:
                dt = pd.to_datetime(s, format=p, errors="raise")
                if roc:
                    # 民國年：
                    #   預設先視為「民國年」
                    #   若解析後 year < 1911，才 +1911 → 轉為西元
                    #   若原本就 >=1911，視為已經是西元，不再調整
                    year = dt.year
                    if year < 1911:
                        dt = dt.replace(year=year + 1911)
                return dt
            except (ValueError, TypeError):
                continue
        return None

    # -------------------------------------------------
    # mode 3：只試西元
    # -------------------------------------------------
    if mode == 3:
        return try_patterns(_DATE_PATTERNS_GREGORIAN, roc=False)

    # -------------------------------------------------
    # mode 4：只試民國
    # -------------------------------------------------
    if mode == 4:
        return try_patterns(_DATE_PATTERNS_ROC, roc=True)

    # -------------------------------------------------
    # mode 2：民國優先，失敗再試西元
    # -------------------------------------------------
    if mode == 2:
        dt = try_patterns(_DATE_PATTERNS_ROC, roc=True)
        if dt is not None:
            return dt
        return try_patterns(_DATE_PATTERNS_GREGORIAN, roc=False)

    # -------------------------------------------------
    # mode 1（預設）：簡易判斷後自動（西元 / 民國）
    # -------------------------------------------------
    # 規則：
    #   若開頭為「1xx」且長度 <= 7，大機率視為民國年 → 先試民國，再試西元
    if re.match(r"^1\d{2}", s) and len(s) <= 7:
        dt = try_patterns(_DATE_PATTERNS_ROC, roc=True)
        if dt is not None:
            return dt
        return try_patterns(_DATE_PATTERNS_GREGORIAN, roc=False)

    # 其餘情況：預設先試西元，再試民國
    dt = try_patterns(_DATE_PATTERNS_GREGORIAN, roc=False)
    if dt is not None:
        return dt
    return try_patterns(_DATE_PATTERNS_ROC, roc=True)


def stringtodate(
    df: pd.DataFrame,
    datecol: Sequence[Hashable],
    mode: int = 1,
) -> pd.DataFrame:
    """
    將 DataFrame 指定欄位的「文字日期」轉成 `datetime64[ns]`。

    實際解析邏輯委由 `_parse_single_date` 處理。

    支援格式（依 `_parse_single_date` 定義）：
        - 西元：
            - YYYYMMDD, YYYY/MM/DD, YYYY-MM-DD, YYYYMM, YYYY-MM
        - 民國：
            - YYYMMDD, YYY/MM/DD, YYY-MM-DD
        - 壓縮民國年月日（mode=5）：
            - 6～7 碼民國年月日（例如：0820412）
            - 年 +1911，月/日為 "00" 時補 "01"

    參數
    ----------
    df : pd.DataFrame
        要處理的資料表。
    datecol : Sequence[Hashable]
        欲轉換為日期的欄位名稱列表。
        若欄位不存在於 df 中，會自動略過。
    mode : int, 預設 1
        轉換模式（直接傳給 `_parse_single_date`）：
            1 → 自動判斷西元 / 民國（預設）
            2 → 民國優先
            3 → 僅西元
            4 → 僅民國
            5 → 壓縮民國年月日（專門對應舊制 6～7 碼 ROC 日期）

    回傳
    ----------
    pd.DataFrame
        傳入的 df 本身（就地修改後再回傳）。
    """
    for col in datecol:
        if col not in df.columns:
            continue
        df[col] = df[col].map(lambda v: _parse_single_date(v, mode=mode))
    return df

# _parse_single_date("110/06/01", mode=1)
# _parse_single_date("110/06/01", mode=2)
# _parse_single_date("110/06/01", mode=4)


# ============================================================
# 字典 / 文字查找工具（原 dict_utils 系列）
# ============================================================

def indexkey(dic: Mapping[Any, Any], index: int) -> Any:
    """
    依照「鍵的順序」取得第 index 個 key（0-based）。

    注意：Python 3.7+ 的 dict 是 insertion-ordered，但若來源不是普通 dict，
    請先確認類型是否有順序保證。
    """
    try:
        return list(dic.keys())[index]
    except IndexError:
        raise IndexError("index 超出 dict 長度")


def findstr(dic: Mapping[str, Any], text: str) -> List[str]:
    """
    在 text 中尋找 dic 的 key，回傳「有出現的 key」列表。
    不判斷 value。

    例：
        dic = {"房貸": 1, "車貸": 2}
        findstr(dic, "本月房貸新增") → ["房貸"]
    """
    if not isinstance(text, str):
        return []
    return [k for k in dic.keys() if k in text]


def randomitem(dic: Mapping[Any, Any]) -> Tuple[Any, Any]:
    """
    隨機回傳 dict 裡的一組 (key, value)。
    """
    if not dic:
        raise ValueError("dic 為空，無法隨機選取")
    key = random.choice(list(dic.keys()))
    return key, dic[key]


def flat(dic: Mapping[Any, Any]) -> Dict[Any, Any]:
    """
    將「可能巢狀」的 dict / Mapping 結構攤平成單層 dict。

    規則：
        - 若 value 仍是 Mapping → 一層層展開
        - 若 value 不是 Mapping → 直接保留

    注意：若不同路徑出現相同 key，後面的會覆蓋前面的。
    """
    result: Dict[Any, Any] = {}

    def _recurse(d: Mapping[Any, Any]) -> None:
        for k, v in d.items():
            if isinstance(v, Mapping):
                _recurse(v)
            else:
                result[k] = v

    _recurse(dic)
    return result


def stack(dic: Mapping[Any, Any]) -> Dict[Any, List[Any]]:
    """
    將巢狀 dict 結構「沿路徑聚合」成 {葉節點: [經過的所有 key]} 的形式。

    例：
        dic = {"A": {"x": 1, "y": 2}, "B": {"x": 3}}
        stack(dic) →
            {
                1: ["A", "x"],
                2: ["A", "y"],
                3: ["B", "x"],
            }

    常用於「scenario_compare」這類需要把多層設定展開的情境。
    """
    result: Dict[Any, List[Any]] = {}

    def _recurse(d: Mapping[Any, Any], path: List[Any]) -> None:
        for k, v in d.items():
            new_path = path + [k]
            if isinstance(v, Mapping):
                _recurse(v, new_path)
            else:
                result[v] = new_path

    _recurse(dic, [])
    return result


def renamekey(
    dic: MutableMapping[Any, Any],
    replacedic: Mapping[Any, Any],
    *,
    error: str = "coerce",
) -> MutableMapping[Any, Any]:
    """
    批次更改 dict 的 key。

    參數：
        dic:
            原始 dict。
        replacedic:
            {舊 key: 新 key} 的對應表。
        error:
            - "coerce"：遇到不存在的 key 就略過
            - "raise" ：遇到不存在的 key 就丟 KeyError

    回傳：
        原 dic（就地修改）並返回。
    """
    for old, new in replacedic.items():
        if old not in dic:
            if error == "raise":
                raise KeyError(f"{old} 不在 dic 中")
            continue
        dic[new] = dic.pop(old)
    return dic


def keyinstr(
    text: str,
    dic: Optional[Mapping[str, Any]] = None,
    lis: Optional[Sequence[str]] = None,
    default: Any = "",
) -> Any:
    """
    在文字 text 中尋找「第一個有出現的 key」，回傳對應的 value 或 key 本身。

    使用方式：
        1. 傳入 dic：
            keyinstr("本月房貸新增放款", dic={"房貸": "HL", "車貸": "CL"})
            → "HL"
        2. 傳入 lis：
            keyinstr("本月房貸新增放款", lis=["房貸", "車貸"])
            → "房貸"

    若都沒找到，回傳 default。
    """
    if not isinstance(text, str):
        return default

    if dic:
        for k, v in dic.items():
            if k in text:
                return v
    if lis:
        for k in lis:
            if k in text:
                return k
    return default


# ============================================================
# 檔案格式轉換
# ============================================================

def xlstoxlsx(path: Union[str, Path]) -> Path:
    """
    將舊格式的 xls / HTML 表格檔轉成 xlsx。

    簡化作法：
        - 以 pandas.read_html 讀取第一個 table
        - 另存為 xlsx 檔案（同路徑、不同副檔名）

    回傳：
        產生的 xlsx 檔案 Path。
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    tables = pd.read_html(str(path))
    if not tables:
        raise ValueError(f"{path} 中沒有找到任何 table")

    df = tables[0]
    new_path = path.with_suffix(".xlsx")
    df.to_excel(new_path, index=False)
    return new_path


__all__ = [
    # 字串
    "safe_replace",
    "findbylist",
    # 數字
    "tonumeric_int",
    "TenPercentile_to_int",
    "safe_numeric_convert",
    "isinstance_dfiter",
    # dtype
    "dtypes_df",
    # 中文 / 數字
    "ChineseStr_bool",
    "numfromright",
    "chinese_number_to_int",
    # 日期
    "stringtodate",
    # dict / 字串工具
    "indexkey",
    "findstr",
    "randomitem",
    "flat",
    "stack",
    "renamekey",
    "keyinstr",
    # 檔案
    "xlstoxlsx",
]
