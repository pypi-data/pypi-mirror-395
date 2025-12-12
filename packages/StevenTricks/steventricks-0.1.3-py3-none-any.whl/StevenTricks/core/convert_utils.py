# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:33:20 2022

@author: 118939
"""


import re
import sys
import locale
import pandas as pd

from os import remove, path


def safe_replace(text,old,new):
    if isinstance(text,str):
        text = text.replace(old,new)
    return text

def findbylist(lis, text):
    # 可以給出一連串文字，放在list裏面，只要list裡面有其中一個文字是在text裡面的話，那就會返回搜尋結果，是一個list
    # 返回的字串以lis裡面匹配的為主
    return re.findall('|'.join([re.escape(_) for _ in lis]), text)


def isinstance_dfiter(df):
    # to tell the df if it is iterable or not
    try:
        iter(df)
        if isinstance(df, pd.DataFrame) is True:
            return False
        elif isinstance(df, pd.DataFrame) is False:
            return True
    except:
        return False
    

def tonumeric_int(char):
    # 用來判斷是否為數字，盡量返回整數，如果不是浮點數也不是整數就返回原來的字符
    try:
        res = float(char)
    except:
        return None
    # 因為float可以返回的種類最多，如果連float都無法返回那一定不是數值類型，就返回None
    # 下面以返回res為主，通常不是返回int，最少也會返回float
    try:
        if res == int(char):
            return int(char)
        else:
            return res
    except:
        return res


def dtypes_df(df):
    df = df.convert_dtypes()
    # 把dataframe的dtypes屬性轉換成純文字的series，可以選擇是否在轉換過程中，統一更名成sql模式的屬性名稱，或是不更名
    return df.dtypes.map(lambda x: x.name)


def TenPercentile_to_int(char, errors="raise", local="en_US.UTF-8"):
    # 可以把帶有逗號的文字用千分位的模式轉換成數字的功能，所以要先檢查輸入的char是否為數字，如果是的話就直接用tonumeric_int轉成數字送出去就好，如果不是的話才要進行下面的功能，進行千分位轉換，如果千分位也無法轉換，那這個就不是數字
    char = tonumeric_int(char)
    if isinstance(char, str) is False:
        return char
    locale.setlocale(locale.LC_ALL, local)
    
    try:
        return locale.atof(char)
    except ValueError:
        if errors == "raise":
            raise ValueError
        elif errors == "ignore":
            return char
        elif errors == "coerce":
            return None
    except:
        print("=====NEW ERROR=====\n{}\n=====NEW ERROR=====\n{}".format(sys.exc_info(), char))
        raise ValueError


def stringtodate(df: pd.DataFrame = pd.DataFrame(),
                            datecol: list[str] = None,
                            mode: int = 1) -> pd.DataFrame:
    """
    將民國/西元多種日期格式轉成 pandas datetime64[ns]（就地更新 df[datecol]）。
    解析失敗者為 NaT。

    參數
    ----
    mode:
      1: 「93年4月12日」→ 2004-04-12
      2: 「9/82」或「9-82」(月/民國年) → 1993-09-01（日預設為1）
      3: 「82/4/12」(民國/月/日) → 1993-04-12
      4: 自動偵測壓縮字串：
         - 6~7 碼數字 → 視為民國壓縮 yyyMMdd（例如 820412 → 1993-04-12）
         - 8  碼數字 → 視為西元壓縮 yyyyMMdd（例如 20250909 → 2025-09-09）
         允許空白、減號、斜線、與小數尾巴（如 '820412.0'、'82-04-12' 會被清理再判斷）
    """
    if isinstance(datecol, list):
        if not datecol:
            return df
    elif isinstance(datecol, str):
        datecol = [datecol]

    cols = [c for c in datecol if c in df.columns]
    if not cols:
        return df

    def _na_dt(series: pd.Series) -> pd.Series:
        return pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")

    def _build_ymd(y, m, d) -> pd.Series:
        """y/m/d 皆為 numeric Series；0 月/日補 1；組字串再 to_datetime"""
        y = pd.to_numeric(y, errors="coerce").astype("Int64")
        m = pd.to_numeric(m, errors="coerce").astype("Int64")
        d = pd.to_numeric(d, errors="coerce").astype("Int64")
        m = m.where(m > 0, 1)
        d = d.where(d > 0, 1)
        ystr = y.astype("string")
        mstr = m.astype(str).str.zfill(2)
        dstr = d.astype(str).str.zfill(2)
        return pd.to_datetime(ystr + "-" + mstr + "-" + dstr, errors="coerce")

    def _mode1(series: pd.Series) -> pd.Series:
        """93年4月12日 → 2004-04-12"""
        s = series.astype("string").str.strip()
        sp = s.str.split(r"年|月|日", expand=True)
        if sp.shape[1] < 3:
            return _na_dt(series)
        y = pd.to_numeric(sp[0], errors="coerce") + 1911
        m = pd.to_numeric(sp[1], errors="coerce")
        d = pd.to_numeric(sp[2], errors="coerce")
        return _build_ymd(y, m, d)

    def _mode2(series: pd.Series) -> pd.Series:
        """9/82 或 9-82 → 1993-09-01（預設日=1）"""
        s = (series.astype("string").str.strip()
             .str.replace("－", "-", regex=False))
        sp = s.str.split(r"[-/]", expand=True)
        if sp.shape[1] < 2:
            return _na_dt(series)
        month = pd.to_numeric(sp[0], errors="coerce")
        roc_y = pd.to_numeric(sp[1], errors="coerce")
        y = roc_y + 1911
        return _build_ymd(y, month, 1)

    def _mode3(series: pd.Series) -> pd.Series:
        """82/4/12 → 1993-04-12"""
        s = (series.astype("string").str.strip()
             .str.replace(" ", "", regex=False)
             .str.replace("-", "/", regex=False))
        sp = s.str.split("/", expand=True)
        if sp.shape[1] < 3:
            return _na_dt(series)
        roc = pd.to_numeric(sp[0], errors="coerce")
        m = pd.to_numeric(sp[1], errors="coerce")
        d = pd.to_numeric(sp[2], errors="coerce")
        y = roc + 1911
        return _build_ymd(y, m, d)

    def _mode4(series: pd.Series) -> pd.Series:
        """
        自動偵測壓縮日期：
        - 6~7 碼 → 民國壓縮 yyyMMdd（820412 → 1993-04-12）
        - 8 碼  → 西元壓縮 yyyyMMdd（20250909 → 2025-09-09）
        會先清理空白、減號、斜線、以及小數尾巴（.0）
        """
        s = (series.astype("string")
                    .str.split(".", n=1).str[0]      # 去小數尾巴
                    .str.replace(" ", "", regex=False)
                    .str.replace("-", "", regex=False)
                    .str.replace("/", "", regex=False))

        # 先做長度/純數字遮罩
        mask8 = s.str.fullmatch(r"\d{8}")            # 西元 yyyyMMdd
        mask67 = s.str.fullmatch(r"\d{6,7}")         # 民國 yyyMMdd（年 2~3 碼）

        out = _na_dt(series)

        # 8碼：yyyyMMdd
        if mask8.any():
            s8 = s.where(mask8)
            y = s8.str.slice(0, 4)
            m = s8.str.slice(4, 6)
            d = s8.str.slice(6, 8)
            out[mask8] = _build_ymd(y, m, d)[mask8]

        # 6~7碼：ROC yyyMMdd
        if mask67.any():
            s67 = s.where(mask67).str.zfill(7)
            y_roc = s67.str.slice(0, -4)
            m = s67.str.slice(-4, -2)
            d = s67.str.slice(-2)
            y = pd.to_numeric(y_roc, errors="coerce") + 1911
            out[mask67] = _build_ymd(y, m, d)[mask67]

        return out

    # 逐欄位轉換（就地）
    if mode == 1:
        df.loc[:, cols] = df.loc[:, cols].apply(_mode1)
    elif mode == 2:
        df.loc[:, cols] = df.loc[:, cols].apply(_mode2)
    elif mode == 3:
        df.loc[:, cols] = df.loc[:, cols].apply(_mode3)
    elif mode == 4:
        df.loc[:, cols] = df.loc[:, cols].apply(_mode4)
    else:
        raise ValueError(f"Unsupported mode: {mode!r}. Use 1|2|3|4.")

    return df


# df = pd.DataFrame({
#     "月年": ["9/82", "9-82", "13/82", None],   # 月/ROC年 → 預設日 = 1 號
#     "roc": ["82/4/12", "114/08/05", "x/y/z","20250909"],   # ROC年/月/日
#     "raw_date": ["0820412", "820412.0", " 82-04-12 ","20250909" ]
# })
# df1 = stringtodate(df, datecol="raw_date", mode=4)


def ChineseStr_bool( char ) :
    if re.sub("[^\u4e00-\u9fa5]", "" , char) == "" :
        return False
    else:
        return True


def numfromright( char ) :
# typ表示要返回文字的部分還是數字的部分，而和值的類型無關
    new = ""
    start_sign = "號"
    preserve_sign = "-之—"
    # stop_sign = "、,~ &?()/;+._'ˋ:∕。"
    # 從 "號" 開始收集往右的非漢字(包含數字和特殊符號),然後遇到漢字就停下來
    for _ in str( char )[ : : -1 ] :
        if new == "" :
            if _ in start_sign :
                new = _
        elif new != "" :
            if _ in preserve_sign :
                new = _ + new
            else :
                try :
                    new = str(int(_)) + new
                except :
                    break
    if new == "" or new in start_sign : return char
    # temp = new.maketrans( point_sign , "."*len( point_sign ) , start_sign )
    # new = new.translate( temp )
    # new = new.split(".")
    # if len(new) == 1 :
        # new = new[0]
    # elif len(new) > 1 :
        # new = "{}.{}".format( new[0] , "".join( new[ 1 : ] ) )
        
    # try :
    #     return float(new)
    # except:
    #     print(new)
    return new


adapter = {
    "unit" : {
        "零" : 1 ,
        "十" : 10,
        "百" : 100,
        "千" : 1000,
        "萬" : 10000,
        "億" : 100000000,
        "兆" : 1000000000000
        },
    "value" : {
        "一" : 1 ,
        "二" : 2 ,
        "三" : 3 ,
        "四" : 4 ,
        "五" : 5 ,
        "六" : 6 ,
        "七" : 7 ,
        "八" : 8 ,
        "九" : 9 ,
        }
    }


def xlstoxlsx(path):
    newpath = path.splitext(path)[0] + '.xlsx'
    with pd.ExcelWriter(newpath) as writer:
        for df in pd.read_html(path, header=0):
            df.to_excel(writer, index=False)
    remove(path)
    return newpath

# =======================================================================
# 字典／字串小工具（原本在 core/dict_utils.py）
# =======================================================================

from random import randint
import re


def indexkey(dic, index):
    """
    依照「第 index 個鍵」取值（字典是有順序時才有意義）。
    找不到就印出提示訊息。
    """
    n = 0
    for key in dic:
        if n == index:
            return dic[key]
        n += 1
    print('index <{}> is out of index. the dic size is {}'.format(str(index), str(n)))


def findstr(dic, text):
    """
    在 key 裡面搜尋符合 text 的字串，回傳所有 key 的 list。
    text 可以是 regex，也可以用 'a|b|c' 這種 pattern。
    """
    res = []
    for key in dic:
        if re.search(text, key):
            res.append(key)
    return res


def randomitem(dic):
    """
    從字典裡隨機抽一個 (key, value)。
    """
    key = list(dic.keys())[randint(0, len(dic)-1)]
    return key, dic[key]


def flat(dic):
    """
    把字典的 value 攤平成 key：

    - 如果 value 是 list → list 裡每個元素變成 key，指向原本的 key
    - 如果 value 不是 list → 直接把 value 當 key，value 變成原本的 key

    例：
        {'a': [1, 2], 'b': 3}
        → {1: 'a', 2: 'a', 3: 'b'}
    """
    res = {}
    for key, value in dic.items():
        if isinstance(value, list) is True:
            res.update(dict.fromkeys(value, key))
        else:
            res[value] = key
    return res


def stack(dic):
    """
    flat 的反向操作：
    - 把「value 相同的 key」，全部收成 list，value 變成新的 key。

    例：
        {1: 'a', 2: 'a', 3: 'b'}
        → {'a': [1, 2], 'b': [3]}
    """
    res = {}
    for key, value in dic.items():
        if value not in res:
            res[value] = []
        res[value].append(key)
    return res


def renamekey(dic, replacedic={}, error='coerce'):
    """
    批次改 key 名稱（in-place）：

    replacedic = { old_key: new_key }

    error:
        - 'coerce'：如果 new_key 原本不存在，先給它一個 None
        - 'ignore'：new_key 不存在就略過
    """
    for key in replacedic:
        if replacedic[key] not in dic:
            if error == 'coerce':
                dic[replacedic[key]] = None
            elif error == 'ignore':
                pass
            continue
        dic[key] = dic.pop(replacedic[key])
    return dic


def keyinstr(str, dic={}, lis=None, default=""):
    """
    先精準比對 dic 的 key：
        - 如果 key == str → 回傳 dic[key]
    若沒找到，再去 lis 裡面看有沒有 substring 出現在 str 中：
        - 如果有，回傳那個 substring
    都沒有 → 回傳 default
    """
    if lis is None:
        lis = []
    for key in dic:
        # 原本用 `in`，會出現部分比對誤判，所以改用 ==
        if key == str:
            return dic[key]
    for i in lis:
        if i in str:
            return i
    return default

"""
from StevenTricks.dev.code_utils import basic_code

# 產生 10 組長度 6 的代碼，尾巴帶 2 位數遞增順序碼，排除某些字串
codes = basic_code(
    length=6,
    with_order=True,
    order_start=1,
    order_digits=2,
    count=10,
    avoid_list=["00", "ABCD"],
    match_mode="fuzzy",
)
"""