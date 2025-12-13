"""Phoneme conversion module.

Provides hiragana to pydomino phoneme conversion functions.
"""


def _hiragana2domino_raw(text):
    """Convert Hiragana to pydomino's phoneme format (without pau wrapper).

    Parameters
    ----------
    text : str
        Hiragana string.

    Returns
    -------
    str
        Space-separated phoneme string (without pau).

    """

    # Filter: keep only hiragana, katakana, and alphabet characters
    # All other characters (punctuation, symbols, long vowel marks, etc.) are ignored
    def is_allowed_char(c):
        cp = ord(c)
        # Hiragana: U+3041-U+3096, U+309B-U+309C (voiced marks)
        if 0x3041 <= cp <= 0x3096 or 0x309B <= cp <= 0x309C:
            return True
        # Katakana: U+30A1-U+30FA
        if 0x30A1 <= cp <= 0x30FA:
            return True
        # Half-width Katakana: U+FF66-U+FF9D
        if 0xFF66 <= cp <= 0xFF9D:
            return True
        # ASCII alphabet: a-z, A-Z
        if 0x0041 <= cp <= 0x005A or 0x0061 <= cp <= 0x007A:
            return True
        # Full-width alphabet: U+FF21-U+FF3A, U+FF41-U+FF5A
        return 0xFF21 <= cp <= 0xFF3A or 0xFF41 <= cp <= 0xFF5A

    text = "".join(c for c in text if is_allowed_char(c))

    # Vu combinations with separated dakuten: う(U+3046) + ゛(U+309B) + small kana
    text = text.replace("う゛ぁ", " b a")
    text = text.replace("う゛ぃ", " b i")
    text = text.replace("う゛ぇ", " b e")
    text = text.replace("う゛ぉ", " b o")
    text = text.replace("う゛ゅ", " by u")

    # Vu combinations with combined character: ゔ(U+3094) + small kana
    text = text.replace("ゔぁ", " b a")
    text = text.replace("ゔぃ", " b i")
    text = text.replace("ゔぇ", " b e")
    text = text.replace("ゔぉ", " b o")
    text = text.replace("ゔゅ", " by u")

    # 2 character conversion rules
    text = text.replace("ぅ゛", " b u")
    text = text.replace("ゔ", " b u")

    text = text.replace("あぁ", " a a")
    text = text.replace("いぃ", " i i")
    text = text.replace("いぇ", " i e")
    text = text.replace("いゃ", " y a")
    text = text.replace("うぅ", " u:")
    text = text.replace("えぇ", " e e")
    text = text.replace("おぉ", " o:")
    text = text.replace("かぁ", " k a:")
    text = text.replace("きぃ", " ky i:")
    text = text.replace("くぅ", " k u:")
    text = text.replace("くゃ", " ky a")
    text = text.replace("くゅ", " ky u")
    text = text.replace("くょ", " ky o")
    text = text.replace("けぇ", " k e:")
    text = text.replace("こぉ", " k o:")
    text = text.replace("がぁ", " g a:")
    text = text.replace("ぎぃ", " gy i:")
    text = text.replace("ぐぅ", " g u:")
    text = text.replace("ぐゃ", " gy a")
    text = text.replace("ぐゅ", " gy u")
    text = text.replace("ぐょ", " gy o")
    text = text.replace("げぇ", " g e:")
    text = text.replace("ごぉ", " g o:")
    text = text.replace("さぁ", " s a:")
    text = text.replace("しぃ", " sh i:")
    text = text.replace("すぅ", " s u:")
    text = text.replace("すゃ", " sh a")
    text = text.replace("すゅ", " sh u")
    text = text.replace("すょ", " sh o")
    text = text.replace("せぇ", " s e:")
    text = text.replace("そぉ", " s o:")
    text = text.replace("ざぁ", " z a:")
    text = text.replace("じぃ", " j i:")
    text = text.replace("ずぅ", " z u:")
    text = text.replace("ずゃ", " zy a")
    text = text.replace("ずゅ", " zy u")
    text = text.replace("ずょ", " zy o")
    text = text.replace("ぜぇ", " z e:")
    text = text.replace("ぞぉ", " z o:")
    text = text.replace("たぁ", " t a:")
    text = text.replace("ちぃ", " ch i:")
    text = text.replace("つぁ", " ts a")
    text = text.replace("つぃ", " ts i")
    text = text.replace("つぅ", " ts u:")
    text = text.replace("つゃ", " ch a")
    text = text.replace("つゅ", " ch u")
    text = text.replace("つょ", " ch o")
    text = text.replace("つぇ", " ts e")
    text = text.replace("つぉ", " ts o")
    text = text.replace("てぇ", " t e:")
    text = text.replace("とぉ", " t o:")
    text = text.replace("だぁ", " d a:")
    text = text.replace("ぢぃ", " j i:")
    text = text.replace("づぅ", " d u:")
    text = text.replace("づゃ", " zy a")
    text = text.replace("づゅ", " zy u")
    text = text.replace("づょ", " zy o")
    text = text.replace("でぇ", " d e:")
    text = text.replace("どぉ", " d o:")
    text = text.replace("なぁ", " n a:")
    text = text.replace("にぃ", " n i:")
    text = text.replace("ぬぅ", " n u:")
    text = text.replace("ぬゃ", " ny a")
    text = text.replace("ぬゅ", " ny u")
    text = text.replace("ぬょ", " ny o")
    text = text.replace("ねぇ", " n e:")
    text = text.replace("のぉ", " n o:")
    text = text.replace("はぁ", " h a:")
    text = text.replace("ひぃ", " h i:")
    text = text.replace("ふぅ", " f u:")
    text = text.replace("ふゃ", " hy a")
    text = text.replace("ふゅ", " hy u")
    text = text.replace("ふょ", " hy o")
    text = text.replace("へぇ", " h e:")
    text = text.replace("ほぉ", " h o:")
    text = text.replace("ばぁ", " b a:")
    text = text.replace("びぃ", " b i:")
    text = text.replace("ぶぅ", " b u:")
    text = text.replace("ふゃ", " hy a")
    text = text.replace("ぶゅ", " by u")
    text = text.replace("ふょ", " hy o")
    text = text.replace("べぇ", " b e:")
    text = text.replace("ぼぉ", " b o:")
    text = text.replace("ぱぁ", " p a:")
    text = text.replace("ぴぃ", " p i:")
    text = text.replace("ぷぅ", " p u:")
    text = text.replace("ぷゃ", " py a")
    text = text.replace("ぷゅ", " py u")
    text = text.replace("ぷょ", " py o")
    text = text.replace("ぺぇ", " p e:")
    text = text.replace("ぽぉ", " p o:")
    text = text.replace("まぁ", " m a:")
    text = text.replace("みぃ", " m i:")
    text = text.replace("むぅ", " m u:")
    text = text.replace("むゃ", " my a")
    text = text.replace("むゅ", " my u")
    text = text.replace("むょ", " my o")
    text = text.replace("めぇ", " m e:")
    text = text.replace("もぉ", " m o:")
    text = text.replace("やぁ", " y a:")
    text = text.replace("ゆぅ", " y u:")
    text = text.replace("ゆゃ", " y a:")
    text = text.replace("ゆゅ", " y u:")
    text = text.replace("ゆょ", " y o:")
    text = text.replace("よぉ", " y o:")
    text = text.replace("らぁ", " r a:")
    text = text.replace("りぃ", " ry i:")
    text = text.replace("るぅ", " r u:")
    text = text.replace("るゃ", " ry a")
    text = text.replace("るゅ", " ry u")
    text = text.replace("るょ", " ry o")
    text = text.replace("れぇ", " r e:")
    text = text.replace("ろぉ", " r o:")
    text = text.replace("わぁ", " w a:")
    text = text.replace("をぉ", " o:")

    text = text.replace("う゛", " b u")
    text = text.replace("でぃ", " d i")
    text = text.replace("でぇ", " d e:")
    text = text.replace("でゃ", " dy a")
    text = text.replace("でゅ", " dy u")
    text = text.replace("でょ", " dy o")
    text = text.replace("てぃ", " t i")
    text = text.replace("てぇ", " t e:")
    text = text.replace("てゃ", " ty a")
    text = text.replace("てゅ", " ty u")
    text = text.replace("てょ", " ty o")
    text = text.replace("すぃ", " s i")
    text = text.replace("ずぁ", " z u a")
    text = text.replace("ずぃ", " z i")
    text = text.replace("ずぅ", " z u")
    text = text.replace("ずゃ", " zy a")
    text = text.replace("ずゅ", " zy u")
    text = text.replace("ずょ", " zy o")
    text = text.replace("ずぇ", " z e")
    text = text.replace("ずぉ", " z o")
    text = text.replace("きゃ", " ky a")
    text = text.replace("きゅ", " ky u")
    text = text.replace("きょ", " ky o")
    text = text.replace("しゃ", " sh a")
    text = text.replace("しゅ", " sh u")
    text = text.replace("しぇ", " sh e")
    text = text.replace("しょ", " sh o")
    text = text.replace("ちゃ", " ch a")
    text = text.replace("ちゅ", " ch u")
    text = text.replace("ちぇ", " ch e")
    text = text.replace("ちょ", " ch o")
    text = text.replace("とぅ", " t u")
    text = text.replace("とゃ", " ty a")
    text = text.replace("とゅ", " ty u")
    text = text.replace("とょ", " ty o")
    text = text.replace("どぁ", " d o a")
    text = text.replace("どぅ", " d u")
    text = text.replace("どゃ", " dy a")
    text = text.replace("どゅ", " dy u")
    text = text.replace("どょ", " dy o")
    text = text.replace("どぉ", " d o:")
    text = text.replace("にゃ", " ny a")
    text = text.replace("にゅ", " ny u")
    text = text.replace("にょ", " ny o")
    text = text.replace("ひゃ", " hy a")
    text = text.replace("ひゅ", " hy u")
    text = text.replace("ひょ", " hy o")
    text = text.replace("みゃ", " my a")
    text = text.replace("みゅ", " my u")
    text = text.replace("みょ", " my o")
    text = text.replace("りゃ", " ry a")
    text = text.replace("りゅ", " ry u")
    text = text.replace("りょ", " ry o")
    text = text.replace("ぎゃ", " gy a")
    text = text.replace("ぎゅ", " gy u")
    text = text.replace("ぎょ", " gy o")
    text = text.replace("ぢぇ", " j e")
    text = text.replace("ぢゃ", " j a")
    text = text.replace("ぢゅ", " j u")
    text = text.replace("ぢょ", " j o")
    text = text.replace("じぇ", " j e")
    text = text.replace("じゃ", " j a")
    text = text.replace("じゅ", " j u")
    text = text.replace("じょ", " j o")
    text = text.replace("びゃ", " by a")
    text = text.replace("びゅ", " by u")
    text = text.replace("びょ", " by o")
    text = text.replace("ぴゃ", " py a")
    text = text.replace("ぴゅ", " py u")
    text = text.replace("ぴょ", " py o")
    text = text.replace("うぁ", " u a")
    text = text.replace("うぃ", " w i")
    text = text.replace("うぇ", " w e")
    text = text.replace("うぉ", " w o")
    text = text.replace("ふぁ", " f a")
    text = text.replace("ふぃ", " f i")
    text = text.replace("ふぅ", " f u")
    text = text.replace("ふゃ", " hy a")
    text = text.replace("ふゅ", " hy u")
    text = text.replace("ふょ", " hy o")
    text = text.replace("ふぇ", " f e")
    text = text.replace("ふぉ", " f o")

    # Single character conversion rules
    text = text.replace("あ", " a")
    text = text.replace("い", " i")
    text = text.replace("う", " u")
    text = text.replace("え", " e")
    text = text.replace("お", " o")
    text = text.replace("か", " k a")
    text = text.replace("き", " ky i")
    text = text.replace("く", " k u")
    text = text.replace("け", " k e")
    text = text.replace("こ", " k o")
    text = text.replace("さ", " s a")
    text = text.replace("し", " sh i")
    text = text.replace("す", " s u")
    text = text.replace("せ", " s e")
    text = text.replace("そ", " s o")
    text = text.replace("た", " t a")
    text = text.replace("ち", " ch i")
    text = text.replace("つ", " ts u")
    text = text.replace("て", " t e")
    text = text.replace("と", " t o")
    text = text.replace("な", " n a")
    text = text.replace("に", " ny i")
    text = text.replace("ぬ", " n u")
    text = text.replace("ね", " n e")
    text = text.replace("の", " n o")
    text = text.replace("は", " h a")
    text = text.replace("ひ", " hy i")
    text = text.replace("ふ", " f u")
    text = text.replace("へ", " h e")
    text = text.replace("ほ", " h o")
    text = text.replace("ま", " m a")
    text = text.replace("み", " my i")
    text = text.replace("む", " m u")
    text = text.replace("め", " m e")
    text = text.replace("も", " m o")
    text = text.replace("ら", " r a")
    text = text.replace("り", " ry i")
    text = text.replace("る", " r u")
    text = text.replace("れ", " r e")
    text = text.replace("ろ", " r o")
    text = text.replace("が", " g a")
    text = text.replace("ぎ", " gy i")
    text = text.replace("ぐ", " g u")
    text = text.replace("げ", " g e")
    text = text.replace("ご", " g o")
    text = text.replace("ざ", " z a")
    text = text.replace("じ", " j i")
    text = text.replace("ず", " z u")
    text = text.replace("ぜ", " z e")
    text = text.replace("ぞ", " z o")
    text = text.replace("だ", " d a")
    text = text.replace("ぢ", " dy i")
    text = text.replace("づ", " z u")
    text = text.replace("で", " d e")
    text = text.replace("ど", " d o")
    text = text.replace("ば", " b a")
    text = text.replace("び", " by i")
    text = text.replace("ぶ", " b u")
    text = text.replace("べ", " b e")
    text = text.replace("ぼ", " b o")
    text = text.replace("ぱ", " p a")
    text = text.replace("ぴ", " py i")
    text = text.replace("ぷ", " p u")
    text = text.replace("ぺ", " p e")
    text = text.replace("ぽ", " p o")
    text = text.replace("や", " y a")
    text = text.replace("ゆ", " y u")
    text = text.replace("よ", " y o")
    text = text.replace("わ", " w a")
    text = text.replace("ゐ", " i")
    text = text.replace("ゑ", " e")
    text = text.replace("ん", " N")
    text = text.replace("っ", " cl")
    # Small kana not yet processed are treated as regular kana
    text = text.replace("ぁ", " a")
    text = text.replace("ぃ", " i")
    text = text.replace("ぅ", " u")
    text = text.replace("ぇ", " e")
    text = text.replace("ぉ", " o")
    text = text.replace("ゎ", " w a")
    text = text.replace("ぉ", " o")

    # Other special cases
    text = text.replace("を", " o")

    text = text.strip()

    return text.replace(":+", ":")


