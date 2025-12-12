"""クラスタリングによる最適値算出モジュール"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class OptimizationResult:
    """最適化結果を格納するデータクラス"""

    paths: List[Tuple[List[float], List[float]]]
    """全パス"""

    labels: np.ndarray
    """各パスのクラスタラベル"""

    centroids: np.ndarray
    """各クラスタの重心（最適点候補）"""

    optimal_k: int
    """選択されたクラスタ数"""

    def get_best_point(self, interpolator=None) -> np.ndarray:
        """
        最も良い最適点を返す

        Parameters
        ----------
        interpolator : SurfaceInterpolator, optional
            指定した場合、予測値が最大の重心を返す
            指定しない場合、最初の重心を返す

        Returns
        -------
        best_point : np.ndarray, shape (2,)
            最適点の座標
        """
        valid_centroids = [c for c in self.centroids if not np.any(np.isnan(c))]
        if not valid_centroids:
            raise ValueError("No valid centroids found")

        if interpolator is None:
            return valid_centroids[0]

        # 予測値が最大の重心を返す
        centroids_array = np.array(valid_centroids)
        predictions = interpolator.predict(centroids_array)
        best_idx = np.argmax(predictions)
        return centroids_array[best_idx]


class OptimalPointFinder:
    """パスの最終地点をクラスタリングして最適値を算出するクラス"""

    def __init__(self, k_min: int = 2, k_max: int = 8):
        """
        Parameters
        ----------
        k_min : int
            最小クラスタ数
        k_max : int
            最大クラスタ数
        """
        self.k_min = k_min
        self.k_max = k_max

    def _select_optimal_k(self, X: np.ndarray) -> int:
        """
        シルエットスコアで最適クラスタ数を選択

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, 2)
            クラスタリング対象のデータ

        Returns
        -------
        best_k : int
            最適なクラスタ数
        """
        n_samples = len(X)

        # サンプル数が少ない場合の処理
        if n_samples <= self.k_min:
            return min(n_samples, self.k_min)

        # silhouette_scoreは少なくとも2サンプル、かつ k < n_samples が必要
        # k_maxをサンプル数-1以下に制限
        effective_k_max = min(self.k_max, n_samples - 1)
        effective_k_min = max(self.k_min, 2)  # silhouette_scoreは最低2クラスタ必要

        if effective_k_min > effective_k_max:
            # クラスタリングできない場合は1を返す
            return 1

        best_k = effective_k_min
        best_score = -1

        for k in range(effective_k_min, effective_k_max + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
            labels = kmeans.fit_predict(X)

            # クラスタが1つだけの場合はスキップ
            if len(set(labels)) <= 1:
                continue

            score = silhouette_score(X, labels)
            if score > best_score:
                best_score = score
                best_k = k

        return best_k

    def _calc_centroids(
        self,
        paths: List[Tuple[List[float], List[float]]],
        labels: np.ndarray,
        n_clusters: int,
    ) -> np.ndarray:
        """
        各クラスタの重心を計算

        Parameters
        ----------
        paths : List[Tuple[List[float], List[float]]]
            全パス
        labels : np.ndarray
            各パスのクラスタラベル
        n_clusters : int
            クラスタ数

        Returns
        -------
        centroids : np.ndarray, shape (n_clusters, 2)
            各クラスタの重心
        """
        final_points = np.array([[px[-1], py[-1]] for px, py in paths])
        centroids = []

        for k in range(n_clusters):
            cluster_points = final_points[labels == k]
            if len(cluster_points) > 0:
                centroids.append(cluster_points.mean(axis=0))
            else:
                centroids.append(np.array([np.nan, np.nan]))

        return np.array(centroids)

    def find_optimal_points(
        self, paths: List[Tuple[List[float], List[float]]]
    ) -> OptimizationResult:
        """
        パスの最終地点をクラスタリングし、各クラスタの重心を最適点として返す

        Parameters
        ----------
        paths : List[Tuple[List[float], List[float]]]
            勾配上昇パスのリスト

        Returns
        -------
        result : OptimizationResult
            最適化結果
        """
        final_points = np.array([[px[-1], py[-1]] for px, py in paths])

        # クラスタ数が1の場合の特別処理
        if self.k_min == 1 and self.k_max == 1:
            optimal_k = 1
        else:
            optimal_k = self._select_optimal_k(final_points)

        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init="auto")
        labels = kmeans.fit_predict(final_points)

        centroids = self._calc_centroids(paths, labels, optimal_k)

        return OptimizationResult(
            paths=paths,
            labels=labels,
            centroids=centroids,
            optimal_k=optimal_k,
        )

