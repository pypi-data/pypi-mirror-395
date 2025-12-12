# ========================================================================================
#  Copyright (C) 2025 CryptoLab Inc. All rights reserved.
#
#  This software is proprietary and confidential.
#  Unauthorized use, modification, reproduction, or redistribution is strictly prohibited.
#
#  Commercial use is permitted only under a separate, signed agreement with CryptoLab Inc.
#
#  For licensing inquiries or permission requests, please contact: pypi@cryptolab.co.kr
# ========================================================================================

import pickle
from pathlib import Path
from typing import List, Tuple


def _load_virtual_cluster_from_pkl(path: str) -> Tuple[List[Tuple[int, int]], int, List[int]]:
    """
    Load virtual cluster tree structure from a pickle file path.
    """
    tree_path = Path(path)
    if not tree_path.exists():
        raise FileNotFoundError(f"Tree description file not found: {tree_path}")

    with open(tree_path, "rb") as f:
        tree_meta = pickle.load(f)

    node_parents = tree_meta.get("node_parents")
    if not node_parents:
        raise ValueError("tree_description must contain 'node_parents'.")

    leaf_to_centroid_idx = tree_meta.get("leaf_to_centroid_idx")
    if leaf_to_centroid_idx is None:
        raise ValueError("tree_description must contain 'leaf_to_centroid_idx'.")

    shifted_nodes = [(1, 0)]

    total_nodes = 0
    for child, parent in sorted(node_parents.items()):
        c = int(child)
        p = int(parent)
        shifted_nodes.append((c + 1, 1 if p == 0 else p + 1))
        if c + 1 > total_nodes:
            total_nodes = c + 1

    max_idx = max(int(idx) for idx in leaf_to_centroid_idx.values())
    centroid_idx_to_leaf_list = [-1] * (max_idx + 1)

    for leaf, idx in leaf_to_centroid_idx.items():
        c_idx = int(idx)
        leaf_id = int(leaf) + 1
        centroid_idx_to_leaf_list[c_idx] = leaf_id

    return shifted_nodes, total_nodes, centroid_idx_to_leaf_list
