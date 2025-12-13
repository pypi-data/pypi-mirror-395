"""jaconv_domino - jaconv extension library for pydomino phoneme conversion.

This library re-exports jaconv's basic functions and adds pydomino phoneme
conversion features.

Basic Japanese character conversion:
    import jaconv_domino
    jaconv_domino.hira2kata('ひらがな')  # -> 'ヒラガナ'
    jaconv_domino.kata2hira('カタカナ')  # -> 'かたかな'
    jaconv_domino.normalize('ﾃｨﾛﾌｨﾅｰﾚ')  # -> 'ティロフィナーレ'

pydomino phoneme conversion (jaconv_domino-specific):
    jaconv_domino.hiragana2domino('ありがとう')  # -> 'pau a ry i g a t o u pau'
    jaconv_domino.domino2hiragana('pau a ry i g a t o u pau')  # -> 'ありがとう'
    jaconv_domino.hiragana_csv2domino('あ,0.0,0.1')  # -> 'pau a pau'
"""

# Re-export basic functions from jaconv (for backward compatibility)
from jaconv import (
    alphabet2kana,
    enlargesmallkana,
    h2z,
    hankaku2zenkaku,
    hira2hkata,
    hira2kata,
    hiragana2julius,
    kana2alphabet,
    kata2hira,
    normalize,
    z2h,
    zen2han,
)

# jaconv_domino-specific features
from .phoneme import (
    DOMINO_TO_HIRAGANA_MAP,
    HIRAGANA_TO_DOMINO_MAP,
    domino2hiragana,
    domino2hiragana_with_timing,
    domino_csv2hiragana,
    domino_csv2hiragana_csv,
    hiragana2domino,
    hiragana2domino_with_mapping,
    hiragana_csv2domino,
)

VERSION = (0, 1, 0)
__version__ = "0.1.0"
__all__ = [
    "DOMINO_TO_HIRAGANA_MAP",
    "HIRAGANA_TO_DOMINO_MAP",
    "alphabet2kana",
    "alphabet2kata",
    "domino2hiragana",
    "domino2hiragana_with_timing",
    "domino_csv2hiragana",
    "domino_csv2hiragana_csv",
    "enlargesmallkana",
    "h2z",
    "han2zen",
    "hankaku2zenkaku",
    "hira2hkata",
    "hira2kata",
    "hiragana2domino",
    "hiragana2domino_with_mapping",
    "hiragana2julius",
    "hiragana_csv2domino",
    "kana2alphabet",
    "kata2alphabet",
    "kata2hira",
    "normalize",
    "z2h",
    "zen2han",
    "zenkaku2hankaku",
]

# Aliases (jaconv compatible)
han2zen = h2z
zenkaku2hankaku = z2h


def kata2alphabet(text: str) -> str:
    """Convert Katakana to alphabet."""
    return kana2alphabet(kata2hira(text))


def alphabet2kata(text: str) -> str:
    """Convert alphabet to Katakana."""
    return hira2kata(alphabet2kana(text))
