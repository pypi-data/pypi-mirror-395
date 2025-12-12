# -*- coding: utf-8 -*-
"""
Driver Tree 工具（Funding_Amt 變動拆解版）
======================================

用途：
    - 解釋「兩個月份（base vs comp）之間 Funding_Amt 的變動」，是由哪些維度
      （產品、地區、結構、客戶、投資人、專案…）所驅動。
    - 自動在給定的一組欄位中，找出「最能解釋 Funding_Amt 變動」的維度，形成
      一棵 driver tree。
    - 每一層都會產出樞紐表（pivot）與中文說明文字，方便直接寫報告。

方法說明（給未來的自己看）：
------------------------

1. 分析目標：
    - 解釋 base_period → comp_period 之間 Funding_Amt 的增減，
      拆成不同維度（產品、地區、結構、客戶、投資人、專案…）的貢獻。

2. 核心邏輯：
    - 在某一層，選一個維度（例如 Product_Flag_new），
      將 Funding_Amt 依該維度分組，計算：
        amt_base, amt_comp, delta_amt
      並用「各群組 delta_amt 的絕對值貢獻」作為 score，
      找出最能集中解釋 Funding_Amt 變動的維度。
    - 重複上述步驟，形成一棵 driver tree，每一層是一個拆解角度。

3. 與傳統 ANOVA 的關係：
    - 沒做正式的 F 檢定 / p-value。
    - 用的是「between-group 變動貢獻」的概念，屬於『類 ANOVA 的 driver tree』，
      著重在解釋力與報告好寫，不是嚴格統計檢定。

4. 為何仍叫 driver_tree：
    - 專注在「找出 Funding_Amt 變動的主要 driver」，
      用樹狀結構分層呈現，方便跟業務 / 管理層溝通。
"""

from __future__ import annotations
from StevenTricks.analysis.driver_tree import run_driver_tree_change
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd


# ------------------------------------------------------------
# 一、欄位角色設定（依你的業務解釋）
# ------------------------------------------------------------

# 欄位角色定義
DIM_ROLE: Dict[str, str] = {
    # 時間（只拿來切 base / comp，不當作 split 維度）
    "Funding_Date_yymm": "time",

    # 產品
    "Product_Flag_new": "product",

    # 地區等級：a+ ~ d，左好右壞
    "Property_Location_Flag": "region",

    # 結構：借款期限 / 寬限期 / OLTV 級距
    "Tenor_Flag": "structure",          # 借款期限
    "Grace_Length_Flag": "structure",   # 寬限期
    "OLTV_Flag": "structure",           # OLTV 級距

    # 客戶：由好到壞分級
    "Cust_Flag": "customer",

    # 投資人 / 管制：
    # - Investor_Flag：受到台灣央行管制的客戶（若文字有 GA，是行內管制）
    # - cb_Investor_flag：屬於台灣中央銀行管制
    # - Public_Flag2024：透過中國信託特殊優惠專案進件
    "Investor_Flag": "investor",
    "cb_Investor_flag": "investor",
    "Public_Flag2024": "investor",

    # 帳戶 / 利率型態：產品編號前四碼 + 後四碼，通常一起看
    "Acct_Type_Code": "account",        # 產品編號前四碼
    "Int_Category_Code": "account",     # 產品編號後四碼

    # 專案 / 案件類型：
    # - Batch_Flag：是否為整批案件
    # - special_flag：產品類型的一種分類
    "Batch_Flag": "project",
    "special_flag": "project",
}

# 角色出場順序：誰優先被拿來做 split 維度
ROLE_ORDER: List[str] = [
    "product",    # 先看產品
    "region",     # 再看地區好壞
    "structure",  # 再看期限 / 寬限期 / OLTV
    "customer",   # 再看客戶等級
    "investor",   # 再看投資人 / 管制 / 專案優惠
    "account",    # 帳戶 / 利率型態
    "project",    # 最後才看 Batch / special 類
]


# ------------------------------------------------------------
# 二、樹節點資料結構
# ------------------------------------------------------------

