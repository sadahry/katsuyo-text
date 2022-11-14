import re

import pytest

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
    IKatsuyo,
)
from katsuyo_text.katsuyo_text import (
    FUKUJOSHI_BAKARI,
    FUKUJOSHI_HODO,
    FUKUJOSHI_KIRI,
    FUKUJOSHI_NADO,
    FUKUJOSHI_ZUTSU,
    JODOUSHI_DA_KAKO_KANRYO,
    JODOUSHI_DESU,
    JODOUSHI_MASU,
    JODOUSHI_TA,
    JUNTAIJOSHI_NN,
    JUNTAIJOSHI_NO,
    KAKUJOSHI_GA,
    KAKUJOSHI_NI,
    KAKUJOSHI_NO,
    KEIJOSHI_MO,
    KURU,
    KURU_KANJI,
    SETSUZOKUJOSHI_BA,
    SETSUZOKUJOSHI_DE,
    SETSUZOKUJOSHI_KEREDO,
    SETSUZOKUJOSHI_TE,
    SETSUZOKUJOSHI_TOMO,
    SETSUZOKUJOSHI_TSUTSU,
    SHUJOSHI_KA,
    SHUJOSHI_KASHIRA,
    SHUJOSHI_NA,
    SHUJOSHI_NO,
    SURU,
    FukushiText,
    KandoushiText,
    KatsuyoText,
    KatsuyoTextError,
    KigoText,
    SetsuzokuText,
    SettoText,
    TaigenText,
)
from katsuyo_text.katsuyo_text_helper import (
    Dantei,
    DanteiTeinei,
    Denbun,
    HikyoReizi,
    Hitei,
    KakoKanryo,
    Keizoku,
    KibouOthers,
    KibouSelf,
    Shieki,
    Suitei,
    Teinei,
    Touzen,
    Ukemi,
    Youtai,
)


