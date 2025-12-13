import jaconv_domino


def test_domino2hiragana():
    """domino2hiragana: phoneme string → hiragana (pau ignored)"""
    print("=" * 50)
    print("domino2hiragana")
    print("=" * 50)

    # 基本的な母音
    assert jaconv_domino.domino2hiragana("a") == "あ"
    assert jaconv_domino.domino2hiragana("a i u e o") == "あいうえお"
    print("✓ 母音変換")

    # 子音+母音
    assert jaconv_domino.domino2hiragana("k a") == "か"
    assert jaconv_domino.domino2hiragana("s a") == "さ"
    assert jaconv_domino.domino2hiragana("t a") == "た"
    print("✓ 子音+母音変換")

    # 拗音
    assert jaconv_domino.domino2hiragana("ky a") == "きゃ"
    assert jaconv_domino.domino2hiragana("sh a") == "しゃ"
    assert jaconv_domino.domino2hiragana("ch a") == "ちゃ"
    print("✓ 拗音変換")

    # 促音
    assert jaconv_domino.domino2hiragana("cl") == "っ"
    assert jaconv_domino.domino2hiragana("k a cl t a") == "かった"
    print("✓ 促音変換")

    # 撥音
    assert jaconv_domino.domino2hiragana("N") == "ん"
    assert jaconv_domino.domino2hiragana("k o N ny i ch i h a") == "こんにちは"
    print("✓ 撥音変換")

    # pau無視
    assert jaconv_domino.domino2hiragana("pau a pau") == "あ"
    assert jaconv_domino.domino2hiragana("pau a ry i g a t o u pau") == "ありがとう"
    print("✓ pau無視")

    # 実用例
    assert jaconv_domino.domino2hiragana("a ry i g a t o u") == "ありがとう"
    assert jaconv_domino.domino2hiragana("s a k u r a") == "さくら"
    print("✓ 実用例")

    print()


def test_hiragana2domino():
    """hiragana2domino: hiragana → phoneme string with pau"""
    print("=" * 50)
    print("hiragana2domino")
    print("=" * 50)

    # 基本的な母音
    assert jaconv_domino.hiragana2domino("あ") == "pau a pau"
    assert jaconv_domino.hiragana2domino("あいうえお") == "pau a i u e o pau"
    print("✓ 母音変換")

    # 子音+母音
    assert jaconv_domino.hiragana2domino("か") == "pau k a pau"
    assert jaconv_domino.hiragana2domino("さ") == "pau s a pau"
    assert jaconv_domino.hiragana2domino("た") == "pau t a pau"
    print("✓ 子音+母音変換")

    # 拗音
    assert jaconv_domino.hiragana2domino("きゃ") == "pau ky a pau"
    assert jaconv_domino.hiragana2domino("しゃ") == "pau sh a pau"
    assert jaconv_domino.hiragana2domino("ちゃ") == "pau ch a pau"
    print("✓ 拗音変換")

    # 促音
    assert jaconv_domino.hiragana2domino("っ") == "pau cl pau"
    assert jaconv_domino.hiragana2domino("かった") == "pau k a cl t a pau"
    print("✓ 促音変換")

    # 撥音
    assert jaconv_domino.hiragana2domino("ん") == "pau N pau"
    assert jaconv_domino.hiragana2domino("こんにちは") == "pau k o N ny i ch i h a pau"
    print("✓ 撥音変換")

    # 改行 → pau (連続pauは1つにまとめる)
    assert jaconv_domino.hiragana2domino("あ\nい") == "pau a pau i pau"
    assert (
        jaconv_domino.hiragana2domino("ありがとう\nこんにちは")
        == "pau a ry i g a t o u pau k o N ny i ch i h a pau"
    )
    print("✓ 改行→pau変換")

    # 実用例
    assert jaconv_domino.hiragana2domino("ありがとう") == "pau a ry i g a t o u pau"
    assert jaconv_domino.hiragana2domino("さくら") == "pau s a k u r a pau"
    print("✓ 実用例")

    print()


