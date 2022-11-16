from typing import NewType
import attrs

DAN = {
    "あ": ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ", "が", "ざ", "だ", "ば", "ぱ"],
    "い": ["い", "き", "し", "ち", "に", "ひ", "み", "り", "ぎ", "じ", "ぢ", "び", "ぴ"],
    "う": ["う", "く", "す", "つ", "ぬ", "ふ", "む", "ゆ", "る", "ぐ", "ず", "づ", "ぶ", "ぷ"],
    "え": ["え", "け", "せ", "て", "ね", "へ", "め", "れ", "げ", "ぜ", "で", "べ", "ぺ"],
    "お": ["お", "こ", "そ", "と", "の", "ほ", "も", "よ", "ろ", "を", "ご", "ぞ", "ど", "ぼ", "ぽ"],
}

GYO = {
    "あ": ["あ", "い", "う", "え", "お"],
    "か": ["か", "き", "く", "け", "こ"],
    "さ": ["さ", "し", "す", "せ", "そ"],
    "た": ["た", "ち", "つ", "て", "と"],
    "な": ["な", "に", "ぬ", "ね", "の"],
    "は": ["は", "ひ", "ふ", "へ", "ほ"],
    "ま": ["ま", "み", "む", "め", "も"],
    "や": ["や", "ゆ", "よ"],
    "ら": ["ら", "り", "る", "れ", "ろ"],
    "わ": ["わ", "を"],
    "が": ["が", "ぎ", "ぐ", "げ", "ご"],
    "ざ": ["ざ", "じ", "ず", "ぜ", "ぞ"],
    "だ": ["だ", "ぢ", "づ", "で", "ど"],
    "ば": ["ば", "び", "ぶ", "べ", "ぼ"],
    "ぱ": ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
}


# ==============================================================================
# 活用系ベース
# ==============================================================================


class IKatsuyo:
    pass


FixedKatsuyo = NewType("FixedKatsuyo", str)
NO_KATSUYO = FixedKatsuyo("")


class IKatsuyoForm:
    pass


@attrs.define(frozen=True, slots=False)
class MizenMixin(IKatsuyoForm):
    """未然形"""

    mizen: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class RenyoMixin(IKatsuyoForm):
    """連用形"""

    renyo: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class ShushiMixin(IKatsuyoForm):
    """終止形"""

    shushi: FixedKatsuyo

    def __str__(self) -> str:
        return self.shushi


@attrs.define(frozen=True, slots=False)
class RentaiMixin(IKatsuyoForm):
    """連体形"""

    rentai: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class KateiMixin(IKatsuyoForm):
    """
    仮定形
    已然形(izen)は仮定形に含める
    """

    katei: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class MeireiMixin(IKatsuyoForm):
    """命令形"""

    meirei: FixedKatsuyo


# 特殊な活用系


@attrs.define(frozen=True, slots=False)
class MizenUMixin(IKatsuyoForm):
    """
    未然形が意思・推量の語尾（あるいは助動詞）の
    「う」に続くとき、活用語尾が変化する活用形が存在する。
    """

    mizen_u: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class MizenReruMixin(IKatsuyoForm):
    """
    未然形が受身の「れる」使役の「せる」に続くとき、
    活用語尾が変化する活用形が存在する。
    """

    mizen_reru: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class MizenRareruMixin(IKatsuyoForm):
    """
    未然形が受身の「られる」や否定の「ぬ」に続くとき、
    活用語尾が変化する活用形が存在する。
    """

    mizen_rareru: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class RenyoTaMixin(IKatsuyoForm):
    """
    連用形に「た・て」などが続くとき、
    活用語尾が変化する活用形が存在する。
    """

    renyo_ta: FixedKatsuyo


@attrs.define(frozen=True, slots=False)
class RenyoNaiMixin(IKatsuyoForm):
    """
    連用形に「ない」などが続くとき、
    活用語尾が変化する活用形が存在する。
    """

    renyo_nai: FixedKatsuyo


# ==============================================================================
# 動詞ベース
# ==============================================================================


@attrs.define(frozen=True, slots=False)
class IDoushiKatsuyo(
    IKatsuyo,
    MizenMixin,
    RenyoMixin,
    ShushiMixin,
    RentaiMixin,
    KateiMixin,
    MeireiMixin,
):
    pass