@dataclass
class DriverTreeNode:
    """Driver Tree 的節點結構。"""

    node_id: int
    depth: int

    # 此節點所代表的條件（例如 {'Product_Flag_new': '房貸A', 'Cust_Flag': '好客戶'}）
    path: Dict[str, Any]

    # 此節點下 base / comp 的 Funding_Amt 總額與變動
    amt_base: float
    amt_comp: float
    delta_amt: float
    delta_share: float  # 相對於整棵樹根節點的變動占比（global_delta 的比例）

    # 此節點用來 split 的欄位（若是葉節點則為 None）
    split_dim: Optional[str] = None

    # 這一層的樞紐表（依 split_dim 分組的 base / comp / delta）
    pivot: Optional[pd.DataFrame] = None

    # 中文說明文字（節點層級摘要）
    summary_zh: Optional[str] = None

    # 子節點
    children: List["DriverTreeNode"] = field(default_factory=list)


# ------------------------------------------------------------
# 三、Driver Tree 主體
# ------------------------------------------------------------

class DriverTree:
    """
    Driver Tree 主類別：用來分析「Funding_Amt 兩期變動」的結構拆解。

    使用方式：

        tree = DriverTree(max_depth=3, min_node_share=0.05, top_k=5)

        tree.fit(
            df,
            base_period="202509",
            comp_period="202510",
            dims=[
                "Product_Flag_new",
                "Property_Location_Flag",
                "Tenor_Flag",
                "Grace_Length_Flag",
                "OLTV_Flag",
                "Cust_Flag",
                "Investor_Flag",
                "Acct_Type_Code",
                "Int_Category_Code",
                "Batch_Flag",
                "special_flag",
                "Public_Flag2024",
                "cb_Investor_flag",
            ],
            target_col="Funding_Amt",
            time_col="Funding_Date_yymm",
        )

        result = tree.to_result()

    result 包含：
        - 'root': 根節點（DriverTreeNode）
        - 'nodes_df': 節點摘要 DataFrame
        - 'pivots': { node_id: pivot_df }
    """

    def __init__(
        self,
        max_depth: int = 3,
        min_node_share: float = 0.05,
        top_k: int = 5,
    ) -> None:
        """
        max_depth:
            樹的最大深度（root 為 depth=0）

        min_node_share:
            若節點的 delta_share（相對根節點）太小，就不再往下拆；
            例如 0.05 表示貢獻度 < 5% 的節點不再繼續分支。

        top_k:
            每次 split 只保留貢獻度最高的前 k 個類別，其餘合併為「其他」。
        """
        self.max_depth = max_depth
        self.min_node_share = min_node_share
        self.top_k = top_k

        self.root: Optional[DriverTreeNode] = None
        self._nodes: List[DriverTreeNode] = []
        self._next_node_id: int = 1

        # 在 fit 時設定
        self.target_col: str = "Funding_Amt"
        self.time_col: str = "Funding_Date_yymm"
        self.base_period: Any = None
        self.comp_period: Any = None
        self.global_delta_amt: float = 0.0

    # --------------------------
    # 公開方法
    # --------------------------

    def fit(
        self,
        df: pd.DataFrame,
        base_period: Any,
        comp_period: Any,
        dims: Optional[List[str]] = None,
        target_col: str = "Funding_Amt",
        time_col: str = "Funding_Date_yymm",
    ) -> "DriverTree":
        """
        建立 Driver Tree，專門解釋 base_period → comp_period 的 Funding_Amt 變動。

        df:
            必須至少包含 time_col、target_col，以及 dims 中的欄位。

        base_period, comp_period:
            Funding_Date_yymm 的兩個值，例如 "202509", "202510"。

        dims:
            想要納入分析的欄位清單，例如：
                ["Product_Flag_new", "Property_Location_Flag", "Tenor_Flag", ...]
            若為 None 則自動使用 DIM_ROLE 裡非 time 的所有欄位。

        target_col:
            預設 "Funding_Amt"。

        time_col:
            預設 "Funding_Date_yymm"。
        """
        self.target_col = target_col
        self.time_col = time_col
        self.base_period = base_period
        self.comp_period = comp_period

        # 若未指定 dims，就用 DIM_ROLE 中所有非 time 的欄位
        if dims is None:
            dims = [
                col for col, role in DIM_ROLE.items()
                if role != "time"
            ]

        # 僅保留 df 中存在的欄位
        dims = [d for d in dims if d in df.columns]

        # 根節點的 base / comp / delta
        df_base = df[df[time_col] == base_period]
        df_comp = df[df[time_col] == comp_period]

        amt_base = float(df_base[target_col].sum())
        amt_comp = float(df_comp[target_col].sum())
        delta_amt = amt_comp - amt_base

        # 避免 global_delta_amt 為 0
        self.global_delta_amt = delta_amt if delta_amt != 0 else 1e-9

        root = DriverTreeNode(
            node_id=self._alloc_node_id(),
            depth=0,
            path={},
            amt_base=amt_base,
            amt_comp=amt_comp,
            delta_amt=delta_amt,
            delta_share=1.0,
            split_dim=None,
            pivot=None,
            summary_zh=None,
            children=[],
        )
        self.root = root
        self._nodes = [root]

        # 從根節點開始建樹
        self._build_node(
            df=df,
            parent_node=root,
            available_dims=dims,
        )

        # 填入每個節點的中文摘要
        self._populate_summaries()

        return self

    def to_result(self) -> Dict[str, Any]:
        """
        將樹結構轉成結果格式，包含：
            - root: 根節點
            - nodes_df: 節點摘要 DataFrame
            - pivots: { node_id: pivot_df }
        """
        if self.root is None:
            raise RuntimeError("請先呼叫 fit() 再取結果。")

        nodes_records = []
        pivots: Dict[int, pd.DataFrame] = {}

        for node in self._nodes:
            rec = {
                "node_id": node.node_id,
                "depth": node.depth,
                "path": node.path,
                "amt_base": node.amt_base,
                "amt_comp": node.amt_comp,
                "delta_amt": node.delta_amt,
                "delta_share": node.delta_share,
                "split_dim": node.split_dim,
                "summary_zh": node.summary_zh,
            }
            nodes_records.append(rec)

            if node.pivot is not None:
                pivots[node.node_id] = node.pivot.copy()

        nodes_df = pd.DataFrame(nodes_records)
        return {
            "root": self.root,
            "nodes_df": nodes_df,
            "pivots": pivots,
        }

    # --------------------------
    # 內部：建樹邏輯
    # --------------------------

    def _alloc_node_id(self) -> int:
        nid = self._next_node_id
        self._next_node_id += 1
        return nid

    def _build_node(
        self,
        df: pd.DataFrame,
        parent_node: DriverTreeNode,
        available_dims: List[str],
    ) -> None:
        """
        遞迴建立子節點。
        """
        # 停止條件 1：深度到達上限
        if parent_node.depth >= self.max_depth:
            return

        # 停止條件 2：此節點的變動占比太小
        if abs(parent_node.delta_share) < self.min_node_share:
            return

        # 篩出符合當前 path 條件的資料
        df_sub = self._filter_by_path(df, parent_node.path)

        # 若子資料量太少，直接停止
        if df_sub.empty:
            return

        # 在剩餘可用欄位中，尋找「最能解釋此節點 delta」的 split_dim
        best_dim, best_pivot, best_score = self._find_best_split_dim(
            df_sub, available_dims
        )

        if best_dim is None or best_pivot is None:
            return

        # 設定此節點的 split 資訊
        parent_node.split_dim = best_dim
        parent_node.pivot = best_pivot

        # 按 delta_amt 絕對值排序，取前 top_k，再把剩下的合併為「其他」
        pivot = best_pivot.copy()
        pivot = pivot.sort_values("delta_amt", ascending=False)

        top = pivot.head(self.top_k).copy()
        others = pivot.iloc[self.top_k:].copy()

        # 前 top_k 類別
        for cat, row in top.iterrows():
            amt_b = float(row["amt_base"])
            amt_c = float(row["amt_comp"])
            delta = float(row["delta_amt"])
            share = float(delta / self.global_delta_amt)

            child_node = DriverTreeNode(
                node_id=self._alloc_node_id(),
                depth=parent_node.depth + 1,
                path={**parent_node.path, best_dim: cat},
                amt_base=amt_b,
                amt_comp=amt_c,
                delta_amt=delta,
                delta_share=share,
                split_dim=None,
                pivot=None,
                summary_zh=None,
                children=[],
            )
            parent_node.children.append(child_node)
            self._nodes.append(child_node)

            # 下一層：同一條路徑上不再重複使用 best_dim
            next_dims = [d for d in available_dims if d != best_dim]

            self._build_node(
                df=df,
                parent_node=child_node,
                available_dims=next_dims,
            )

        # 把「其他」合併為一個 child（若有）
        if not others.empty:
            amt_b = float(others["amt_base"].sum())
            amt_c = float(others["amt_comp"].sum())
            delta = float(others["delta_amt"].sum())
            share = float(delta / self.global_delta_amt)

            child_node = DriverTreeNode(
                node_id=self._alloc_node_id(),
                depth=parent_node.depth + 1,
                path={**parent_node.path, best_dim: "其他"},
                amt_base=amt_b,
                amt_comp=amt_c,
                delta_amt=delta,
                delta_share=share,
                split_dim=None,
                pivot=None,
                summary_zh=None,
                children=[],
            )
            parent_node.children.append(child_node)
            self._nodes.append(child_node)

            next_dims = [d for d in available_dims if d != best_dim]

            self._build_node(
                df=df,
                parent_node=child_node,
                available_dims=next_dims,
            )

    def _filter_by_path(self, df: pd.DataFrame, path: Dict[str, Any]) -> pd.DataFrame:
        """依照 path（多欄位條件）過濾 DataFrame。"""
        if not path:
            return df
        mask = pd.Series(True, index=df.index)
        for col, val in path.items():
            if val == "其他":
                # 「其他」在建樹時是用 pivot 的殘餘合併，
                # 這裡為簡化，不再精確還原「其他」成員，直接視為不加條件。
                continue
            mask &= (df[col] == val)
        return df[mask]

    def _find_best_split_dim(
        self,
        df_sub: pd.DataFrame,
        candidate_dims: List[str],
    ) -> Tuple[Optional[str], Optional[pd.DataFrame], float]:
        """
        在 candidate_dims 中，依「角色順序」尋找解釋 Funding_Amt 變動最好的欄位。

        流程：
            1. 先把 candidate_dims 依角色（product / region / ...）分類。
            2. 按 ROLE_ORDER 順序：
                - 只在該角色底下的欄位中評分，挑出分數最高者。
                - 一旦有某個角色產生有效欄位，即採用，不再往後找角色。
        """
        best_dim = None
        best_pivot = None
        best_score = -np.inf

        # 先把 candidate_dims 按角色分組
        role_to_dims: Dict[str, List[str]] = {}
        for dim in candidate_dims:
            role = DIM_ROLE.get(dim)
            if role is None or role == "time":
                continue
            role_to_dims.setdefault(role, []).append(dim)

        for role in ROLE_ORDER:
            dims_in_role = role_to_dims.get(role, [])
            if not dims_in_role:
                continue

            role_best_dim = None
            role_best_pivot = None
            role_best_score = -np.inf

            for dim in dims_in_role:
                if dim not in df_sub.columns:
                    continue

                pivot = self._pivot_change_by_dim(df_sub, dim)
                if pivot is None or pivot.empty:
                    continue

                # 以「此節點的 delta」做正規化
                node_delta = float(pivot["delta_amt"].sum())
                denom = abs(node_delta) if node_delta != 0 else 1e-9

                tmp = pivot.copy()
                tmp["abs_delta"] = tmp["delta_amt"].abs()
                tmp = tmp.sort_values("abs_delta", ascending=False)
                top = tmp.head(self.top_k)

                score = float(top["abs_delta"].sum() / denom)

                if score > role_best_score:
                    role_best_score = score
                    role_best_dim = dim
                    role_best_pivot = pivot

            # 這個角色若有找到候選，就採用，不再往後找
            if role_best_dim is not None:
                best_dim = role_best_dim
                best_pivot = role_best_pivot
                best_score = role_best_score
                break

        return best_dim, best_pivot, best_score

    def _pivot_change_by_dim(
        self,
        df_sub: pd.DataFrame,
        dim: str,
    ) -> Optional[pd.DataFrame]:
        """
        針對一個欄位 dim，計算此節點底下 base / comp / delta 樞紐表。

        回傳欄位：
            index: dim 的各個類別
            columns:
                - amt_base
                - amt_comp
                - delta_amt
                - delta_share_in_node（相對於此節點 delta 的占比）
        """
        mask_base = (df_sub[self.time_col] == self.base_period)
        mask_comp = (df_sub[self.time_col] == self.comp_period)

        df_b = df_sub[mask_base]
        df_c = df_sub[mask_comp]

        if df_b.empty and df_c.empty:
            return None

        g_b = df_b.groupby(dim)[self.target_col].sum()
        g_c = df_c.groupby(dim)[self.target_col].sum()

        pivot = pd.DataFrame({
            "amt_base": g_b,
            "amt_comp": g_c,
        }).fillna(0.0)

        pivot["delta_amt"] = pivot["amt_comp"] - pivot["amt_base"]

        node_delta = float(pivot["delta_amt"].sum())
        denom = abs(node_delta) if node_delta != 0 else 1e-9
        pivot["delta_share_in_node"] = pivot["delta_amt"] / denom

        return pivot

    # --------------------------
    # 內部：中文摘要產生
    # --------------------------

    def _populate_summaries(self) -> None:
        """為每一個節點產生中文說明文字。"""
        for node in self._nodes:
            node.summary_zh = self._build_node_summary(node)

    def _build_node_summary(self, node: DriverTreeNode) -> str:
        """依節點資訊產出中文摘要。"""
        path_str = self._format_path(node.path)
        amt_b = node.amt_base
        amt_c = node.amt_comp
        delta = node.delta_amt
        share = node.delta_share * 100

        direction = "增加" if delta >= 0 else "減少"
        delta_abs = abs(delta)

        base_line = (
            f"在條件 {path_str} 下，"
            f"從基準月（{self.base_period}）到比較月（{self.comp_period}），"
            f"Funding_Amt 由 {amt_b:,.0f} 變為 {amt_c:,.0f}，"
            f"{direction} {delta_abs:,.0f}，"
            f"約占整體變動的 {share:.1f}%。"
        )

        if node.split_dim is None or node.pivot is None:
            return base_line

        # 再補一句「本層主要由哪幾個分類貢獻」
        pivot = node.pivot.copy()
        pivot = pivot.sort_values("delta_amt", ascending=False)

        top = pivot.head(3)
        parts = []
        for idx, row in top.iterrows():
            d = float(row["delta_amt"])
            if d == 0:
                continue
            dir2 = "增加" if d >= 0 else "減少"
            d_abs = abs(d)
            share2 = float(d / self.global_delta_amt * 100)
            parts.append(
                f"{node.split_dim} = {idx}：{dir2} {d_abs:,.0f}（占整體約 {share2:.1f}%）"
            )

        if not parts:
            return base_line

        detail_line = " 主要差異來自：" + "；".join(parts) + "。"
        return base_line + detail_line

    def _format_path(self, path: Dict[str, Any]) -> str:
        """將 path dict 轉成容易閱讀的中文條件句。"""
        if not path:
            return "【全體】"
        items = []
        for k, v in path.items():
            if v == "其他":
                items.append(f"{k} = 其他")
            else:
                items.append(f"{k} = {v}")
        return "、".join(items)


