import pytest
from katsuyo_text.katsuyo_text import (
    FUKUJOSHI_BAKARI,
    FUKUJOSHI_HODO,
    FUKUJOSHI_KIRI,
    FUKUJOSHI_NADO,
    FUKUJOSHI_ZUTSU,
    KAKUJOSHI_NI,
    KAKUJOSHI_NO,
    KAKUJOSHI_GA,
    KEIJOSHI_MO,
    JODOUSHI_DA_KAKO_KANRYO,
    JODOUSHI_TA,
    JODOUSHI_DESU,
    JODOUSHI_MASU,
    KURU,
    KURU_KANJI,
    SHUJOSHI_KA,
    SHUJOSHI_KASHIRA,
    SHUJOSHI_NA,
    SHUJOSHI_NO,
    SETSUZOKUJOSHI_TE,
    SETSUZOKUJOSHI_DE,
    SETSUZOKUJOSHI_KEREDO,
    SETSUZOKUJOSHI_BA,
    SETSUZOKUJOSHI_TSUTSU,
    SETSUZOKUJOSHI_TOMO,
    JUNTAIJOSHI_NO,
    JUNTAIJOSHI_NN,
    SURU,
    KatsuyoText,
    KatsuyoTextError,
    TaigenText,
    FukushiText,
    SettoText,
    KandoushiText,
    SetsuzokuText,
    KigoText,
)
from katsuyo_text.katsuyo import (
    GODAN_BA_GYO,
    GODAN_GA_GYO,
    GODAN_IKU,
    GODAN_KA_GYO,
    GODAN_MA_GYO,
    GODAN_NA_GYO,
    GODAN_RA_GYO,
    GODAN_SA_GYO,
    GODAN_TA_GYO,
    GODAN_WAA_GYO,
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


# TODO KeiyoushiKatsuyo, KeiyoudoushiKatsuyo, TaKatsuyo, MasuKatsuyo, DesuKatsuyoのテスト
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
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですが",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますが",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態が",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりが",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらが",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしが",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "SettoText",
            SettoText("前々"),
            "前々が",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺が",
        ),
    ],
)
def test_KakujoshiText(msg, katsuyo_text, expected):
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
            "遊びも",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見も",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めも",
        ),
        (
            "カ変活用",
            KURU,
            "きも",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングしも",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重しも",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじも",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくも",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗でも",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態も",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほども",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "ても",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_KA,
            "かも",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
            "にも",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んも",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "FukushiText",
            FukushiText("あんまり"),
            "あんまりも",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらも",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしも",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々も",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺も",
        ),
    ],
)
def test_KeijoshiText(msg, katsuyo_text, expected):
    keijoshi = KEIJOSHI_MO
    result = katsuyo_text + keijoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "助動詞「た」",
            JODOUSHI_TA,
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
        ),
    ],
)
def test_KeijoshiText_error(msg, katsuyo_text):
    keijoshi = KEIJOSHI_MO
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + keijoshi
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
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですばかり",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますばかり",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態ばかり",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
            "めっちゃばかり",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらばかり",
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
            "でもばかり",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々ばかり",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺ばかり",
        ),
    ],
)
def test_FukujoshiRentaiText(msg, katsuyo_text, expected):
    fukujoshi = FUKUJOSHI_BAKARI
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
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですなど",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますなど",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態など",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
            "めっちゃなど",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらなど",
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
            "でもなど",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々など",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺など",
        ),
    ],
)
def test_FukujoshiGokanText(msg, katsuyo_text, expected):
    fukujoshi = FUKUJOSHI_NADO
    result = katsuyo_text + fukujoshi
    assert str(result) == expected, msg


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
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺ずつ",
        ),
    ],
)
def test_FukujoshiTaigenText(msg, katsuyo_text, expected):
    fukujoshi = FUKUJOSHI_ZUTSU
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
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_FukujoshiTaigenText_error(msg, katsuyo_text):
    fukujoshi = FUKUJOSHI_ZUTSU
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + fukujoshi
        assert False, msg


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
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺きり",
        ),
    ],
)
def test_FukujoshiKiriText(msg, katsuyo_text, expected):
    fukujoshi = FUKUJOSHI_KIRI
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
            "助動詞「です」",
            JODOUSHI_DESU,
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_FukujoshiKiriText_error(msg, katsuyo_text):
    fukujoshi = FUKUJOSHI_KIRI
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + fukujoshi
        assert False, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        # 五段活用を念入りにテスト
        (
            "五段活用",
            KatsuyoText(
                gokan="歩",
                katsuyo=GODAN_KA_GYO,
            ),
            "歩いて",
        ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="稼",
        #         katsuyo=GODAN_GA_GYO,
        #     ),
        #     "稼いで",
        # ),
        (
            "五段活用",
            KatsuyoText(
                gokan="話",
                katsuyo=GODAN_SA_GYO,
            ),
            "話して",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="待",
                katsuyo=GODAN_TA_GYO,
            ),
            "待って",
        ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="死",
        #         katsuyo=GODAN_NA_GYO,
        #     ),
        #     "死んで",
        # ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="遊",
        #         katsuyo=GODAN_BA_GYO,
        #     ),
        #     "遊んで",
        # ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="読",
        #         katsuyo=GODAN_MA_GYO,
        #     ),
        #     "読んで",
        # ),
        (
            "五段活用",
            KatsuyoText(
                gokan="帰",
                katsuyo=GODAN_RA_GYO,
            ),
            "帰って",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="買",
                katsuyo=GODAN_WAA_GYO,
            ),
            "買って",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="行",
                katsuyo=GODAN_IKU,
            ),
            "行って",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見て",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めて",
        ),
        (
            "カ変活用",
            KURU,
            "きて",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングして",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重して",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじて",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくて",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗だって",
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "でして",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "まして",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺て",
        ),
    ],
)
def test_SetuzokujoshiTeText(msg, katsuyo_text, expected):
    setsuzokujoshi = SETSUZOKUJOSHI_TE
    result = katsuyo_text + setsuzokujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="稼",
                katsuyo=GODAN_GA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="死",
                katsuyo=GODAN_NA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="読",
                katsuyo=GODAN_MA_GYO,
            ),
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
        ),
        (
            "TaigenText",
            TaigenText("それ"),
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_SetuzokujoshiTeText_error(msg, katsuyo_text):
    setsuzokujoshi = SETSUZOKUJOSHI_TE
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + setsuzokujoshi
        assert False, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        # 五段活用を念入りにテスト
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="歩",
        #         katsuyo=GODAN_KA_GYO,
        #     ),
        #     "歩いて",
        # ),
        (
            "五段活用",
            KatsuyoText(
                gokan="稼",
                katsuyo=GODAN_GA_GYO,
            ),
            "稼いで",
        ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="話",
        #         katsuyo=GODAN_SA_GYO,
        #     ),
        #     "話して",
        # ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="待",
        #         katsuyo=GODAN_TA_GYO,
        #     ),
        #     "待って",
        # ),
        (
            "五段活用",
            KatsuyoText(
                gokan="死",
                katsuyo=GODAN_NA_GYO,
            ),
            "死んで",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊んで",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="読",
                katsuyo=GODAN_MA_GYO,
            ),
            "読んで",
        ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="帰",
        #         katsuyo=GODAN_RA_GYO,
        #     ),
        #     "帰って",
        # ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="買",
        #         katsuyo=GODAN_WAA_GYO,
        #     ),
        #     "買って",
        # ),
        # (
        #     "五段活用",
        #     KatsuyoText(
        #         gokan="行",
        #         katsuyo=GODAN_IKU,
        #     ),
        #     "行って",
        # ),
        # (
        #     "上一段活用",
        #     KatsuyoText(
        #         gokan="見",
        #         katsuyo=KAMI_ICHIDAN,
        #     ),
        #     "見て",
        # ),
        # (
        #     "下一段活用",
        #     KatsuyoText(
        #         gokan="求め",
        #         katsuyo=SHIMO_ICHIDAN,
        #     ),
        #     "求めて",
        # ),
        # (
        #     "カ変活用",
        #     KURU,
        #     "きて",
        # ),
        # (
        #     "サ変活用",
        #     KatsuyoText(
        #         gokan="ウォーキング",
        #         katsuyo=SA_GYO_HENKAKU_SURU,
        #     ),
        #     "ウォーキングして",
        # ),
        # (
        #     "サ変活用(する)",
        #     KatsuyoText(
        #         gokan="尊重",
        #         katsuyo=SA_GYO_HENKAKU_SURU,
        #     ),
        #     "尊重して",
        # ),
        # (
        #     "サ変活用(ずる)",
        #     KatsuyoText(
        #         gokan="重ん",
        #         katsuyo=SA_GYO_HENKAKU_ZURU,
        #     ),
        #     "重んじて",
        # ),
        # (
        #     "形容詞",
        #     KatsuyoText(
        #         gokan="美し",
        #         katsuyo=KEIYOUSHI,
        #     ),
        #     "美しかって",
        # ),
        # (
        #     "形容動詞",
        #     KatsuyoText(
        #         gokan="綺麗",
        #         katsuyo=KEIYOUDOUSHI,
        #     ),
        #     "綺麗だって",
        # ),
        # (
        #     "助動詞「です」",
        #     JODOUSHI_DESU,
        #     "でして",
        # ),
        # (
        #     "助動詞「ます」",
        #     JODOUSHI_MASU,
        #     "まして",
        # ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺で",
        ),
    ],
)
def test_SetuzokujoshiDeText(msg, katsuyo_text, expected):
    setsuzokujoshi = SETSUZOKUJOSHI_DE
    result = katsuyo_text + setsuzokujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="歩",
                katsuyo=GODAN_KA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="話",
                katsuyo=GODAN_SA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="待",
                katsuyo=GODAN_TA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="帰",
                katsuyo=GODAN_RA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="買",
                katsuyo=GODAN_WAA_GYO,
            ),
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="行",
                katsuyo=GODAN_IKU,
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
            "助動詞「た」",
            JODOUSHI_TA,
        ),
        (
            "TaigenText",
            TaigenText("それ"),
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_SetuzokujoshiDeText_error(msg, katsuyo_text):
    setsuzokujoshi = SETSUZOKUJOSHI_DE
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + setsuzokujoshi
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
            "遊ぶけれど",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るけれど",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるけれど",
        ),
        (
            "カ変活用",
            KURU,
            "くるけれど",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするけれど",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するけれど",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるけれど",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいけれど",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗だけれど",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たけれど",
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですけれど",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますけれど",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んけれど",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺けれど",
        ),
    ],
)
def test_SetsuzokujoshiShushiText(msg, katsuyo_text, expected):
    setsuzokujoshi = SETSUZOKUJOSHI_KEREDO
    result = katsuyo_text + setsuzokujoshi
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
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_SetsuzokujoshiShushiText_error(msg, katsuyo_text):
    setsuzokujoshi = SETSUZOKUJOSHI_KEREDO
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + setsuzokujoshi
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
            "遊べば",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見れば",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めれば",
        ),
        (
            "カ変活用",
            KURU,
            "くれば",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングすれば",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重すれば",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずれば",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しければ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗ならば",
        ),
        # 聞き慣れないが文法的には正しい
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますれば",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺ば",
        ),
    ],
)
def test_SetsuzokujoshiKateiText(msg, katsuyo_text, expected):
    setsuzokujoshi = SETSUZOKUJOSHI_BA
    result = katsuyo_text + setsuzokujoshi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "助動詞「た」",
            JODOUSHI_TA,
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
        ),
        (
            "TaigenText",
            TaigenText("それ"),
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_SetsuzokujoshiKateiText_error(msg, katsuyo_text):
    setsuzokujoshi = SETSUZOKUJOSHI_BA
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + setsuzokujoshi
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
            "遊びつつ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見つつ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めつつ",
        ),
        (
            "カ変活用",
            KURU,
            "きつつ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングしつつ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重しつつ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじつつ",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺つつ",
        ),
    ],
)
def test_SetsuzokujoshiRenyoText(msg, katsuyo_text, expected):
    setsuzokujoshi = SETSUZOKUJOSHI_TSUTSU
    result = katsuyo_text + setsuzokujoshi
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
            "助動詞「た」",
            JODOUSHI_TA,
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
        ),
        (
            "TaigenText",
            TaigenText("状態"),
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_KA,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
        ),
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_SetsuzokujoshiRenyoText_error(msg, katsuyo_text):
    setsuzokujoshi = SETSUZOKUJOSHI_TSUTSU
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + setsuzokujoshi
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
            "遊ぶとも",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るとも",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるとも",
        ),
        (
            "カ変活用",
            KURU,
            "くるとも",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするとも",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するとも",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるとも",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくとも",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗だとも",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たとも",
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですとも",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますとも",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺とも",
        ),
    ],
)
def test_SetsuzokujoshiTomoText(msg, katsuyo_text, expected):
    setsuzokujoshi = SETSUZOKUJOSHI_TOMO
    result = katsuyo_text + setsuzokujoshi
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
            FUKUJOSHI_HODO,
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
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
        ),
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_SetsuzokujoshiTomoText_error(msg, katsuyo_text):
    setsuzokujoshi = SETSUZOKUJOSHI_TOMO
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + setsuzokujoshi
        assert False, msg


