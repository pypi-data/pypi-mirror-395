"""近傍線形回帰による勾配上昇法モジュール"""

import numpy as np
from sklearn.linear_model import LinearRegression
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .interpolator import SurfaceInterpolator


class GradientAscentOptimizer:
    """近傍線形回帰による勾配上昇法で最適点を探索するクラス"""

    def __init__(
        self,
        interpolator: "SurfaceInterpolator",
        n_steps: int = 8,
        radius: float = 10.0,
        n_samples: int = 100,
    ):
        """
        Parameters
        ----------
        interpolator : SurfaceInterpolator
            学習済みの補完モデル
        n_steps : int
            勾配上昇の最大ステップ数
        radius : float
            局所サンプリングの半径
        n_samples : int
            各ステップでのサンプリング点数
        """
        self.interpolator = interpolator
        self.n_steps = n_steps
        self.radius = radius
        self.n_samples = n_samples

    def _sample_circle_points(self, x0: float, y0: float) -> np.ndarray:
        """
        円内に均一ランダムサンプリング

        Parameters
        ----------
        x0, y0 : float
            円の中心座標

        Returns
        -------
        points : np.ndarray, shape (n_samples, 2)
            サンプリングされた点
        """
        U = np.random.uniform(0, 1, self.n_samples)
        theta = np.random.uniform(0, 2 * np.pi, self.n_samples)
        xs = x0 + self.radius * np.sqrt(U) * np.cos(theta)
        ys = y0 + self.radius * np.sqrt(U) * np.sin(theta)
        return np.c_[xs, ys]

    def _estimate_local_gradient(
        self, x0: float, y0: float, sample_points: np.ndarray
    ) -> np.ndarray:
        """
        局所線形回帰で勾配を推定

        Parameters
        ----------
        x0, y0 : float
            中心座標
        sample_points : np.ndarray, shape (n_samples, 2)
            サンプリング点

        Returns
        -------
        grad : np.ndarray, shape (2,)
            推定された勾配ベクトル
        """
        X_local = sample_points - np.array([x0, y0])
        y_local = self.interpolator.predict(sample_points)
        linreg = LinearRegression()
        linreg.fit(X_local, y_local)
        return linreg.coef_

    def compute_path(
        self, x0: float, y0: float
    ) -> Tuple[List[float], List[float]]:
        """
        1つの開始点から勾配上昇パスを計算

        Parameters
        ----------
        x0, y0 : float
            開始点の座標

        Returns
        -------
        path_x, path_y : List[float]
            パスの座標列
        """
        path_x, path_y = [x0], [y0]
        prev_grad = None

        for _ in range(self.n_steps):
            sample_points = self._sample_circle_points(x0, y0)
            grad = self._estimate_local_gradient(x0, y0, sample_points)

            # 勾配が逆方向になったら終了（局所最適点に到達）
            if prev_grad is not None and np.dot(grad, prev_grad) < 0:
                break
            prev_grad = grad.copy()

            # 勾配方向に移動
            grad_norm = np.linalg.norm(grad)
            if grad_norm > 0:
                delta = grad / grad_norm * self.radius
                x0 += delta[0]
                y0 += delta[1]

            path_x.append(x0)
            path_y.append(y0)

        return path_x, path_y

    def compute_paths(
        self, start_points: np.ndarray
    ) -> List[Tuple[List[float], List[float]]]:
        """
        複数の開始点からパスを計算

        Parameters
        ----------
        start_points : np.ndarray, shape (n_starts, 2)
            開始点の配列

        Returns
        -------
        paths : List[Tuple[List[float], List[float]]]
            各開始点からのパスのリスト
        """
        paths = []
        for x0, y0 in start_points:
            path = self.compute_path(float(x0), float(y0))
            paths.append(path)
        return paths

