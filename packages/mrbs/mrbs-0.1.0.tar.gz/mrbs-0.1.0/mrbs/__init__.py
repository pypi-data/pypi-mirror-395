"""
MRBS - Model-based Response surface optimization with Bootstrap Sampling

部分的なデータをXGBoostで補完し、勾配上昇法で最適点を探索、
クラスタリングで最適値を算出するライブラリ
"""

from .interpolator import SurfaceInterpolator
from .gradient_ascent import GradientAscentOptimizer
from .clustering import OptimalPointFinder, OptimizationResult

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = [
    "SurfaceInterpolator",
    "GradientAscentOptimizer",
    "OptimalPointFinder",
    "OptimizationResult",
    "__version__",
]