def hiragana2domino(text: str) -> str:
    r"""Convert Hiragana to pydomino's phoneme format with pau markers.

    Newlines are converted to pau markers. Consecutive pau markers are merged.

    Args:
        text: Hiragana string (newlines OK)

    Returns:
        str: Space-separated phoneme string wrapped with pau markers.

    Examples:
        >>> hiragana2domino('てっぽう')
        'pau t e cl p o u pau'
        >>> hiragana2domino('あり\nがとう')
        'pau a ry i pau g a t o u pau'
        >>> hiragana2domino('あ\n\nい')
        'pau a pau i pau'

    """
    if not text or not text.strip():
        return ""

    # Split by newlines and process each line
    lines = text.strip().split("\n")
    phoneme_parts = []

    for line in lines:
        line = line.strip()
        if line:
            raw = _hiragana2domino_raw(line)
            if raw:
                phoneme_parts.append(raw)

    if not phoneme_parts:
        return ""

    # Join with pau as separator: pau line1 pau line2 pau
    # This automatically merges consecutive pau (empty lines are skipped)
    return "pau " + " pau ".join(phoneme_parts) + " pau"


# Hiragana to phoneme mapping table (domino format)
# Define multi-char combinations first (for longest match)
HIRAGANA_TO_DOMINO_MAP = {
    # Vu with separated dakuten: う(U+3046) + ゛(U+309B) + small kana
    "う゛ぁ": ["b", "a"],
    "う゛ぃ": ["b", "i"],
    "う゛ぇ": ["b", "e"],
    "う゛ぉ": ["b", "o"],
    "う゛ゅ": ["by", "u"],
    "ぅ゛": ["b", "u"],
    # Vu with combined character: ゔ(U+3094) + small kana
    "ゔぁ": ["b", "a"],
    "ゔぃ": ["b", "i"],
    "ゔぇ": ["b", "e"],
    "ゔぉ": ["b", "o"],
    "ゔゅ": ["by", "u"],
    "ゔ": ["b", "u"],
    # Palatalized sounds (2 characters)
    "きゃ": ["ky", "a"],
    "きゅ": ["ky", "u"],
    "きょ": ["ky", "o"],
    "しゃ": ["sh", "a"],
    "しゅ": ["sh", "u"],
    "しぇ": ["sh", "e"],
    "しょ": ["sh", "o"],
    "ちゃ": ["ch", "a"],
    "ちゅ": ["ch", "u"],
    "ちぇ": ["ch", "e"],
    "ちょ": ["ch", "o"],
    "にゃ": ["ny", "a"],
    "にゅ": ["ny", "u"],
    "にょ": ["ny", "o"],
    "ひゃ": ["hy", "a"],
    "ひゅ": ["hy", "u"],
    "ひょ": ["hy", "o"],
    "みゃ": ["my", "a"],
    "みゅ": ["my", "u"],
    "みょ": ["my", "o"],
    "りゃ": ["ry", "a"],
    "りゅ": ["ry", "u"],
    "りょ": ["ry", "o"],
    "ぎゃ": ["gy", "a"],
    "ぎゅ": ["gy", "u"],
    "ぎょ": ["gy", "o"],
    "じゃ": ["j", "a"],
    "じゅ": ["j", "u"],
    "じぇ": ["j", "e"],
    "じょ": ["j", "o"],
    "ぢゃ": ["j", "a"],
    "ぢゅ": ["j", "u"],
    "ぢぇ": ["j", "e"],
    "ぢょ": ["j", "o"],
    "びゃ": ["by", "a"],
    "びゅ": ["by", "u"],
    "びょ": ["by", "o"],
    "ぴゃ": ["py", "a"],
    "ぴゅ": ["py", "u"],
    "ぴょ": ["py", "o"],
    # Other 2-character combinations
    "でぃ": ["d", "i"],
    "でゃ": ["dy", "a"],
    "でゅ": ["dy", "u"],
    "でょ": ["dy", "o"],
    "てぃ": ["t", "i"],
    "てゃ": ["ty", "a"],
    "てゅ": ["ty", "u"],
    "てょ": ["ty", "o"],
    "すぃ": ["s", "i"],
    "ずぁ": ["z", "u", "a"],
    "ずぃ": ["z", "i"],
    "ずぅ": ["z", "u"],
    "ずゃ": ["zy", "a"],
    "ずゅ": ["zy", "u"],
    "ずょ": ["zy", "o"],
    "ずぇ": ["z", "e"],
    "ずぉ": ["z", "o"],
    "とぅ": ["t", "u"],
    "とゃ": ["ty", "a"],
    "とゅ": ["ty", "u"],
    "とょ": ["ty", "o"],
    "どぁ": ["d", "o", "a"],
    "どぅ": ["d", "u"],
    "どゃ": ["dy", "a"],
    "どゅ": ["dy", "u"],
    "どょ": ["dy", "o"],
    "うぁ": ["u", "a"],
    "うぃ": ["w", "i"],
    "うぇ": ["w", "e"],
    "うぉ": ["w", "o"],
    "ふぁ": ["f", "a"],
    "ふぃ": ["f", "i"],
    "ふぇ": ["f", "e"],
    "ふぉ": ["f", "o"],
    "ふゃ": ["hy", "a"],
    "ふゅ": ["hy", "u"],
    "ふょ": ["hy", "o"],
    "う゛": ["b", "u"],
    # Vowels
    "あ": ["a"],
    "い": ["i"],
    "う": ["u"],
    "え": ["e"],
    "お": ["o"],
    # K-row
    "か": ["k", "a"],
    "き": ["ky", "i"],
    "く": ["k", "u"],
    "け": ["k", "e"],
    "こ": ["k", "o"],
    # S-row
    "さ": ["s", "a"],
    "し": ["sh", "i"],
    "す": ["s", "u"],
    "せ": ["s", "e"],
    "そ": ["s", "o"],
    # T-row
    "た": ["t", "a"],
    "ち": ["ch", "i"],
    "つ": ["ts", "u"],
    "て": ["t", "e"],
    "と": ["t", "o"],
    # N-row
    "な": ["n", "a"],
    "に": ["ny", "i"],
    "ぬ": ["n", "u"],
    "ね": ["n", "e"],
    "の": ["n", "o"],
    # H-row
    "は": ["h", "a"],
    "ひ": ["hy", "i"],
    "ふ": ["f", "u"],
    "へ": ["h", "e"],
    "ほ": ["h", "o"],
    # M-row
    "ま": ["m", "a"],
    "み": ["my", "i"],
    "む": ["m", "u"],
    "め": ["m", "e"],
    "も": ["m", "o"],
    # Y-row
    "や": ["y", "a"],
    "ゆ": ["y", "u"],
    "よ": ["y", "o"],
    # R-row
    "ら": ["r", "a"],
    "り": ["ry", "i"],
    "る": ["r", "u"],
    "れ": ["r", "e"],
    "ろ": ["r", "o"],
    # W-row
    "わ": ["w", "a"],
    "ゐ": ["i"],
    "ゑ": ["e"],
    "を": ["o"],
    # N (syllabic nasal)
    "ん": ["N"],
    # Geminate consonant
    "っ": ["cl"],
    # Voiced consonants (G-row)
    "が": ["g", "a"],
    "ぎ": ["gy", "i"],
    "ぐ": ["g", "u"],
    "げ": ["g", "e"],
    "ご": ["g", "o"],
    # Voiced consonants (Z-row)
    "ざ": ["z", "a"],
    "じ": ["j", "i"],
    "ず": ["z", "u"],
    "ぜ": ["z", "e"],
    "ぞ": ["z", "o"],
    # Voiced consonants (D-row)
    "だ": ["d", "a"],
    "ぢ": ["dy", "i"],
    "づ": ["z", "u"],
    "で": ["d", "e"],
    "ど": ["d", "o"],
    # Voiced consonants (B-row)
    "ば": ["b", "a"],
    "び": ["by", "i"],
    "ぶ": ["b", "u"],
    "べ": ["b", "e"],
    "ぼ": ["b", "o"],
    # Semi-voiced consonants (P-row)
    "ぱ": ["p", "a"],
    "ぴ": ["py", "i"],
    "ぷ": ["p", "u"],
    "ぺ": ["p", "e"],
    "ぽ": ["p", "o"],
    # Small kana
    "ぁ": ["a"],
    "ぃ": ["i"],
    "ぅ": ["u"],
    "ぇ": ["e"],
    "ぉ": ["o"],
    "ゃ": ["y", "a"],
    "ゅ": ["y", "u"],
    "ょ": ["y", "o"],
    "ゎ": ["w", "a"],
}

