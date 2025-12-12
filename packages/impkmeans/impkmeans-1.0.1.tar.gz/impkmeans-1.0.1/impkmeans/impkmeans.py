# impkmeans.py
# ImpKMeans: Improved K-Means via KDE + KD-Tree high-density centroid initialization
#
# Implements the algorithm described in:
# "ImpKmeans: An Improved Version of the K-Means Algorithm by Determining Optimum Initial
#  Centroids Based on Multivariate Kernel Density Estimation and KD-Tree"
#
# Fully deterministic when random_state is supplied.
# Compatible with scikit-learn's estimator API.


import numpy as np
from sklearn.neighbors import KernelDensity, KDTree
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.preprocessing import MinMaxScaler
from typing import Optional
import warnings


class ImpKMeans:
    """
    Improved K-Means initialization using KDE + KD-Tree-based mode seeking.
    
    Parameters
    ----------
    k : int
        Number of candidate initial points to attempt (paper: random in search).
    r : float
        Radius for KDTree removal (paper: defines region suppression).
    bandwidth : float, default=0.05
        KDE bandwidth (paper uses 0.05).
    kernel : str, default="gaussian"
        KDE kernel.
    random_state : int or None
        Random seed for reproducibility.
    
    Attributes
    ----------
    initial_points_ : ndarray
        Selected high-density points used as K-Means initialization.
    labels_ : ndarray
        Cluster labels.
    centers_ : ndarray
        Final cluster centers.
    """

    def __init__(self, k: int, r: float, bandwidth: float = 0.05,
                 kernel: str = "gaussian", random_state: Optional[int] = None):

        self.k = int(k)
        self.r = float(r)
        self.bandwidth = float(bandwidth)
        self.kernel = kernel
        self.random_state = random_state

        # Outputs
        self.initial_points_ = None
        self.labels_ = None
        self.centers_ = None

    # -------------------------------------------------------------
    # Core algorithm
    # -------------------------------------------------------------
    def _find_initial_points(self, X: np.ndarray) -> np.ndarray:
        """
        KDE-based mode seeking + KDTree radius deletion
        (Exactly as in your paper).
        """
        X_work = X.copy()
        points = np.empty((0, X.shape[1]), float)

        for j in range(self.k):
            if X_work.shape[0] == 0:
                break

            kde = KernelDensity(kernel=self.kernel,
                                bandwidth=self.bandwidth).fit(X_work)

            density = kde.score_samples(X_work)
            idx = np.argmax(density)

            # Add selected mode
            points = np.vstack((points, X_work[idx]))

            # Remove neighborhood using KDTree
            tree = KDTree(X_work)
            ind = tree.query_radius([X_work[idx]], self.r)[0]
            X_work = np.delete(X_work, ind, axis=0)

        return points

    # -------------------------------------------------------------
    def fit(self, X: np.ndarray):
        """
        Fit the improved K-Means model.

        Parameters
        ----------
        X : ndarray
            Input data.

        Returns
        -------
        self
        """
        X = np.asarray(X, float)

        scaler = MinMaxScaler()
        X_norm = scaler.fit_transform(X)

        # 1) KDE + KDTree initialization (paper)
        init_points = self._find_initial_points(X_norm)
        if init_points.shape[0] == 0:
            raise ValueError("No initial points were generated. Increase k or r.")

        self.initial_points_ = init_points

        # 2) KMeans with max_iter = 1 (exactly as the paper)
        kmeans = KMeans(
            n_clusters=init_points.shape[0],
            init=init_points,
            n_init=1,
            max_iter=1,
            random_state=self.random_state
        ).fit(X_norm)

        self.labels_ = kmeans.labels_.copy()
        self.centers_ = kmeans.cluster_centers_.copy()

        return self

    def fit_predict(self, X: np.ndarray):
        """Fit and return labels."""
        self.fit(X)
        return self.labels_

    def predict(self, X: np.ndarray):
        """Predict using nearest cluster center."""
        if self.centers_ is None:
            raise ValueError("Model must be fitted before prediction.")

        X = np.asarray(X, float)
        scaler = MinMaxScaler()
        X_norm = scaler.fit_transform(X)

        dists = np.linalg.norm(X_norm[:, None, :] - self.centers_[None, :, :], axis=2)
        return np.argmin(dists, axis=1)

    # -------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------
    def score(self, X: np.ndarray, y_true: np.ndarray):
        """Compute ARI score."""
        preds = self.fit_predict(X)
        return adjusted_rand_score(y_true, preds)

    def get_params(self, deep=True):
        return {
            "k": self.k,
            "r": self.r,
            "bandwidth": self.bandwidth,
            "kernel": self.kernel,
            "random_state": self.random_state,
        }

    def set_params(self, **params):
        for k, v in params.items():
            setattr(self, k, v)
        return self
