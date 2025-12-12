"""
data_store
==========

統一包裝 DBPkl + 歷史版本管理 + 簡易 log 的高階介面。

設計分層：
- DBPkl（在 internal_db.py）：底層 pickle 資料庫引擎。
- DataHistoryManager：負責歷史版本（存在 history_root/db_name 底下）。
- DataStore：給你在專案裡用的高階入口，平常只要碰這一層即可。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd

from StevenTricks.db.internal_db import DBPkl
from StevenTricks.io.file_utils import pickleio, logmaker


# ======================================================================
# 歷史版本管理（原本在 track_utils.py）
# ======================================================================

@dataclass
class HistoryVersion:
    """單一版本資訊（目前暫時沒有對外使用，只是預留型別結構）。"""
    version_id: str
    created_at: datetime
    tag: Optional[str]
    path: Path
    meta: Dict[str, Any]


class DataHistoryManager:
    """
    DataHistoryManager
    -------------------
    專門負責「某一個 db_name 的歷史版本管理」，讓 DataStore 可以很單純地呼叫：

        history = DataHistoryManager(history_root, db_name="funding_amt")
        history.save_version(df, tag="2025-11-30_每日彙總", meta={"rows": len(df)})
        history.list_versions()
        history.load_version(version_id)

    設計原則：
    - 不再處理「log / cache 雙模式」；只做 history 版本管理。
    - 每個版本是一個獨立的 .pkl 檔，檔名 = {version_id}.pkl
    - 版本索引存成一個 CSV：versions.csv，方便人眼檢查。
    """

    def __init__(self, history_root: Path, db_name: str) -> None:
        # 歷史目錄：{history_root}/{db_name}/
        self.history_root = Path(history_root)
        self.db_name = db_name
        self.dir = self.history_root / db_name
        self.dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.dir / "versions.csv"

    # ---------- 內部小工具 ----------

    def _now_str(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _load_index_df(self) -> pd.DataFrame:
        if not self.index_path.exists():
            return pd.DataFrame(
                columns=["version_id", "created_at", "tag", "path", "meta_json"]
            )
        return pd.read_csv(self.index_path)

    def _save_index_df(self, df: pd.DataFrame) -> None:
        df.to_csv(self.index_path, index=False)

    # ---------- 對外 API ----------

    def save_version(
        self,
        df: pd.DataFrame,
        tag: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        儲存一個新的歷史版本，回傳 version_id。

        Parameters
        ----------
        df : pd.DataFrame
            要儲存的資料。
        tag : Optional[str]
            自訂標籤，通常用來記錄日期或情境說明（例如 '2025-11-30_daily'）。
        meta : Optional[dict]
            其他想記錄的資訊，例如 rows, note 等，會被序列化成 JSON 字串。
        """
        meta = meta or {}
        ts = self._now_str()

        # 避免同一秒多次呼叫撞名，簡單加流水號
        base_id = ts if tag is None else f"{ts}_{tag}"
        version_id = base_id
        i = 1
        while (self.dir / f"{version_id}.pkl").exists():
            version_id = f"{base_id}_{i}"
            i += 1

        path = self.dir / f"{version_id}.pkl"
        pickleio(path, df, mode="save")

        idx_df = self._load_index_df()
        new_row = {
            "version_id": version_id,
            "created_at": ts,
            "tag": tag or "",
            "path": str(path),
            "meta_json": json.dumps(meta, ensure_ascii=False),
        }
        idx_df = pd.concat([idx_df, pd.DataFrame([new_row])], ignore_index=True)
        self._save_index_df(idx_df)
        return version_id

    def list_versions(self) -> pd.DataFrame:
        """
        回傳歷史版本一覽表（依 created_at 由新到舊排序）。
        """
        df = self._load_index_df()
        if df.empty:
            return df
        return df.sort_values("created_at", ascending=False).reset_index(drop=True)

    def load_version(self, version_id: str) -> pd.DataFrame:
        """
        依 version_id 載入對應的 DataFrame。
        """
        path = self.dir / f"{version_id}.pkl"
        if not path.exists():
            raise FileNotFoundError(f"找不到 version_id={version_id!r} 對應的檔案：{path}")
        return pickleio(path, mode="load")