# ==============================================================================
# 動詞::五段活用
# see: https://ja.wikipedia.org/wiki/五段活用
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class GodanKatsuyo(
    IDoushiKatsuyo,
    # 「う」の場合、オ段となる
    MizenUMixin,
    RenyoTaMixin,
):
    pass


# カ行
GODAN_KA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("か"),
    mizen_u=FixedKatsuyo("こ"),
    renyo=FixedKatsuyo("き"),
    renyo_ta=FixedKatsuyo("い"),
    shushi=FixedKatsuyo("く"),
    rentai=FixedKatsuyo("く"),
    katei=FixedKatsuyo("け"),
    meirei=FixedKatsuyo("け"),
)

# ガ行
GODAN_GA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("が"),
    mizen_u=FixedKatsuyo("ご"),
    renyo=FixedKatsuyo("ぎ"),
    renyo_ta=FixedKatsuyo("い"),
    shushi=FixedKatsuyo("ぐ"),
    rentai=FixedKatsuyo("ぐ"),
    katei=FixedKatsuyo("げ"),
    meirei=FixedKatsuyo("げ"),
)

# サ行
GODAN_SA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("さ"),
    mizen_u=FixedKatsuyo("そ"),
    renyo=FixedKatsuyo("し"),
    renyo_ta=FixedKatsuyo("し"),
    shushi=FixedKatsuyo("す"),
    rentai=FixedKatsuyo("す"),
    katei=FixedKatsuyo("せ"),
    meirei=FixedKatsuyo("せ"),
)

# タ行
GODAN_TA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("た"),
    mizen_u=FixedKatsuyo("と"),
    renyo=FixedKatsuyo("ち"),
    renyo_ta=FixedKatsuyo("っ"),
    shushi=FixedKatsuyo("つ"),
    rentai=FixedKatsuyo("つ"),
    katei=FixedKatsuyo("て"),
    meirei=FixedKatsuyo("て"),
)

# ナ行
GODAN_NA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("な"),
    mizen_u=FixedKatsuyo("の"),
    renyo=FixedKatsuyo("に"),
    renyo_ta=FixedKatsuyo("ん"),
    shushi=FixedKatsuyo("ぬ"),
    rentai=FixedKatsuyo("ぬ"),
    katei=FixedKatsuyo("ね"),
    meirei=FixedKatsuyo("ね"),
)

# バ行
GODAN_BA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("ば"),
    mizen_u=FixedKatsuyo("ぼ"),
    renyo=FixedKatsuyo("び"),
    renyo_ta=FixedKatsuyo("ん"),
    shushi=FixedKatsuyo("ぶ"),
    rentai=FixedKatsuyo("ぶ"),
    katei=FixedKatsuyo("べ"),
    meirei=FixedKatsuyo("べ"),
)

# マ行
GODAN_MA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("ま"),
    mizen_u=FixedKatsuyo("も"),
    renyo=FixedKatsuyo("み"),
    renyo_ta=FixedKatsuyo("ん"),
    shushi=FixedKatsuyo("む"),
    rentai=FixedKatsuyo("む"),
    katei=FixedKatsuyo("め"),
    meirei=FixedKatsuyo("め"),
)

# ラ行
GODAN_RA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("ら"),
    mizen_u=FixedKatsuyo("ろ"),
    renyo=FixedKatsuyo("り"),
    renyo_ta=FixedKatsuyo("っ"),
    shushi=FixedKatsuyo("る"),
    rentai=FixedKatsuyo("る"),
    katei=FixedKatsuyo("れ"),
    meirei=FixedKatsuyo("れ"),
)

# ワア行
GODAN_WAA_GYO = GodanKatsuyo(
    mizen=FixedKatsuyo("わ"),
    mizen_u=FixedKatsuyo("お"),
    renyo=FixedKatsuyo("い"),
    renyo_ta=FixedKatsuyo("っ"),
    shushi=FixedKatsuyo("う"),
    rentai=FixedKatsuyo("う"),
    katei=FixedKatsuyo("え"),
    meirei=FixedKatsuyo("え"),
)

# 「行く」は特殊な活用形を持つ。
GODAN_IKU = GodanKatsuyo(
    mizen=FixedKatsuyo("か"),
    mizen_u=FixedKatsuyo("こ"),
    renyo=FixedKatsuyo("き"),
    renyo_ta=FixedKatsuyo("っ"),
    shushi=FixedKatsuyo("く"),
    rentai=FixedKatsuyo("く"),
    katei=FixedKatsuyo("け"),
    meirei=FixedKatsuyo("け"),
)

