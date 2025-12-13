# jaconv-domino

[![PyPI version](https://img.shields.io/pypi/v/jaconv-domino.svg)](https://pypi.org/project/jaconv-domino/)
[![Python versions](https://img.shields.io/pypi/pyversions/jaconv-domino.svg)](https://pypi.org/project/jaconv-domino/)
[![License](https://img.shields.io/pypi/l/jaconv-domino.svg)](https://pypi.org/project/jaconv-domino/)

jaconv-domino is a Japanese character converter library extending [jaconv](https://github.com/ikegami-yukino/jaconv) with [pydomino](https://github.com/DwangoMediaVillage/pydomino) phoneme conversion features.

[English README](README.md)

## Installation

```bash
pip install jaconv-domino
```

## jaconv について

jaconv の機能については以下を参照してください：

- PyPI: https://pypi.org/project/jaconv/
- GitHub: https://github.com/ikegami-yukino/jaconv

jaconv の機能は以下のように呼び出せます：

```python
import jaconv_domino

# ひらがな → カタカナ
jaconv_domino.hira2kata('ともえまみ')
# => 'トモエマミ'

# カタカナ → ひらがな
jaconv_domino.kata2hira('マミサン')
# => 'まみさん'

# ひらがな → 半角カタカナ
jaconv_domino.hira2hkata('ともえまみ')
# => 'ﾄﾓｴﾏﾐ'

# 半角 → 全角
jaconv_domino.h2z('ﾃｨﾛﾌｨﾅｰﾚ')
# => 'ティロフィナーレ'
jaconv_domino.hankaku2zenkaku('ﾃｨﾛﾌｨﾅｰﾚ')  # エイリアス
jaconv_domino.han2zen('ﾃｨﾛﾌｨﾅｰﾚ')  # エイリアス

# 全角 → 半角
jaconv_domino.z2h('ティロフィナーレ')
# => 'ﾃｨﾛﾌｨﾅｰﾚ'
jaconv_domino.zenkaku2hankaku('ティロフィナーレ')  # エイリアス
jaconv_domino.zen2han('ティロフィナーレ')  # エイリアス

# 正規化 (半角カナ→全角、波ダッシュ→長音など)
jaconv_domino.normalize('ﾃｨﾛ･フィナ〜レ')
# => 'ティロ・フィナーレ'

# かな → ローマ字
jaconv_domino.kana2alphabet('ばなな')
# => 'banana'

# ローマ字 → ひらがな
jaconv_domino.alphabet2kana('ohayou')
# => 'おはよう'

# カタカナ → ローマ字
jaconv_domino.kata2alphabet('バナナ')
# => 'banana'

# ローマ字 → カタカナ
jaconv_domino.alphabet2kata('ohayou')
# => 'オハヨウ'

# 小さいかな → 通常のかな
jaconv_domino.enlargesmallkana('ぁぃぅぇぉ')
# => 'あいうえお'

# ひらがな → Julius音素形式
jaconv_domino.hiragana2julius('てんきすごくいいいいいい')
# => 't e N k i s u g o k u i:'
```

## pydomino 音素変換 (jaconv-domino 固有機能)

### ひらがな → 音素

```python
import jaconv_domino

# ひらがなを pydomino 音素形式に変換
jaconv_domino.hiragana2domino('ありがとう')
# => 'pau a ry i g a t o u pau'

# 改行は pau に変換される (連続する pau は1つにまとめる)
jaconv_domino.hiragana2domino('ありがとう\nこんにちは')
# => 'pau a ry i g a t o u pau k o N ny i ch i h a pau'

# 文字と音素のマッピング付きで変換
phonemes, mapping = jaconv_domino.hiragana2domino_with_mapping('ありがとう')
# phonemes => 'pau a ry i g a t o u pau'
# mapping => [('あ', ['a']), ('り', ['ry', 'i']), ('が', ['g', 'a']), ('と', ['t', 'o']), ('う', ['u'])]
```

### 音素 → ひらがな

```python
# pydomino 音素形式をひらがなに変換 (pau は無視される)
jaconv_domino.domino2hiragana('pau a ry i g a t o u pau')
# => 'ありがとう'

jaconv_domino.domino2hiragana('k o N ny i ch i h a')
# => 'こんにちは'

# タイミング付き音素をタイミング付きひらがなに変換
phoneme_timings = [
    ("a", 0.0, 0.1),
    ("ry", 0.1, 0.15),
    ("i", 0.15, 0.2),
    ("g", 0.2, 0.25),
    ("a", 0.25, 0.3),
]
jaconv_domino.domino2hiragana_with_timing(phoneme_timings)
# => [('あ', 0.0, 0.1), ('り', 0.1, 0.2), ('が', 0.2, 0.3)]
```

### CSV 形式変換 (domino-song 連携用)

```python
# CSV 音素タイミング → ひらがな文字列
# 最初と最後の pau は無視、中間の pau は改行に変換
csv = """start,end,phoneme
0.000,0.620,pau
0.620,0.680,a
0.680,1.350,ry
1.350,2.010,i
2.010,2.100,pau
2.100,3.260,a
3.260,3.290,t
3.290,3.510,o
3.510,3.620,u
3.620,3.739,pau"""

jaconv_domino.domino_csv2hiragana(csv)
# => 'あり\nあとう'

# CSV 音素タイミング → CSV ひらがなタイミング
jaconv_domino.domino_csv2hiragana_csv(csv)
# => 'hiragana,start,end\nあ,0.62,0.68\nり,0.68,2.01\n...'

# ひらがな CSV → 音素文字列
hiragana_csv = """あ,0.0,0.1
り,0.1,0.2
が,0.2,0.3
と,0.3,0.4
う,0.4,0.5"""

jaconv_domino.hiragana_csv2domino(hiragana_csv)
# => 'pau a ry i g a t o u pau'
```

Notes:
- カラム順序はヘッダーから自動検出 (`start,end,phoneme` または `phoneme,start,end`)
- `pau` (ポーズ) 音素: `domino2*` では無視、`*2domino` では改行が pau に変換
- ひらがな・カタカナ・アルファベット以外の文字 (句読点、記号、長音記号など) は無視されます

## API Reference

### jaconv 再エクスポート関数

| 関数 | 説明 |
|------|------|
| `hira2kata(text)` | ひらがな → 全角カタカナ |
| `hira2hkata(text)` | ひらがな → 半角カタカナ |
| `kata2hira(text)` | 全角カタカナ → ひらがな |
| `h2z(text)` | 半角 → 全角 |
| `z2h(text)` | 全角 → 半角 |
| `normalize(text)` | Unicode 正規化 |
| `kana2alphabet(text)` | かな → ローマ字 |
| `alphabet2kana(text)` | ローマ字 → ひらがな |
| `kata2alphabet(text)` | カタカナ → ローマ字 |
| `alphabet2kata(text)` | ローマ字 → カタカナ |
| `enlargesmallkana(text)` | 小さいかな → 通常サイズ |
| `hiragana2julius(text)` | ひらがな → Julius 音素形式 |

エイリアス: `hankaku2zenkaku`=`h2z`, `han2zen`=`h2z`, `zenkaku2hankaku`=`z2h`, `zen2han`=`z2h`

### jaconv-domino 固有関数

| 関数 | 説明 |
|------|------|
| `hiragana2domino(text)` | ひらがな → pydomino 音素形式 |
| `hiragana2domino_with_mapping(text)` | ひらがな → 音素 (文字マッピング付き) |
| `domino2hiragana(phonemes)` | pydomino 音素 → ひらがな |
| `domino2hiragana_with_timing(timings)` | 音素タイミング → ひらがなタイミング |
| `domino_csv2hiragana(csv)` | CSV 音素タイミング → ひらがな文字列 |
| `domino_csv2hiragana_csv(csv)` | CSV 音素タイミング → CSV ひらがなタイミング |
| `hiragana_csv2domino(csv)` | ひらがな CSV → 音素文字列 |

## License

MIT License