@pytest.fixture(scope="session")
def unsupported_katsuyo_text():
    class UnsupportedKatsuyo(IKatsuyo):
        pass

    return KatsuyoText(
        gokan="{{gokan}}",
        katsuyo=UnsupportedKatsuyo(),
    )


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ばれる",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見られる",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="蹴",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "蹴られる",
        ),
        (
            "カ変活用",
            KURU,
            "こられる",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングされる",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重される",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んぜられる",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくなられる",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗になられる",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態になられる",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどになられる",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NO,
            "のになられる",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺になられる",
        ),
    ],
)
def test_jodoushi_ukemi(msg, katsuyo_text, expected):
    jodoushi = Ukemi()
    result = katsuyo_text + jodoushi
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
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
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
def test_jodoushi_ukemi_value_error(msg, katsuyo_text):
    jodoushi = Ukemi()
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + jodoushi
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
            "遊ばせる",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見させる",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めさせる",
        ),
        (
            "カ変活用",
            KURU,
            "こさせる",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングさせる",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重させる",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじさせる",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくさせる",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗にさせる",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態にさせる",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどにさせる",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_NO,
            "のにさせる",
        ),
        # 記号は厳密にハンドリングせずに許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺にさせる",
        ),
    ],
)
def test_jodoushi_shieki(msg, katsuyo_text, expected):
    jodoushi = Shieki()
    result = katsuyo_text + jodoushi
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
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
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
def test_jodoushi_shieki_value_error(msg, katsuyo_text):
    jodoushi = Shieki()
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + jodoushi
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
            "遊ばない",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見ない",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めない",
        ),
        (
            "カ変活用",
            KURU,
            "こない",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングしない",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重しない",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじない",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくない",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗でない",
        ),
        (
            "TaigenText",
            TaigenText("症状"),
            "症状がない",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどではない",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てはない",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のではない",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もない",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がない",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のない",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりない",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらない",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしはない",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "SettoText",
            SettoText("前々"),
            "前々ではない",
        ),
        # 文法的には微妙だが、現状は許容している
        (
            "KigoText",
            KigoText("🥺"),
            "🥺ではない",
        ),
    ],
)
def test_jodoushi_hiteii(msg, katsuyo_text, expected):
    jodoushi = Hitei()
    result = katsuyo_text + jodoushi
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
def test_jodoushi_Hitei_self_value_error(msg, katsuyo_text):
    jodoushi = Hitei()
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + jodoushi
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
            "遊びたい",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見たい",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めたい",
        ),
        (
            "カ変活用",
            KURU,
            "きたい",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングしたい",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重したい",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじたい",
        ),
    ],
)
def test_jodoushi_kibou_self(msg, katsuyo_text, expected):
    jodoushi = KibouSelf()
    result = katsuyo_text + jodoushi
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
            SHUJOSHI_NO,
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
        (
            "KigoText",
            KigoText("🥺"),
        ),
    ],
)
def test_jodoushi_kibou_self_value_error(msg, katsuyo_text):
    jodoushi = KibouSelf()
    with pytest.raises(KatsuyoTextError, match=re.compile(r"Unsupported.*")):
        katsuyo_text + jodoushi
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
            "遊びたがる",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見たがる",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めたがる",
        ),
        (
            "カ変活用",
            KURU,
            "きたがる",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングしたがる",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重したがる",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじたがる",
        ),
    ],
)
def test_jodoushi_kibou_others(msg, katsuyo_text, expected):
    jodoushi = KibouOthers()
    result = katsuyo_text + jodoushi
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
            "TaigenText",
            TaigenText("状態"),
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
            "FukujoshiText",
            FUKUJOSHI_HODO,
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
        ),
        (
            "SettoText",
            SettoText("前々"),
        ),
        (
            "KigoText",
            KigoText("🥺"),
        ),
    ],
)
def test_jodoushi_kibou_others_value_error(msg, katsuyo_text):
    jodoushi = KibouOthers()
    with pytest.raises(KatsuyoTextError, match=re.compile(r"Unsupported.*")):
        katsuyo_text + jodoushi
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
            "歩いた",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="稼",
                katsuyo=GODAN_GA_GYO,
            ),
            "稼いだ",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="話",
                katsuyo=GODAN_SA_GYO,
            ),
            "話した",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="待",
                katsuyo=GODAN_TA_GYO,
            ),
            "待った",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="死",
                katsuyo=GODAN_NA_GYO,
            ),
            "死んだ",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊んだ",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="読",
                katsuyo=GODAN_MA_GYO,
            ),
            "読んだ",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="帰",
                katsuyo=GODAN_RA_GYO,
            ),
            "帰った",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="買",
                katsuyo=GODAN_WAA_GYO,
            ),
            "買った",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="行",
                katsuyo=GODAN_IKU,
            ),
            "行った",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見た",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めた",
        ),
        (
            "カ変活用",
            KURU,
            "きた",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングした",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重した",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじた",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しかった",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗だった",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態だった",
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "でした",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ました",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどだった",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てだった",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のだった",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もだった",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がだった",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のだった",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりだった",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらだった",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしだった",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々だった",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺だった",
        ),
    ],
)
def test_jodoushi_kako_kanryo(msg, katsuyo_text, expected):
    jodoushi = KakoKanryo()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "助動詞「た」",
            JODOUSHI_TA,
        ),
    ],
)
def test_jodoushi_kako_kanryo_value_error(katsuyo_text, msg):
    jodoushi = KakoKanryo()
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + jodoushi
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
            "遊びそうだ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見そうだ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めそうだ",
        ),
        (
            "カ変活用",
            KURU,
            "きそうだ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングしそうだ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重しそうだ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじそうだ",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しそうだ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗そうだ",
        ),
        # TODO 意志推量「う」の実装
        # (
        #     "助動詞「です」",
        #     JODOUSHI_DESU,
        #     "でしょう",
        # ),
        # (
        #     "助動詞「ます」",
        #     JODOUSHI_MASU,
        #     "ましょう",
        # ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態そうだ",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどそうだ",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てそうだ",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のそうだ",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もそうだ",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がそうだ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のそうだ",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりそうだ",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらそうだ",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしそうだ",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々そうだ",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺そうだ",
        ),
    ],
)
def test_jodoushi_youtaii(msg, katsuyo_text, expected):
    jodoushi = Youtai()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, katsuyo_text",
    [
        (
            "助動詞「た」",
            JODOUSHI_TA,
        ),
        # TODO 意志推量「う」の実装
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
def test_jodoushi_Youtai_value_error(msg, katsuyo_text):
    jodoushi = Youtai()
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + jodoushi
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
            "遊ぶそうだ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るそうだ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるそうだ",
        ),
        (
            "カ変活用",
            KURU,
            "くるそうだ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするそうだ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するそうだ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるそうだ",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいそうだ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗だそうだ",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態だそうだ",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たそうだ",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですそうだ",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますそうだ",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどだそうだ",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てだそうだ",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のだそうだ",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もだそうだ",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がだそうだ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のだそうだ",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりだそうだ",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらだそうだ",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしだそうだ",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々だそうだ",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺だそうだ",
        ),
    ],
)
def test_jodoushi_denbun(msg, katsuyo_text, expected):
    jodoushi = Denbun()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_denbun_value_error(unsupported_katsuyo_text):
    jodoushi = Denbun()
    with pytest.raises(KatsuyoTextError):
        unsupported_katsuyo_text + jodoushi


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶらしい",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るらしい",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるらしい",
        ),
        (
            "カ変活用",
            KURU,
            "くるらしい",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするらしい",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するらしい",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるらしい",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいらしい",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗らしい",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態らしい",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たらしい",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですらしい",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますらしい",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどらしい",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てらしい",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のらしい",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もらしい",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がらしい",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のらしい",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりらしい",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほららしい",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしらしい",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々らしい",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺らしい",
        ),
    ],
)
def test_jodoushi_suitei(msg, katsuyo_text, expected):
    jodoushi = Suitei()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_suitei_value_error(unsupported_katsuyo_text):
    jodoushi = Suitei()
    with pytest.raises(KatsuyoTextError):
        unsupported_katsuyo_text + jodoushi


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶべきだ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るべきだ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるべきだ",
        ),
        (
            "カ変活用",
            KURU,
            "くるべきだ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするべきだ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するべきだ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるべきだ",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくあるべきだ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗であるべきだ",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態であるべきだ",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどであるべきだ",
        ),
        # 文法的に微妙だが許容する
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てであるべきだ",
        ),
        # 文法的に微妙だが許容する
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のであるべきだ",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もであるべきだ",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がであるべきだ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のであるべきだ",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりであるべきだ",
        ),
        # 文法的に微妙だが許容する
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらであるべきだ",
        ),
        # 文法的に微妙だが許容する
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしであるべきだ",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々であるべきだ",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺であるべきだ",
        ),
    ],
)
def test_jodoushi_touzen(msg, katsuyo_text, expected):
    jodoushi = Touzen()
    result = katsuyo_text + jodoushi
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
        # 文法的に微妙だが許容する
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
        ),
    ],
)
def test_jodoushi_touzen_value_error(katsuyo_text, msg):
    jodoushi = Touzen()
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + jodoushi
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
            "遊ぶようだ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るようだ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるようだ",
        ),
        (
            "カ変活用",
            KURU,
            "くるようだ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするようだ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するようだ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるようだ",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいようだ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なようだ",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態のようだ",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たようだ",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですようだ",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますようだ",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどのようだ",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てのようだ",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "ののようだ",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "ものようだ",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がのようだ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "ののようだ",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりのようだ",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらのようだ",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしのようだ",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々のようだ",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺のようだ",
        ),
    ],
)
def test_jodoushi_hikyo_reizi(msg, katsuyo_text, expected):
    jodoushi = HikyoReizi()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_hikyo_reizi_value_error(unsupported_katsuyo_text):
    jodoushi = HikyoReizi()
    with pytest.raises(KatsuyoTextError):
        unsupported_katsuyo_text + jodoushi


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶのだ",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るのだ",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるのだ",
        ),
        (
            "カ変活用",
            KURU,
            "くるのだ",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするのだ",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するのだ",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるのだ",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいのだ",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なのだ",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態だ",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たのだ",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "ですのだ",
        ),
        # 文法的に微妙だが許容する
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ますのだ",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどだ",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てだ",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のだ",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もだ",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がだ",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のだ",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりだ",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらだ",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしだ",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々だ",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺だ",
        ),
    ],
)
def test_jodoushi_dantei(msg, katsuyo_text, expected):
    jodoushi = Dantei()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_dantei_value_error(unsupported_katsuyo_text):
    jodoushi = Dantei()
    with pytest.raises(KatsuyoTextError):
        unsupported_katsuyo_text + jodoushi


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊ぶのです",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見るのです",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めるのです",
        ),
        (
            "カ変活用",
            KURU,
            "くるのです",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングするのです",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重するのです",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んずるのです",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいです",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗です",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態です",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たのです",
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "です",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ます",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどです",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てです",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のです",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もです",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がです",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のです",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりです",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらです",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしです",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々です",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺です",
        ),
    ],
)
def test_jodoushi_dantei_teinei(msg, katsuyo_text, expected):
    jodoushi = DanteiTeinei()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_dantei_teinei_value_error(unsupported_katsuyo_text):
    jodoushi = DanteiTeinei()
    with pytest.raises(KatsuyoTextError):
        unsupported_katsuyo_text + jodoushi