# ======================================================================
# 高階倉庫介面：DataStore
# ======================================================================

class DataStore:
    """
    高階資料倉庫介面：
    - 實際資料儲存交給 DBPkl
    - 歷史版本管理交給 DataHistoryManager
    - 簡單操作紀錄交給 logmaker（可視需要擴充）

    典型用法：

        from pathlib import Path
        from StevenTricks.db.data_store import DataStore

        store = DataStore(
            db_dir=Path("/some/path/to/db"),
            history_dir=Path("/some/path/to/history"),  # 可選
            log_dir=Path("/some/path/to/logs"),         # 可選
            db_name="funding_amt",
        )

        store.save(df, tag="2025-11-30_每日彙總", meta={"rows": len(df)})

        latest = store.load_latest()
        history_df = store.list_history()
    """

    def __init__(
        self,
        db_dir: Path,
        history_dir: Optional[Path] = None,
        log_dir: Optional[Path] = None,
        db_name: str = "default",
    ) -> None:
        self.db_dir = Path(db_dir)
        self.history_dir = Path(history_dir) if history_dir is not None else None
        self.log_dir = Path(log_dir) if log_dir is not None else None
        self.db_name = db_name

        # ---- 實際 DB 物件：對應一個 table ----
        # DBPkl 的參數是 (db_name=資料夾路徑, table_name=表名)
        self.db = DBPkl(
            db_name=str(self.db_dir),
            table_name=self.db_name,
        )

        # ---- 歷史版本管理（如果有指定 history_dir）----
        if self.history_dir is not None:
            self.history_mgr: Optional[DataHistoryManager] = DataHistoryManager(
                history_root=self.history_dir,
                db_name=self.db_name,
            )
        else:
            self.history_mgr = None

    # ---------- 寫入主表 + 歷史 + log ----------

    def save(
        self,
        df: pd.DataFrame,
        tag: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        儲存 DataFrame 到 DBPkl，並視需要記錄歷史與簡單 log。

        設計取向：
        - 這裡走「簡單路線」，不開放所有 write_db 參數，
          讓 DataStore 當成「高階、好用版本」。
        - 如果要精細控制 primary key / convert_mode / partition 等，
          建議直接用 DBPkl。
        """
        if df is None or df.empty:
            # 安全起見，不寫空表進 DB；若你之後想改行為，再來調整這邊。
            return

        # 1) 主體資料儲存（單一 table，不切 partition）
        #    convert_mode 選擇 "upcast"：盡量把舊新欄位自動提升型別，減少寫入失敗。
        self.db.write_db(
            df=df,
            convert_mode="upcast",
            primary_key=None,
            update_existing=True,
            overwrite_rows=True,
            allow_new_columns=True,
            allow_remove_columns=False,
            allow_remove_rows=False,
            allow_new_rows=True,
            save_schema=True,
        )

        # 2) 歷史版本紀錄
        if self.history_mgr is not None:
            self.history_mgr.save_version(df, tag=tag, meta=meta)

        # 3) 簡單 log（目前只是一個 placeholder，之後若需要可擴充結構）
        if self.log_dir is not None:
            # 這裡沿用原本 logmaker 介面：write_dt / data_dt 都先給 db_name
            logmaker(write_dt=self.db_name, data_dt=self.db_name, log=None)

    # ---------- 讀取目前主表 ----------

    def load_latest(self) -> pd.DataFrame:
        """
        載入目前主表（使用 DBPkl.load_db）。

        注意：
        - 如果表不存在，DBPkl.load_db 會拋 FileNotFoundError。
        """
        return self.db.load_db()

    # ---------- 歷史查詢 ----------

    def list_history(self) -> Optional[pd.DataFrame]:
        """
        列出歷史版本一覽表（若有啟用 history_mgr）。
        """
        if self.history_mgr is None:
            return None
        return self.history_mgr.list_versions()

    def load_version(self, version_id: str) -> pd.DataFrame:
        """
        載入特定歷史版本。
        """
        if self.history_mgr is None:
            raise RuntimeError("未啟用 DataHistoryManager（history_dir 未設定）")
        return self.history_mgr.load_version(version_id)
