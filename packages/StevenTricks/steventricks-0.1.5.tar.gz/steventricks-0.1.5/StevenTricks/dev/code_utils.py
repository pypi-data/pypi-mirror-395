# -*- coding: utf-8 -*-
"""
StevenTricks.dev.naming
=======================

功能：
    - basic_code：產生隨機代碼，可選擇附帶遞增順序碼，並避開指定清單。
    - CodeFormatConfig / NameGenerator：依格式樣板產生檔名。
    - sleepteller：隨機 sleep，模擬長 / 短任務。

設計原則：
    - 全部用函式 / 類別呼叫，不做 I/O。
    - 保留原本介面，避免破壞既有程式。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from random import choices, randint
from string import ascii_letters, digits
from time import sleep
from typing import List, Optional, Sequence, Union, Literal


CodeList = Union[str, List[str]]
MatchMode = Literal["exact", "fuzzy"]


# ===============================
#  基礎代碼產生器
# ===============================

def basic_code(
    length: int = 4,
    with_order: bool = False,
    order_start: int = 1,
    order_digits: int = 2,
    count: int = 1,
    avoid_list: Optional[Sequence[str]] = None,
    match_mode: MatchMode = "exact",
) -> CodeList:
    """
    ✅ 隨機產生代碼（可選擇包含遞增順序碼），並避免與已存在的代碼重複。

    參數：
        length:
            代碼「總長度」（含順序碼）。若順序碼位數超過 length，字母區段會被壓縮到至少 1 碼。
        with_order:
            是否在尾端加入數字遞增順序碼。
        order_start:
            順序碼起始數字。
        order_digits:
            最小順序碼位數（例如 2 → 01, 02, ..., 99）。
        count:
            要產生的代碼數量。
        avoid_list:
            禁用代碼 / 字串清單。
        match_mode:
            - "exact"：整串完全比對（code in avoid_list）
            - "fuzzy"：只要 avoid_list 中任一字串出現在 code 中就排除

    回傳：
        - count == 1：回傳 str
        - count  > 1：回傳 List[str]

    範例：
        basic_code(length=6, with_order=True, count=3)
        → ['t9KfN101', 'XTcYx302', 'Bh7Lm503']
    """
    avoid_list = list(avoid_list or [])

    def is_conflict(code: str) -> bool:
        if match_mode == "exact":
            return code in avoid_list
        if match_mode == "fuzzy":
            # 原本反過來寫成 any(code in s for s in avoid_list)，會完全失效
            return any(substr in code for substr in avoid_list)
        raise ValueError("match_mode 必須是 'exact' 或 'fuzzy'")

    results: List[str] = []
    current_order = order_start
    min_order_digits = max(1, order_digits)

    while len(results) < count:
        if with_order:
            # 依目前順序碼實際長度 & 最小位數決定要保留幾位
            order_str_raw = str(current_order)
            order_len = max(min_order_digits, len(order_str_raw))
            order_str = order_str_raw.zfill(order_len)

            # 總長度固定，順序碼變長就壓縮前面的隨機碼長度，但至少保留 1 碼
            char_len = max(1, length - order_len)
            char_part = "".join(
                choices(ascii_letters + digits, k=char_len)
            )
            code = f"{char_part}{order_str}"
        else:
            code = "".join(
                choices(ascii_letters + digits, k=length)
            )

        if not is_conflict(code):
            results.append(code)

        current_order += 1

    return results if count > 1 else results[0]


# ===============================
#  檔名設定 & 產生器
# ===============================

@dataclass
class CodeFormatConfig:
    """
    檔名規則設定檔（適用於產出檔案名稱）

    name_format 中可以用以下保留字：
        - "code"  ：隨機 / 自訂代碼
        - "time"  ：時間戳記
        - "order" ：獨立順序碼
        - ".ext"  ：副檔名占位符，會被 ext 取代

    例如：
        name_format = "code_time_order.ext"
        → abc12_20250717_001.pkl
    """
    name_format: str = "code_time_order.ext"
    code: str = ""                       # 若不採隨機，可手動指定 code
    random_code: bool = True             # True → 使用 basic_code 產生
    code_with_order: bool = False        # random_code 時，是否在 code 裡也加順序碼
    code_length: int = 4                 # random_code 時，代碼總長度
    code_order_digits: int = 2           # 若 code 含順序碼，初始位數
    timestamp_precision: Literal["date", "second"] = "second"
    ext: str = ".pkl"                    # 副檔名（包含 .）
    order_start: int = 1                 # 檔名中獨立順序碼起始值
    order_digits: int = 3                # 檔名中獨立順序碼最小位數
    count: int = 1                       # 要產生幾組檔名
    avoid_list: List[str] = field(default_factory=list)  # 代碼禁用清單（傳給 basic_code）
    match_mode: MatchMode = "exact"      # 代碼比對模式


class NameGenerator:
    """
    檔名產生器：依照 CodeFormatConfig 組合檔名。
    """

    def __init__(self, config: CodeFormatConfig) -> None:
        self.config = config

    def generate(self) -> CodeList:
        """
        根據 config 產出檔名，可支援：
            - 隨機代碼（可加順序）
            - 時間戳記（精準到日或秒）
            - 全自訂樣板

        常見格式：
            code_time_order.ext → abc123_20250717_001.pkl
            time_order.ext      → 20250717_001.pkl
            code.ext            → XyZ9.pkl
        """
        fmt = self.config.name_format

        flags = {
            "code": "code" in fmt,
            "time": "time" in fmt,
            "order": "order" in fmt,
            "ext": ".ext" in fmt,
        }

        # 時間戳記
        ts_fmt = "%Y%m%d" if self.config.timestamp_precision == "date" else "%Y%m%d%H%M%S"
        timestamp = datetime.now().strftime(ts_fmt)

        results: List[str] = []
        current_order = self.config.order_start
        min_order_digits = max(1, self.config.order_digits)

        while len(results) < self.config.count:
            base_name = fmt

            # code 區段
            if flags["code"]:
                if self.config.random_code:
                    code_part = basic_code(
                        length=self.config.code_length,
                        with_order=self.config.code_with_order,
                        order_start=current_order,
                        order_digits=self.config.code_order_digits,
                        count=1,
                        avoid_list=self.config.avoid_list,
                        match_mode=self.config.match_mode,
                    )
                else:
                    code_part = self.config.code

                base_name = base_name.replace("code", code_part)

            # time 區段
            if flags["time"]:
                base_name = base_name.replace("time", timestamp)

            # 獨立 order 區段
            if flags["order"]:
                order_str_raw = str(current_order)
                order_len = max(min_order_digits, len(order_str_raw))
                order_str = order_str_raw.zfill(order_len)
                base_name = base_name.replace("order", order_str)

            # 副檔名
            if flags["ext"]:
                base_name = base_name.replace(".ext", self.config.ext)

            # 避免在同一批次中重複（避免同一輪 count 的衝撞）
            if base_name not in results:
                results.append(base_name)

            current_order += 1

        return results if self.config.count > 1 else results[0]


# ===============================
#  通用 sleep 工具
# ===============================

def sleepteller(mode: Optional[str] = None) -> None:
    """
    隨機 sleep，方便在排程 / 測試時避免固定間隔被偵測。

    參數：
        mode:
            - 'long'：600～660 秒
            - 其他 / None：10～30 秒
    """
    if mode == "long":
        seconds = randint(600, 660)
    else:
        seconds = randint(10, 30)

    print(f"Be about to sleep {seconds} seconds")
    sleep(seconds)


__all__ = [
    "basic_code",
    "CodeFormatConfig",
    "NameGenerator",
    "sleepteller",
]

"""
if __name__ == "__main__":
    cfg = CodeFormatConfig(
        name_format="code_time_order.ext",
        code_length=5,
        code_with_order=True,
        code_order_digits=3,
        timestamp_precision="second",
        order_start=998,
        order_digits=3,
        count=5,
        ext=".pkl",
    )
    gen = NameGenerator(cfg)
    print(gen.generate())


"""