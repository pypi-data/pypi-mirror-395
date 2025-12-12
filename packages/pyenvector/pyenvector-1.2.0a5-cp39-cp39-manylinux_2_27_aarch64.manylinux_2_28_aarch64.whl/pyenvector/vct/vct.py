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

"""
APIs for Virtual Centroids Tree.
Programmatic APIs for preparing and merging Virtual Centroid Tree payloads.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

import faiss
import numpy as np

DEFAULT_MERGE_THRESHOLD = 4096
ProgressCallback = Optional[Callable[[str, str], None]]
NodeVectors = Dict[int, List[int]]


@dataclass(frozen=True)
class PreparedVCT:
    """Container that carries the prepared payload plus tree metadata."""

    payload: dict
    counts: np.ndarray
    leaf_start: int
    total_nodes: int


@dataclass(frozen=True)
class PreprocessedVCT:
    """Result bundle after merging prepared VCT nodes."""

    payload: dict
    merge_count: int
    node_vectors: NodeVectors
    total_nodes: int
    threshold: int


def _emit_progress(callback: ProgressCallback, label: str, message: str) -> None:
    if callback is not None:
        callback(label, message)


def _normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    normalized = np.array(vectors, dtype=np.float32, copy=True)
    norms = np.linalg.norm(normalized, axis=1, keepdims=True)
    if np.any(norms == 0.0):
        raise ValueError("Vectors contain zero-norm entries; normalization impossible.")
    normalized /= norms
    return normalized


def assign_vectors_to_centroids(vectors: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    if vectors.shape[1] != centroids.shape[1]:
        raise ValueError(f"Vector dimension {vectors.shape[1]} does not match centroid dimension {centroids.shape[1]}.")

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(np.ascontiguousarray(centroids, dtype=np.float32))
    _, labels = index.search(np.ascontiguousarray(vectors, dtype=np.float32), 1)
    return labels.astype(np.int32).ravel()


def _next_power_of_two(value: int) -> int:
    if value < 1:
        raise ValueError("At least one centroid is required to build the tree.")
    return 1 << (value - 1).bit_length()


def _compute_active_node_mask(num_clusters: int, leaf_slots: int) -> np.ndarray:
    total_nodes = leaf_slots * 2 - 1
    mask = np.zeros(total_nodes + 1, dtype=bool)
    leaf_start = leaf_slots
    for offset in range(num_clusters):
        node_id = leaf_start + offset
        while node_id >= 1 and not mask[node_id]:
            mask[node_id] = True
            node_id //= 2
    return mask


def compute_node_counts(cluster_ids: np.ndarray, num_clusters: int, leaf_slots: int) -> Tuple[np.ndarray, int, int]:
    leaf_start = leaf_slots
    total_nodes = leaf_slots * 2 - 1
    counts = np.zeros(total_nodes + 1, dtype=np.int64)

    cluster_counts = np.bincount(cluster_ids, minlength=num_clusters)
    for cluster_id, count in enumerate(cluster_counts):
        node_id = leaf_start + cluster_id
        counts[node_id] = int(count)

    for node_id in range(total_nodes, 1, -1):
        parent_id = node_id // 2
        counts[parent_id] += counts[node_id]

    return counts, leaf_start, total_nodes


def _build_cluster_entries(cluster_ids: np.ndarray, leaf_start: int, num_clusters: int) -> list[dict]:
    clusters = []
    for cluster_id in range(num_clusters):
        vector_ids = np.where(cluster_ids == cluster_id)[0].tolist()
        node_id = leaf_start + cluster_id
        clusters.append(
            {
                "id": cluster_id,
                "node_id": node_id,
                "vector_ids": vector_ids,
            }
        )
    return clusters


def _build_nodes_metadata(total_nodes: int, active_mask: Optional[np.ndarray] = None) -> list[dict]:
    entries = []
    for node_id in range(1, total_nodes + 1):
        if active_mask is not None and not active_mask[node_id]:
            continue
        entries.append(
            {
                "id": int(node_id),
                "parent": int(node_id // 2 if node_id > 1 else 0),
            }
        )
    return entries


def _prepare_payload(
    centroids: np.ndarray,
    vectors: np.ndarray,
    *,
    normalize_inputs: bool = True,
    progress_cb: ProgressCallback = None,
) -> PreparedVCT:
    centroids_arr = np.asarray(centroids, dtype=np.float32)
    vectors_arr = np.asarray(vectors, dtype=np.float32)

    if centroids_arr.ndim != 2:
        raise ValueError(f"Centroids must be 2D; got {centroids_arr.shape}.")
    if vectors_arr.ndim != 2:
        raise ValueError(f"Vectors must be 2D; got {vectors_arr.shape}.")
    if centroids_arr.shape[1] != vectors_arr.shape[1]:
        raise ValueError(
            f"Vector dimension {vectors_arr.shape[1]} does not match centroid dimension {centroids_arr.shape[1]}."
        )

    if normalize_inputs:
        centroids_arr = _normalize_vectors(centroids_arr)
        vectors_arr = _normalize_vectors(vectors_arr)

    _emit_progress(progress_cb, "3/5", "Assigning vectors to the provided centroids...")
    cluster_ids = assign_vectors_to_centroids(vectors_arr, centroids_arr)

    _emit_progress(progress_cb, "4/5", "Computing tree metadata...")
    num_clusters = centroids_arr.shape[0]
    leaf_slots = _next_power_of_two(num_clusters)
    counts, leaf_start, total_nodes = compute_node_counts(cluster_ids, num_clusters, leaf_slots)
    active_mask = _compute_active_node_mask(num_clusters, leaf_slots)

    clusters = _build_cluster_entries(cluster_ids, leaf_start, num_clusters)
    nodes = _build_nodes_metadata(total_nodes, active_mask)

    payload = {
        "dimensions": vectors_arr.shape[1],
        "num_vectors": vectors_arr.shape[0],
        "num_clusters": centroids_arr.shape[0],
        "cluster_ids": cluster_ids,
        "clusters": clusters,
        "nodes": nodes,
        "tree": {
            "root_node_id": 1,
            "leaf_start_node_id": leaf_start,
            "leaf_count": num_clusters,
            "total_nodes": total_nodes,
        },
        "centroids": centroids_arr,
        "vectors": vectors_arr,
    }
    payload["centroid_list"] = centroids_arr.tolist()

    return PreparedVCT(payload=payload, counts=counts, leaf_start=leaf_start, total_nodes=total_nodes)


def initialize_node_vectors(payload: dict) -> Tuple[NodeVectors, int, int]:
    tree_info = payload.get("tree")
    if tree_info is None:
        raise ValueError("Tree metadata missing from prepared payload.")

    total_nodes = int(tree_info["total_nodes"])
    leaf_start = int(tree_info["leaf_start_node_id"])

    node_vectors: NodeVectors = {node_id: [] for node_id in range(1, total_nodes + 1)}
    clusters: Sequence[dict] = payload.get("clusters", [])
    for cluster in clusters:
        node_id = int(cluster["node_id"])
        node_vectors[node_id] = list(cluster.get("vector_ids", []))

    return node_vectors, leaf_start, total_nodes


def compute_subtree_sizes(node_vectors: NodeVectors, leaf_start: int, total_nodes: int) -> List[int]:
    """Return the total number of vectors that belong to each node's subtree."""
    subtree_sizes = [0] * (total_nodes + 2)
    for node_id in range(total_nodes, 0, -1):
        if node_id >= leaf_start:
            subtree_sizes[node_id] = len(node_vectors[node_id])
            continue

        left_child = node_id * 2
        right_child = left_child + 1
        total = 0
        if left_child <= total_nodes:
            total += subtree_sizes[left_child]
        if right_child <= total_nodes:
            total += subtree_sizes[right_child]
        subtree_sizes[node_id] = total
    return subtree_sizes