# TODO 接続助詞の個別テスト


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
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですの",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますの",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NN,
            "んの",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺の",
        ),
    ],
)
def test_ShujoshiYogenText(msg, katsuyo_text, expected):
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
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
    ],
)
def test_ShujoshiYogenText_error(msg, katsuyo_text):
    shujoshi = SHUJOSHI_NO
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
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですな",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますな",
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
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺な",
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
            FUKUJOSHI_HODO,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NI,
        ),
        (
            "FukushiText",
            FukushiText("めっちゃ"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
        ),
        (
            "SettoText",
            SettoText("前々"),
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
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですか",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますか",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態か",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
            "めっちゃか",
        ),
        (
            "感動詞",
            KandoushiText("んー"),
            "んーか",
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
            "でもか",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々か",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺か",
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
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですかしら",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますかしら",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態かしら",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        (
            "FukushiText",
            FukushiText("めっちゃ"),
            "めっちゃかしら",
        ),
        (
            "感動詞",
            KandoushiText("んー"),
            "んーかしら",
        ),
        (
            "接続詞",
            SetsuzokuText("でも"),
            "でもかしら",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々かしら",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺かしら",
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
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですの",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますの",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態の",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
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
        # 文法的には微妙だが、現状は許容している
        (
            "FukushiText",
            FukushiText("めっちゃ"),
            "めっちゃの",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "感動詞",
            KandoushiText("んー"),
            "んーの",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしの",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々の",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺の",
        ),
    ],
)
def test_JONTAIJOSHI(msg, katsuyo_text, expected):
    shujoshi = JUNTAIJOSHI_NO
    result = katsuyo_text + shujoshi
    assert str(result) == expected, msg