# Sort keys by length (for longest match)
_SORTED_KEYS = sorted(HIRAGANA_TO_DOMINO_MAP.keys(), key=len, reverse=True)


def hiragana2domino_with_mapping(text: str) -> tuple[str, list[tuple[str, list[str]]]]:
    """Convert hiragana to pydomino phonemes with character-phoneme mapping.

    Args:
        text: Hiragana string.

    Returns:
        tuple:
            - phonemes: Space-separated phoneme sequence (str)
            - mapping: [(character, [phoneme_list]), ...]

    Examples:
        >>> phonemes, mapping = hiragana2domino_with_mapping('ありがとう')
        >>> phonemes
        'a ry i g a t o u'
        >>> mapping
        [('あ', ['a']), ('り', ['ry', 'i']), ('が', ['g', 'a']), ('と', ['t', 'o']), ('う', ['u'])]

    """
    if not text:
        return "", []

    # Remove spaces (fullwidth and halfwidth)
    text = text.replace("　", "").replace(" ", "")

    if not text:
        return "", []

    mapping = []
    phonemes = []
    i = 0

    while i < len(text):
        matched = False
        # Search by longest match
        for key in _SORTED_KEYS:
            if text[i:].startswith(key):
                phoneme_list = HIRAGANA_TO_DOMINO_MAP[key]
                mapping.append((key, phoneme_list))
                phonemes.extend(phoneme_list)
                i += len(key)
                matched = True
                break

        if not matched:
            # Skip characters not in mapping
            i += 1

    return " ".join(phonemes), mapping


