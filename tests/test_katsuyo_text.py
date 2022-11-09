import pytest
from katsuyo_text.katsuyo_text import (
    FUKUZYOSHI_BAKARI,
    FUKUZYOSHI_DAKE,
    FUKUZYOSHI_HODO,
    FUKUZYOSHI_KA,
    FUKUZYOSHI_KIRI,
    FUKUZYOSHI_KURAI,
    FUKUZYOSHI_MADE,
    FUKUZYOSHI_NADO,
    FUKUZYOSHI_NARI,
    FUKUZYOSHI_NOMI,
    FUKUZYOSHI_YARA,
    FUKUZYOSHI_ZUTSU,
    KAKUJOSHI_NI,
    KAKUJOSHI_NO,
    KAKUJOSHI_GA,
    KEIJOSHI_MO,
    JODOUSHI_DA_KAKO_KANRYO,
    JODOUSHI_TA,
    KURU,
    KURU_KANJI,
    SHUJOSHI_KA,
    SHUJOSHI_KASHIRA,
    SHUJOSHI_NA,
    SHUJOSHI_NO,
    SHUJOSHI_NONI,
    SETSUZOKUJOSHI_TE,
    SETSUZOKUJOSHI_KEREDO,
    JUNTAIJOSHI_NO,
    JUNTAIJOSHI_NN,
    SURU,
    KatsuyoText,
    KatsuyoTextError,
    TaigenText,
)
from katsuyo_text.katsuyo import (
    GODAN_BA_GYO,
    GODAN_KA_GYO,
    GODAN_SA_GYO,
    KAMI_ICHIDAN,
    KEIYOUDOUSHI,
    KEIYOUSHI,
    SA_GYO_HENKAKU_SURU,
    SA_GYO_HENKAKU_ZURU,
    SHIMO_ICHIDAN,
)


@pytest.mark.parametrize(
    "msg, katsuyo_text1, katsuyo_text2, expected",
    [
        # NOTE: このテストではあくまで文法的なパターンを記載しているのみであり、
        #       すべてのパターンで自然な結果を返すことを保証していない。
        #
        #       たとえば「来る」＋「みる」=「来てみる」が自然だといえそうだが
        #       この加算式では「来みる」になる。
        #
        #       自然な結果の出力はIKatsuyoTextHeplerの実装方式に依存する。
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            KatsuyoText(
                gokan="歩",
                katsuyo=GODAN_KA_GYO,
            ),
            "遊び歩く",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            KatsuyoText(
                gokan="歩",
                katsuyo=GODAN_KA_GYO,
            ),
            "見歩く",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="蹴",
                katsuyo=SHIMO_ICHIDAN,
            ),
            KatsuyoText(
                gokan="飛ば",
                katsuyo=GODAN_SA_GYO,
            ),
            "蹴飛ばす",
        ),
        (
            "カ変活用",
            KURU_KANJI,
            KatsuyoText(
                gokan="すぎ",
                katsuyo=KAMI_ICHIDAN,
            ),
            "来すぎる",
        ),
        (
            "サ変活用",
            SURU,
            KatsuyoText(
                gokan="直",
                katsuyo=GODAN_SA_GYO,
            ),
            "し直す",
        ),
    ],
)
def test_add(msg, katsuyo_text1, katsuyo_text2, expected):
    assert str(katsuyo_text1 + katsuyo_text2) == expected, msg


def test_error():
    with pytest.raises(BaseException):
        KURU_KANJI + 1