def try_merge_node(
    node_id: int,
    node_vectors: NodeVectors,
    total_nodes: int,
    subtree_sizes: Sequence[int],
    threshold: int,
) -> bool:
    left_child = node_id * 2
    right_child = left_child + 1
    if right_child > total_nodes:
        return False  # Leaf node, nothing to merge.

    left_vectors = node_vectors[left_child]
    right_vectors = node_vectors[right_child]
    left_total = subtree_sizes[left_child]
    right_total = subtree_sizes[right_child]
    if len(left_vectors) != left_total or len(right_vectors) != right_total:
        return False  # Children still host unmerged vectors deeper in the subtree.

    combined_size = left_total + right_total
    if combined_size <= threshold:
        # Parent absorbs both children (even if one is empty).
        node_vectors[node_id] = left_vectors + right_vectors
        node_vectors[left_child] = []
        node_vectors[right_child] = []
        return True

    # Combined size exceeds threshold ⇒ no merge.
    return False


def _merge_tree_nodes(
    node_vectors: NodeVectors,
    leaf_start: int,
    total_nodes: int,
    subtree_sizes: Sequence[int],
    threshold: int,
) -> int:
    merges = 0
    for node_id in range(leaf_start - 1, 0, -1):
        if try_merge_node(node_id, node_vectors, total_nodes, subtree_sizes, threshold):
            merges += 1
    return merges


