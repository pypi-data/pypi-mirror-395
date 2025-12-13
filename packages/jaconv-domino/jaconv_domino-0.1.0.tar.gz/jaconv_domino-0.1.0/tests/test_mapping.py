"""hiragana2domino_with_mapping のテスト"""

import pytest

from jaconv_domino import hiragana2domino_with_mapping


class TestBasicVowels:
    """基本母音のテスト"""

    @pytest.mark.parametrize(
        "input_text,expected_phonemes,expected_mapping",
        [
            ("あ", "a", [("あ", ["a"])]),
            ("い", "i", [("い", ["i"])]),
            ("う", "u", [("う", ["u"])]),
            ("え", "e", [("え", ["e"])]),
            ("お", "o", [("お", ["o"])]),
        ],
    )
    def test_single_vowel(self, input_text, expected_phonemes, expected_mapping):
        phonemes, mapping = hiragana2domino_with_mapping(input_text)
        assert phonemes == expected_phonemes
        assert mapping == expected_mapping

    def test_all_vowels(self):
        phonemes, mapping = hiragana2domino_with_mapping("あいうえお")
        assert phonemes == "a i u e o"
        assert mapping == [
            ("あ", ["a"]),
            ("い", ["i"]),
            ("う", ["u"]),
            ("え", ["e"]),
            ("お", ["o"]),
        ]


class TestBasicConsonants:
    """基本子音のテスト"""

    @pytest.mark.parametrize(
        "input_text,expected_phonemes,expected_mapping",
        [
            ("か", "k a", [("か", ["k", "a"])]),
            ("き", "ky i", [("き", ["ky", "i"])]),
            ("く", "k u", [("く", ["k", "u"])]),
            ("さ", "s a", [("さ", ["s", "a"])]),
            ("し", "sh i", [("し", ["sh", "i"])]),
            ("す", "s u", [("す", ["s", "u"])]),
            ("た", "t a", [("た", ["t", "a"])]),
            ("ち", "ch i", [("ち", ["ch", "i"])]),
            ("つ", "ts u", [("つ", ["ts", "u"])]),
            ("な", "n a", [("な", ["n", "a"])]),
            ("に", "ny i", [("に", ["ny", "i"])]),
            ("は", "h a", [("は", ["h", "a"])]),
            ("ひ", "hy i", [("ひ", ["hy", "i"])]),
            ("ふ", "f u", [("ふ", ["f", "u"])]),
            ("ま", "m a", [("ま", ["m", "a"])]),
            ("み", "my i", [("み", ["my", "i"])]),
            ("や", "y a", [("や", ["y", "a"])]),
            ("ゆ", "y u", [("ゆ", ["y", "u"])]),
            ("よ", "y o", [("よ", ["y", "o"])]),
            ("ら", "r a", [("ら", ["r", "a"])]),
            ("り", "ry i", [("り", ["ry", "i"])]),
            ("わ", "w a", [("わ", ["w", "a"])]),
            ("を", "o", [("を", ["o"])]),
            ("ん", "N", [("ん", ["N"])]),
        ],
    )
    def test_single_consonant(self, input_text, expected_phonemes, expected_mapping):
        phonemes, mapping = hiragana2domino_with_mapping(input_text)
        assert phonemes == expected_phonemes
        assert mapping == expected_mapping


class TestVoicedConsonants:
    """濁音・半濁音のテスト"""

    @pytest.mark.parametrize(
        "input_text,expected_phonemes,expected_mapping",
        [
            ("が", "g a", [("が", ["g", "a"])]),
            ("ぎ", "gy i", [("ぎ", ["gy", "i"])]),
            ("ざ", "z a", [("ざ", ["z", "a"])]),
            ("じ", "j i", [("じ", ["j", "i"])]),
            ("だ", "d a", [("だ", ["d", "a"])]),
            ("ば", "b a", [("ば", ["b", "a"])]),
            ("び", "by i", [("び", ["by", "i"])]),
            ("ぱ", "p a", [("ぱ", ["p", "a"])]),
            ("ぴ", "py i", [("ぴ", ["py", "i"])]),
        ],
    )
    def test_voiced_consonant(self, input_text, expected_phonemes, expected_mapping):
        phonemes, mapping = hiragana2domino_with_mapping(input_text)
        assert phonemes == expected_phonemes
        assert mapping == expected_mapping


