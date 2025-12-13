# myjaconv リファクタリング計画

## 概要

myjaconvをjaconvの拡張ライブラリとして再構築する。jaconvで提供される基本機能を削除し、myjaconv独自の機能のみを保持する。

## 現状分析

### 重複機能（jaconvで代替可能）: 14個

| カテゴリ | 関数 | 対応するjaconv関数 |
|---------|------|-------------------|
| **ひらがな↔カタカナ** | hira2kata | jaconv.hira2kata |
| | hira2hkata | jaconv.hira2hkata |
| | kata2hira | jaconv.kata2hira |
| | enlargesmallkana | jaconv.enlargesmallkana |
| **全角↔半角** | h2z | jaconv.h2z |
| | z2h | jaconv.z2h |
| | han2zen | jaconv.han2zen |
| | zen2han | jaconv.zen2han |
| | hankaku2zenkaku | jaconv.hankaku2zenkaku |
| | zenkaku2hankaku | jaconv.zenkaku2hankaku |
| **正規化** | normalize | jaconv.normalize |
| **ローマ字** | kana2alphabet | jaconv.kana2alphabet |
| | alphabet2kana | jaconv.alphabet2kana |
| | kata2alphabet | jaconv.kata2alphabet |
| | alphabet2kata | jaconv.alphabet2kata |
| **Julius音素** | hiragana2julius | jaconv.hiragana2julius |

### myjaconv独自機能（保持対象）: 12個

| カテゴリ | 関数/定数 | 説明 |
|---------|----------|------|
| **Pydomino音素変換** | hiragana2domino | ひらがな→pydomino音素 |
| | hiragana2domino_with_mapping | 上記 + マッピング情報 |
| | domino2hiragana | pydomino音素→ひらがな |
| | domino2hiragana_with_timing | タイミング付き逆変換 |
| **マッピングテーブル** | HIRAGANA_TO_DOMINO_MAP | ひらがな→音素辞書 |
| | DOMINO_TO_HIRAGANA_MAP | 音素→ひらがな辞書 |
| **歌詞処理** | lyrics2domino | 歌詞→音素文字列 |
| | lyrics2domino_lines | 歌詞→行ごと音素 |
| | lyrics2domino_csv | 歌詞→CSV音素 |
| | lyrics2domino_csv_lines | 歌詞→行ごとCSV |
| | domino_csv2hiragana | CSV音素→ひらがな |
| | domino_csv2hiragana_csv | CSV音素→CSVひらがな |

## リファクタリング計画

### Phase 1: 依存関係の追加

1. `pyproject.toml` に jaconv を依存関係として追加
   ```toml
   dependencies = [
       "jaconv>=0.4.0",
   ]
   ```

### Phase 2: 削除対象ファイル/モジュール

以下のファイル内の重複機能を削除：

| ファイル | 削除対象 | 残す内容 |
|---------|---------|---------|
| `myjaconv/converter.py` | 全削除 | - |
| `myjaconv/romanize.py` | 全削除 | - |
| `myjaconv/conv_table.py` | jaconv重複部分 | DOMINO関連テーブルのみ |
| `myjaconv/phoneme.py` | hiragana2julius | domino関連関数のみ |
| `myjaconv/lyrics.py` | 変更なし | 全保持 |

### Phase 3: 新しいモジュール構成

```
myjaconv/
├── __init__.py          # 公開API（独自機能のみ）
├── conv_table.py        # DOMINO用マッピングテーブルのみ
├── phoneme.py           # domino音素変換関数のみ
└── lyrics.py            # 歌詞処理パイプライン（変更なし）
```

### Phase 4: `__init__.py` の更新

```python
"""myjaconv - jaconvの拡張ライブラリ（pydomino音素変換・歌詞処理）"""

# jaconvの機能を再エクスポート（後方互換性）
from jaconv import (
    hira2kata,
    hira2hkata,
    kata2hira,
    h2z,
    z2h,
    normalize,
    kana2alphabet,
    alphabet2kana,
    kata2alphabet,
    alphabet2kata,
    hiragana2julius,
    # ... 他
)

# myjaconv独自機能
from myjaconv.phoneme import (
    hiragana2domino,
    hiragana2domino_with_mapping,
    domino2hiragana,
    domino2hiragana_with_timing,
)
from myjaconv.conv_table import (
    HIRAGANA_TO_DOMINO_MAP,
    DOMINO_TO_HIRAGANA_MAP,
)
from myjaconv.lyrics import (
    lyrics2domino,
    lyrics2domino_lines,
    lyrics2domino_csv,
    lyrics2domino_csv_lines,
    domino_csv2hiragana,
    domino_csv2hiragana_csv,
)
```

### Phase 5: 内部実装の更新

`lyrics.py` 内でjaconv関数を利用するように変更：

```python
# Before
from myjaconv.converter import kata2hira, normalize

# After
from jaconv import kata2hira, normalize
```

### Phase 6: テストの更新

1. 重複機能のテストを削除（jaconvのテストに委譲）
2. 独自機能のテストのみ保持
3. jaconv連携のインテグレーションテスト追加

## 削除されるコード量の概算

| 項目 | 行数（概算） |
|-----|-------------|
| converter.py | 〜200行 削除 |
| romanize.py | 〜150行 削除 |
| conv_table.py（重複部分） | 〜300行 削除 |
| phoneme.py（julius部分） | 〜50行 削除 |
| **合計** | **〜700行 削減** |

## 後方互換性

jaconvの関数を`__init__.py`で再エクスポートすることで、既存のコードが壊れないようにする。

```python
# 既存コードはそのまま動作
from myjaconv import hira2kata  # → jaconv.hira2kata が呼ばれる
```

## 実行順序

1. [ ] jaconvを依存関係に追加
2. [ ] conv_table.py からjaconv重複テーブルを削除
3. [ ] converter.py を削除
4. [ ] romanize.py を削除
5. [ ] phoneme.py からjulius関数を削除
6. [ ] lyrics.py のimportをjaconvに変更
7. [ ] __init__.py を更新（再エクスポート追加）
8. [ ] テストを更新
9. [ ] 動作確認

## 備考

- jaconvのバージョン: 0.4.0以上を推奨
- Python要件: jaconvはPython 2/3両対応だが、myjaconvは3.9+を維持