def build_preprocessed_payload(
    node_vectors: NodeVectors,
    vectors: np.ndarray,
    threshold: int,
    *,
    tree_info: Optional[dict] = None,
    tree_nodes: Optional[Sequence[dict]] = None,
    centroids: Optional[np.ndarray] = None,
    original_vector_ids: Optional[np.ndarray] = None,
    leaf_start: Optional[int] = None,
    num_clusters: Optional[int] = None,
) -> dict:
    active_nodes = []
    if original_vector_ids is None:
        raise ValueError("original_vector_ids metadata is required to reconstruct vector_ids.")
    original_ids = np.asarray(original_vector_ids, dtype=np.int64)
    allowed_nodes: Optional[Set[int]] = None
    if tree_nodes is not None:
        allowed_nodes = {int(node.get("id", 0)) for node in tree_nodes}

    if tree_info is not None:
        if leaf_start is None:
            leaf_start = int(tree_info.get("leaf_start_node_id", 0))
        if num_clusters is None:
            leaf_count_info = tree_info.get("leaf_count")
            if leaf_count_info is not None:
                num_clusters = int(leaf_count_info)
    effective_leaf_count = num_clusters

    centroid_arr = None
    centroid_list = None
    if centroids is not None:
        centroid_arr = np.asarray(centroids, dtype=np.float32)
        centroid_list = centroid_arr.tolist()

    for node_id in sorted(node_vectors.keys()):
        if allowed_nodes is not None and int(node_id) not in allowed_nodes:
            continue
        vector_indices = node_vectors[node_id]
        vector_indices_arr = np.asarray(vector_indices, dtype=np.int64)
        if vector_indices_arr.size:
            node_vectors_array = vectors[vector_indices_arr]
            mapped_ids = original_ids[vector_indices_arr].astype(np.int64).tolist()
            vectors_list = np.asarray(node_vectors_array, dtype=np.float32).tolist()
        else:
            mapped_ids = []
            vectors_list = []

        node_entry: Dict[str, Any] = {
            "node_id": int(node_id),
            "vector_ids": mapped_ids,
            "vectors": vectors_list,
        }

        if (
            centroid_arr is not None
            and leaf_start is not None
            and effective_leaf_count is not None
            and effective_leaf_count > 0
            and leaf_start <= node_id < leaf_start + effective_leaf_count
        ):
            centroid_idx = int(node_id - leaf_start)
            if 0 <= centroid_idx < len(centroid_arr):
                node_entry["centroid"] = centroid_arr[centroid_idx].tolist()

        active_nodes.append(node_entry)

    payload = {
        "dimensions": vectors.shape[1] if vectors.ndim == 2 else len(vectors),
        "threshold": threshold,
        "node_count": len(active_nodes),
        "nodes": active_nodes,
    }

    if tree_info is not None:
        payload["tree"] = {k: int(v) if isinstance(v, (np.integer, int)) else v for k, v in tree_info.items()}
    if tree_nodes is not None:
        payload["tree_nodes"] = [
            {
                "id": int(node.get("id", 0)),
                "parent": int(node.get("parent", 0)),
            }
            for node in tree_nodes
        ]
    if centroid_arr is not None:
        payload["centroids"] = centroid_arr
        payload["centroid_list"] = centroid_list or centroid_arr.tolist()
        leaf_start_node = leaf_start
        if leaf_start_node is None and tree_info is not None:
            leaf_start_node = int(tree_info.get("leaf_start_node_id", 0))
        if leaf_start_node:
            payload["centroid_nodes"] = [
                {
                    "node_id": int(leaf_start_node + idx),
                    "centroid_vector": centroid_vec.tolist(),
                }
                for idx, centroid_vec in enumerate(centroid_arr)
            ]

    return payload