# TODO KeijoshiTextTextのテストを追加
# TODO SetsuzokujoshiTextのテストを追加


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶ人",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見る人",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求める人",
        ),
        (
            "カ変活用",
            KURU,
            "くる人",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングする人",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重する人",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずる人",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しい人",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗な人",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "た人",
        ),
        (
            "TaigenText",
            TaigenText("民間"),
            "民間人",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほど人",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "て人",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "の人",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "も人",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NO,
            "の人",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "ん人",
        ),
    ],
)
def test_TAIGEN(msg, katsuyo_text, expected):
    kakujoshi = TaigenText("人")
    result = katsuyo_text + kakujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶが",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るが",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるが",
        ),
        (
            "カ変活用",
            KURU,
            "くるが",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするが",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するが",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるが",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいが",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なが",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たが",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態が",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどが",
        ),
        # 接続されるケースがあるが稀なためスキップ
        # (
        #     "SetsuzokujoshiText",
        #     SETSUZOKUJOSHI_TE,
        #     "てから",
        # ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のが",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もが",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NO,
            "のが",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んが",
        ),
    ],
)
def test_KAKUJOSHI(msg, katsuyo_text, expected):
    kakujoshi = KAKUJOSHI_GA
    result = katsuyo_text + kakujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶばかり",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るばかり",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるばかり",
        ),
        (
            "カ変活用",
            KURU,
            "くるばかり",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするばかり",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するばかり",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるばかり",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいばかり",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なばかり",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たばかり",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態ばかり",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどばかり",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てばかり",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のばかり",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にばかり",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んばかり",
        ),
    ],
)
def test_FUKUZYOSHI_BAKARI(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_BAKARI
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶまで",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るまで",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるまで",
        ),
        (
            "カ変活用",
            KURU,
            "くるまで",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするまで",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するまで",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるまで",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいまで",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なまで",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たまで",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態まで",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどまで",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てまで",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のまで",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にまで",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んまで",
        ),
    ],
)
def test_FUKUZYOSHI_MADE(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_MADE
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶだけ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るだけ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるだけ",
        ),
        (
            "カ変活用",
            KURU,
            "くるだけ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするだけ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するだけ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるだけ",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいだけ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なだけ",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "ただけ",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態だけ",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどだけ",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てだけ",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のだけ",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にだけ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んだけ",
        ),
    ],
)
def test_FUKUZYOSHI_DAKE(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_DAKE
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶほど",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るほど",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるほど",
        ),
        (
            "カ変活用",
            KURU,
            "くるほど",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするほど",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するほど",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるほど",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいほど",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なほど",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たほど",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態ほど",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_ZUTSU,
            "ずつほど",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てほど",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のほど",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にほど",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んほど",
        ),
    ],
)
def test_FUKUZYOSHI_HODO(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_HODO
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶくらい",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るくらい",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるくらい",
        ),
        (
            "カ変活用",
            KURU,
            "くるくらい",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするくらい",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するくらい",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるくらい",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいくらい",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なくらい",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たくらい",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態くらい",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどくらい",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てくらい",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のくらい",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にくらい",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んくらい",
        ),
    ],
)
def test_FUKUZYOSHI_KURAI(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_KURAI
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶなど",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るなど",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるなど",
        ),
        (
            "カ変活用",
            KURU,
            "くるなど",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするなど",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するなど",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるなど",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいなど",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗など",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たなど",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態など",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどなど",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てなど",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のなど",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "になど",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んなど",
        ),
    ],
)
def test_FUKUZYOSHI_NADO(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_NADO
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶなり",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るなり",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるなり",
        ),
        (
            "カ変活用",
            KURU,
            "くるなり",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするなり",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するなり",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるなり",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいなり",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なり",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たなり",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態なり",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどなり",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てなり",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のなり",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "になり",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んなり",
        ),
    ],
)
def test_FUKUZYOSHI_NARI(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_NARI
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶやら",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るやら",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるやら",
        ),
        (
            "カ変活用",
            KURU,
            "くるやら",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするやら",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するやら",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるやら",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいやら",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗やら",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たやら",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態やら",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどやら",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てやら",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のやら",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にやら",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んやら",
        ),
    ],
)
def test_FUKUZYOSHI_YARA(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_YARA
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶか",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るか",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるか",
        ),
        (
            "カ変活用",
            KURU,
            "くるか",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするか",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するか",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるか",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいか",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗か",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たか",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態か",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどか",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てか",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のか",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にか",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んか",
        ),
    ],
)
def test_FUKUZYOSHI_KA(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_KA
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶのみ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るのみ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるのみ",
        ),
        (
            "カ変活用",
            KURU,
            "くるのみ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするのみ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するのみ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるのみ",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいのみ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗のみ",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たのみ",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態のみ",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどのみ",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てのみ",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "ののみ",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にのみ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んのみ",
        ),
    ],
)
def test_FUKUZYOSHI_NOMI(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_NOMI
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="付",
                katsuyo=GODAN_KA_GYO,
            ),
            "付ききり",
        ),
        # 上一段活用では特殊なケースを除き、事例が存在しなかった
        # 特殊なケースであり、文語(BCCWJ)のみに見られたため対応しない
        # (
        #     "上一段活用",
        #     KatsuyoText(
        #         gokan="い",
        #         katsuyo=KAMI_ICHIDAN,
        #     ),
        #     "いるきり",
        # ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="閉め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "閉めきり",
        ),
        # カ変活用では事例が存在しなかった
        # (
        #     "カ変活用",
        #     KURU,
        #     "くるか",
        # ),
        # サ変活用では事例が存在しなかった
        # (
        #     "サ変活用",
        #     KatsuyoText(
        #         gokan="ウォーキング",
        #         katsuyo=SA_GYO_HENKAKU_SURU,
        #     ),
        #     "ウォーキングするか",
        # ),
        # (
        #     "サ変活用(する)",
        #     KatsuyoText(
        #         gokan="尊重",
        #         katsuyo=SA_GYO_HENKAKU_SURU,
        #     ),
        #     "尊重するか",
        # ),
        # (
        #     "サ変活用(ずる)",
        #     KatsuyoText(
        #         gokan="重ん",
        #         katsuyo=SA_GYO_HENKAKU_ZURU,
        #     ),
        #     "重んずるか",
        # ),
        (
            "JodoushiText",
            JODOUSHI_TA,
            "たきり",  # e.g. 寝たきり
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てきり",
        ),
        (
            "JodoushiText",
            JODOUSHI_DA_KAKO_KANRYO,
            "だきり",  # e.g. 遊んだきり
        ),
        (
            "TaigenText",
            TaigenText("ひとり"),
            "ひとりきり",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んきり",
        ),
    ],
)
def test_FUKUZYOSHI_KIRI(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_KIRI
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NA,
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
        ),
    ],
)
def test_FUKUZYOSHI_KIRI_error(msg, katsuyo_text):
    fukujoshi = FUKUZYOSHI_KIRI
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + fukujoshi
        assert False, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "TaigenText",
            TaigenText("２個"),
            "２個ずつ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んずつ",
        ),
    ],
)
def test_FUKUZYOSHI_ZUTSU(msg, katsuyo_text, expected):
    fukujoshi = FUKUZYOSHI_ZUTSU
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "カ変活用",
            KURU,
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NA,
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
        ),
    ],
)
def test_FUKUZYOSHI_ZUTSU_error(msg, katsuyo_text):
    fukujoshi = FUKUZYOSHI_ZUTSU
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + fukujoshi
        assert False, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶの",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るの",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるの",
        ),
        (
            "カ変活用",
            KURU,
            "くるの",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするの",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するの",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるの",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいの",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なの",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たの",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んの",
        ),
    ],
)
def test_SHUJOSHI_NO(msg, katsuyo_text, expected):
    shujoshi = SHUJOSHI_NO
    result = katsuyo_text + shujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "TaigenText",
            TaigenText("それ"),
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NA,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
        ),
    ],
)
def test_SHUJOSHI_NO_error(msg, katsuyo_text):
    fukujoshi = SHUJOSHI_NO
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + fukujoshi
        assert False, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶのに",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るのに",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるのに",
        ),
        (
            "カ変活用",
            KURU,
            "くるのに",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするのに",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するのに",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるのに",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいのに",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なのに",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たのに",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んのに",
        ),
    ],
)
def test_SHUJOSHI_NONI(msg, katsuyo_text, expected):
    shujoshi = SHUJOSHI_NONI
    result = katsuyo_text + shujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "TaigenText",
            TaigenText("それ"),
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NA,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
        ),
    ],
)
def test_SHUJOSHI_NONI_error(msg, katsuyo_text):
    fukujoshi = SHUJOSHI_NONI
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + fukujoshi
        assert False, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶな",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るな",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるな",
        ),
        (
            "カ変活用",
            KURU,
            "くるな",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするな",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するな",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるな",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいな",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗だな",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たな",
        ),
        # NOTE: 現代語の表現として存在しうるが、
        #       取得する手段がなく、特殊なケースであるためサポートしない
        # # text = それな
        # 1       それ    それ    PRON    代名詞  _       0       root    _       SpaceAfter=No|BunsetuBILabel=B|BunsetuPositionType=ROOT|NP_B|Reading=ソレ
        # 2       な      だ      PART    助動詞  _       1       mark    _       SpaceAfter=No|BunsetuBILabel=I|BunsetuPositionType=SYN_HEAD|Inf=助動詞-ダ,連体形-一般|Reading=ナ
        # (
        #     "TaigenText",
        #     TaigenText("それ"),
        #     "それな",
        # ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_KEREDO,
            "けれどな",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もな",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んな",
        ),
    ],
)
def test_SHUJOSHI_NA(msg, katsuyo_text, expected):
    shujoshi = SHUJOSHI_NA
    result = katsuyo_text + shujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "TaigenText",
            TaigenText("状態"),
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
        ),
    ],
)
def test_SHUJOSHI_NA_error(msg, katsuyo_text):
    shujoshi = SHUJOSHI_NA
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + shujoshi
        assert False, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶか",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るか",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるか",
        ),
        (
            "カ変活用",
            KURU,
            "くるか",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするか",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するか",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるか",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいか",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗か",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たか",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態か",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどか",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のか",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もか",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にか",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んか",
        ),
    ],
)
def test_SHUJOSHI_KA(msg, katsuyo_text, expected):
    shujoshi = SHUJOSHI_KA
    result = katsuyo_text + shujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶかしら",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るかしら",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるかしら",
        ),
        (
            "カ変活用",
            KURU,
            "くるかしら",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするかしら",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するかしら",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるかしら",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいかしら",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗かしら",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たかしら",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態かしら",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどかしら",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のかしら",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もかしら",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にかしら",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んかしら",
        ),
    ],
)
def test_SHUJOSHI_KASHIRA(msg, katsuyo_text, expected):
    shujoshi = SHUJOSHI_KASHIRA
    result = katsuyo_text + shujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶの",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るの",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるの",
        ),
        (
            "カ変活用",
            KURU,
            "くるの",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするの",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するの",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるの",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいの",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なの",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たの",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態の",
        ),
        (
            "FukujoshiText",
            FUKUZYOSHI_HODO,
            "ほどの",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のの",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もの",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にの",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んの",
        ),
    ],
)
def test_JONTAIJOSHI(msg, katsuyo_text, expected):
    shujoshi = JUNTAIJOSHI_NO
    result = katsuyo_text + shujoshi
    assert str(result) == expected, msg
