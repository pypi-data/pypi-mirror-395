# steventricks/staging.py
import shutil
import uuid
from pathlib import Path
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


@contextmanager
def staging_path(target_path, enable: bool, staging_root):
    """
    DB staging 通用工具：
    - target_path: 原始 DB 路徑（可能是檔案或資料夾）
    - enable: 是否啟用 staging
    - staging_root: 本機暫存根目錄（例如 ~/Library/Caches/arsenal_db_staging）

    yield 出來的是「真正要給 DBPkl / ORMDB 用的路徑」。
    """
    target_path = Path(target_path).expanduser()
    staging_root = Path(staging_root).expanduser()

    # 沒開 staging 就直接用原路徑
    if not enable:
        logger.debug("[staging] disabled, use original path: %s", target_path)
        yield target_path
        return

    # ---- 這裡開始是新的實作 ----
    staging_root.mkdir(parents=True, exist_ok=True)

    # 不再用亂數流水號，而是固定一個名稱：
    # 例如 target_path = ".../cleaned" → tmp_dir = "<staging_root>/staging_cleaned"
    tmp_dir = staging_root / f"staging_{target_path.name}"

    # 如果上一次程式異常結束，tmp_dir 可能還在；先整個清掉
    if tmp_dir.exists():
        try:
            shutil.rmtree(tmp_dir)
            logger.info("[staging] remove previous tmp_dir before reuse: %s", tmp_dir)
        except Exception as e:
            logger.warning("[staging] failed to cleanup previous tmp_dir %s: %s", tmp_dir, e)

    tmp_dir.mkdir(parents=True, exist_ok=False)

    # 決定本機實際使用的路徑
    local_path = tmp_dir / target_path.name


    # 1) 先把原始 DB 複製到本機（如果存在）
    if target_path.exists():
        if target_path.is_dir():
            logger.info("[staging] copy dir -> local: %s -> %s", target_path, local_path)
            shutil.copytree(target_path, local_path)
        else:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info("[staging] copy file -> local: %s -> %s", target_path, local_path)
            shutil.copy2(target_path, local_path)
    else:
        # 原始 DB 不存在：表示第一次建立，就讓本機這份當作初始 DB
        if local_path.suffix:
            # 看起來像檔案路徑，例如 xxx.db
            local_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            # 看起來像資料夾路徑
            local_path.mkdir(parents=True, exist_ok=True)
        logger.info("[staging] target not exists, using new local path: %s", local_path)

    success = False
    try:
        # 2) 把 local_path 給外層使用（DBPkl / ORM）
        yield local_path
        success = True
    finally:
        try:
            if success:
                # 3) 完成且無錯誤：覆蓋回原始路徑
                if local_path.exists():
                    if local_path.is_dir():
                        logger.info("[staging] sync back dir: %s -> %s", local_path, target_path)
                        if target_path.exists():
                            shutil.rmtree(target_path)
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(local_path, target_path)
                    else:
                        logger.info("[staging] sync back file: %s -> %s", local_path, target_path)
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(local_path, target_path)
            else:
                logger.warning("[staging] aborted, keep original target: %s", target_path)
        finally:
            # 4) 清掉暫存資料夾
            try:
                if tmp_dir.exists():
                    shutil.rmtree(tmp_dir)
                    logger.debug("[staging] cleaned tmp_dir: %s", tmp_dir)
            except Exception as e:
                logger.warning("[staging] failed to cleanup tmp_dir %s: %s", tmp_dir, e)

# from StevenTricks.io.file_utils import PathWalk_df, merge_excel_sheets_from_folder
#
# files_df = PathWalk_df("/some/path", pattern="*.xlsx")
#
# merged = merge_excel_sheets_from_folder(
#     folder="/some/path",
#     sheet_name="Sheet1"
# )
# from pathlib import Path
# from StevenTricks.io.staging import staging_path
#
# base = Path("/Users/stevenhsu/Data")
# today_staging = staging_path(base, "twse", date_folder=True)