@pytest.mark.parametrize(
    "msg, katsuyo_text, expected",
    [
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊びます",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見ます",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めます",
        ),
        (
            "カ変活用",
            KURU,
            "きます",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングします",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重します",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじます",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しいです",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗です",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態です",
        ),
        (
            "助動詞「た」",
            JODOUSHI_TA,
            "たのです",
        ),
        (
            "助動詞「です」",
            JODOUSHI_DESU,
            "です",
        ),
        (
            "助動詞「ます」",
            JODOUSHI_MASU,
            "ます",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどです",
        ),
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
            "てです",
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
            "のです",
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
            "もです",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がです",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のです",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりです",
        ),
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらです",
        ),
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしです",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々です",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺です",
        ),
    ],
)
def test_jodoushi_teinei(msg, katsuyo_text, expected):
    jodoushi = Teinei()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_teinei_value_error(unsupported_katsuyo_text):
    jodoushi = Teinei()
    with pytest.raises(KatsuyoTextError):
        unsupported_katsuyo_text + jodoushi


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
            "歩いている",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="稼",
                katsuyo=GODAN_GA_GYO,
            ),
            "稼いでいる",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="話",
                katsuyo=GODAN_SA_GYO,
            ),
            "話している",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="待",
                katsuyo=GODAN_TA_GYO,
            ),
            "待っている",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="死",
                katsuyo=GODAN_NA_GYO,
            ),
            "死んでいる",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
            "遊んでいる",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="読",
                katsuyo=GODAN_MA_GYO,
            ),
            "読んでいる",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="帰",
                katsuyo=GODAN_RA_GYO,
            ),
            "帰っている",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="買",
                katsuyo=GODAN_WAA_GYO,
            ),
            "買っている",
        ),
        (
            "五段活用",
            KatsuyoText(
                gokan="行",
                katsuyo=GODAN_IKU,
            ),
            "行っている",
        ),
        (
            "上一段活用",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
            "見ている",
        ),
        (
            "下一段活用",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
            "求めている",
        ),
        (
            "カ変活用",
            KURU,
            "きている",
        ),
        (
            "サ変活用",
            KatsuyoText(
                gokan="ウォーキング",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "ウォーキングしている",
        ),
        (
            "サ変活用(する)",
            KatsuyoText(
                gokan="尊重",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
            "尊重している",
        ),
        (
            "サ変活用(ずる)",
            KatsuyoText(
                gokan="重ん",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
            "重んじている",
        ),
        (
            "形容詞",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
            "美しくいる",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗でいる",
        ),
        (
            "TaigenText",
            TaigenText("状態"),
            "状態でいる",
        ),
        (
            "FukujoshiText",
            FUKUJOSHI_HODO,
            "ほどでいる",
        ),
        (
            "KakujoshiText",
            KAKUJOSHI_GA,
            "がでいる",
        ),
        (
            "JuntaijoshiText",
            JUNTAIJOSHI_NO,
            "のでいる",
        ),
        (
            "FukushiText",
            FukushiText("かなり"),
            "かなりでいる",
        ),
        # 文法的に微妙だが許容する
        (
            "感動詞",
            KandoushiText("ほら"),
            "ほらでいる",
        ),
        # 文法的に微妙だが許容する
        (
            "接続詞",
            SetsuzokuText("しかし"),
            "しかしでいる",
        ),
        (
            "SettoText",
            SettoText("前々"),
            "前々でいる",
        ),
        (
            "KigoText",
            KigoText("🥺"),
            "🥺でいる",
        ),
    ],
)
def test_jodoushi_keizoku(msg, katsuyo_text, expected):
    jodoushi = Keizoku()
    result = katsuyo_text + jodoushi
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
        (
            "SetsuzokujoshiText",
            SETSUZOKUJOSHI_TE,
        ),
        (
            "ShujoshiText",
            SHUJOSHI_NO,
        ),
        (
            "KeijoshiText",
            KEIJOSHI_MO,
        ),
    ],
)
def test_jodoushi_Keizoku_value_error(msg, katsuyo_text):
    jodoushi = Keizoku()
    with pytest.raises(KatsuyoTextError):
        katsuyo_text + jodoushi
        assert False, msg
