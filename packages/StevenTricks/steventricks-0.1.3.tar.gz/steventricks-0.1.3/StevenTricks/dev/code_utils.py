import random
import string
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Union


def basic_code(
    length: int = 4,
    with_order: bool = False,
    order_start: int = 1,
    order_digits: int = 2,
    count: int = 1,
    avoid_list: Optional[List[str]] = None,
    match_mode: str = "exact"
) -> Union[str, List[str]]:
    """
    ✅ 隨機產生代碼（可選擇包含遞增順序碼），並避免與已存在的代碼重複。

    參數說明：
        length (int): 代碼總長度（含順序碼），預設為 4。
        with_order (bool): 是否加入數字遞增順序碼（附在代碼尾部），預設 False。
        order_start (int): 順序碼的起始數字，預設為 1。
        order_digits (int): 初始順序碼位數（如 2 → 01、99），自動擴增，預設 2。
        count (int): 產生幾組代碼。
        avoid_list (list[str]): 禁止出現的代碼清單，預設為空。
        match_mode (str): 比對模式：
            - "exact": 僅與整體比對。
            - "fuzzy": 只要代碼包含 avoid_list 裡的任一字串就排除。

    回傳：
        str 或 list[str]: 回傳單組或多組代碼。

    範例：
        basic_code(length=6, with_order=True, count=3)
        → ['t9KfN101', 'XTcYx302', 'Bh7Lm503']
    """
    if avoid_list is None:
        avoid_list = []

    def is_conflict(code):
        if match_mode == "exact":
            return code in avoid_list
        elif match_mode == "fuzzy":
            return any(code in s for s in avoid_list)
        else:
            raise ValueError("match_mode 必須是 'exact' 或 'fuzzy'")

    results = []
    current_order_digits = order_digits
    i = order_start

    while len(results) < count:
        if with_order:
            order_str = f"{i:0{current_order_digits}d}"
            # 若數字位數超過原設定，自動調整位數與代碼長度
            if len(order_str) > current_order_digits:
                current_order_digits = len(order_str)
                length = max(length, current_order_digits + 1)
            char_len = length - current_order_digits
            char_part = ''.join(random.choices(string.ascii_letters + string.digits, k=char_len))
            code = f"{char_part}{order_str}"
        else:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        if not is_conflict(code):
            results.append(code)

        i += 1

    return results if count > 1 else results[0]


# ===============================
# 專門管理命名格式的資料結構
# ===============================

@dataclass
class CodeFormatConfig:
    """
    設定檔：用於組合命名規則（適用於產出檔案名稱）
    """
    name_format: str = "code_time_order.ext"  # 命名格式樣板
    code: str = ""                            # 若不採隨機，可手動指定 code
    random_code: bool = True                  # 是否使用隨機 code（否則使用手動 code）
    code_with_order: bool = False             # 隨機 code 是否包含順序碼
    code_length: int = 4                      # 隨機 code 的總長度
    code_order_digits: int = 2                # 若 code 含順序碼，初始佔幾位數
    timestamp_precision: str = "second"       # 時間格式（"date" 或 "second"）
    ext: str = ".pkl"                         # 副檔名
    order_start: int = 1                      # 起始順序碼
    order_digits: int = 3                     # order 的位數（非 code 的）
    count: int = 1                            # 要產生幾組名稱
    avoid_list: List[str] = field(default_factory=list)  # 避免重複清單
    match_mode: str = "exact"                 # 比對模式（精準或模糊）


# ===============================
# 檔名產生器主程式
# ===============================

class NameGenerator:
    def __init__(self, config: CodeFormatConfig):
        self.config = config

    def generate(self) -> Union[str, List[str]]:
        """
        根據組態 config 產出檔名，可支援：
        - 隨機代碼（可加順序）
        - 時間戳記（精準到日或秒）
        - 全部自訂格式

        格式範例：
            code_time_order.ext → abc123_20250717_001.pkl
            time_order.ext → 20250717_001.pkl
            code.ext → XyZ9.pkl
        """
        flags = {
            "code": "code" in self.config.name_format,
            "time": "time" in self.config.name_format,
            "order": "order" in self.config.name_format,
            "ext": ".ext" in self.config.name_format
        }

        timestamp_fmt = "%Y%m%d" if self.config.timestamp_precision == "date" else "%Y%m%d%H%M%S"
        timestamp = datetime.now().strftime(timestamp_fmt)

        results = []
        i = self.config.order_start
        current_order_digits = self.config.order_digits

        while len(results) < self.config.count:
            base_name = self.config.name_format

            # 產生 code 區段
            if flags["code"]:
                if self.config.random_code:
                    code_part = basic_code(
                        length=self.config.code_length,
                        with_order=self.config.code_with_order,
                        order_start=i,
                        order_digits=self.config.code_order_digits,
                        count=1,
                        avoid_list=self.config.avoid_list,
                        match_mode=self.config.match_mode
                    )
                else:
                    code_part = self.config.code
                base_name = base_name.replace("code", code_part)

            # 加入時間區段
            if flags["time"]:
                base_name = base_name.replace("time", timestamp)

            # 加入獨立順序碼區段
            if flags["order"]:
                order_str = f"{i:0{current_order_digits}d}"
                if len(order_str) > current_order_digits:
                    current_order_digits = len(order_str)
                base_name = base_name.replace("order", order_str)

            # 加上副檔名
            if flags["ext"]:
                base_name = base_name.replace(".ext", self.config.ext)

            # 避免重複
            if base_name not in results:
                results.append(base_name)

            i += 1

        return results if self.config.count > 1 else results[0]

from time import sleep
from random import randint

def sleepteller(mode=None):
    if mode == 'long':
        time = randint(600, 660)
    else:
        time = randint(10, 30)
    print('Be about to sleep {}'.format(str(time)))
    sleep(time)



# from pprint import pprint
#
# # 建立命名設定
# cfg = CodeFormatConfig(
#     name_format="code_time_order.ext",
#     code_length=5,
#     code_with_order=True,
#     code_order_digits=3,
#     timestamp_precision="second",
#     order_start=998,
#     order_digits=3,
#     count=5,
#     ext=".pkl"
# )
#
# # 建立名稱產生器
# gen = NameGenerator(cfg)
#
# # 產生檔名
# names = gen.generate()
#
# pprint(names)

# ['M4zjL_20250717090510_998.pkl',
#  '7B1kU_20250717090510_999.pkl',
#  'Tx9Uv_20250717090510_1000.pkl',
#  'LF9is_20250717090510_1001.pkl',
#  'qR8Em_20250717090510_1002.pkl']