def _merge_prepared_payload(
    payload: dict,
    *,
    threshold: int = DEFAULT_MERGE_THRESHOLD,
) -> PreprocessedVCT:
    node_vectors, leaf_start, total_nodes = initialize_node_vectors(payload)
    if "vectors" not in payload:
        raise ValueError("Prepared payload missing 'vectors' array required for merging.")
    vectors = np.asarray(payload["vectors"])
    tree_info = payload.get("tree")
    tree_nodes = payload.get("nodes")
    centroids = payload.get("centroids")
    num_clusters = payload.get("num_clusters")
    original_vector_ids = payload.get("original_vector_ids")
    if original_vector_ids is None:
        raise ValueError("Prepared payload missing 'original_vector_ids' required for tracing vectors.")
    original_vector_ids = np.asarray(original_vector_ids, dtype=np.int64)
    if original_vector_ids.shape[0] != vectors.shape[0]:
        raise ValueError("Length of original_vector_ids does not match number of vectors.")
    subtree_sizes = compute_subtree_sizes(node_vectors, leaf_start, total_nodes)

    merge_count = _merge_tree_nodes(node_vectors, leaf_start, total_nodes, subtree_sizes, threshold)
    preprocessed = build_preprocessed_payload(
        node_vectors,
        vectors,
        threshold,
        tree_info=tree_info,
        tree_nodes=tree_nodes,
        centroids=centroids,
        original_vector_ids=original_vector_ids,
        leaf_start=leaf_start,
        num_clusters=int(num_clusters) if num_clusters is not None else None,
    )

    return PreprocessedVCT(
        payload=preprocessed,
        merge_count=merge_count,
        node_vectors=node_vectors,
        total_nodes=total_nodes,
        threshold=threshold,
    )


def prepare_data(
    centroids: np.ndarray,
    vectors: np.ndarray,
    *,
    normalize_inputs: bool = True,
    progress_cb: ProgressCallback = None,
    return_metadata: bool = False,
) -> Union[dict, PreparedVCT]:
    """Prepare IVF/VCT payloads from in-memory centroids and vectors."""
    result = _prepare_payload(
        centroids,
        vectors,
        normalize_inputs=normalize_inputs,
        progress_cb=progress_cb,
    )
    return result if return_metadata else result.payload


def merge_tree(
    prepared_payload: dict,
    *,
    threshold: int = DEFAULT_MERGE_THRESHOLD,
    return_metadata: bool = False,
) -> Union[dict, PreprocessedVCT]:
    """Merge prepared payloads according to the VCT merging rule."""
    result = _merge_prepared_payload(prepared_payload, threshold=threshold)
    return result if return_metadata else result.payload