# Phoneme to hiragana mapping table (for domino format reverse conversion)
# Key is phoneme tuple, value is hiragana
# When multiple hiragana map to the same phoneme, choose the more common one
DOMINO_TO_HIRAGANA_MAP = {
    # Vowels
    ("a",): "あ",
    ("i",): "い",
    ("u",): "う",
    ("e",): "え",
    ("o",): "お",
    # K-row
    ("k", "a"): "か",
    ("ky", "i"): "き",
    ("k", "u"): "く",
    ("k", "e"): "け",
    ("k", "o"): "こ",
    # S-row
    ("s", "a"): "さ",
    ("sh", "i"): "し",
    ("s", "u"): "す",
    ("s", "e"): "せ",
    ("s", "o"): "そ",
    # T-row
    ("t", "a"): "た",
    ("ch", "i"): "ち",
    ("ts", "u"): "つ",
    ("t", "e"): "て",
    ("t", "o"): "と",
    # N-row
    ("n", "a"): "な",
    ("ny", "i"): "に",
    ("n", "u"): "ぬ",
    ("n", "e"): "ね",
    ("n", "o"): "の",
    # H-row
    ("h", "a"): "は",
    ("hy", "i"): "ひ",
    ("f", "u"): "ふ",
    ("h", "e"): "へ",
    ("h", "o"): "ほ",
    # M-row
    ("m", "a"): "ま",
    ("my", "i"): "み",
    ("m", "u"): "む",
    ("m", "e"): "め",
    ("m", "o"): "も",
    # Y-row
    ("y", "a"): "や",
    ("y", "u"): "ゆ",
    ("y", "o"): "よ",
    # R-row
    ("r", "a"): "ら",
    ("ry", "i"): "り",
    ("r", "u"): "る",
    ("r", "e"): "れ",
    ("r", "o"): "ろ",
    # W-row
    ("w", "a"): "わ",
    # Special
    ("N",): "ん",
    ("cl",): "っ",
    # Voiced consonants (G-row)
    ("g", "a"): "が",
    ("gy", "i"): "ぎ",
    ("g", "u"): "ぐ",
    ("g", "e"): "げ",
    ("g", "o"): "ご",
    # Voiced consonants (Z-row)
    ("z", "a"): "ざ",
    ("j", "i"): "じ",
    ("z", "u"): "ず",
    ("z", "e"): "ぜ",
    ("z", "o"): "ぞ",
    # Voiced consonants (D-row)
    ("d", "a"): "だ",
    ("dy", "i"): "ぢ",
    ("d", "e"): "で",
    ("d", "o"): "ど",
    # Voiced consonants (B-row)
    ("b", "a"): "ば",
    ("by", "i"): "び",
    ("b", "u"): "ぶ",
    ("b", "e"): "べ",
    ("b", "o"): "ぼ",
    # Semi-voiced consonants (P-row)
    ("p", "a"): "ぱ",
    ("py", "i"): "ぴ",
    ("p", "u"): "ぷ",
    ("p", "e"): "ぺ",
    ("p", "o"): "ぽ",
    # Palatalized sounds (2 characters)
    ("ky", "a"): "きゃ",
    ("ky", "u"): "きゅ",
    ("ky", "o"): "きょ",
    ("sh", "a"): "しゃ",
    ("sh", "u"): "しゅ",
    ("sh", "e"): "しぇ",
    ("sh", "o"): "しょ",
    ("ch", "a"): "ちゃ",
    ("ch", "u"): "ちゅ",
    ("ch", "e"): "ちぇ",
    ("ch", "o"): "ちょ",
    ("ny", "a"): "にゃ",
    ("ny", "u"): "にゅ",
    ("ny", "o"): "にょ",
    ("hy", "a"): "ひゃ",
    ("hy", "u"): "ひゅ",
    ("hy", "o"): "ひょ",
    ("my", "a"): "みゃ",
    ("my", "u"): "みゅ",
    ("my", "o"): "みょ",
    ("ry", "a"): "りゃ",
    ("ry", "u"): "りゅ",
    ("ry", "o"): "りょ",
    ("gy", "a"): "ぎゃ",
    ("gy", "u"): "ぎゅ",
    ("gy", "o"): "ぎょ",
    ("j", "a"): "じゃ",
    ("j", "u"): "じゅ",
    ("j", "e"): "じぇ",
    ("j", "o"): "じょ",
    ("by", "a"): "びゃ",
    ("by", "u"): "びゅ",
    ("by", "o"): "びょ",
    ("py", "a"): "ぴゃ",
    ("py", "u"): "ぴゅ",
    ("py", "o"): "ぴょ",
    # Special 2-character combinations
    ("f", "a"): "ふぁ",
    ("f", "i"): "ふぃ",
    ("f", "e"): "ふぇ",
    ("f", "o"): "ふぉ",
    ("t", "i"): "てぃ",
    ("d", "i"): "でぃ",
    ("w", "i"): "うぃ",
    ("w", "e"): "うぇ",
    ("w", "o"): "うぉ",
    ("s", "i"): "すぃ",
    ("z", "i"): "ずぃ",
    ("t", "u"): "とぅ",
    ("d", "u"): "どぅ",
    ("ty", "a"): "てゃ",
    ("ty", "u"): "てゅ",
    ("ty", "o"): "てょ",
    ("dy", "a"): "でゃ",
    ("dy", "u"): "でゅ",
    ("dy", "o"): "でょ",
    ("zy", "a"): "ずゃ",
    ("zy", "u"): "ずゅ",
    ("zy", "o"): "ずょ",
    ("ts", "a"): "つぁ",
    ("ts", "i"): "つぃ",
    ("ts", "e"): "つぇ",
    ("ts", "o"): "つぉ",
    ("u", "a"): "うぁ",
}

