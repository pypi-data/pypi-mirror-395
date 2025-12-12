StevenTricks/
  ARCHITECTURE.md
  setup.py
  prepare_release.py
  version_task.py
  StevenTricks/
    __init__.py

    core/        # 型別轉換、DataFrame 工具
      convert_utils.py
      df_utils.py

    io/          # 檔案 / 網路 / staging / log
      file_utils.py
      net_utils.py
      staging.py

    db/          # pickle-based DB + 歷史版本
      internal_db.py
      data_store.py
      track_utils.py

    analysis/    # 分析工具（目前以 driver tree、cluster 為主）
      driver_tree.py
      cluster_utils.py

    dev/         # 開發輔助工具（命名規則、code generator 等）
      code_utils.py