# ==============================================================================
# 動詞::上一段活用
# see: https://ja.wikipedia.org/wiki/上一段活用
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class KamiIchidanKatsuyo(
    # 命令形「-○よ」は登録しない
    # 「-○ろ」のほうが口語的だと判断
    IDoushiKatsuyo,
):
    pass


KAMI_ICHIDAN = KamiIchidanKatsuyo(
    mizen=FixedKatsuyo(""),
    renyo=FixedKatsuyo(""),
    shushi=FixedKatsuyo("る"),
    rentai=FixedKatsuyo("る"),
    katei=FixedKatsuyo("れ"),
    meirei=FixedKatsuyo("ろ"),
)

# ==============================================================================
# 動詞::下一段活用
# see: https://ja.wikipedia.org/wiki/下一段活用
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class ShimoIchidanKatsuyo(
    # 命令形「-○よ」は登録しない
    # 「-○ろ」のほうが口語的だと判断
    IDoushiKatsuyo,
):
    pass


SHIMO_ICHIDAN = ShimoIchidanKatsuyo(
    mizen=FixedKatsuyo(""),
    renyo=FixedKatsuyo(""),
    shushi=FixedKatsuyo("る"),
    rentai=FixedKatsuyo("る"),
    katei=FixedKatsuyo("れ"),
    meirei=FixedKatsuyo("ろ"),
)

# ==============================================================================
# 動詞::カ行変格活用
# see: https://ja.wikipedia.org/wiki/カ行変格活用
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class KaGyoHenkakuKatsuyo(
    IDoushiKatsuyo,
):
    pass


# 「くる」のみ特殊な活用形を持つ。
KA_GYO_HENKAKU_KURU = KaGyoHenkakuKatsuyo(
    mizen=FixedKatsuyo("こ"),
    renyo=FixedKatsuyo("き"),
    shushi=FixedKatsuyo("くる"),
    rentai=FixedKatsuyo("くる"),
    katei=FixedKatsuyo("くれ"),
    meirei=FixedKatsuyo("こい"),
)

# 「来る」と「くる」を区別
# TODO ReadingをKatsuyoに含める際には語幹から「来」を除く
KA_GYO_HENKAKU_KURU_KANJI = KaGyoHenkakuKatsuyo(
    mizen=FixedKatsuyo(""),
    renyo=FixedKatsuyo(""),
    shushi=FixedKatsuyo("る"),
    rentai=FixedKatsuyo("る"),
    katei=FixedKatsuyo("れ"),
    meirei=FixedKatsuyo("い"),
)

# ==============================================================================
# 動詞::サ行変格活用
# see: https://ja.wikipedia.org/wiki/サ行変格活用
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class SaGyoHenkakuKatsuyo(
    # 命令形「せよ」は登録しない
    # 「しろ」のほうが口語的だと判断
    IDoushiKatsuyo,
    MizenReruMixin,
    MizenRareruMixin,
):
    pass


# 「〜する」の特殊な活用形
# e.g. 愛（あい）する
SA_GYO_HENKAKU_SURU = SaGyoHenkakuKatsuyo(
    mizen=FixedKatsuyo("し"),
    mizen_reru=FixedKatsuyo("さ"),
    mizen_rareru=FixedKatsuyo("せ"),
    renyo=FixedKatsuyo("し"),
    shushi=FixedKatsuyo("する"),
    rentai=FixedKatsuyo("する"),
    katei=FixedKatsuyo("すれ"),
    meirei=FixedKatsuyo("しろ"),
)

# 「〜ずる」の特殊な活用形
# e.g. 生（しょう）ずる
SA_GYO_HENKAKU_ZURU = SaGyoHenkakuKatsuyo(
    mizen=FixedKatsuyo("じ"),
    mizen_reru=FixedKatsuyo("ざ"),
    mizen_rareru=FixedKatsuyo("ぜ"),
    renyo=FixedKatsuyo("じ"),
    shushi=FixedKatsuyo("ずる"),
    rentai=FixedKatsuyo("ずる"),
    katei=FixedKatsuyo("ずれ"),
    meirei=FixedKatsuyo("じろ"),
)