# Sort phoneme tuples by length (for longest match)
_SORTED_DOMINO_KEYS = sorted(DOMINO_TO_HIRAGANA_MAP.keys(), key=len, reverse=True)


def domino2hiragana(phonemes: str) -> str:
    """Convert pydomino phoneme format string to hiragana.

    Args:
        phonemes: Space-separated phoneme sequence (e.g., "pau a ry i g a t o u pau")

    Returns:
        str: Hiragana string (e.g., "ありがとう")

    Note:
        'pau' (pause) markers are automatically ignored.

    Examples:
        >>> domino2hiragana("pau a ry i g a t o u pau")
        'ありがとう'
        >>> domino2hiragana("k o N ny i ch i h a")
        'こんにちは'
        >>> domino2hiragana("pau t e cl p o u pau")
        'てっぽう'

    """
    if not phonemes or not phonemes.strip():
        return ""

    # Split by spaces into phoneme list and filter out 'pau'
    phoneme_list = [p for p in phonemes.split() if p != "pau"]
    if not phoneme_list:
        return ""

    result = []
    i = 0

    while i < len(phoneme_list):
        matched = False
        # Search by longest match (try longer keys first)
        for key in _SORTED_DOMINO_KEYS:
            key_len = len(key)
            if i + key_len <= len(phoneme_list):
                candidate = tuple(phoneme_list[i : i + key_len])
                if candidate == key:
                    result.append(DOMINO_TO_HIRAGANA_MAP[key])
                    i += key_len
                    matched = True
                    break

        if not matched:
            # Skip unmatched phonemes
            i += 1

    return "".join(result)


