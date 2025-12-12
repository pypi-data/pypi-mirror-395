# -*- coding: utf-8 -*-
"""
Core DataFrame utilities for StevenTricks.

包含：
- safe_numeric_convert
- dateseries / dateseriesdict
- replace_series
- DataFrameMerger
"""

from StevenTricks.core.df_utils import (
    safe_numeric_convert, findval, dateseries, periodictable,
    replace_series, unique_series, cutoutliers_series,
    dfrows_iter, make_series, dateinterval_series,
    list_union, numinterval_series, replacebyseries,
    DataFrameMerger,
)

# 後面就是既有的 safe_numeric_convert / dateseries / replace_series / DataFrameMerger ...


def safe_numeric_convert(df: pd.DataFrame, cols):
    """
    將指定欄位轉成數值；先做 NFKC 折疊以處理全形→半形。
    - 括號視為負號：(1,234) → -1234
    - 支援千分位小數
    - 轉不動為 NaN
    """
    cols = [c for c in cols if c in df.columns]
    if not cols:
        return df

    pat = r'([+\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?|[+\-]?\d+(?:\.\d+)?)'

    for c in cols:
        s = df[c].astype(str).map(lambda x: ud.normalize('NFKC', x))   # ✅ 全形→半形（廣義）
        s = s.str.replace(r'^\s*\((.*)\)\s*$', r'-\1', regex=True)      # 括號當負號
        s = s.str.extract(pat, expand=False)                             # 抽第一個數字片段
        s = s.str.replace(',', '', regex=False)                          # 去千分位
        df[c] = pd.to_numeric(s, errors='coerce')
    return df
def findval(df, val):
    for col in df:
        series = df.loc[df[col].isin([val]), col]
        res = zip(series.index, series.size*[col])
        for ind, col1 in res:
            yield ind, col1


def dateseries(seriesname="", pendix="", datemin="", datemax=datetime.now().date(), freq="", defaultval=None):
    # 這是用來產生時間當作index的一串series
    # seriesname,pendix就是這個series的name和前綴詞，如果需要放註記避免重複可以用pendix
    # mindate、maxdate可以用來指定特定區間，maxdate預設是當天，freq是指這段區間的頻率，可以是Ｄ、Ｗ、Ｍ、Ｑ、Ｙ
    # defaultstr是這個series產生的時候內部預設的文字，因為如果跟其他series結合，沒有值的話python本身就是預設None，所以如果要用作判斷是結合後為空直，還是本身就是空直，盡量default不要是none
    d = pd.date_range(start=datemin, end=datemax, freq=freq)
    d = d.append(pd.DatetimeIndex([datemax]))
    # 因為d的屬性是pandas.core.indexes.datetimes.DatetimeIndex，實質上是index，所以要用index內建的function，pd.concat只能用在df和series
    d = d.unique()
    return pd.Series(np.repeat(defaultval, d.size), index=d, name=pendix + seriesname)


def periodictable(perioddict={}, datemin=None):
    # 傳入的格式為{name:{'datemin':'yyyy-m-d','freq':'D' or 'ME'}}，可多個name同時傳入
    # datemin有沒有給都沒差，他會自己去抓periodict裡面的datemin來用
    df = []
    for key in perioddict:
        if datemin is not None:
            perioddict[key]['datemin'] = datemin
        df.append(dateseries(seriesname=key, datemin=perioddict[key]['datemin'], freq=perioddict[key]['freq'], defaultval='wait'))
    df = pd.concat(df, axis=1)
    return df


# dateseries(seriesname='ssss',mindate='2010-1-1',freq='W')
def replace_series(series, std_dict, na=False, mode="fuzz"):
    # series依照std_dict給定的對照表，去replace每一個值，std_dict只能是一對一的dict，取代的方式分為fuzz和exac兩個模式，exac比較快速但適用範圍較窄，fuzz適用範圍比較廣，但是比較慢，在可以預期的情況下盡量使用exac
    res = []
    for key, value_list in std_dict.items():
        if isinstance(value_list, list) is False:
            value_list = [value_list]
        value = '|'.join(map(re.escape, value_list))
        # 一定要在|內的全部的條件都配對到，才會進行replace
        if mode == 'exac':
            ind = series.map(lambda x: True if len(set(value_list)) == len(set(re.findall(value, x))) else False)
        # 只要|裡面其中一個條件有配對到，就會把值替換掉
        elif mode == 'fuzz':
            ind = series.map(lambda x: True if re.search(value, x) else False)
        series[ind] = key
        res.append(series[ind])
        series = series.drop(series[ind].index, axis=0)
        if series.empty is True:
            break

    if na is True:
        res.append(series)
    return pd.concat(res, axis=0)


def unique_series(series, mode=""):
    series = series.dropna( axis=0)
    if mode in ["timestamp", "datetime64[ns]", "timedelta64"]:
        series = series.map(lambda x: str(x.year).split(".")[0])
    return series.unique()


def cutoutliers_series(series, bottom=0.05, up=0.95):
    return series[(series >= series.quantile(bottom)) & (series <= series.quantile(up))]


