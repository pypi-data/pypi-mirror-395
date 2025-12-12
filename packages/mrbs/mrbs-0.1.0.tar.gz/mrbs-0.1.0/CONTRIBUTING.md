# Contributing to MRBS

MRBS へのコントリビューションを歓迎します！🎉

## 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yutotakagi/MRBS.git
cd MRBS

# 仮想環境を作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 開発用依存関係をインストール
pip install -e ".[dev]"
```

## 開発フロー

### 1. Issue の作成

バグ報告や機能提案は、まず [Issue](https://github.com/yutotakagi/MRBS/issues) を作成してください。

### 2. ブランチの作成

```bash
# develop ブランチから新しいブランチを作成
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### ブランチ命名規則

| プレフィックス | 用途 |
|---------------|------|
| `feature/` | 新機能の追加 |
| `fix/` | バグ修正 |
| `docs/` | ドキュメントの更新 |
| `refactor/` | リファクタリング |

### 3. コードの変更

- コードスタイルは [Ruff](https://docs.astral.sh/ruff/) に従います
- 型ヒントを使用してください
- docstring を書いてください（NumPy スタイル推奨）

```bash
# リンターの実行
ruff check mrbs/
ruff format mrbs/
```

### 4. テスト

```bash
# インポートテスト
python -c "from mrbs import SurfaceInterpolator; print('OK')"

# ビルドテスト
python -m build
python -m twine check dist/*
```

### 5. コミット

コミットメッセージは以下の形式を推奨します：

```
<type>: <subject>

<body>
```

**type の種類:**
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `style`: フォーマット変更
- `refactor`: リファクタリング
- `test`: テスト追加・修正
- `chore`: ビルド・ツール関連

**例:**
```
feat: add minimize option to GradientAscentOptimizer

Add `maximize` parameter to support both gradient ascent and descent.
Default is True (ascent) for backward compatibility.
```

### 6. Pull Request

1. 変更をプッシュ
   ```bash
   git push origin feature/your-feature-name
   ```

2. GitHub で Pull Request を作成
   - `develop` ブランチに向けて PR を作成
   - 変更内容を説明
   - 関連する Issue があればリンク

## コードスタイル

### Python

- Python 3.9+ をサポート
- 型ヒントを使用
- docstring は NumPy スタイル

```python
def example_function(param1: int, param2: str = "default") -> bool:
    """
    関数の簡単な説明

    Parameters
    ----------
    param1 : int
        パラメータ1の説明
    param2 : str, optional
        パラメータ2の説明, by default "default"

    Returns
    -------
    bool
        戻り値の説明
    """
    pass
```

### インポート順序

```python
# 1. 標準ライブラリ
import os
from typing import List

# 2. サードパーティ
import numpy as np
import pandas as pd

# 3. ローカル
from .interpolator import SurfaceInterpolator
```

## リリースプロセス

リリースはメンテナーが行います：

1. `develop` → `main` へマージ
2. バージョンタグを作成 (`v0.1.0`)
3. GitHub Actions が自動で PyPI に公開

## 質問・サポート

- [GitHub Issues](https://github.com/yutotakagi/MRBS/issues) で質問を受け付けています
- バグ報告の際は、再現手順と環境情報を含めてください

## ライセンス

コントリビューションは MIT ライセンスの下で提供されます。