def domino2hiragana_with_timing(
    phoneme_timings: list[tuple[str, float, float]],
) -> list[tuple[str, float, float]]:
    """Generate hiragana with timing from pydomino phonemes and timing info.

    Args:
        phoneme_timings: [(phoneme, start_time, end_time), ...] list
            e.g., [("k", 0.0, 0.05), ("o", 0.05, 0.1), ...]

    Returns:
        list: [(hiragana, start_time, end_time), ...] list
            e.g., [("ko", 0.0, 0.1), ...]

    Note:
        - 'pau' (pause) markers are automatically ignored.
        - When multiple phonemes map to a single hiragana (e.g., k+a -> ka),
          the start time is from the first phoneme and
          the end time is from the last phoneme.

    Examples:
        >>> phoneme_timings = [("a", 0.0, 0.1), ("ry", 0.1, 0.15), ("i", 0.15, 0.2)]
        >>> domino2hiragana_with_timing(phoneme_timings)
        [('あ', 0.0, 0.1), ('り', 0.1, 0.2)]

    """
    if not phoneme_timings:
        return []

    # Filter out 'pau' (pause) markers
    phoneme_timings = [(p, s, e) for p, s, e in phoneme_timings if p != "pau"]
    if not phoneme_timings:
        return []

    result = []
    i = 0

    while i < len(phoneme_timings):
        matched = False
        # Search by longest match (try longer keys first)
        for key in _SORTED_DOMINO_KEYS:
            key_len = len(key)
            if i + key_len <= len(phoneme_timings):
                # Extract only phonemes into tuple
                candidate = tuple(pt[0] for pt in phoneme_timings[i : i + key_len])
                if candidate == key:
                    hiragana = DOMINO_TO_HIRAGANA_MAP[key]
                    start_time = phoneme_timings[i][1]
                    end_time = phoneme_timings[i + key_len - 1][2]
                    result.append((hiragana, start_time, end_time))
                    i += key_len
                    matched = True
                    break

        if not matched:
            # Skip unmatched phonemes
            i += 1

    return result


