import numpy as np
from sklearn.neighbors import KernelDensity
from scipy.spatial import distance_matrix, cKDTree
import heapq


class ANDClust:
    """
    ANDClust: Adaptive Neighborhood Density-Based Clustering.

    This implementation follows the algorithm structure described in the
    corresponding academic publication while providing a clean, sklearn-
    compatible API and optimized performance.

    The clustering procedure combines:
    - Local AND weights derived from k-nearest-neighbor statistics
    - Kernel density estimation (KDE)
    - A constrained MST growth strategy regulated by normalized distances

    Parameters
    ----------
    N : int, default=5
        Minimum cluster size required to accept a cluster.
    k : int, default=5
        Number of nearest neighbors used when computing local weights.
    eps : float, default=0.2
        Normalized distance tolerance used during MST expansion.
    krnl : str, default='gaussian'
        Kernel type passed to sklearn.neighbors.KernelDensity.
    b_width : float, default=0.5
        Bandwidth for kernel density estimation.

    Attributes
    ----------
    labels_ : ndarray (n_samples,)
        Cluster labels assigned after calling fit(). Noise = 0.
    distWeight : ndarray (n_samples,)
        Precomputed AND weights.
    x : ndarray (n_samples,)
        Log-density values obtained from KDE.
    clusterNo : int
        Total number of detected clusters.
    """

    def __init__(self, N=5, k=5, eps=0.2, krnl='gaussian', b_width=0.5):
        # Store parameters (sklearn-compatible design)
        self.N = int(N)
        self.k = int(k)
        self.eps = float(eps)
        self.krnl = krnl
        self.b_width = float(b_width)

        # Placeholders (populated during fit)
        self.X = None
        self.n_samples = None
        self.d = None
        self.labels_ = None
        self.distWeight = None
        self.x = None
        self.clusterNo = 0
        self.distances = None
        self.starting_point = None

    # ----------------------------------------------------------------------
    # Main sklearn API methods
    # ----------------------------------------------------------------------
    def fit(self, X):
        """
        Fit the ANDClust model to the dataset X.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input dataset.

        Returns
        -------
        self : object
            Fitted model.
        """
        self.X = np.asarray(X, dtype=float)
        if self.X.ndim != 2:
            raise ValueError("X must be a 2D array of shape (n_samples, n_features).")

        self.n_samples, self.d = self.X.shape
        if self.k >= self.n_samples:
            self.k = self.n_samples - 1

        self.labels_ = np.zeros(self.n_samples, dtype=int)
        self.distWeight = np.zeros(self.n_samples, dtype=float)
        self.x = np.full(self.n_samples, np.nan, dtype=float)
        self.clusterNo = 0

        # Precompute distance matrix (required for MST expansion)
        self.distances = distance_matrix(self.X, self.X)

        # Compute model components
        self._compute_and_weights()
        self._compute_kde()
        self._extract_clusters()

        return self

    def predict(self):
        """
        Return cluster labels after the model has been fitted.

        Returns
        -------
        ndarray
            Cluster labels for each sample.
        """
        if self.labels_ is None:
            raise RuntimeError("The model must be fitted before calling predict().")
        return self.labels_

    def fit_predict(self, X):
        """
        Fit the model and return cluster labels.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)

        Returns
        -------
        ndarray
        """
        self.fit(X)
        return self.labels_

    # ----------------------------------------------------------------------
    # Internal: AND weight computation
    # ----------------------------------------------------------------------
    def _compute_and_weights(self):
        """
        Compute AND weights based on k-nearest-neighbor statistics.

        The weight of each sample is derived from the mean of its neighbors'
        average kNN distances, following the ANDClust definition.
        """
        tree = cKDTree(self.X)
        dists, neighs = tree.query(self.X, k=self.k + 1)

        # Exclude self-distance
        knn_dists = dists[:, 1:self.k + 1]
        knn_inds = neighs[:, 1:self.k + 1]

        # Mean distance to k-NN
        knn_avg = np.mean(knn_dists, axis=1)

        # Final AND weight for each point
        weights = np.empty(self.n_samples, dtype=float)
        for i in range(self.n_samples):
            valid = knn_inds[i][(knn_inds[i] >= 0)]
            weights[i] = knn_avg[i] if valid.size == 0 else np.mean(knn_avg[valid])

        # Replace zero/nan values
        zero_mask = (weights <= 0) | ~np.isfinite(weights)
        if np.any(zero_mask):
            fill = np.nanmedian(weights[~zero_mask]) if np.any(~zero_mask) else 1.0
            weights[zero_mask] = fill

        self.distWeight = weights

    # ----------------------------------------------------------------------
    # Internal: KDE density estimation
    # ----------------------------------------------------------------------
    def _compute_kde(self):
        """
        Compute log-density values using sklearn KernelDensity.

        Using float32 for KDE input improves performance without causing
        numerical issues for downstream cluster membership tests.
        """
        X32 = self.X.astype(np.float32)
        kde = KernelDensity(kernel=self.krnl, bandwidth=self.b_width).fit(X32)
        self.x = kde.score_samples(X32).astype(float)

    # ----------------------------------------------------------------------
    # Internal: Cluster extraction (density-first growth)
    # ----------------------------------------------------------------------
    def _extract_clusters(self):
        """
        Select the densest available point and grow a cluster around it using
        a constrained MST expansion. Clusters smaller than N are rejected.
        """
        while np.count_nonzero(np.isfinite(self.x)) >= self.N:
            try:
                self.starting_point = int(np.nanargmax(self.x))
            except ValueError:
                break

            indices = self._expand_cluster()

            # Mark used points
            self.x[self.starting_point] = np.nan
            if indices.size > 0:
                self.x[indices] = np.nan

            # Accept cluster only if large enough
            if indices.size >= self.N:
                self.clusterNo += 1
                self.labels_[indices] = self.clusterNo

    # ----------------------------------------------------------------------
    # Internal: Prim-like MST expansion
    # ----------------------------------------------------------------------
    def _expand_cluster(self):
        """
        Expand a cluster using a normalized-distance MST growth rule.

        Returns
        -------
        ndarray
            Sorted indices of cluster members.
        """
        visited = np.zeros(self.n_samples, dtype=bool)
        mst_edges = []
        heap = [(0.0, self.starting_point, -1)]

        while heap:
            dist_val, current, parent = heapq.heappop(heap)
            if visited[current] or not np.isfinite(self.x[current]):
                continue

            visited[current] = True
            if parent >= 0:
                mst_edges.append((parent, current))

            dw = self.distWeight[current]
            if dw <= 0 or not np.isfinite(dw):
                dw = 1e-12

            row = self.distances[current]
            valid = (~visited) & (self.labels_ == 0) & np.isfinite(row)
            valid[current] = False

            if not np.any(valid):
                continue

            idx = np.nonzero(valid)[0]
            dvals = row[idx]
            ratios = dvals / (dw + 1e-12)

            selected = idx[(ratios >= (1 - self.eps)) & (ratios <= (1 + self.eps))]

            for j in selected:
                heapq.heappush(heap, (float(row[j]), int(j), current))

        # Build connected component
        selected = set()
        queue = [self.starting_point]

        while queue:
            cur = queue.pop(0)
            selected.add(cur)
            for u, v in mst_edges:
                if u == cur and v not in selected:
                    queue.append(v)
                elif v == cur and u not in selected:
                    queue.append(u)

        return np.array(sorted(selected), dtype=int)