def test_domino_csv2hiragana():
    """domino_csv2hiragana: CSV phoneme timing → hiragana string (internal pau → newline)"""
    print("=" * 50)
    print("domino_csv2hiragana")
    print("=" * 50)

    # 基本変換
    csv1 = "phoneme,start,end\na,0.0,0.1"
    assert jaconv_domino.domino_csv2hiragana(csv1) == "あ"
    print("✓ 基本変換")

    # 子音+母音
    csv2 = "phoneme,start,end\nk,0.0,0.05\na,0.05,0.1"
    assert jaconv_domino.domino_csv2hiragana(csv2) == "か"
    print("✓ 子音+母音")

    # 複数文字
    csv3 = """phoneme,start,end
a,0.0,0.1
ry,0.1,0.15
i,0.15,0.2
g,0.2,0.25
a,0.25,0.3
t,0.3,0.35
o,0.35,0.4
u,0.4,0.5"""
    assert jaconv_domino.domino_csv2hiragana(csv3) == "ありがとう"
    print("✓ 複数文字 (ありがとう)")

    # 最初と最後のpauは無視
    csv4 = """start,end,phoneme
0.0,0.5,pau
0.5,0.6,a
0.6,0.7,i
0.7,1.0,pau"""
    assert jaconv_domino.domino_csv2hiragana(csv4) == "あい"
    print("✓ 最初・最後のpau無視")

    # 中間のpauは改行に変換
    csv5 = """start,end,phoneme
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
    result = jaconv_domino.domino_csv2hiragana(csv5)
    assert result == "あり\nあとう"
    print("✓ 中間pau→改行 (あり\\nあとう)")

    # ヘッダーなし
    csv6 = "a,0.0,0.1"
    assert jaconv_domino.domino_csv2hiragana(csv6, has_header=False) == "あ"
    print("✓ ヘッダーなし対応")

    print()


def test_domino_csv2hiragana_csv():
    """domino_csv2hiragana_csv: CSV phoneme timing → CSV hiragana timing"""
    print("=" * 50)
    print("domino_csv2hiragana_csv")
    print("=" * 50)

    # 基本変換
    csv1 = "phoneme,start,end\na,0.0,0.1"
    result1 = jaconv_domino.domino_csv2hiragana_csv(csv1)
    assert result1 == "hiragana,start,end\nあ,0.0,0.1"
    print("✓ 基本変換")

    # 複数文字 (タイミング付き)
    csv2 = """start,end,phoneme
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
    result2 = jaconv_domino.domino_csv2hiragana_csv(csv2)
    print(result2)
    lines = result2.strip().split("\n")
    lines[0] == "hiragana,start,end"
    lines[1] == "あ,0.0,0.1"
    lines[2] == "り,0.1,0.2"
    lines[3] == "が,0.2,0.3"
    lines[4] == "と,0.3,0.4"
    lines[5] == "う,0.4,0.5"
    print("✓ 複数文字タイミング (ありがとう)")

    print()


def test_hiragana_csv2domino():
    """hiragana_csv2domino: hiragana CSV/text → phoneme string with pau"""
    print("=" * 50)
    print("hiragana_csv2domino")
    print("=" * 50)

    # 単純なひらがな
    assert jaconv_domino.hiragana_csv2domino("あ") == "pau a pau"
    print("✓ 単純なひらがな")

    # タイミング付きCSV
    csv1 = """あ,0.0,0.1
り,0.1,0.2
が,0.2,0.3
と,0.3,0.4
う,0.4,0.5"""
    assert jaconv_domino.hiragana_csv2domino(csv1) == "pau a ry i g a t o u pau"
    print("✓ タイミング付きCSV")

    # ヘッダー付きCSV
    csv2 = """hiragana,start,end
あ,0.62,0.68
り,0.68,2.01"""
    assert jaconv_domino.hiragana_csv2domino(csv2, has_header=True) == "pau a ry i pau"
    print("✓ ヘッダー付きCSV")

    # ひらがなのみの行
    csv3 = """あ
り
が
と
う"""
    assert jaconv_domino.hiragana_csv2domino(csv3) == "pau a ry i g a t o u pau"
    print("✓ ひらがなのみの行")

    # 空入力
    assert jaconv_domino.hiragana_csv2domino("") == ""
    assert jaconv_domino.hiragana_csv2domino("   ") == ""
    print("✓ 空入力")

    print()


def test_roundtrip():
    """往復変換テスト"""
    print("=" * 50)
    print("往復変換テスト")
    print("=" * 50)

    # hiragana → domino → hiragana
    original = "ありがとう"
    domino = jaconv_domino.hiragana2domino(original)
    back = jaconv_domino.domino2hiragana(domino)
    assert back == original
    print(f"✓ '{original}' → '{domino}' → '{back}'")

    original2 = "こんにちは"
    domino2 = jaconv_domino.hiragana2domino(original2)
    back2 = jaconv_domino.domino2hiragana(domino2)
    assert back2 == original2
    print(f"✓ '{original2}' → '{domino2}' → '{back2}'")

    original3 = "「き」ゃりー$ぱみゅぱみゅ"
    domino3 = jaconv_domino.hiragana2domino(original3)
    back3 = jaconv_domino.domino2hiragana(domino3)
    # assert back3 == original3
    print(f"✓ '{original3}' → '{domino3}' → '{back3}'")

    print()


def main():
    print("jaconv_domino テスト")
    print()

    test_domino2hiragana()
    test_hiragana2domino()
    test_domino_csv2hiragana()
    test_domino_csv2hiragana_csv()
    test_hiragana_csv2domino()
    test_roundtrip()

    print("=" * 50)
    print("全テスト完了!")
    print("=" * 50)


if __name__ == "__main__":
    main()
