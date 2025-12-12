from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


@dataclass
class HyperSphere:
    """
    Minimal enclosing hypersphere in n-dimensional space.

    CONVENTION:
      - Rows   = points (samples)
      - Columns = dimensions (features)

    So X has shape (n_points, n_dims).
    """

    normalize: bool = True
    random_state: Optional[int] = 42

    center_: Optional[np.ndarray] = None   # shape (n_dims,)
    radius_: Optional[float] = None
    scaler_: Optional[StandardScaler] = None
    n_dims_: Optional[int] = None
    n_points_: Optional[int] = None

    # ------------------------
    # Public API
    # ------------------------
    def fit(self, X) -> "HyperSphere":
        """
        Fit minimal enclosing sphere on training data.

        Parameters
        ----------
        X : pandas.DataFrame or numpy.ndarray
            Shape (n_points, n_dims).
        """
        X_arr = self._to_array(X)          # (n_points, n_dims)
        self.n_points_, self.n_dims_ = X_arr.shape

        if self.normalize:
            self.scaler_ = StandardScaler()
            X_scaled = self.scaler_.fit_transform(X_arr)
        else:
            self.scaler_ = None
            X_scaled = X_arr

        # Compute minimal enclosing ball in this n_dims_-D space
        self.center_, self.radius_ = self._min_enclosing_ball(X_scaled)
        return self

    def distance(self, X) -> np.ndarray:
        """
        Distance of each point (row) in X to the fitted center.

        Parameters
        ----------
        X : DataFrame or ndarray
            Shape (n_points_test, n_dims), same n_dims as training.

        Returns
        -------
        distances : ndarray of shape (n_points_test,)
        """
        self._check_fitted()
        X_arr = self._to_array(X)

        if X_arr.shape[1] != self.n_dims_:
            raise ValueError(
                f"X has {X_arr.shape[1]} columns, but model was fitted with {self.n_dims_} dimensions."
            )

        if self.normalize and self.scaler_ is not None:
            X_scaled = self.scaler_.transform(X_arr)
        else:
            X_scaled = X_arr

        diff = X_scaled - self.center_
        return np.linalg.norm(diff, axis=1)

    def is_inside(self, X, tol: float = 1e-9) -> np.ndarray:
        """
        Boolean array: True if point lies inside or on the hypersphere.
        """
        d = self.distance(X)
        return d <= (self.radius_ + tol)

    def summary(self) -> dict:
        """
        Basic info about the hypersphere.
        """
        self._check_fitted()
        return {
            "n_dims": int(self.n_dims_),
            "n_points": int(self.n_points_),
            "radius": float(self.radius_),
            "center": self.center_.tolist(),
        }

    # ------------------------
    # Visualization (2D PCA)
    # ------------------------
    def plot_2d(self, X, title: str = "2D projection with enclosing circle"):
        """
        2D PCA projection of points and their enclosing circle.

        X should follow the same convention: (n_points, n_dims).
        """
        self._check_fitted()
        X_arr = self._to_array(X)

        if self.normalize and self.scaler_ is not None:
            X_scaled = self.scaler_.transform(X_arr)
        else:
            X_scaled = X_arr

        pca = PCA(n_components=2, random_state=self.random_state)
        X_2d = pca.fit_transform(X_scaled)
        center_2d = pca.transform(self.center_.reshape(1, -1))[0]

        # Approximate projected radius using boundary points
        dists = np.linalg.norm(X_scaled - self.center_, axis=1)
        boundary_mask = np.isclose(dists, self.radius_, rtol=0.01, atol=1e-3)
        if boundary_mask.any():
            boundary_2d = X_2d[boundary_mask]
            rad_2d = np.mean(np.linalg.norm(boundary_2d - center_2d, axis=1))
        else:
            rad_2d = np.max(np.linalg.norm(X_2d - center_2d, axis=1))

        fig, ax = plt.subplots()
        ax.scatter(X_2d[:, 0], X_2d[:, 1], alpha=0.6, label="points")
        ax.scatter(center_2d[0], center_2d[1], marker="x", s=100, label="center")

        circle = plt.Circle(center_2d, rad_2d, fill=False, linestyle="--", linewidth=2)
        ax.add_patch(circle)

        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()
        plt.show()

    # ------------------------
    # Internal helpers
    # ------------------------
    def _to_array(self, X) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            arr = X.values.astype(float)
        else:
            arr = np.asarray(X, dtype=float)

        if arr.ndim != 2:
            raise ValueError("Input must be 2D: (n_points, n_dims).")
        return arr

    def _check_fitted(self):
        if self.center_ is None or self.radius_ is None:
            raise RuntimeError("HyperSphere is not fitted yet. Call .fit(X) first.")

    # ------------------------
    # Minimal enclosing ball (Welzl's algorithm)
    # ------------------------
    def _min_enclosing_ball(self, X: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Compute minimal enclosing ball using Welzl's algorithm.

        X: shape (n_points, n_dims).
        """
        points = [p for p in X]  # list of n_dim vectors

        if self.random_state is not None:
            rng = np.random.default_rng(self.random_state)
            rng.shuffle(points)
        else:
            np.random.shuffle(points)

        # n_dims_ already set in fit()
        return self._welzl(points, [])

    def _welzl(
        self,
        P: List[np.ndarray],
        R: List[np.ndarray],
    ) -> Tuple[np.ndarray, float]:
        # Base cases
        if len(P) == 0 or len(R) == self.n_dims_ + 1:
            return self._ball_from(R)

        p = P.pop()
        center, radius = self._welzl(P, R)

        if np.linalg.norm(p - center) <= radius + 1e-12:
            P.append(p)
            return center, radius
        else:
            center2, radius2 = self._welzl(P, R + [p])
            P.append(p)
            return center2, radius2

    def _ball_from(self, R: List[np.ndarray]) -> Tuple[np.ndarray, float]:
        """
        Compute the unique minimal ball defined by points in R.
        """
        if len(R) == 0:
            center = np.zeros(self.n_dims_, dtype=float)
            radius = 0.0

        elif len(R) == 1:
            center = R[0]
            radius = 0.0

        elif len(R) == 2:
            p1, p2 = R
            center = (p1 + p2) / 2.0
            radius = np.linalg.norm(p1 - center)

        else:
            # General case: sphere through all points in R
            pts = np.array(R)      # (k, n_dims)
            p0 = pts[0]
            A = 2.0 * (pts[1:] - p0)
            b = np.sum(pts[1:] ** 2 - p0 ** 2, axis=1)

            c, *_ = np.linalg.lstsq(A, b, rcond=None)
            center = c
            radius = float(np.max(np.linalg.norm(pts - center, axis=1)))

        return center, radius

