"""XGBoostによる曲面補完モジュール"""

import numpy as np
import xgboost as xgb
from typing import Tuple, Optional


class SurfaceInterpolator:
    """部分的なデータからXGBoostで曲面を補完するクラス"""

    def __init__(
        self,
        n_estimators: int = 300,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        **xgb_params,
    ):
        """
        Parameters
        ----------
        n_estimators : int
            XGBoostの木の数
        max_depth : int
            木の最大深さ
        learning_rate : float
            学習率
        **xgb_params
            XGBRegressorに渡す追加パラメータ
        """
        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            **xgb_params,
        )
        self._is_fitted = False
        self.x_range: Optional[Tuple[float, float]] = None
        self.y_range: Optional[Tuple[float, float]] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "SurfaceInterpolator":
        """
        モデルを学習

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, 2)
            特徴量 (x, y)
        y : np.ndarray, shape (n_samples,)
            目的変数 F

        Returns
        -------
        self : SurfaceInterpolator
            学習済みインスタンス
        """
        self.model.fit(X, y)
        self._is_fitted = True
        self.x_range = (float(X[:, 0].min()), float(X[:, 0].max()))
        self.y_range = (float(X[:, 1].min()), float(X[:, 1].max()))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        任意の点で予測

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, 2)
            予測したい点の座標

        Returns
        -------
        y_pred : np.ndarray, shape (n_samples,)
            予測値
        """
        if not self._is_fitted:
            raise RuntimeError("Model is not fitted. Call fit() first.")
        return self.model.predict(X)

    def generate_grid(
        self, n_grid: int = 100
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        均一グリッドを生成して予測値を返す

        Parameters
        ----------
        n_grid : int
            各軸の分割数

        Returns
        -------
        xx : np.ndarray, shape (n_grid, n_grid)
            x座標のメッシュグリッド
        yy : np.ndarray, shape (n_grid, n_grid)
            y座標のメッシュグリッド
        F_pred_grid : np.ndarray, shape (n_grid, n_grid)
            グリッド上の予測値
        """
        if self.x_range is None or self.y_range is None:
            raise RuntimeError("Model is not fitted. Call fit() first.")

        xx, yy = np.meshgrid(
            np.linspace(self.x_range[0], self.x_range[1], n_grid),
            np.linspace(self.y_range[0], self.y_range[1], n_grid),
        )
        grid_points = np.c_[xx.ravel(), yy.ravel()]
        F_pred = self.predict(grid_points)
        F_pred_grid = F_pred.reshape(xx.shape)
        return xx, yy, F_pred_grid

    @property
    def is_fitted(self) -> bool:
        """モデルが学習済みかどうか"""
        return self._is_fitted

