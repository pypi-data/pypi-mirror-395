# -*- coding: utf-8 -*-
"""
File Utility Toolkit
Consolidated utilities for file management, metadata access, serialization, and logging.
"""



from datetime import datetime
import pickle
from os import makedirs
from pathlib import Path
import pandas as pd

def runninginfo():
    """Print the current execution time and source file (if available)."""
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        file = __file__
    except NameError:
        file = ""
    print(f"在{t}/n執行{file}")
    return {"Time": t, "File": file}


def pickleio(path, data=None, mode="load"):
    """Unified function to save or load Python objects using pickle.

    Parameters:
        path (str): Path to the pickle file.
        data (any): Data to be saved (required if mode='save').
        mode (str): 'save' or 'load'.

    Returns:
        Loaded data if mode is 'load'. None if mode is 'save'.
    """
    if mode == "save":
        makedirs(Path(path).parent, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    elif mode == "load":
        with open(path, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError("mode must be either 'save' or 'load'")


def pathlevel(left, right):
    """計算 right 相對於 left 的目錄層數"""
    left, right = Path(left).resolve(), Path(right).resolve()
    try:
        return len(right.relative_to(left).parts)
    except ValueError:
        return None  # 若 right 不在 left 之下，返回 None

def _get_path_stat(p: Path):
    """Extract file/directory timestamps or return None values."""
    stat = p.stat() if p.exists() else None
    return {
        "created_time": datetime.fromtimestamp(stat.st_ctime) if stat else None,
        "modified_time": datetime.fromtimestamp(stat.st_mtime) if stat else None,
        "accessed_time": datetime.fromtimestamp(stat.st_atime) if stat else None
    }


def _list_files(path, file_filter=None):
    """Internal utility to list all files recursively under a path."""
    base = Path(path)
    for p in base.rglob("*"):
        if p.is_file() and (file_filter is None or file_filter(p)):
            yield p


def PathWalk_df(path, dirinclude=[], direxclude=[], fileexclude=[], fileinclude=[], level=None, name_format=None):
    """
    🔍 遍歷指定資料夾下的所有檔案，依照條件進行篩選與解析，回傳為一個 pandas DataFrame。

    ✅ 功能亮點：
        - 遞迴列出所有檔案，包含完整路徑與層級資訊。
        - 支援資料夾/檔案的「包含」與「排除」條件。
        - 可限制最深搜尋層級。
        - 可解析檔名格式，分出 code、time、order、ext 等欄位。
        - ✅ 內建 `dir` 欄位，代表每個檔案所屬的資料夾名稱。

    📥 參數說明：
        path (str or Path):
            要搜尋的根目錄。

        dirinclude (list[str]):
            只包含路徑中含有這些字串的檔案（通常用於資料夾名稱過濾）。

        direxclude (list[str]):
            排除路徑中含有這些字串的檔案。

        fileinclude (list[str]):
            只包含檔名中含有這些字串的檔案（例如只包含 ".pkl"）。

        fileexclude (list[str]):
            排除檔名中含有這些字串的檔案。

        level (int or None):
            限制檔案距離根目錄的最大層數（根目錄為 0），None 則不限制。

        name_format (str or None):
            指定檔名格式，例如 "code_time_order.ext"。符合格式的檔名會解析成多個欄位。

    📤 回傳：
        pandas.DataFrame，包含以下欄位：
            - file：檔案名稱（不含路徑）
            - path：完整路徑
            - level：相對於根目錄的層數（根目錄下的檔案為 1，子資料夾為 2，以此類推）
            - dir：父資料夾名稱
            - [code/time/order/ext]：若有給定 name_format，會額外解析出對應欄位
    """

    # ⬇️ 建立所有檔案的紀錄清單
    rows = []
    for p in _list_files(path):
        rel = str(p.relative_to(path))         # 相對路徑字串（未使用但可拓展）
        file = p.name                          # 檔案名稱
        full_path = str(p)                     # 絕對路徑字串
        level_val = pathlevel(path, p)         # 相對層級
        dir_name = p.parent.name               # 所屬資料夾名稱
        rows.append((file, full_path, level_val, dir_name))

    # ⬇️ 建立成 DataFrame
    df = pd.DataFrame(rows, columns=["file", "path", "level", "dir"])

    # ⬇️ 過濾層級
    if level is not None:
        df = df[df["level"] <= level]

    # ⬇️ 過濾資料夾包含字串（透過路徑比對）
    if dirinclude:
        df = df[df["path"].str.contains("|".join(dirinclude), na=False)]

    # ⬇️ 排除資料夾包含字串
    if direxclude:
        df = df[~df["path"].str.contains("|".join(direxclude), na=False)]

    # ⬇️ 檔名包含字串過濾
    if fileinclude:
        df = df[df["file"].str.contains("|".join(fileinclude), na=False)]

    # ⬇️ 檔名排除字串過濾
    if fileexclude:
        df = df[~df["file"].str.contains("|".join(fileexclude), na=False)]

    # ⬇️ 若指定 name_format，解析檔名為多個欄位
    if name_format:
        format_parts = name_format.split("_")
        has_ext = format_parts[-1].endswith(".ext")
        split_keys = [p.replace(".ext", "") for p in format_parts]

        def parse_parts(filename: str):
            # 將檔名分成主體與副檔名
            stem, ext = filename, None
            if has_ext and "." in filename:
                stem, ext = filename.rsplit(".", 1)
            parts = stem.split("_")
            result = {}
            for i, key in enumerate(split_keys):
                result[key] = parts[i] if i < len(parts) else None
            result["ext"] = ext if has_ext else None
            return result

        parsed = df["file"].apply(parse_parts)
        parsed_df = pd.DataFrame(parsed.tolist())
        df = pd.concat([df, parsed_df], axis=1)

    return df.reset_index(drop=True)

def merge_excel_sheets_from_folder(
    root,
    output_filename="統整.xlsx",
    level=None,
    dirinclude=None,
    direxclude=None,
    fileinclude=None,
    fileexclude=None,
):
    """
    將資料夾底下所有 Excel 檔案的工作表，依「工作表名稱」進行縱向合併，
    並輸出成一個新的 Excel 檔（每個工作表一個 sheet）。

    使用情境（對應你原本的 file_append.py）：
        - 指定一個資料夾 root
        - 找出裡面的所有 Excel 檔（含子資料夾）
        - 每支檔案用 `pd.read_excel(..., sheet_name=None)` 讀成多工作表
        - 依工作表名稱把 DataFrame concat 起來
        - 最後寫出一個 `統整.xlsx` 放在 root 底下

    Parameters
    ----------
    root : str or pathlib.Path
        要搜尋的根目錄。
    output_filename : str or pathlib.Path, default "統整.xlsx"
        輸出的 Excel 檔名。如果給相對路徑，會寫在 root 底下。
    level : int or None, default None
        傳給 PathWalk_df，用來限制搜尋的目錄層級。
    dirinclude, direxclude, fileinclude, fileexclude : list[str] or None
        同 PathWalk_df 的過濾條件。預設 None 代表不特別限制。

    Returns
    -------
    pathlib.Path
        實際寫出的檔案完整路徑。

    Notes
    -----
    - 目前會搜尋副檔名為 .xls / .xlsx / .xlsm 的檔案。
    - 如果沒有找到任何符合條件的 Excel 檔，會 raise FileNotFoundError。
    """

    root = Path(root).resolve()

    # 使用既有的 PathWalk_df 取得檔案清單
    df_paths = PathWalk_df(
        root,
        dirinclude=dirinclude or [],
        direxclude=direxclude or [],
        fileexclude=fileexclude or [],
        fileinclude=fileinclude or [],
        level=level,
    )

    if df_paths.empty:
        raise FileNotFoundError(f"在資料夾 {root} 底下找不到任何檔案（PathWalk_df 結果為空）")

    # 只保留 Excel 檔
    excel_mask = df_paths["file"].str.lower().str.endswith((".xls", ".xlsx", ".xlsm"))
    df_paths = df_paths[excel_mask]

    if df_paths.empty:
        raise FileNotFoundError(f"在資料夾 {root} 底下找不到任何 Excel 檔（.xls/.xlsx/.xlsm）")

    # 開始依工作表名稱累積 DataFrame
    sheets: dict[str, pd.DataFrame] = {}

    for path_str in df_paths["path"]:
        path_file = Path(path_str)
        # 讀取整支 Excel：回傳 dict(sheet_name -> DataFrame)
        xls_dict = pd.read_excel(path_file, sheet_name=None)

        for sheet_name, df in xls_dict.items():
            if sheet_name not in sheets:
                sheets[sheet_name] = df.copy()
            else:
                sheets[sheet_name] = pd.concat(
                    [sheets[sheet_name], df],
                    ignore_index=True,
                )

    # 決定輸出路徑
    out_path = Path(output_filename)
    if not out_path.is_absolute():
        out_path = root / out_path

    # 寫成一個多工作表的統整檔案
    if not sheets:
        raise RuntimeError("沒有任何工作表可以寫出（sheets 為空）。")

    with pd.ExcelWriter(out_path) as writer:
        for sheet_name, df in sheets.items():
            # Excel sheet 名稱最多 31 字元，超過就截斷
            safe_name = str(sheet_name)[:31]
            df.to_excel(writer, sheet_name=safe_name, index=False)

    return out_path

def logmaker(write_dt, data_dt, log=pd.Series(dtype='object'), period=None, index=None):
    """Compose a logging Series with optional period granularity."""
    if period == "month":
        period = str(data_dt).rsplit("-", 1)[0]
    elif period == "year":
        period = str(data_dt.year)
    elif period == "day":
        period = data_dt
    base = pd.Series({
        "write_dt": write_dt,
        "data_dt": data_dt,
        "period": period,
        "index": index
    }, dtype='object')
    return pd.concat([base, log], axis=1).dropna(how="any", axis=1)

def logfromfolder(path_df, log=None, fillval=None, avoid=None):
    """
    根據資料夾內實際存在的檔案，更新 log DataFrame。

    參數
    ----
    path_df : pandas.DataFrame
        通常由 PathWalk_df 回傳的結果，至少需要 'file' 欄位。
    log : pandas.DataFrame or None
        原本的 log 資料表，index 通常是「某種 ID」，欄位是狀態欄位。
        若為 None，則建立一個新的空 DataFrame。
    fillval : Any
        找到對應檔案時，要填入 log 的值，例如 "succeed" / True 等。
    avoid : list or None
        若 log 原本該格的值在 avoid 裡，就跳過不覆蓋。

    回傳
    ----
    pandas.DataFrame
        更新後的 log。
    """
    import pandas as pd

    if log is None:
        log = pd.DataFrame()

    if avoid is None:
        avoid = []

    # 先把既有的 'succeed' 視為待確認狀態（照你原本邏輯）
    log = log.replace({"succeed": "wait"})

    for name in path_df["file"]:
        parts = name.split("_")
        if len(parts) < 2:
            continue

        col = parts[0]
        ind = parts[1].split(".")[0]

        if col in log and ind in log.index:
            if log.loc[ind, col] in avoid:
                # 這些狀態不覆寫
                continue

        log.loc[ind, col] = fillval

    return log


"""
from StevenTricks.io.file_utils import merge_excel_sheets_from_folder

root = r"D:\轉檔\nums_application資料清理\10AH25YA23TA_AU_資料匯入9至16"

out_path = merge_excel_sheets_from_folder(root)
print(out_path)


# 只處理第 0 層（不往子資料夾跑），且只吃檔名含「_9至16」的
out_path = merge_excel_sheets_from_folder(
    root,
    level=0,
    fileinclude=["9至16"],
)
from StevenTricks.io.file_utils import merge_excel_sheets_from_folder
merge_excel_sheets_from_folder(r"D:\轉檔\...")


"""