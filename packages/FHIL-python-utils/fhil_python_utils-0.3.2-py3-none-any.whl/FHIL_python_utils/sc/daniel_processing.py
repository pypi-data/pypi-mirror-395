"""
Daniel's custom processing pipeline for single-cell data. This was somewhat assembled with AI, so inner logic may be imperfect.
"""

import numpy as np
from scipy.sparse import csr_matrix, isspmatrix_csr
import umap
import igraph
import leidenalg
from scanpy.tl import leiden


def _daniel_normalization(X, min_tx_prop=1e-3):
    """Normalize and log-transform data."""
    if isspmatrix_csr(X):
        X = X.toarray()
    X = X.astype(np.float32)
    X /= X.sum(axis=1, keepdims=True)
    X = np.log(np.clip(X, min_tx_prop, 1.0))
    return X


def _daniel_neighbors(X, k=15, metric='euclidean'):
    """Compute K-nearest neighbors."""
    indices, distances, _ = umap.umap_.nearest_neighbors(
        X,
        n_neighbors=k,
        metric=metric,
        metric_kwds=None,
        angular=False,
        random_state=None
    )
    return indices, distances


def _daniel_umap(knn, X, k=15):
    """Compute UMAP embedding using precomputed KNN."""
    Xumap = umap.UMAP(n_neighbors=k, precomputed_knn=knn).fit_transform(X)
    return Xumap


def _daniel_knn_graph(X, knn):
    """Build igraph graph from KNN results."""
    edges = []
    for i in range(knn[0].shape[0]):
        edges.extend([(i, j) for j in knn[0][i, :]])
    G = igraph.Graph(X.shape[0], edges)
    return G


def _daniel_leiden(knn_graph, resolution=1.0):
    """Compute Leiden clustering."""
    partition = leidenalg.find_partition(
        knn_graph,
        leidenalg.RBConfigurationVertexPartition,
        resolution_parameter=resolution
    )
    return partition.membership


def _write_scanpy_neighbors(adata, knn_indices, knn_distances, n_neighbors):
    """
    Store a precomputed KNN graph in an AnnData object in a Scanpy-compatible way.
    """
    n_cells, k = knn_indices.shape

    # Build connectivities adjacency
    rows = np.repeat(np.arange(n_cells), k)
    cols = knn_indices.flatten()
    vals = np.ones(len(cols), dtype=float)

    connectivities = csr_matrix((vals, (rows, cols)), shape=(n_cells, n_cells))

    # Distances matrix (same edges, but using actual distances)
    dist_vals = knn_distances.flatten()
    distances = csr_matrix((dist_vals, (rows, cols)), shape=(n_cells, n_cells))

    # Write to adata
    adata.obsp["connectivities"] = connectivities
    adata.obsp["distances"] = distances

    adata.uns["neighbors"] = {
        "connectivities_key": "connectivities",
        "distances_key": "distances",
        "params": {
            "method": "custom_daniel_knn",
            "n_neighbors": n_neighbors,
            "metric": "euclidean",
        },
    }


def _graph_from_knn(knn_indices):
    """Rebuild igraph graph from knn index list."""
    n = knn_indices.shape[0]
    edges = [(i, j) for i in range(n) for j in knn_indices[i]]
    return igraph.Graph(n=n, edges=edges)



def daniel_processing(adata, neighbors=15, raw_data_layer='counts', 
                     write_data_layer='UMAP_processed', features=None):
    """
    Complete processing pipeline for single-cell data.
    
    Parameters
    ----------
    adata : AnnData
        Annotated data object
    neighbors : int, default=15
        Number of neighbors for KNN graph
    raw_data_layer : str, default='counts'
        Layer name containing raw count data
    write_data_layer : str, default='UMAP_processed'
        Layer name to write processed data to
    features : array-like, optional
        Subset of features to use. If None, uses all features.
    
    Returns
    -------
    None
        Modifies adata in place
    """
    # 1) Normalize
    adata.layers[write_data_layer] = _daniel_normalization(
        adata.layers[raw_data_layer]
    )

    # 2) Use all genes (or subset if specified)
    clustering_data = adata.layers[write_data_layer]
    if features is not None:
        clustering_data = clustering_data[:, features]

    # 3) Compute KNN
    knn_indices, knn_distances = _daniel_neighbors(
        clustering_data, k=neighbors
    )

    # 4) Store the raw knn results too (optional)
    adata.uns['knn'] = {
        'indices': knn_indices,
        'distances': knn_distances,
    }

    # 5) Write Scanpy-compatible neighbor graph
    _write_scanpy_neighbors(
        adata,
        knn_indices=knn_indices,
        knn_distances=knn_distances,
        n_neighbors=neighbors
    )

    # 6) Build igraph graph for Leiden
    knn_graph = _graph_from_knn(knn_indices)

    # 7) Leiden clustering using your graph
    # adata.obs['leiden'] = pd.Series(_daniel_leiden(knn_graph, resolution=1.0)).astype('category')
    leiden(adata, flavor='igraph', n_iterations=2)

    # 8) UMAP using precomputed KNN
    umap_model = umap.UMAP(
        n_neighbors=neighbors,
        metric="euclidean",
        precomputed_knn=(knn_indices, knn_distances)
    )
    adata.obsm['X_umap'] = umap_model.fit_transform(clustering_data)
