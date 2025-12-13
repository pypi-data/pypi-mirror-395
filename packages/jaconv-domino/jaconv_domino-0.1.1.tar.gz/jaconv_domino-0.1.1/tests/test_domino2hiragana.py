"""domino2hiragana のテスト"""

import pytest

from jaconv_domino import domino2hiragana


class TestBasicVowels:
    """母音のテスト"""

    @pytest.mark.parametrize(
        "phonemes,expected",
        [
            ("a", "あ"),
            ("i", "い"),
            ("u", "う"),
            ("e", "え"),
            ("o", "お"),
        ],
    )
    def test_single_vowel(self, phonemes, expected):
        assert domino2hiragana(phonemes) == expected

    def test_all_vowels(self):
        assert domino2hiragana("a i u e o") == "あいうえお"


class TestBasicConsonants:
    """基本子音のテスト"""

    @pytest.mark.parametrize(
        "phonemes,expected",
        [
            ("k a", "か"),
            ("ky i", "き"),
            ("k u", "く"),
            ("k e", "け"),
            ("k o", "こ"),
            ("s a", "さ"),
            ("sh i", "し"),
            ("s u", "す"),
            ("s e", "せ"),
            ("s o", "そ"),
            ("t a", "た"),
            ("ch i", "ち"),
            ("ts u", "つ"),
            ("t e", "て"),
            ("t o", "と"),
            ("n a", "な"),
            ("ny i", "に"),
            ("n u", "ぬ"),
            ("n e", "ね"),
            ("n o", "の"),
            ("h a", "は"),
            ("hy i", "ひ"),
            ("f u", "ふ"),
            ("h e", "へ"),
            ("h o", "ほ"),
            ("m a", "ま"),
            ("my i", "み"),
            ("m u", "む"),
            ("m e", "め"),
            ("m o", "も"),
            ("y a", "や"),
            ("y u", "ゆ"),
            ("y o", "よ"),
            ("r a", "ら"),
            ("ry i", "り"),
            ("r u", "る"),
            ("r e", "れ"),
            ("r o", "ろ"),
            ("w a", "わ"),
            ("N", "ん"),
        ],
    )
    def test_basic_consonant(self, phonemes, expected):
        assert domino2hiragana(phonemes) == expected


class TestVoicedConsonants:
    """濁音・半濁音のテスト"""

    @pytest.mark.parametrize(
        "phonemes,expected",
        [
            ("g a", "が"),
            ("gy i", "ぎ"),
            ("g u", "ぐ"),
            ("g e", "げ"),
            ("g o", "ご"),
            ("z a", "ざ"),
            ("j i", "じ"),
            ("z u", "ず"),
            ("z e", "ぜ"),
            ("z o", "ぞ"),
            ("d a", "だ"),
            ("d e", "で"),
            ("d o", "ど"),
            ("b a", "ば"),
            ("by i", "び"),
            ("b u", "ぶ"),
            ("b e", "べ"),
            ("b o", "ぼ"),
            ("p a", "ぱ"),
            ("py i", "ぴ"),
            ("p u", "ぷ"),
            ("p e", "ぺ"),
            ("p o", "ぽ"),
        ],
    )
    def test_voiced_consonant(self, phonemes, expected):
        assert domino2hiragana(phonemes) == expected


class TestYouon:
    """拗音のテスト"""

    @pytest.mark.parametrize(
        "phonemes,expected",
        [
            ("ky a", "きゃ"),
            ("ky u", "きゅ"),
            ("ky o", "きょ"),
            ("sh a", "しゃ"),
            ("sh u", "しゅ"),
            ("sh o", "しょ"),
            ("ch a", "ちゃ"),
            ("ch u", "ちゅ"),
            ("ch o", "ちょ"),
            ("ny a", "にゃ"),
            ("ny u", "にゅ"),
            ("ny o", "にょ"),
            ("hy a", "ひゃ"),
            ("hy u", "ひゅ"),
            ("hy o", "ひょ"),
            ("my a", "みゃ"),
            ("my u", "みゅ"),
            ("my o", "みょ"),
            ("ry a", "りゃ"),
            ("ry u", "りゅ"),
            ("ry o", "りょ"),
            ("gy a", "ぎゃ"),
            ("gy u", "ぎゅ"),
            ("gy o", "ぎょ"),
            ("j a", "じゃ"),
            ("j u", "じゅ"),
            ("j o", "じょ"),
            ("by a", "びゃ"),
            ("by u", "びゅ"),
            ("by o", "びょ"),
            ("py a", "ぴゃ"),
            ("py u", "ぴゅ"),
            ("py o", "ぴょ"),
        ],
    )
    def test_youon(self, phonemes, expected):
        assert domino2hiragana(phonemes) == expected


class TestSokuon:
    """促音のテスト"""

    def test_single_sokuon(self):
        assert domino2hiragana("cl") == "っ"

    def test_sokuon_in_word_katta(self):
        # かった = k a cl t a
        assert domino2hiragana("k a cl t a") == "かった"

    def test_sokuon_in_word_kitto(self):
        # きっと = ky i cl t o
        assert domino2hiragana("ky i cl t o") == "きっと"


class TestPracticalExamples:
    """実用例のテスト"""

    def test_arigatou(self):
        # ありがとう
        assert domino2hiragana("a ry i g a t o u") == "ありがとう"

    def test_konnichiha(self):
        # こんにちは
        assert domino2hiragana("k o N ny i ch i h a") == "こんにちは"

    def test_sakura(self):
        # さくら
        assert domino2hiragana("s a k u r a") == "さくら"

    def test_kyouko(self):
        # きょうこ
        assert domino2hiragana("ky o u k o") == "きょうこ"

    def test_teppou(self):
        # てっぽう
        assert domino2hiragana("t e cl p o u") == "てっぽう"


class TestEdgeCases:
    """エッジケースのテスト"""

    def test_empty_string(self):
        assert domino2hiragana("") == ""

    def test_only_spaces(self):
        assert domino2hiragana("   ") == ""


class TestSpecialPhonemes:
    """特殊な音素のテスト"""

    @pytest.mark.parametrize(
        "phonemes,expected",
        [
            ("f a", "ふぁ"),
            ("f i", "ふぃ"),
            ("f e", "ふぇ"),
            ("f o", "ふぉ"),
            ("t i", "てぃ"),
            ("d i", "でぃ"),
            ("w i", "うぃ"),
            ("w e", "うぇ"),
            ("w o", "うぉ"),
            ("sh e", "しぇ"),
            ("ch e", "ちぇ"),
            ("j e", "じぇ"),
        ],
    )
    def test_special_phoneme(self, phonemes, expected):
        assert domino2hiragana(phonemes) == expected