class TestYouon:
    """拗音のテスト"""

    @pytest.mark.parametrize(
        "input_text,expected_phonemes,expected_mapping",
        [
            ("きゃ", "ky a", [("きゃ", ["ky", "a"])]),
            ("きゅ", "ky u", [("きゅ", ["ky", "u"])]),
            ("きょ", "ky o", [("きょ", ["ky", "o"])]),
            ("しゃ", "sh a", [("しゃ", ["sh", "a"])]),
            ("しゅ", "sh u", [("しゅ", ["sh", "u"])]),
            ("しょ", "sh o", [("しょ", ["sh", "o"])]),
            ("ちゃ", "ch a", [("ちゃ", ["ch", "a"])]),
            ("ちゅ", "ch u", [("ちゅ", ["ch", "u"])]),
            ("ちょ", "ch o", [("ちょ", ["ch", "o"])]),
            ("にゃ", "ny a", [("にゃ", ["ny", "a"])]),
            ("ひゃ", "hy a", [("ひゃ", ["hy", "a"])]),
            ("みゃ", "my a", [("みゃ", ["my", "a"])]),
            ("りゃ", "ry a", [("りゃ", ["ry", "a"])]),
            ("ぎゃ", "gy a", [("ぎゃ", ["gy", "a"])]),
            ("じゃ", "j a", [("じゃ", ["j", "a"])]),
            ("びゃ", "by a", [("びゃ", ["by", "a"])]),
            ("ぴゃ", "py a", [("ぴゃ", ["py", "a"])]),
        ],
    )
    def test_youon(self, input_text, expected_phonemes, expected_mapping):
        phonemes, mapping = hiragana2domino_with_mapping(input_text)
        assert phonemes == expected_phonemes
        assert mapping == expected_mapping


class TestSokuon:
    """促音のテスト"""

    def test_single_sokuon(self):
        phonemes, mapping = hiragana2domino_with_mapping("っ")
        assert phonemes == "cl"
        assert mapping == [("っ", ["cl"])]

    def test_sokuon_in_word_katta(self):
        phonemes, mapping = hiragana2domino_with_mapping("かった")
        assert phonemes == "k a cl t a"
        assert mapping == [
            ("か", ["k", "a"]),
            ("っ", ["cl"]),
            ("た", ["t", "a"]),
        ]

    def test_sokuon_in_word_kitto(self):
        phonemes, mapping = hiragana2domino_with_mapping("きっと")
        assert phonemes == "ky i cl t o"
        assert mapping == [
            ("き", ["ky", "i"]),
            ("っ", ["cl"]),
            ("と", ["t", "o"]),
        ]


class TestPracticalExamples:
    """実用例のテスト"""

    def test_arigatou(self):
        phonemes, mapping = hiragana2domino_with_mapping("ありがとう")
        assert phonemes == "a ry i g a t o u"
        assert mapping == [
            ("あ", ["a"]),
            ("り", ["ry", "i"]),
            ("が", ["g", "a"]),
            ("と", ["t", "o"]),
            ("う", ["u"]),
        ]

    def test_konnichiha(self):
        phonemes, mapping = hiragana2domino_with_mapping("こんにちは")
        assert phonemes == "k o N ny i ch i h a"
        assert mapping == [
            ("こ", ["k", "o"]),
            ("ん", ["N"]),
            ("に", ["ny", "i"]),
            ("ち", ["ch", "i"]),
            ("は", ["h", "a"]),
        ]

    def test_sakura(self):
        phonemes, mapping = hiragana2domino_with_mapping("さくら")
        assert phonemes == "s a k u r a"
        assert mapping == [
            ("さ", ["s", "a"]),
            ("く", ["k", "u"]),
            ("ら", ["r", "a"]),
        ]

    def test_kyouko(self):
        phonemes, mapping = hiragana2domino_with_mapping("きょうこ")
        assert phonemes == "ky o u k o"
        assert mapping == [
            ("きょ", ["ky", "o"]),
            ("う", ["u"]),
            ("こ", ["k", "o"]),
        ]


class TestEdgeCases:
    """境界値・エッジケースのテスト"""

    def test_empty_string(self):
        phonemes, mapping = hiragana2domino_with_mapping("")
        assert phonemes == ""
        assert mapping == []

    def test_full_width_space(self):
        phonemes, mapping = hiragana2domino_with_mapping("　")
        assert phonemes == ""
        assert mapping == []

    def test_half_width_space(self):
        phonemes, mapping = hiragana2domino_with_mapping(" ")
        assert phonemes == ""
        assert mapping == []

    def test_mixed_spaces(self):
        phonemes, mapping = hiragana2domino_with_mapping("あ　い")
        assert phonemes == "a i"
        assert mapping == [("あ", ["a"]), ("い", ["i"])]


class TestSmallKana:
    """小文字かなのテスト"""

    @pytest.mark.parametrize(
        "input_text,expected_phonemes,expected_mapping",
        [
            ("ぁ", "a", [("ぁ", ["a"])]),
            ("ぃ", "i", [("ぃ", ["i"])]),
            ("ぅ", "u", [("ぅ", ["u"])]),
            ("ぇ", "e", [("ぇ", ["e"])]),
            ("ぉ", "o", [("ぉ", ["o"])]),
        ],
    )
    def test_small_kana(self, input_text, expected_phonemes, expected_mapping):
        phonemes, mapping = hiragana2domino_with_mapping(input_text)
        assert phonemes == expected_phonemes
        assert mapping == expected_mapping
