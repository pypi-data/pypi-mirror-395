"""可視化モジュール"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

from .clustering import OptimizationResult


def plot_surface(
    xx: np.ndarray,
    yy: np.ndarray,
    F_grid: np.ndarray,
    figsize: Tuple[int, int] = (8, 6),
    cmap: str = "viridis",
    title: str = "Predicted Surface",
    show: bool = True,
) -> Optional[plt.Figure]:
    """
    曲面を等高線プロット

    Parameters
    ----------
    xx, yy : np.ndarray
        メッシュグリッド
    F_grid : np.ndarray
        グリッド上の値
    figsize : Tuple[int, int]
        図のサイズ
    cmap : str
        カラーマップ
    title : str
        タイトル
    show : bool
        plt.show()を呼ぶかどうか

    Returns
    -------
    fig : plt.Figure or None
        show=Falseの場合、Figureオブジェクトを返す
    """
    fig = plt.figure(figsize=figsize)
    contour = plt.contourf(xx, yy, F_grid, 50, cmap=cmap)
    plt.colorbar(contour, label="Predicted F")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(title)

    if show:
        plt.show()
        return None
    return fig


def plot_optimization_result(
    xx: np.ndarray,
    yy: np.ndarray,
    F_grid: np.ndarray,
    result: OptimizationResult,
    plot_paths: bool = True,
    show_origin: bool = True,
    figsize: Tuple[int, int] = (8, 6),
    cmap: str = "viridis",
    title: Optional[str] = None,
    show: bool = True,
) -> Optional[plt.Figure]:
    """
    最適化結果を可視化

    Parameters
    ----------
    xx, yy : np.ndarray
        メッシュグリッド
    F_grid : np.ndarray
        グリッド上の予測値
    result : OptimizationResult
        最適化結果
    plot_paths : bool
        パス全体を描画するか、最終点のみか
    show_origin : bool
        原点にマーカーを表示するか
    figsize : Tuple[int, int]
        図のサイズ
    cmap : str
        カラーマップ
    title : str, optional
        タイトル（Noneの場合は自動設定）
    show : bool
        plt.show()を呼ぶかどうか

    Returns
    -------
    fig : plt.Figure or None
        show=Falseの場合、Figureオブジェクトを返す
    """
    fig = plt.figure(figsize=figsize)
    plt.contourf(xx, yy, F_grid, 50, cmap=cmap)

    colors = plt.cm.tab10.colors
    paths = result.paths
    labels = result.labels
    centroids = result.centroids

    # パスまたは最終点を描画
    for idx, (path_x, path_y) in enumerate(paths):
        c = colors[labels[idx] % len(colors)]
        if plot_paths:
            plt.plot(path_x, path_y, "-o", color=c, alpha=0.6, markersize=4)
        else:
            plt.plot(path_x[-1], path_y[-1], "o", color=c, alpha=0.6)

    # 各クラスタの重心（最適点）を描画
    for i, centroid in enumerate(centroids):
        if not np.any(np.isnan(centroid)):
            plt.plot(
                centroid[0],
                centroid[1],
                "o",
                color=colors[i % len(colors)],
                markersize=17,
                markeredgecolor="black",
                markeredgewidth=2,
                label=f"Optimal Point {i + 1}: ({centroid[0]:.2f}, {centroid[1]:.2f})",
            )

    # 原点マーカー
    if show_origin:
        xlength = 7
        ylength = 7
        plt.plot([-xlength, xlength], [-ylength, ylength], color="black", lw=2)
        plt.plot([-xlength, xlength], [ylength, -ylength], color="black", lw=2)
        plt.text(0, 0, "(0,0)", fontsize=10, va="bottom", ha="left")

    plt.colorbar(label="Predicted F")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc="best")

    if title is None:
        title = "Gradient Ascent Paths" if plot_paths else "Final Points"
        title += f" (k={result.optimal_k})"
    plt.title(title)

    if show:
        plt.show()
        return None
    return fig


def plot_paths_comparison(
    xx: np.ndarray,
    yy: np.ndarray,
    F_grid: np.ndarray,
    result: OptimizationResult,
    figsize: Tuple[int, int] = (14, 6),
    show: bool = True,
) -> Optional[plt.Figure]:
    """
    パスと最終点の比較図を並べて表示

    Parameters
    ----------
    xx, yy : np.ndarray
        メッシュグリッド
    F_grid : np.ndarray
        グリッド上の予測値
    result : OptimizationResult
        最適化結果
    figsize : Tuple[int, int]
        図のサイズ
    show : bool
        plt.show()を呼ぶかどうか

    Returns
    -------
    fig : plt.Figure or None
        show=Falseの場合、Figureオブジェクトを返す
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    colors = plt.cm.tab10.colors
    paths = result.paths
    labels = result.labels
    centroids = result.centroids

    for ax_idx, (ax, plot_paths) in enumerate(zip(axes, [True, False])):
        ax.contourf(xx, yy, F_grid, 50, cmap="viridis")

        for idx, (path_x, path_y) in enumerate(paths):
            c = colors[labels[idx] % len(colors)]
            if plot_paths:
                ax.plot(path_x, path_y, "-o", color=c, alpha=0.6, markersize=4)
            else:
                ax.plot(path_x[-1], path_y[-1], "o", color=c, alpha=0.6)

        for i, centroid in enumerate(centroids):
            if not np.any(np.isnan(centroid)):
                ax.plot(
                    centroid[0],
                    centroid[1],
                    "o",
                    color=colors[i % len(colors)],
                    markersize=15,
                    markeredgecolor="black",
                    markeredgewidth=2,
                )

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Gradient Ascent Paths" if plot_paths else "Final Points & Centroids")

    plt.tight_layout()

    if show:
        plt.show()
        return None
    return fig

