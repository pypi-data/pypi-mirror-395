"""domino2hiragana_with_timing のテスト"""

from jaconv_domino import domino2hiragana_with_timing


class TestBasicConversion:
    """基本的な変換のテスト"""

    def test_single_vowel(self):
        # 'あ' = a
        phoneme_timings = [("a", 0.0, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("あ", 0.0, 0.1)]

    def test_consonant_vowel(self):
        # 'か' = k a
        phoneme_timings = [("k", 0.0, 0.05), ("a", 0.05, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        # 'か' の時刻は k の開始から a の終了まで
        assert result == [("か", 0.0, 0.1)]

    def test_multiple_characters(self):
        # 'あい' = a i
        phoneme_timings = [("a", 0.0, 0.1), ("i", 0.1, 0.2)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("あ", 0.0, 0.1), ("い", 0.1, 0.2)]


class TestYouon:
    """拗音のテスト"""

    def test_kya(self):
        # 'きゃ' = ky a
        phoneme_timings = [("ky", 0.0, 0.05), ("a", 0.05, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("きゃ", 0.0, 0.1)]

    def test_sha(self):
        # 'しゃ' = sh a
        phoneme_timings = [("sh", 0.0, 0.05), ("a", 0.05, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("しゃ", 0.0, 0.1)]

    def test_cha(self):
        # 'ちゃ' = ch a
        phoneme_timings = [("ch", 0.0, 0.05), ("a", 0.05, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("ちゃ", 0.0, 0.1)]


class TestSokuon:
    """促音のテスト"""

    def test_single_sokuon(self):
        # 'っ' = cl
        phoneme_timings = [("cl", 0.0, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("っ", 0.0, 0.1)]

    def test_katta(self):
        # 'かった' = k a cl t a
        phoneme_timings = [
            ("k", 0.0, 0.05),
            ("a", 0.05, 0.1),
            ("cl", 0.1, 0.15),
            ("t", 0.15, 0.2),
            ("a", 0.2, 0.25),
        ]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [
            ("か", 0.0, 0.1),
            ("っ", 0.1, 0.15),
            ("た", 0.15, 0.25),
        ]


class TestPracticalExamples:
    """実用例のテスト"""

    def test_arigatou(self):
        # 'ありがとう' = a ry i g a t o u
        phoneme_timings = [
            ("a", 0.0, 0.1),
            ("ry", 0.1, 0.15),
            ("i", 0.15, 0.2),
            ("g", 0.2, 0.25),
            ("a", 0.25, 0.3),
            ("t", 0.3, 0.35),
            ("o", 0.35, 0.4),
            ("u", 0.4, 0.5),
        ]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [
            ("あ", 0.0, 0.1),
            ("り", 0.1, 0.2),
            ("が", 0.2, 0.3),
            ("と", 0.3, 0.4),
            ("う", 0.4, 0.5),
        ]

    def test_konnichiha(self):
        # 'こんにちは' = k o N ny i ch i h a
        phoneme_timings = [
            ("k", 0.0, 0.05),
            ("o", 0.05, 0.1),
            ("N", 0.1, 0.15),
            ("ny", 0.15, 0.2),
            ("i", 0.2, 0.25),
            ("ch", 0.25, 0.3),
            ("i", 0.3, 0.35),
            ("h", 0.35, 0.4),
            ("a", 0.4, 0.5),
        ]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [
            ("こ", 0.0, 0.1),
            ("ん", 0.1, 0.15),
            ("に", 0.15, 0.25),
            ("ち", 0.25, 0.35),
            ("は", 0.35, 0.5),
        ]

    def test_kyouko(self):
        # 'きょうこ' = ky o u k o
        phoneme_timings = [
            ("ky", 0.0, 0.05),
            ("o", 0.05, 0.1),
            ("u", 0.1, 0.15),
            ("k", 0.15, 0.2),
            ("o", 0.2, 0.25),
        ]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [
            ("きょ", 0.0, 0.1),
            ("う", 0.1, 0.15),
            ("こ", 0.15, 0.25),
        ]


class TestEdgeCases:
    """エッジケースのテスト"""

    def test_empty_list(self):
        result = domino2hiragana_with_timing([])
        assert result == []

    def test_n_phoneme(self):
        # 'ん' = N
        phoneme_timings = [("N", 0.0, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("ん", 0.0, 0.1)]


class TestSpecialPhonemes:
    """特殊な音素のテスト"""

    def test_fa(self):
        # 'ふぁ' = f a
        phoneme_timings = [("f", 0.0, 0.05), ("a", 0.05, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("ふぁ", 0.0, 0.1)]

    def test_ti(self):
        # 'てぃ' = t i
        phoneme_timings = [("t", 0.0, 0.05), ("i", 0.05, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("てぃ", 0.0, 0.1)]

    def test_di(self):
        # 'でぃ' = d i
        phoneme_timings = [("d", 0.0, 0.05), ("i", 0.05, 0.1)]
        result = domino2hiragana_with_timing(phoneme_timings)
        assert result == [("でぃ", 0.0, 0.1)]