def domino_csv2hiragana(csv_text: str, has_header: bool = True) -> str:
    r"""Convert CSV phoneme timing data to hiragana string.

    Args:
        csv_text: CSV phoneme timing data
            Format: phoneme,start,end or start,end,phoneme
        has_header: Whether there is a header row

    Returns:
        str: Hiragana string (pau markers become newlines)

    Note:
        - Column order is auto-detected from header
        - 'pau' (pause) markers are converted to newlines

    Examples:
        >>> csv = '''phoneme,start,end
        ... a,0.0,0.1
        ... ry,0.1,0.2'''
        >>> domino_csv2hiragana(csv)
        'あり'

        >>> csv = '''start,end,phoneme
        ... 0.0,0.5,pau
        ... 0.5,0.6,a
        ... 0.6,0.7,pau
        ... 0.7,0.8,i'''
        >>> domino_csv2hiragana(csv)
        'あ\nい'

    """
    if not csv_text or not csv_text.strip():
        return ""

    lines = csv_text.strip().split("\n")
    if not lines:
        return ""

    # Detect phoneme column index (default: first column)
    phoneme_idx = 0

    if has_header and lines:
        header = lines[0].lower().strip()
        header_parts = [p.strip() for p in header.split(",")]
        if len(header_parts) >= 1:
            # Identify phoneme column index from header
            for i, col in enumerate(header_parts):
                if col == "phoneme":
                    phoneme_idx = i
                    break

    # Data row start position
    data_start = 1 if has_header else 0
    if data_start >= len(lines):
        return ""

    # Parse CSV lines into phoneme list
    phonemes = []
    for line in lines[data_start:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) >= 3:
            phoneme = parts[phoneme_idx].strip()
            phonemes.append(phoneme)

    if not phonemes:
        return ""

    # Strip leading and trailing pau markers
    while phonemes and phonemes[0] == "pau":
        phonemes.pop(0)
    while phonemes and phonemes[-1] == "pau":
        phonemes.pop()

    if not phonemes:
        return ""

    # Convert phonemes to hiragana, using internal pau as line separator
    groups = []
    current_group = []

    for p in phonemes:
        if p == "pau":
            if current_group:
                # Convert current group to hiragana
                group_str = " ".join(current_group)
                hiragana = domino2hiragana(group_str)
                if hiragana:
                    groups.append(hiragana)
                current_group = []
        else:
            current_group.append(p)

    # Don't forget the last group
    if current_group:
        group_str = " ".join(current_group)
        hiragana = domino2hiragana(group_str)
        if hiragana:
            groups.append(hiragana)

    return "\n".join(groups)