def dfrows_iter(df, colname_list, std_dict={}, nodropcol_list=[]):
    # 根據傳入的幾個col，把他們全部用笛卡爾積相連
    res_list = []
    df = df.convert_dtypes()
    dtype_dict = dtypes_df(df)
    if std_dict:
        dtype_dict = replace_series(dtype_dict, std_dict, True, "fuzz")
    for col in colname_list:
        list_temp = unique_series(df[col], dtype_dict[col])
        res_list.append(product([col], list_temp))
    res_list = product(*res_list)
    # 然後分別產出不同的區塊(rows)，可以指定保留那些col，所以善用nodropcol_list，這樣出來的區塊就會有那個欄位，然後指定的col因為需要取出唯一值，所以可以用std_dict去改變唯一值
    for data_colkey in res_list:
        key_list = []
        res_df = df.copy()
        for col, key in data_colkey:
            if dtype_dict[col] in ["timestamp", "datetime64[ns]", "timedelta64"]:
                res_df = res_df.loc[res_df[col].map(lambda x: True if str(x.year) == key else False), :]
            else:
                res_df = res_df.loc[res_df[col] == key, :]
            if col not in nodropcol_list:
                res_df = res_df.drop([col], axis=1)
            key_list.append(key)
        if res_df.empty is True:
            continue
        yield [key_list, res_df]

def make_series(df, column_name, ind_name="date"):
    """
    從 DataFrame 中抽出特定欄位，並將 date 作為 index 欄位合併輸出。

    Parameters:
        df (pd.DataFrame): 原始資料。
        column_name (str): 欲抽取的欄位名稱。
        date_name (str): 欲命名的日期欄位（預設為 'date'）。

    Returns:
        pd.DataFrame: 包含 date 與欄位值的新資料框。
    """
    result = df[column_name].copy()
    result.index = df[ind_name]
    return result


def dateinterval_series(series, freq="MS"):
    date_range = pd.date_range(start=series.min(), end=series.max(), freq='MS', inclusive='both')
    # "MS" "QS"

    date_range = date_range.union(pd.date_range(date_range[0] - date_range.freq, periods=1, freq=date_range.freq))
    date_range = date_range.union(pd.date_range(date_range[-1] + date_range.freq, periods=1, freq=date_range.freq))

    res = pd.cut(pd.to_datetime(series), bins=date_range, include_lowest=True, right=False)
    res = res.map(lambda x: x.left.date)
    return res


def list_union(list_tup):
    # list_tup for example => [ [1,2] , [3,2,1] ]
    return sorted(list(set().union(*list_tup)))


def numinterval_series(series, std_list, label=None):
    if series.min() < min(std_list):
        std_list = list_union([std_list, [series.min()]])
    if series.max() > max(std_list):
        std_list = list_union([std_list, [series.max()]])
    res = pd.cut(series, bins=std_list, include_lowest=True, right=True, labels=label)
    if label is None:
        res = res.map(lambda x: "{}~{}".format(x.left, x.right))
    return res


# 加上詳細註解的 DataFrameMerger 類別
class DataFrameMerger:
    def __init__(self, left: pd.DataFrame):
        # 初始化合併器，設定初始 DataFrame，並建立更新歷程記錄清單
        self.left = left.copy()
        self.history = []  # 儲存每次更新的前後狀態

    def renew(self, right: pd.DataFrame, overwrite: bool = True) -> pd.DataFrame:
        # 判斷右邊資料是否為空
        if right.empty:
            print("Empty right ...")
            return self.left
        # 若左邊資料為空，直接回傳右邊資料作為新狀態
        elif self.left.empty:
            print("Empty left ...")
            self.left = right.copy()
            return self.left
        # 若兩邊資料完全相同，無需處理
        if self.left.equals(right):
            print("No difference ...")
            return self.left

        # 建立左邊資料的副本作為更新基礎
        updated = self.left.copy()

        # 找出左右共同的欄位
        shared_cols = [col for col in right.columns if col in updated.columns]

        if overwrite:
            # 若允許覆寫，直接使用 pandas 的 update 方法就地更新
            try:
                updated.update(right[shared_cols])
            except ValueError as e:
                print(e)
                updated = updated.reset_index(drop=True)
                right = right.reset_index(drop=True)
                updated.update(right[shared_cols])
        else:
            # 若不允許覆寫，只更新 NaN 的欄位值
            for col in shared_cols:
                common_index = updated.index.intersection(right.index)
                for idx in common_index:
                    if pd.isna(updated.at[idx, col]):
                        updated.at[idx, col] = right.at[idx, col]

        # 處理 right 中的新欄位（left 中不存在）
        new_cols = [col for col in right.columns if col not in updated.columns]
        for col in new_cols:
            # 轉換型別以支援 NA（nullable）
            col_dtype = right[col].dtype
            if pd.api.types.is_integer_dtype(col_dtype):
                safe_dtype = 'Int64'
            elif pd.api.types.is_bool_dtype(col_dtype):
                safe_dtype = 'boolean'
            else:
                safe_dtype = col_dtype

            # 在 updated 中建立新欄位並初始化為 NA
            updated[col] = pd.Series([pd.NA] * len(updated), index=updated.index, dtype=safe_dtype)

            # 將新欄位在共有 index 中的資料從 right 填入 updated
            common_index = right.index.intersection(updated.index)
            updated.loc[common_index, col] = right.loc[common_index, col]

        # 新增 right 中在 left 中不存在的 index 對應的列
        new_rows = right.loc[~right.index.isin(updated.index)]
        updated = pd.concat([updated, new_rows], axis=0)

        # 儲存本次更新的歷史（包含更新前、更新使用的 right、更新後）
        self.history.append({
            "before": self.left.copy(),
            "right": right.copy(),
            "after": updated.copy()
        })

        # 更新內部狀態
        self.left = updated
        return updated



def replacebyseries(toreplace = "", res = "" , df = pd.DataFrame()):
    temp = df[[toreplace, res]].values
    return pd.Series([_[1].replace(_[0],'') for _ in temp ])





if __name__ == '__main__':
    pass