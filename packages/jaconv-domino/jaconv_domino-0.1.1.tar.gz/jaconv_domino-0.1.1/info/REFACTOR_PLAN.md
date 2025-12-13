# myjaconv リファクタリング計画

## 現状
- `myjaconv.py`: 1300行以上の単一ファイル
- 複数の機能が混在

## 分割計画

```
myjaconv/
├── __init__.py        # 公開API（エクスポート）
├── converter.py       # 基本変換（ひらがな↔カタカナ、全角↔半角）
├── romanize.py        # ローマ字変換
├── phoneme.py         # 音素変換
├── conv_table.py      # 変換テーブル（既存）
└── compat.py          # 互換性（既存）
```

## 各ファイルの内容

### converter.py
| 関数 | 行 | 説明 |
|------|-----|------|
| `_exclude_ignorechar` | 16 | 内部: ignore文字除外 |
| `_convert` | 22 | 内部: 変換実行 |
| `_translate` | 26 | 内部: 変換ラッパー |
| `hira2kata` | 33 | ひらがな→全角カタカナ |
| `hira2hkata` | 58 | ひらがな→半角カタカナ |
| `kata2hira` | 83 | カタカナ→ひらがな |
| `enlargesmallkana` | 108 | 小文字かな→大文字かな |
| `h2z` | 133 | 半角→全角 |
| `z2h` | 210 | 全角→半角 |
| `normalize` | 267 | Unicode正規化 |

### romanize.py
| 関数 | 行 | 説明 |
|------|-----|------|
| `kana2alphabet` | 308 | かな→ローマ字 |
| `alphabet2kana` | 379 | ローマ字→かな |

### phoneme.py
| 関数 | 行 | 説明 |
|------|-----|------|
| `hiragana2julius` | 526 | ひらがな→Julius音素 |
| `hiragana2domino` | 854 | ひらがな→domino音素 |
| `hiragana2domino_with_mapping` | 1261 | ひらがな→domino音素+マッピング |
| `HIRAGANA_TO_DOMINO_MAP` | 1185 | 音素マッピングテーブル |

## 依存関係

```
__init__.py
    ├── converter.py ← conv_table.py, compat.py
    ├── romanize.py ← conv_table.py, compat.py
    └── phoneme.py ← conv_table.py
```

## テスト戦略
1. リファクタリング前にテスト実行（ベースライン）
2. 分割後にテスト実行（リグレッション確認）