# ------------------------------------------------------------
# 四、外部方便呼叫的包裝函式
# ------------------------------------------------------------

def run_driver_tree_change(
    df: pd.DataFrame,
    base_period: Any,
    comp_period: Any,
    dims: Optional[List[str]] = None,
    target_col: str = "Funding_Amt",
    time_col: str = "Funding_Date_yymm",
    max_depth: int = 3,
    min_node_share: float = 0.05,
    top_k: int = 5,
) -> Dict[str, Any]:
    """
    方便呼叫的封裝函式。

    回傳：
        {
            "root": DriverTreeNode,
            "nodes_df": DataFrame（節點摘要，每列一個節點）,
            "pivots": { node_id: pivot_df, ... }
        }

    典型用法：

        from driver_tree import run_driver_tree_change
    """
        result = run_driver_tree_change(
            df=df,
            base_period="202509",
            comp_period="202510",
            result=run_driver_tree_change(
                df=df,
                base_period="2025-01",
                comp_period="2025-06",
                dims=["Product", "Region", "Channel", "Investor_Flag"],
                target_col="Funding_Amt",
                time_col="Funding_Date_yymm",
            )

    nodes_df = result["nodes_df"]
    pivots = result["pivots"]

    你想看「根節點按產品拆解」的樞紐表，就看：
        pivots[result["root"].node_id]
    """
    tree = DriverTree(
        max_depth=max_depth,
        min_node_share=min_node_share,
        top_k=top_k,
    )
    tree.fit(
        df=df,
        base_period=base_period,
        comp_period=comp_period,
        dims=dims,
        target_col=target_col,
        time_col=time_col,
    )
    return tree.to_result()
