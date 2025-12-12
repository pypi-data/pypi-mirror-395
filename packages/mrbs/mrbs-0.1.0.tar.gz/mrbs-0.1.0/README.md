# MRBS

[![PyPI version](https://badge.fury.io/py/mrbs.svg)](https://badge.fury.io/py/mrbs)
[![Python versions](https://img.shields.io/pypi/pyversions/mrbs.svg)](https://pypi.org/project/mrbs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/yutotakagi/MRBS/actions/workflows/test.yml/badge.svg)](https://github.com/yutotakagi/MRBS/actions/workflows/test.yml)

**Model-based Response surface optimization with Bootstrap Sampling**

部分的なデータをXGBoostで補完し、勾配上昇法とクラスタリングで最適点を探索するPythonライブラリです。

## 特徴

- **XGBoost補完**: 部分的なサンプリングデータから曲面を補完
- **勾配上昇法**: 近傍線形回帰による局所勾配推定で最適点を探索
- **クラスタリング**: 複数の探索パスの終点をK-Meansでクラスタリングし、最適点候補を算出

## インストール

```bash
pip install mrbs
```

開発版のインストール:

```bash
git clone https://github.com/yutotakagi/MRBS.git
cd MRBS
pip install -e ".[dev]"
```

## クイックスタート

```python
import numpy as np
import pandas as pd
from mrbs import SurfaceInterpolator, GradientAscentOptimizer, OptimalPointFinder
from mrbs.visualization import plot_optimization_result

# 1. データ読み込み・補完
df = pd.read_csv("data/sphere_sampled_benchmark_xy_F.csv")
X = df[["x", "y"]].values
y = df["F"].values

interpolator = SurfaceInterpolator(n_estimators=300)
interpolator.fit(X, y)
xx, yy, F_grid = interpolator.generate_grid(n_grid=100)

# 2. 勾配上昇パス計算
optimizer = GradientAscentOptimizer(interpolator, n_steps=10, radius=10)
start_points = np.random.uniform(-100, 100, size=(20, 2))
paths = optimizer.compute_paths(start_points)

# 3. クラスタリング・最適点算出
finder = OptimalPointFinder(k_min=1, k_max=5)
result = finder.find_optimal_points(paths)

# 4. 結果表示
print("最適点候補:")
for i, centroid in enumerate(result.centroids):
    print(f"  Point {i+1}: x={centroid[0]:.4f}, y={centroid[1]:.4f}")

# 5. 可視化
plot_optimization_result(xx, yy, F_grid, result)
```

## モジュール構成

| モジュール | 説明 |
|-----------|------|
| `mrbs.interpolator` | `SurfaceInterpolator` - XGBoostによる曲面補完 |
| `mrbs.gradient_ascent` | `GradientAscentOptimizer` - 勾配上昇法による最適点探索 |
| `mrbs.clustering` | `OptimalPointFinder` - クラスタリングによる最適点算出 |
| `mrbs.visualization` | 可視化関数 |

## 依存パッケージ

- Python >= 3.9
- numpy >= 1.20
- pandas >= 1.3
- xgboost >= 1.5
- scikit-learn >= 1.0
- matplotlib >= 3.4

## コントリビューション

コントリビューションを歓迎します！詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

このプロジェクトは [Contributor Covenant](CODE_OF_CONDUCT.md) に基づく行動規範を採用しています。

## ライセンス

[MIT License](LICENSE)

## 関連リンク

- [PyPI](https://pypi.org/project/mrbs/)
- [GitHub Repository](https://github.com/yutotakagi/MRBS)
- [Issue Tracker](https://github.com/yutotakagi/MRBS/issues)