def domino_csv2hiragana_csv(csv_text: str, has_header: bool = True) -> str:
    r"""Convert CSV phoneme timing data to CSV hiragana timing data.

    Args:
        csv_text: CSV phoneme timing data
        has_header: Whether there is a header row

    Returns:
        str: CSV hiragana timing data (with timing preserved)

    Note:
        - 'pau' markers are ignored (not included in output)

    Examples:
        >>> csv = '''phoneme,start,end
        ... a,0.0,0.1'''
        >>> domino_csv2hiragana_csv(csv)
        'hiragana,start,end\nあ,0.0,0.1'

    """
    if not csv_text or not csv_text.strip():
        return "hiragana,start,end"

    csv_lines = csv_text.strip().split("\n")
    if not csv_lines:
        return "hiragana,start,end"

    # Detect column order
    phoneme_idx, start_idx, end_idx = 0, 1, 2  # Default: phoneme,start,end

    if has_header and csv_lines:
        header = csv_lines[0].lower().strip()
        header_parts = [p.strip() for p in header.split(",")]
        if len(header_parts) >= 3:
            for i, col in enumerate(header_parts):
                if col == "phoneme":
                    phoneme_idx = i
                elif col == "start":
                    start_idx = i
                elif col == "end":
                    end_idx = i

    # Data row start position
    data_start = 1 if has_header else 0
    if data_start >= len(csv_lines):
        return "hiragana,start,end"

    # Parse CSV lines into phoneme timings
    phoneme_timings = []
    for line in csv_lines[data_start:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) >= 3:
            phoneme = parts[phoneme_idx].strip()
            start = float(parts[start_idx].strip())
            end = float(parts[end_idx].strip())
            phoneme_timings.append((phoneme, start, end))

    if not phoneme_timings:
        return "hiragana,start,end"

    # Convert using domino2hiragana_with_timing (pau filtering is done there)
    hiragana_timings = domino2hiragana_with_timing(phoneme_timings)

    lines = ["hiragana,start,end"]
    for hiragana, start, end in hiragana_timings:
        lines.append(f"{hiragana},{start},{end}")

    return "\n".join(lines)


def hiragana_csv2domino(csv_text: str, has_header: bool = False) -> str:
    """Convert CSV hiragana data to domino phoneme string.

    Args:
        csv_text: CSV hiragana data
            Format: hiragana,start,end or hiragana only (one per line)
        has_header: Whether there is a header row

    Returns:
        str: Space-separated phoneme string with pau markers

    Note:
        - Timing data (start, end) is ignored
        - All hiragana are concatenated and converted as one string
        - 'pau' markers are added at start and end only

    Examples:
        >>> csv = '''あ,0.0,0.1
        ... り,0.1,0.2'''
        >>> hiragana_csv2domino(csv)
        'pau a ry i pau'

    """
    if not csv_text or not csv_text.strip():
        return ""

    lines = csv_text.strip().split("\n")
    if not lines:
        return ""

    # Skip header if present
    data_start = 1 if has_header else 0
    if data_start >= len(lines):
        return ""

    # Extract hiragana from each line and concatenate
    hiragana_chars = []
    for line in lines[data_start:]:
        line = line.strip()
        if not line:
            continue
        # CSV format: hiragana,start,end or just hiragana
        parts = line.split(",")
        hiragana = parts[0].strip()
        if hiragana:
            hiragana_chars.append(hiragana)

    if not hiragana_chars:
        return ""

    # Concatenate all hiragana and convert to domino (no newlines = no internal pau)
    hiragana_text = "".join(hiragana_chars)
    return hiragana2domino(hiragana_text)
