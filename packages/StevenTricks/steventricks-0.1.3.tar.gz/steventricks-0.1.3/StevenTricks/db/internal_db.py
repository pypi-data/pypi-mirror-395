import pandas as pd
import numpy as np
from pathlib import Path
from StevenTricks.db.data_store import DataStore


store = DataStore(
    db_dir=Path("/some/path/to/db"),
    history_dir=Path("/some/path/to/history"),
    log_dir=Path("/some/path/to/logs"),
    db_name="funding_amt",
)

store.save(df_new)        # 寫入並記錄版本
df_all = store.load()     # 讀取現有完整資料
history = store.list_versions()  # 查看歷史版本（實際方法名稱依原碼為準）



class DBPkl:
    """
    用 pickle 模擬簡易 DB 的工具，支援「主鍵合併」、「欄位 schema 檢查」等功能。
    ...
    """

    def __init__(
            self,
            db_name: str,
            table_name: str,
            logical_table_name: Optional[str] = None,
    ):
        """
        db_name:
            資料夾路徑
        table_name:
            實際存檔用的 table 名（例如：'三大法人買賣超日報__2012'）
        logical_table_name:
            邏輯上的 table 名，用來決定 schema 檔名。
            不給的話，預設 = table_name（維持舊行為）
        """
        self.db_name = str(db_name)
        self.table_name = str(table_name)

        # ★ 新增：邏輯 table 名，專門給 schema 用
        self.logical_table_name = (
            str(logical_table_name) if logical_table_name else self.table_name
        )

        self.base_dir = Path(self.db_name)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # ★ 改成用 logical_table_name 產生 schema 檔
        self.schema_path = (
                self.base_dir / f"{self.logical_table_name}_schema"
        ).with_suffix(".pkl")

        self.schema: Optional[Dict[str, Any]] = None
        self.schema_conflict: Optional[Dict[str, Any]] = None

    def write_db(self,
                 df: pd.DataFrame,
                 convert_mode: str,
                 primary_key: Optional[Union[str, List[str]]] = None,
                 update_existing: bool = True,
                 overwrite_rows: bool = True,
                 allow_new_columns: bool = True,
                 allow_remove_columns: bool = False,
                 allow_remove_rows: bool = False,
                 allow_new_rows: bool = True,
                 save_schema: bool = True) -> None:

        if df.empty:
            return

        existing_schema = self.schema
        self._validate_schema_conflict(df, primary_key, convert_mode=convert_mode)

        df, schema_data = self._prepare_schema(df, primary_key, existing_schema)

        main_path = self.base_dir / f"{self.table_name}.pkl"
        df = self._merge_existing_data(df, main_path, schema_data, update_existing,
                                       overwrite_rows, allow_new_columns,
                                       allow_remove_columns, allow_remove_rows,
                                       allow_new_rows)

        pickleio(main_path, data=df, mode="save")

        if save_schema:
            pickleio(self.schema_path, data=schema_data, mode="save")
            self.schema = schema_data


    def write_partition(
        self,
        df: pd.DataFrame,
        convert_mode: str,
        partition_cols: Union[str, List[str]],
        primary_key: Optional[Union[str, List[str]]] = None,
        save_schema: bool = True,
    ) -> None:
        """
        依指定 partition 欄位（例如 'date'）做「整批覆寫」：

        - 先用 _validate_schema_conflict / _prepare_schema 做 schema 檢查與 link 轉換
        - 若舊表存在：把舊表中 partition key 出現在新資料裡的列全部刪掉
        - 再把新資料接回去 → 達成「按 partition 覆寫」效果

        適用情境：
        - TWSE 類日報表，整份檔案都是單一日期，
          希望「每次清這一天，就整天重算覆寫」，避免逐筆主鍵比對。
        """
        if df.empty:
            return

        # -------- 1) 整理 partition 欄位參數 --------
        if isinstance(partition_cols, str):
            part_cols = [partition_cols]
        else:
            part_cols = list(partition_cols)

        if not part_cols:
            raise ValueError(f"write_partition() 需要至少一個 partition 欄位")

        missing_in_new = [c for c in part_cols if c not in df.columns]
        if missing_in_new:
            raise ValueError(
                f"Partition 欄位 {missing_in_new} 不存在於新資料 DataFrame（table={self.table_name}）。"
            )

        # -------- 2) 先做 schema 檢查與 link 轉換 --------
        existing_schema = self.schema
        self._validate_schema_conflict(df, primary_key, convert_mode=convert_mode)

        # _prepare_schema 會：
        # - 檢查 / 建立 primary key
        # - 根據既有 schema 做 dtype / link 轉換
        df, schema_data = self._prepare_schema(df, primary_key, existing_schema)

        main_path = self.base_dir / f"{self.table_name}.pkl"

        # -------- 3) 若舊表存在：先把需要覆寫的 partition 刪掉 --------
        if main_path.exists():
            old_df = pickleio(main_path, mode="load")

            # 確認舊表也有這些 partition 欄位
            missing_in_old = [c for c in part_cols if c not in old_df.columns]
            if missing_in_old:
                raise ValueError(
                    f"Partition 欄位 {missing_in_old} 不存在於既有資料表（table={self.table_name}）。"
                )

            def _make_partition_key(df0: pd.DataFrame) -> pd.Series:
                """
                把多個 partition 欄位壓成一個字串 key，方便比對。
                單一欄位時就直接轉成字串。
                """
                if len(part_cols) == 1:
                    return df0[part_cols[0]].astype("string")
                else:
                    cols_as_str = [df0[c].astype("string") for c in part_cols]
                    key = cols_as_str[0]
                    for s in cols_as_str[1:]:
                        key = key.str.cat(s, sep="||")
                    return key

            old_key = _make_partition_key(old_df)
            new_key = _make_partition_key(df)

            # 新資料中有哪些 partition 要被覆寫
            replace_keys = set(new_key.dropna().unique().tolist())

            # 保留「不在新 partition 集合」的舊列
            keep_mask = ~old_key.isin(replace_keys)
            kept_df = old_df[keep_mask].copy()

            # 把舊的其他 partition + 新 partition 接在一起
            out_df = pd.concat([kept_df, df], ignore_index=True)
        else:
            # 沒有舊表，直接使用新資料即可
            out_df = df.copy()

        # -------- 4) 依 schema 調整欄位順序並存檔 --------
        ordered_cols = list(schema_data["dtypes"].keys())
        missing_in_out = [c for c in ordered_cols if c not in out_df.columns]
        if missing_in_out:
            raise ValueError(
                f"write_partition() 內部錯誤：schema 欄位 {missing_in_out} 不在合併後 DataFrame 中（table={self.table_name}）。"
            )

        out_df = out_df[ordered_cols]

        pickleio(main_path, data=out_df, mode="save")

        if save_schema:
            pickleio(self.schema_path, data=schema_data, mode="save")
            self.schema = schema_data

    def _coerce_series_to_dtype(self, s: pd.Series, expected: str) -> tuple[pd.Series, bool]:
        """嘗試把 s 轉成 expected dtype；回傳 (converted_series, ok)"""
        exp = expected.lower()

        # 數值：先 to_numeric，再精準轉 expected
        if exp.startswith("int") or exp.startswith("float"):
            try:
                out = pd.to_numeric(s, errors="coerce")
                if exp.startswith("int"):
                    # 目標是整數：若含 NaN 就視為轉型失敗（避免靜默資料遺失）
                    if out.isna().any():
                        return s, False
                    return out.astype(expected), True
                # 目標是浮點
                return out.astype(expected), True
            except Exception:
                return s, False

        # 日期時間
        if exp.startswith("datetime64"):
            try:
                out = pd.to_datetime(s, errors="coerce")
                # 若需要精準單位（ns），astype 一次；失敗則 False
                if str(out.dtype) == expected:
                    return out, True
                try:
                    return out.astype(expected), True
                except Exception:
                    return s, False
            except Exception:
                return s, False

        # 布林（支援 pandas nullable boolean）
        if exp in {"bool", "boolean"}:
            try:
                tmp = s
                # 常見字串/數字 map
                if (s.dtype == "O") or pd.api.types.is_string_dtype(s) or pd.api.types.is_numeric_dtype(s):
                    m = s.astype(str).str.strip().str.lower()
                    mapping = {"true": True, "false": False, "1": True, "0": False, "是": True, "否": False}
                    mapped = m.map(mapping)
                    tmp = pd.Series(np.where(mapped.isna(), s, mapped), index=s.index)
                return tmp.astype("boolean" if exp == "boolean" else "bool"), True
            except Exception:
                return s, False

        # 文字/物件
        if exp in {"string", "object"}:
            try:
                return (s.astype("string") if exp == "string" else s.astype("object")), True
            except Exception:
                return s, False

        # 其他型別：盡力一試
        try:
            return s.astype(expected), True
        except Exception:
            return s, False

    def _validate_schema_conflict(
            self,
            df: pd.DataFrame,
            primary_key: Optional[Union[str, List[str]]],
            convert_mode: str = "error",
    ) -> None:
        """
        檢查 df 與既有表的 schema 是否相容。

        mode：
          - "error"（預設）：嚴格模式，發現 dtype/PK 不相符就 raise。
          - "coerce"：若 dtype 不相符，嘗試把 df[col] 轉成既有表的 dtype（能轉就當作無衝突；轉不了才 raise）。
          - "upcast"：若雙方皆為數值型，將 df[col] 升級為 float64 後視為可接受（schema 會在後續 _prepare_schema 被覆寫成新 dtype）；
                      其他型別仍依 "coerce" 規則處理。

        注意：本函式可能就地（in-place）修改 df 的欄位 dtype。
        """
        # ---- 驗證 mode ----
        mode = (convert_mode or "error").lower().strip()
        if mode not in {"error", "coerce", "upcast"}:
            raise ValueError(f"Unknown mode: {mode!r}. Expected 'error'|'coerce'|'upcast'.")

        # ---- 若沒有既有 schema，直接通過 ----
        if self.schema is None:
            return

        # ---- 檢查 Primary Key 一致性（沿用原行為）----
        new_pk = primary_key if primary_key is not None else None
        if new_pk != self.schema.get("primary_key"):
            try:
                old_tail = pickleio(self.base_dir / f"{self.table_name}.pkl", mode="load").tail(1)
            except Exception:
                old_tail = None
            self.schema_conflict = {
                "table": self.table_name,
                "type": "primary_key_mismatch",
                "existing_primary_key": self.schema.get("primary_key"),
                "new_primary_key": new_pk,
                "old_row": old_tail,
                "new_row": df.tail(1),
            }
            raise ValueError("Primary key mismatch. Please resolve manually.")

        expected_dtypes: Dict[str, str] = self.schema.get("dtypes", {}) or {}

        def _is_numeric_dtype_str(s: str) -> bool:
            ls = (s or "").lower()
            # 支援 numpy/pandas 可見的 'int64'/'float64'/'Int64'/'Float64' 等寫法
            return ls.startswith("int") or ls.startswith("float")

        # ---- 逐欄比對 ----
        for col in df.columns:
            # schema 未定義者視為允許（沿用你原邏輯）
            if col not in expected_dtypes:
                continue

            expected = expected_dtypes[col]
            actual = str(df[col].dtype)

            # 已一致
            if actual == expected:
                continue

            if mode == "error":
                # 嚴格模式：直接報衝突
                try:
                    old_tail = pickleio(self.base_dir / f"{self.table_name}.pkl", mode="load").tail(1)
                    old_sample = old_tail[[col]] if (old_tail is not None and col in old_tail.columns) else old_tail
                except Exception:
                    old_sample = None
                self.schema_conflict = {
                    "table": self.table_name,
                    "type": "dtype_mismatch",
                    "column": col,
                    "expected_dtype": expected,
                    "actual_dtype": actual,
                    "old_row": old_sample,
                    "new_row": df[[col]].tail(1),
                }
                raise TypeError("Column dtype mismatch. Please resolve manually.")

            # "coerce" 與 "upcast"：先判斷是否兩邊皆為數值
            both_numeric = _is_numeric_dtype_str(expected) and pd.api.types.is_numeric_dtype(df[col].dtype)

            if mode == "upcast" and both_numeric:
                # 統一升級成 float64（避免 int/float 交替）
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
                # 在 upcast 下，數值欄不再要求等於舊 schema 的 dtype，讓後續 _prepare_schema 覆寫 schema
                continue

            # 其餘情況依 "coerce" 規則處理：嘗試轉成舊 schema dtype
            converted, ok = self._coerce_series_to_dtype(df[col], expected)
            if ok and str(converted.dtype) == expected:
                df[col] = converted
                continue

            # 仍失敗：記錄衝突並 raise
            try:
                old_tail = pickleio(self.base_dir / f"{self.table_name}.pkl", mode="load").tail(1)
                old_sample = old_tail[[col]] if (old_tail is not None and col in old_tail.columns) else old_tail
            except Exception:
                old_sample = None

            self.schema_conflict = {
                "table": self.table_name,
                "type": "dtype_mismatch",
                "column": col,
                "expected_dtype": expected,
                "actual_dtype": actual if not ok else str(converted.dtype),
                "old_row": old_sample,
                "new_row": df[[col]].tail(1),
            }
            raise TypeError("Column dtype mismatch. Please resolve manually.")

        # 全部通過
        self.schema_conflict = None
        return
    def _prepare_schema(self, df: pd.DataFrame, primary_key: Optional[Union[str, List[str]]], existing_schema: Optional[Dict]) -> (pd.DataFrame, Dict):
        schema_data = {"dtypes": {col: str(df[col].dtype) for col in df.columns}, "links": {}}

        if primary_key:
            self._check_primary_key_valid(df, primary_key)
            schema_data["primary_key"] = primary_key
        else:
            auto_pk_name = "AutoPrimaryKey_1"
            counter = 1
            while auto_pk_name in df.columns:
                counter += 1
                auto_pk_name = f"AutoPrimaryKey_{counter}"
            df.insert(0, auto_pk_name, range(1, len(df) + 1))
            schema_data["primary_key"] = [auto_pk_name]
            schema_data["dtypes"][auto_pk_name] = str(df[auto_pk_name].dtype)

        for col in df[[c for c in df if c not in schema_data["primary_key"]]]:
            if df[col].dtype == object and df[col].duplicated().any():
                # unique_vals = sorted(df[col].dropna().unique())
                unique_vals = (
                    pd.Series(df[col], dtype="object")
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .replace("", pd.NA)
                    .dropna()
                    .drop_duplicates()
                    .tolist()
                )
                link_df = self._generate_link_df(col, unique_vals, existing_schema)

                non_null_mapping = dict(zip(link_df[col], link_df['link_id']))
                df[col] = df[col].map(non_null_mapping).fillna(pd.NA)

                schema_data["links"][col] = link_df.to_dict(orient="list")

        return df, schema_data

    def _check_primary_key_valid(self, df: pd.DataFrame, primary_key: Union[str, List[str]]) -> None:
        if isinstance(primary_key, str):
            if primary_key not in df.columns:
                raise ValueError(f"Primary key column '{primary_key}' missing in DataFrame")
            if df.duplicated(subset=[primary_key]).any():
                raise ValueError(f"Primary key column '{primary_key}' does not form a unique constraint")
        elif isinstance(primary_key, list):
            if not all(col in df.columns for col in primary_key):
                raise ValueError(f"Some primary key columns {primary_key} missing in DataFrame")
            if df.duplicated(subset=primary_key).any():
                raise ValueError(f"Primary key columns {primary_key} do not form a unique constraint")

    def _generate_link_df(self, col: str, unique_vals: List[str], existing_schema: Optional[Dict]) -> pd.DataFrame:
        """
        產生/擴充字典型欄位的對照表（links），欄位結構固定為：
          - <col>: 原字串值
          - link_id: 整數遞增主鍵（1 起算）

        修補要點：
          1) 安全處理「舊對照表存在但為空 / link_id 皆 NaN」→ 從 1 起算
          2) 去除 None/NaN/空字串，並以字串形態去重
          3) 舊對照表可能沒有正確 dtype → 轉成可比較數字後再取 max
        """
        # ---- 規整新的候選值 ----
        # 去掉 None/NaN / 空白，強制轉 str，並去重（保持穩定序）
        new_vals_raw = pd.Series(unique_vals, dtype="object")
        new_vals = (
            new_vals_raw
            .dropna()
            .astype(str)
            .str.strip()
        )
        new_vals = new_vals[new_vals != ""].drop_duplicates().tolist()

        # 若 schema 內已有 links，先載入舊表
        if existing_schema and col in (existing_schema.get("links") or {}):
            old_link_df = pd.DataFrame(existing_schema["links"][col])

            # 舊表缺欄時補齊
            if col not in old_link_df.columns:
                old_link_df[col] = pd.Series(dtype="string")
            if "link_id" not in old_link_df.columns:
                old_link_df["link_id"] = pd.Series(dtype="Int64")

            # 規整舊值
            old_link_df[col] = (
                old_link_df[col]
                .astype("string")
                .str.strip()
            )
            # 移除空字串列
            old_link_df = old_link_df[old_link_df[col].notna() & (old_link_df[col] != "")].copy()

            # 確保 link_id 為整數或可轉為整數
            link_id_num = pd.to_numeric(old_link_df["link_id"], errors="coerce")
            # 若全是 NaN（或舊表為空），max_id 預設為 0（之後從 1 起算）
            max_id = int(link_id_num.max()) if link_id_num.notna().any() else 0

            # 建立既有 mapping
            old_mapping = dict(zip(old_link_df[col].astype(str), link_id_num.astype("Int64")))

            # 挑出真的新的字串值
            add_vals = [v for v in new_vals if v not in old_mapping]

            if add_vals:
                # 從 max_id+1 接續
                start = max_id + 1
                new_ids = list(range(start, start + len(add_vals)))
                new_entries = pd.DataFrame({col: add_vals, "link_id": new_ids})
                out = pd.concat([old_link_df[[col, "link_id"]], new_entries], ignore_index=True)
            else:
                out = old_link_df[[col, "link_id"]].copy()

            # 最終排序（選擇性）
            out = out.drop_duplicates(subset=[col]).sort_values("link_id").reset_index(drop=True)
            return out

        # ---- 沒有舊 schema：全新建立 ----
        if not new_vals:
            # 真的沒有任何有效字串 → 回傳空表但保留欄位
            return pd.DataFrame({col: pd.Series(dtype="string"), "link_id": pd.Series(dtype="Int64")})

        link_df = pd.DataFrame({col: new_vals})
        link_df["link_id"] = range(1, len(link_df) + 1)
        # 欄位型別統一
        link_df[col] = link_df[col].astype("string")
        link_df["link_id"] = link_df["link_id"].astype("Int64")
        return link_df

    def _merge_existing_data(
            self,
            df: pd.DataFrame,
            path: Path,
            schema_data: Dict,
            update_existing: bool,
            overwrite_rows: bool,
            allow_new_columns: bool,
            allow_remove_columns: bool,
            allow_remove_rows: bool,
            allow_new_rows: bool,
    ) -> pd.DataFrame:
        if not path.exists():
            return df

        old_df = pickleio(path, mode="load")

        # 取得主鍵設定
        pk = schema_data.get("primary_key")

        # ---- 1) 兩邊都先把索引設為主鍵----
        old_df = old_df.set_index(pk, drop=True)
        df = df.set_index(pk, drop=True)

        # ---- 2) 欄位對齊（在索引設好之後再做）----
        if update_existing:
            if allow_new_columns:
                # 只挑 df 中 old_df 沒有的「新欄位」
                new_cols = [c for c in df.columns if c not in old_df.columns]
                if new_cols:
                    # 以「索引=主鍵」為鍵，把 df 的新欄位 merge 到 old_df
                    # left join：保留 old_df 的所有列；新欄位在 df 沒值的列會是 NaN
                    old_df = old_df.merge( df[new_cols], left_index=True, right_index=True, how="left")
            if allow_remove_columns:
                # 僅保留兩邊都有的欄位（注意此時 old_df 已可能多了新欄位）
                keep_cols = [c for c in old_df.columns if c in df.columns]
                old_df = old_df[keep_cols]
            # 欄位順序以舊表為準
            df = df[[c for c in df.columns if c in old_df.columns]]

        # ---- 3) 合併（以索引=主鍵 對齊）----
        # 允許刪除列：移除舊表中不在這次 df 的索引
        if allow_remove_rows:
            old_df = old_df[old_df.index.isin(df.index)]

        if allow_new_rows:
            old_df = pd.concat([old_df, df[~df.index.isin(old_df.index)]])

        if overwrite_rows:
            # 直接就地覆蓋舊表相同索引的值
            old_df.update(df)
        # ---- 4) 把主鍵從索引還原成欄位----
        old_df = old_df.reset_index()
        return old_df

    def load_db(self, decode_links: bool = True) -> pd.DataFrame:
        path = self.base_dir / f"{self.table_name}.pkl"
        if not path.exists():
            raise FileNotFoundError(f"Table '{self.table_name}' not found at {path}")

        df = pickleio(path, mode="load")

        if self.schema:
            self.validate_schema(df)

            if decode_links:
                for col, records in self.schema.get("links", {}).items():
                    link_df = pd.DataFrame(records)
                    mapping = dict(zip(link_df['link_id'], link_df[col]))
                    if col in df.columns:
                        df[col] = df[col].map(mapping)

            schema_cols = list(self.schema.get("dtypes", {}).keys())
            df = df[[col for col in schema_cols if col in df.columns]]

        return df


    def load_raw(self) -> pd.DataFrame:
        """
        直接載入主資料表（<table_name>.pkl），
        不做任何 schema 驗證、不還原 link 欄位。

        用途：
        - 給維運 / schema migration 使用
        - 正常情況請用 load_db()
        """
        path = self.base_dir / f"{self.table_name}.pkl"
        if not path.exists():
            raise FileNotFoundError(f"Table '{self.table_name}' not found at {path}")
        return pickleio(path, mode="load")

    def load_schema(self) -> Optional[Dict]:
        """
        直接讀取 schema 檔（<table_name>_schema.pkl）。

        邏輯：
        - 若 self.schema 已經有值，直接回傳（避免重複 IO）
        - 若檔案存在，就從磁碟讀進來並同步更新 self.schema
        - 若檔案不存在，回傳 None
        """
        if self.schema is not None:
            return self.schema
        if self.schema_path.exists():
            self.schema = pickleio(self.schema_path, mode="load")
            return self.schema
        return None

    def save_schema(self, schema: Dict) -> None:
        """
        顯式覆寫 schema 檔，並同步更新 self.schema。

        用途：
        - 給 migration 或手動維護時使用
        - 正常 write_db() 也會自己呼叫 pickleio 寫 schema
        """
        pickleio(self.schema_path, data=schema, mode="save")
        self.schema = schema

    def migrate_column_dtype(
        self,
        col: str,
        target_dtype: str,
        *,
        coerce: bool = True,
    ) -> None:
        """
        Schema 遷移工具：
        將指定欄位 `col` 轉型成 `target_dtype`，並更新 schema["dtypes"][col]。

        流程：
        1. 用 load_raw() 讀出目前實際存的 DataFrame（不驗 schema）
        2. 用 load_schema() 讀出 schema，若不存在就建一個空的骨架
        3. 呼叫內建的 _coerce_series_to_dtype() 嘗試轉型
        4. 成功：
            - 更新 df[col]
            - 更新 schema["dtypes"][col]
            - 回寫 <table_name>.pkl + <table_name>_schema.pkl
        5. 失敗：
            - 若 coerce=True → raise TypeError（避免靜默壞資料）
            - 若 coerce=False → 直接 return，不做任何更動

        這個方法只做「遷移」，不會更改 primary_key，也不動 links。
        """
        # 1) 讀 raw df & schema（不做驗證）
        df = self.load_raw()
        schema = self.load_schema() or {"dtypes": {}, "links": {}, "primary_key": []}

        # 2) 確認欄位存在
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in table '{self.table_name}'")

        # 3) 嘗試轉型（用已經存在的 _coerce_series_to_dtype）
        converted, ok = self._coerce_series_to_dtype(df[col], target_dtype)

        if not ok:
            if coerce:
                # 嚴格模式：轉型失敗就炸掉，讓你看到問題
                raise TypeError(
                    f"Cannot safely convert column '{col}' to '{target_dtype}' "
                    f"in table '{self.table_name}'"
                )
            else:
                # 寬鬆模式：轉不動就略過
                return

        # 4) 寫回 df + 更新 schema
        df[col] = converted

        schema.setdefault("dtypes", {})
        schema["dtypes"][col] = str(df[col].dtype)

        # 5) 實際回寫檔案
        main_path = self.base_dir / f"{self.table_name}.pkl"
        pickleio(main_path, data=df, mode="save")
        self.save_schema(schema)



    def validate_schema(self, df: pd.DataFrame) -> None:
        if not self.schema:
            raise FileNotFoundError(f"No schema loaded for table '{self.table_name}'")

        pk = self.schema.get("primary_key")
        if isinstance(pk, str):
            # 用單一欄位當主鍵
            if pk not in df.columns:
                raise ValueError(f"Primary key column '{pk}' missing in DataFrame for table '{self.table_name}'")
            if df[pk].isna().any():
                raise ValueError(f"Primary key column '{pk}' contains NaN in table '{self.table_name}'")
            if df.duplicated(subset=[pk]).any():
                raise ValueError(f"Primary key column '{pk}' does not form a unique constraint in table '{self.table_name}'")
        elif isinstance(pk, list):
            if not all(col in df.columns for col in pk):
                raise ValueError(f"Some primary key columns {pk} missing in DataFrame for table '{self.table_name}'")
            if df.duplicated(subset=pk).any():
                raise ValueError(f"Primary key columns {pk} in table '{self.table_name}' do not form a unique constraint")

        for col, expected_type in self.schema.get("dtypes", {}).items():
            if col not in df.columns:
                raise ValueError(f"Missing column '{col}' in table '{self.table_name}'")
            actual_type = str(df[col].dtype)
            if actual_type != expected_type:
                raise TypeError(f"Column '{col}' in table '{self.table_name}' expected type '{expected_type}', got '{actual_type}'")