# ==============================================================================
# 形容詞
# see: https://www.kokugobunpou.com/用言/形容詞-2-活用/#gsc.tab=0
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class KeiyoushiKatsuyo(
    IKatsuyo,
    MizenMixin,
    RenyoMixin,
    RenyoTaMixin,
    ShushiMixin,
    RentaiMixin,
    KateiMixin,
    # NO: MeireiMixin,
):
    pass


KEIYOUSHI = KeiyoushiKatsuyo(
    mizen=FixedKatsuyo("かろ"),
    renyo=FixedKatsuyo("く"),
    renyo_ta=FixedKatsuyo("かっ"),
    shushi=FixedKatsuyo("い"),
    rentai=FixedKatsuyo("い"),
    katei=FixedKatsuyo("けれ"),
)

# ==============================================================================
# 形容動詞
# see: https://www.kokugobunpou.com/用言/形容動詞-2-活用/#gsc.tab=0
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class KeiyoudoushiKatsuyo(
    IKatsuyo,
    MizenMixin,
    RenyoMixin,
    RenyoTaMixin,
    RenyoNaiMixin,
    ShushiMixin,
    RentaiMixin,
    KateiMixin,
    # NO: MeireiMixin,
):
    pass


KEIYOUDOUSHI = KeiyoudoushiKatsuyo(
    mizen=FixedKatsuyo("だろ"),
    # NOTE: 活用としては形容動詞の連用形は「で」が正しいが、
    #       動詞との紐付きや「させる」等の助動詞の活用との関係から「に」を採用
    renyo=FixedKatsuyo("に"),
    renyo_ta=FixedKatsuyo("だっ"),
    renyo_nai=FixedKatsuyo("で"),
    shushi=FixedKatsuyo("だ"),
    rentai=FixedKatsuyo("な"),
    katei=FixedKatsuyo("なら"),
)

# ==============================================================================
# 助動詞ベース
# see: https://ja.wikipedia.org/wiki/助動詞_(国文法)
# ==============================================================================


@attrs.define(frozen=True, slots=False)
class IJodoushiKatsuyo(IKatsuyo):
    """
    このクラスは助動詞の活用形を表すクラスではなく、
    特殊な活用であることを表すクラスである。
    """

    pass


# ==============================================================================
# 助動詞「た」「だ」
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class TaKatsuyo(
    IJodoushiKatsuyo,
    MizenMixin,
    # NO: RenyoMixin,
    ShushiMixin,
    RentaiMixin,
    KateiMixin,
    # NO: MeireiMixin,
):
    pass


JODOUSHI_TA = TaKatsuyo(
    mizen=FixedKatsuyo("たろ"),
    shushi=FixedKatsuyo("た"),
    rentai=FixedKatsuyo("た"),
    katei=FixedKatsuyo("たら"),
)

JODOUSHI_DA_KAKO_KANRYO = TaKatsuyo(
    mizen=FixedKatsuyo("だろ"),
    shushi=FixedKatsuyo("だ"),
    rentai=FixedKatsuyo("だ"),
    katei=FixedKatsuyo("だら"),
)


@attrs.define(frozen=True, slots=True)
class MasuKatsuyo(
    IJodoushiKatsuyo,
    MizenMixin,
    MizenUMixin,
    RenyoMixin,
    ShushiMixin,
    RentaiMixin,
    KateiMixin,
    MeireiMixin,
    # 命令形「まし」は登録しない
    # 「ませ」のほうが口語的だと判断
):
    pass


JODOUSHI_MASU = MasuKatsuyo(
    mizen=FixedKatsuyo("せ"),
    mizen_u=FixedKatsuyo("しょ"),
    renyo=FixedKatsuyo("し"),
    shushi=FixedKatsuyo("す"),
    rentai=FixedKatsuyo("す"),
    katei=FixedKatsuyo("すれ"),
    meirei=FixedKatsuyo("せ"),
)


@attrs.define(frozen=True, slots=True)
class DesuKatsuyo(
    IJodoushiKatsuyo,
    MizenMixin,
    RenyoMixin,
    ShushiMixin,
    RentaiMixin,
    # NO: KateiMixin,
    # NO: MeireiMixin,
):
    pass


JODOUSHI_DESU = DesuKatsuyo(
    mizen=FixedKatsuyo("しょ"),
    renyo=FixedKatsuyo("し"),
    shushi=FixedKatsuyo("す"),
    rentai=FixedKatsuyo("す"),
)
