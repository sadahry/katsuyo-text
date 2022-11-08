import re
import pytest
from katsuyo_text.katsuyo_text import (
    KURU,
    KatsuyoText,
    TaigenText,
    KatsuyoTextError,
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
    IKatsuyo,
    KAMI_ICHIDAN,
    KEIYOUDOUSHI,
    KEIYOUSHI,
    SA_GYO_HENKAKU_SURU,
    SA_GYO_HENKAKU_ZURU,
    SHIMO_ICHIDAN,
)
from katsuyo_text.katsuyo_text_helper import (
    Denbun,
    HikyoReizi,
    Hitei,
    Keizoku,
    KibouOthers,
    Shieki,
    Suitei,
    Touzen,
    Ukemi,
    KibouSelf,
    KakoKanryo,
    Youtai,
    Dantei,
    DanteiTeinei,
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
    ],
)
def test_jodoushi_ukemi(msg, katsuyo_text, expected):
    jodoushi = Ukemi()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_ukemi_value_error(unsupported_katsuyo_text):
    jodoushi = Ukemi()
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
    ],
)
def test_jodoushi_shieki(msg, katsuyo_text, expected):
    jodoushi = Shieki()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_shieki_value_error(unsupported_katsuyo_text):
    jodoushi = Shieki()
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
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態ではない",
        ),
    ],
)
def test_jodoushi_hiteii(msg, katsuyo_text, expected):
    jodoushi = Hitei()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_hitei_value_error(unsupported_katsuyo_text):
    jodoushi = Hitei()
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
            "TaigenText",
            TaigenText("状態"),
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
    ],
)
def test_jodoushi_kako_kanryo(msg, katsuyo_text, expected):
    jodoushi = KakoKanryo()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_kako_kanryo_value_error(unsupported_katsuyo_text):
    jodoushi = KakoKanryo()
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
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態そうだ",
        ),
    ],
)
def test_jodoushi_youtaii(msg, katsuyo_text, expected):
    jodoushi = Youtai()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_youtai_value_error(unsupported_katsuyo_text):
    jodoushi = Youtai()
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
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態だそうだ",
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
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態らしい",
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
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態であるべきだ",
        ),
    ],
)
def test_jodoushi_touzen(msg, katsuyo_text, expected):
    jodoushi = Touzen()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_touzen_value_error(unsupported_katsuyo_text):
    jodoushi = Touzen()
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
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態のようだ",
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
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態だ",
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
            "美しいのです",
        ),
        (
            "形容動詞",
            KatsuyoText(
                gokan="綺麗",
                katsuyo=KEIYOUDOUSHI,
            ),
            "綺麗なのです",
        ),
        # TODO 助詞のハンドリング
        (
            "TaigenText",
            TaigenText("状態"),
            "状態です",
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
    ],
)
def test_jodoushi_keizoku(msg, katsuyo_text, expected):
    jodoushi = Keizoku()
    result = katsuyo_text + jodoushi
    assert str(result) == expected, msg


def test_jodoushi_keizoku_value_error(unsupported_katsuyo_text):
    jodoushi = Keizoku()
    with pytest.raises(KatsuyoTextError):
        unsupported_katsuyo_text + jodoushi
