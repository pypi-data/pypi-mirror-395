"""domino CSV形式変換のテスト"""

from jaconv_domino import (
    domino_csv2hiragana,
    domino_csv2hiragana_csv,
    hiragana_csv2domino,
)


class TestDominoCsvToHiragana:
    """CSV形式の音素タイミング→ひらがな文字列変換"""

    def test_simple_vowel(self):
        csv_text = "phoneme,start,end\na,0.0,0.1"
        result = domino_csv2hiragana(csv_text)
        assert result == "あ"

    def test_consonant_vowel(self):
        csv_text = "phoneme,start,end\nk,0.0,0.05\na,0.05,0.1"
        result = domino_csv2hiragana(csv_text)
        assert result == "か"

    def test_arigatou(self):
        csv_text = """phoneme,start,end
a,0.0,0.1
ry,0.1,0.15
i,0.15,0.2
g,0.2,0.25
a,0.25,0.3
t,0.3,0.35
o,0.35,0.4
u,0.4,0.5"""
        result = domino_csv2hiragana(csv_text)
        assert result == "ありがとう"

    def test_youon_kya(self):
        csv_text = """phoneme,start,end
ky,0.0,0.05
a,0.05,0.1"""
        result = domino_csv2hiragana(csv_text)
        assert result == "きゃ"

    def test_sokuon(self):
        # かった = k a cl t a
        csv_text = """phoneme,start,end
k,0.0,0.05
a,0.05,0.1
cl,0.1,0.15
t,0.15,0.2
a,0.2,0.25"""
        result = domino_csv2hiragana(csv_text)
        assert result == "かった"

    def test_empty_csv(self):
        csv_text = "phoneme,start,end"
        result = domino_csv2hiragana(csv_text)
        assert result == ""

    def test_no_header(self):
        # ヘッダーなしでも動作
        csv_text = "a,0.0,0.1"
        result = domino_csv2hiragana(csv_text, has_header=False)
        assert result == "あ"

    def test_different_column_order(self):
        # start,end,phoneme の順序
        csv_text = """start,end,phoneme
0.0,0.1,a
0.1,0.2,ry
0.2,0.3,i"""
        result = domino_csv2hiragana(csv_text)
        assert result == "あり"

    def test_ignore_pau(self):
        # 最初と最後のpauは無視（改行にならない）
        csv_text = """start,end,phoneme
0.0,0.5,pau
0.5,0.6,a
0.6,0.7,i
0.7,1.0,pau"""
        result = domino_csv2hiragana(csv_text)
        assert result == "あい"

    def test_arigatou_with_pau(self):
        # 実際のdomino-song出力形式（最初と最後のpauは無視）
        csv_text = """start,end,phoneme
0.000,0.620,pau
0.620,0.680,a
0.680,1.350,ry
1.350,2.010,i
2.010,2.100,g
2.100,3.260,a
3.260,3.290,t
3.290,3.510,o
3.510,3.620,u
3.620,3.739,pau"""
        result = domino_csv2hiragana(csv_text)
        assert result == "ありがとう"

    def test_internal_pau_becomes_newline(self):
        # 中間のpauは改行に変換
        csv_text = """start,end,phoneme
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
        result = domino_csv2hiragana(csv_text)
        assert result == "あり\nあとう"


class TestDominoCsvToHiraganaCsv:
    """CSV形式の音素タイミング→CSV形式のひらがなタイミング変換"""

    def test_simple(self):
        csv_text = "phoneme,start,end\na,0.0,0.1"
        result = domino_csv2hiragana_csv(csv_text)
        expected = "hiragana,start,end\nあ,0.0,0.1"
        assert result == expected

    def test_arigatou(self):
        csv_text = """phoneme,start,end
a,0.0,0.1
ry,0.1,0.15
i,0.15,0.2
g,0.2,0.25
a,0.25,0.3
t,0.3,0.35
o,0.35,0.4
u,0.4,0.5"""
        result = domino_csv2hiragana_csv(csv_text)
        lines = result.strip().split("\n")
        assert lines[0] == "hiragana,start,end"
        assert lines[1] == "あ,0.0,0.1"
        assert lines[2] == "り,0.1,0.2"
        assert lines[3] == "が,0.2,0.3"
        assert lines[4] == "と,0.3,0.4"
        assert lines[5] == "う,0.4,0.5"


class TestHiraganaCsvToDomino:
    """ひらがなCSV→domino phoneme文字列変換"""

    def test_simple(self):
        result = hiragana_csv2domino("あ")
        assert result == "pau a pau"

    def test_csv_with_timing(self):
        """CSV形式（タイミング付き）からdomino phonemeへ"""
        csv = """あ,0.0,0.1
り,0.1,0.2
が,0.2,0.3
と,0.3,0.4
う,0.4,0.5"""
        result = hiragana_csv2domino(csv)
        assert result == "pau a ry i g a t o u pau"

    def test_csv_with_header(self):
        """ヘッダー付きCSV"""
        csv = """hiragana,start,end
あ,0.62,0.68
り,0.68,2.01"""
        result = hiragana_csv2domino(csv, has_header=True)
        assert result == "pau a ry i pau"

    def test_hiragana_only_lines(self):
        """ひらがなのみの行（タイミングなし）"""
        csv = """あ
り
が
と
う"""
        result = hiragana_csv2domino(csv)
        assert result == "pau a ry i g a t o u pau"

    def test_empty(self):
        result = hiragana_csv2domino("")
        assert result == ""

    def test_only_spaces(self):
        result = hiragana_csv2domino("   ")
        assert result == ""
