from typing import Optional, Union, TypeVar, Generic, NewType
import attrs
import abc
import katsuyo_text.katsuyo as k

A = TypeVar(
    "A",
    "KatsuyoText",
    "FixedKatsuyoText",
    # 以下はINonKatsuyoTextの実装クラス
    "KakujoshiText",
    "KeijoshiText",
    "TaigenText",
    "FukujoshiText",
    "SetsuzokujoshiText",
    "ShujoshiText",
    "JuntaijoshiText",
)
M = TypeVar(
    "M",
    "KatsuyoText",
    "FixedKatsuyoText",
    # 以下はINonKatsuyoTextの実装クラス
    "KakujoshiText",
    "KeijoshiText",
    "TaigenText",
    "FukujoshiText",
    "SetsuzokujoshiText",
    "ShujoshiText",
    "JuntaijoshiText",
)


class KatsuyoTextError(ValueError):
    pass


KatsuyoTextErrorMessage = NewType("KatsuyoTextErrorMessage", str)
KatsuyoTextHasError = NewType("KatsuyoTextHasError", bool)


@attrs.define(frozen=True, slots=False)
class IKatsuyoTextSource(abc.ABC):
    """活用系テキスト"""

    gokan: str
    katsuyo: Union[
        k.IKatsuyo,  # KatsuyoText
        k.FixedKatsuyo,  # FixedKatsuyoText
        None,  # INonKatsuyoText
    ]

    @abc.abstractmethod
    def __add__(self, post: "IKatsuyoTextAppendant[A]") -> A:
        # NOTE: postを保持しておいて文字列化する際に再帰呼び出し的にしてもいいかもしれない
        #       ただadd時のエラーがわかりにくくなるので現状は都度gokanに追記するようにしている
        raise NotImplementedError()


class IKatsuyoTextAppendant(abc.ABC, Generic[M]):
    """
    IKatsuyoTextSourceに追加する要素を表す。
    あくまでIKatsuyoTextSourceへaddするためのインターフェースであり、
    このインターフェースを実装したクラスへaddすることはできない。
    """

    @abc.abstractmethod
    def merge(self, pre: IKatsuyoTextSource) -> M:
        raise NotImplementedError()


@attrs.define(frozen=True, slots=True)
class KatsuyoText(IKatsuyoTextSource, IKatsuyoTextAppendant["KatsuyoText"]):
    """
    活用形を含む動詞,形容詞,形容動詞,副詞の表現を表すクラス。用言を表す。
    """

    gokan: str
    katsuyo: k.IKatsuyo

    def merge(self, pre: IKatsuyoTextSource) -> "KatsuyoText":
        """
        基本的には連用形で受けるが、下位クラスで上書きすることで
        任意の活用形に変換して返すことがある。
        """
        if isinstance(pre, FixedKatsuyoText):
            return pre + self
        elif isinstance(pre, INonKatsuyoText):
            # 簡単のため、INonKatsuyoTextはすべて許容とする
            # 助詞「だ」など不適切なものもあるが現状管理しない
            return pre + self
        else:
            assert isinstance(pre, KatsuyoText)
            if (fkt := pre.as_fkt_renyo) is not None:
                return fkt + self

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )

    def __add__(self, post: IKatsuyoTextAppendant[A]) -> A:
        # 日本語の特性上、KatsuyoTextの活用形は前に接続される品詞の影響を受ける。
        return post.merge(self)

    @property
    def as_fkt_gokan(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.MizenMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=k.NO_KATSUYO,
            )
        return None

    @property
    def as_fkt_mizen(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.MizenMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.mizen,
            )
        return None

    @property
    def as_fkt_renyo(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.RenyoMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.renyo,
            )
        return None

    @property
    def as_fkt_shushi(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.ShushiMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.shushi,
            )
        return None

    @property
    def as_fkt_rentai(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.RentaiMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.rentai,
            )
        return None

    @property
    def as_fkt_katei(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.KateiMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.katei,
            )
        return None

    @property
    def as_fkt_meirei(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.MeireiMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.meirei,
            )
        return None

    @property
    def as_fkt_mizen_u(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.MizenUMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.mizen_u,
            )
        return None

    @property
    def as_fkt_mizen_reru(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.MizenReruMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.mizen_reru,
            )
        return None

    @property
    def as_fkt_mizen_rareru(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.MizenRareruMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.mizen_rareru,
            )
        return None

    @property
    def as_fkt_renyo_ta(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.RenyoTaMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.renyo_ta,
            )
        return None

    @property
    def as_fkt_renyo_nai(self) -> Optional["FixedKatsuyoText"]:
        if isinstance(self.katsuyo, k.RenyoNaiMixin):
            return FixedKatsuyoText(
                gokan=self.gokan,
                katsuyo=self.katsuyo.renyo_nai,
            )
        return None

    def __str__(self):
        return f"{self.gokan}{self.katsuyo}"


@attrs.define(frozen=True, slots=True)
class FixedKatsuyoText(IKatsuyoTextSource):
    """
    活用変形されたKatsuyoTextを格納するクラス。用言を表す。
    """

    gokan: str
    katsuyo: k.FixedKatsuyo

    def __add__(self, post: IKatsuyoTextAppendant[A]) -> A:
        if isinstance(post, KatsuyoText):
            return KatsuyoText(
                gokan=str(self) + post.gokan,
                katsuyo=post.katsuyo,
            )
        else:
            return post.merge(self)

    def __str__(self):
        return f"{self.gokan}{self.katsuyo}"


@attrs.define(frozen=True, slots=False)
class INonKatsuyoText(IKatsuyoTextSource):
    """
    活用形を含まない文字列を表すクラス。
    名詞,助詞,接続詞,感動詞,記号,連体詞,接頭辞,接尾辞,補助記号,フィラー,
    その他,そのままKatsuyoTextにaddする品詞を想定。
    """

    gokan: str
    katsuyo: None = None

    def __add__(self, post: IKatsuyoTextAppendant[A]) -> A:
        if isinstance(post, KatsuyoText):
            return KatsuyoText(
                gokan=str(self) + post.gokan,
                katsuyo=post.katsuyo,
            )
        else:
            return post.merge(self)

    def __str__(self):
        return self.gokan


# ==============================================================================
# KatsuyoText
# TODO 別ファイルに分割する
# ==============================================================================

# ==============================================================================
# 動詞
# ==============================================================================

KURU = KatsuyoText(
    gokan="",
    katsuyo=k.KA_GYO_HENKAKU_KURU,
)

KURU_KANJI = KatsuyoText(
    gokan="来",
    katsuyo=k.KA_GYO_HENKAKU_KURU_KANJI,
)

SURU = KatsuyoText(
    gokan="",
    katsuyo=k.SA_GYO_HENKAKU_SURU,
)

ZURU = KatsuyoText(
    gokan="",
    katsuyo=k.SA_GYO_HENKAKU_ZURU,
)


# ==============================================================================
# 補助動詞/補助形容詞
# see:https://www.kokugobunpou.com/用言/補助動詞-補助形容詞
# ==============================================================================


class HojoKatsuyoText(KatsuyoText):
    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self
        elif isinstance(pre, INonKatsuyoText):
            if isinstance(pre, KakujoshiText):
                # TODO 助詞の精査
                return pre + self

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
                    pre.katsuyo.shushi in ["ぐ", "ぬ", "ぶ", "む"]
                ):
                    return pre + DaKakoKanryo() + self
                return pre + Ta() + self
            elif isinstance(pre.katsuyo, k.KeiyoushiKatsuyo):
                assert (fkt := pre.as_fkt_renyo) is not None
                return fkt + self
            elif isinstance(pre.katsuyo, k.KeiyoudoushiKatsuyo):
                assert (fkt := pre.as_fkt_renyo_nai) is not None
                return fkt + self

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


HOJO_NAI = HojoKatsuyoText(
    gokan="な",
    katsuyo=k.KEIYOUSHI,
)

HOJO_ARU = HojoKatsuyoText(
    gokan="あ",
    katsuyo=k.GODAN_RA_GYO,
)

HOJO_IRU = HojoKatsuyoText(
    gokan="い",
    katsuyo=k.KAMI_ICHIDAN,
)

# ==============================================================================
# 助動詞
# see: https://ja.wikipedia.org/wiki/助動詞_(国文法)
# ==============================================================================


class IJodoushiKatsuyoText(KatsuyoText):
    @property
    def katsuyo_text(self) -> KatsuyoText:
        return KatsuyoText(
            gokan=self.gokan,
            katsuyo=self.katsuyo,
        )


# ==============================================================================
# 助動詞::受身
# ==============================================================================


class Reru(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="れ",
            katsuyo=k.SHIMO_ICHIDAN,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                if isinstance(pre.katsuyo, k.SaGyoHenkakuKatsuyo):
                    assert (fkt := pre.as_fkt_mizen_reru) is not None
                    return fkt + self.katsuyo_text
                assert (fkt := pre.as_fkt_mizen) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


class Rareru(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="られ",
            katsuyo=k.SHIMO_ICHIDAN,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                if isinstance(pre.katsuyo, k.SaGyoHenkakuKatsuyo):
                    assert (fkt := pre.as_fkt_mizen_rareru) is not None
                    return fkt + self.katsuyo_text
                assert (fkt := pre.as_fkt_mizen) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_RERU = Reru()
JODOUSHI_RARERU = Rareru()

# ==============================================================================
# 助動詞::使役
# ==============================================================================


class Seru(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="せ",
            katsuyo=k.SHIMO_ICHIDAN,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                if isinstance(pre.katsuyo, k.SaGyoHenkakuKatsuyo):
                    assert (fkt := pre.as_fkt_mizen_reru) is not None
                    return fkt + self.katsuyo_text
                assert (fkt := pre.as_fkt_mizen) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


SASERU = KatsuyoText(
    gokan="させ",
    katsuyo=k.SHIMO_ICHIDAN,
)


class Saseru(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan=SASERU.gokan,
            katsuyo=SASERU.katsuyo,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                # サ変活用「〜ずる」には未然形「〜じ させる」を採用したため他と同一の未然形に
                assert (fkt := pre.as_fkt_mizen) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_SERU = Seru()
JODOUSHI_SASERU = Saseru()

# ==============================================================================
# 助動詞::否定
# ==============================================================================


class Nai(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="な",
            katsuyo=k.KEIYOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                assert (fkt := pre.as_fkt_mizen) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_NAI = Nai()

# ==============================================================================
# 助動詞::希望
# ==============================================================================


class Tai(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="た",
            katsuyo=k.KEIYOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                assert (fkt := pre.as_fkt_renyo) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


class Tagaru(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="たが",
            katsuyo=k.GODAN_RA_GYO,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                assert (fkt := pre.as_fkt_renyo) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_TAI = Tai()
JODOUSHI_TAGARU = Tagaru()

# ==============================================================================
# 助動詞::過去・完了
# ==============================================================================


class Ta(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="",
            katsuyo=k.JODOUSHI_TA,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            # TODO 「だ」となりうる語の除外とテストコード追加
            # if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
            #     pre.katsuyo.shushi in ["ぐ", "ぬ", "ぶ", "む"]
            # ):
            #     raise KatsuyoTextError(
            #         f"Should be 「だ」: {pre} "
            #         f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            #     )

            if (fkt := pre.as_fkt_renyo_ta) is not None:
                return fkt + self.katsuyo_text
            elif (fkt := pre.as_fkt_renyo) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


class DaKakoKanryo(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="",
            katsuyo=k.JODOUSHI_DA_KAKO_KANRYO,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            # TODO 「た」となりうる語の除外とテストコード追加
            # if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
            #     pre.katsuyo.shushi not in ["ぐ", "ぬ", "ぶ", "む"]
            # ):
            #     raise KatsuyoTextError(
            #         f"Should be 「た」: {pre} "
            #         f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            #     )

            if (fkt := pre.as_fkt_renyo_ta) is not None:
                return fkt + self.katsuyo_text
            elif (fkt := pre.as_fkt_renyo) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_TA = Ta()
JODOUSHI_DA_KAKO_KANRYO = DaKakoKanryo()


# ==============================================================================
# 助動詞::丁寧
# ==============================================================================


class Masu(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="ま",
            katsuyo=k.JODOUSHI_MASU,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                assert (fkt := pre.as_fkt_renyo) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_MASU = Masu()

# ==============================================================================
# 助動詞::様態
# ==============================================================================


class SoudaYoutai(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="そう",
            katsuyo=k.KEIYOUDOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo)):
                assert (fkt := pre.as_fkt_gokan) is not None
                return fkt + self.katsuyo_text
            elif (fkt := pre.as_fkt_renyo) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_SOUDA_YOUTAI = SoudaYoutai()

# ==============================================================================
# 助動詞::伝聞
# ==============================================================================


class SoudaDenbun(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="そう",
            # NOTE: 本来「伝聞」の活用系は形容動詞とは異なる(e.g., 未然形が存在しない)
            #       現状の意味を厳密に扱わない状態においては、形容動詞の活用系を使う
            katsuyo=k.KEIYOUDOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_shushi) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_SOUDA_DENBUN = SoudaDenbun()


# ==============================================================================
# 助動詞::推定
# ==============================================================================


class Rashii(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="らし",
            # NOTE: 本来の活用系は形容詞とは異なる(e.g., 未然形が存在しない)
            #       現状の意味を厳密に扱わない状態においては、形容詞の活用系を使う
            katsuyo=k.KEIYOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            if isinstance(pre, TaigenText):
                return pre + self.katsuyo_text
            elif isinstance(pre, KakujoshiText):
                # TODO 助詞の精査
                return pre + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.KeiyoudoushiKatsuyo):
                assert (fkt := pre.as_fkt_gokan) is not None
                return fkt + self.katsuyo_text
            elif (fkt := pre.as_fkt_shushi) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_RASHII = Rashii()

# ==============================================================================
# 助動詞::当然
# ==============================================================================


class Bekida(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="べき",
            katsuyo=k.KEIYOUDOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                assert (fkt := pre.as_fkt_shushi) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_BEKIDA = Bekida()

# ==============================================================================
# 助動詞::比況 例示 推定
# ==============================================================================


class Youda(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="よう",
            katsuyo=k.KEIYOUDOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            if isinstance(pre, KakujoshiText):
                # TODO 助詞の精査
                return pre + self.katsuyo_text

            # 定義上は連体詞「この」等に接続するが、現状はサポートしない

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_rentai) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_YOUDA = Youda()

# ==============================================================================
# 助動詞::断定
# ==============================================================================


class Desu(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="で",
            katsuyo=k.JODOUSHI_DESU,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            return pre + self.katsuyo_text
        else:
            assert isinstance(pre, KatsuyoText)

            # 未然形「でしょ」でのみ使用可能だが、helperで対処する
            # if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            #     assert (fkt := pre.as_fkt_rentai) is not None
            #     return fkt + self.katsuyo_text
            if isinstance(pre.katsuyo, k.KeiyoushiKatsuyo):
                assert (fkt := pre.as_fkt_rentai) is not None
                return fkt + self.katsuyo_text
            elif isinstance(pre.katsuyo, k.KeiyoudoushiKatsuyo):
                assert (fkt := pre.as_fkt_gokan) is not None
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_DESU = Desu()


class DaDantei(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="",
            katsuyo=k.KEIYOUDOUSHI,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            return pre + self.katsuyo_text
        else:
            assert isinstance(pre, KatsuyoText)

            # 仮定形「なら」未然形「だろ」でのみ使用可能だが、helperで対処する
            # if isinstance(pre.katsuyo, (k.IDoushiKatsuyo, k.KeiyoushiKatsuyo)):
            #     assert (fkt := pre.as_fkt_rentai) is not None
            #     return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_DA_DANTEI = DaDantei()


# ==============================================================================
# 助動詞::継続
# 助動詞の参照リンクには含まれないが、口語では頻出されるため追記
# ref. https://ja.wiktionary.org/wiki/てる#助動詞
# ==============================================================================


class Teiru(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="てい",
            katsuyo=k.KAMI_ICHIDAN,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_renyo_ta) is not None:
                return fkt + self.katsuyo_text
            elif (fkt := pre.as_fkt_renyo) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


class Deiru(IJodoushiKatsuyoText):
    def __init__(self):
        super().__init__(
            gokan="でい",
            katsuyo=k.KAMI_ICHIDAN,
        )

    def merge(self, pre: IKatsuyoTextSource) -> KatsuyoText:
        if isinstance(pre, FixedKatsuyoText):
            return pre + self.katsuyo_text
        if isinstance(pre, INonKatsuyoText):
            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: "
                f"{pre} type: {type(pre)}"
            )
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_renyo_ta) is not None:
                return fkt + self.katsuyo_text
            elif (fkt := pre.as_fkt_renyo) is not None:
                return fkt + self.katsuyo_text

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JODOUSHI_TEIRU = Teiru()
JODOUSHI_DEIRU = Deiru()

# ==============================================================================
# 体言
# ref. https://ja.wiktionary.org/wiki/体言
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class TaigenText(INonKatsuyoText, IKatsuyoTextAppendant["TaigenText"]):
    """体言"""

    def _merge(self, pre: IKatsuyoTextSource) -> "TaigenText":
        assert isinstance(pre, (FixedKatsuyoText, INonKatsuyoText))
        return TaigenText(str(pre) + self.gokan)

    def merge(self, pre: IKatsuyoTextSource) -> "TaigenText":
        if isinstance(pre, (FixedKatsuyoText, INonKatsuyoText)):
            return self._merge(pre)
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_rentai) is not None:
                return self._merge(fkt)

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


# ==============================================================================
# 格助詞
# NOTE: 活用形が明確ではないため、用例によっては厳密な活用形とはなっていない
# ref. https://ja.wikipedia.org/wiki/助詞#格助詞
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class KakujoshiText(INonKatsuyoText, IKatsuyoTextAppendant["KakujoshiText"]):
    """
    格助詞
    """

    def _merge(self, pre: IKatsuyoTextSource) -> "KakujoshiText":
        assert isinstance(pre, (FixedKatsuyoText, INonKatsuyoText))
        return KakujoshiText(str(pre) + self.gokan)

    def merge(self, pre: IKatsuyoTextSource) -> "KakujoshiText":
        if isinstance(pre, (FixedKatsuyoText, INonKatsuyoText)):
            return self._merge(pre)
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_rentai) is not None:
                return self._merge(fkt)

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


# TODO 特殊な活用系のHelper実装
#      e.g., 同じ格助詞「に」であっても、目的を表す場合のみ動詞の連用形につくケースがある
# 概ね体言と連体形に適用されるため、細かなハンドリングが現状行わなっていない
KAKUJOSHI_GA = KakujoshiText("が")
KAKUJOSHI_NI = KakujoshiText("に")
KAKUJOSHI_NO = KakujoshiText("の")
KAKUJOSHI_DE = KakujoshiText("で")
KAKUJOSHI_DA = KakujoshiText("だ")

# ==============================================================================
# 係助詞
# NOTE: 活用形が明確ではないため、用例によっては厳密な活用形とはなっていない
# ref. https://ja.wikipedia.org/wiki/助詞#係助詞
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class KeijoshiText(INonKatsuyoText, IKatsuyoTextAppendant["KeijoshiText"]):
    """
    係助詞
    """

    def _merge(self, pre: IKatsuyoTextSource) -> "KeijoshiText":
        assert isinstance(pre, (FixedKatsuyoText, INonKatsuyoText))
        return KeijoshiText(str(pre) + self.gokan)

    def merge(self, pre: IKatsuyoTextSource) -> "KeijoshiText":
        if isinstance(pre, (FixedKatsuyoText, INonKatsuyoText)):
            return self._merge(pre)
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_renyo_nai) is not None:
                return self._merge(fkt)
            elif (fkt := pre.as_fkt_renyo) is not None:
                return self._merge(fkt)

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


KEIJOSHI_MO = KeijoshiText("も")
KEIJOSHI_HA = KeijoshiText("は")
KEIJOSHI_KOSO = KeijoshiText("こそ")
# 「ぞ」の用例としては体言のみだったが細かく管理しない
KEIJOSHI_ZO = KeijoshiText("ぞ")


# ==============================================================================
# 副助詞
# NOTE: 活用形が明確ではないため、用例によっては厳密な活用形とはなっていない
# ref. https://ja.wikipedia.org/wiki/助詞#副助詞
# ==============================================================================


@attrs.define(frozen=True, slots=False)
class FukujoshiText(INonKatsuyoText):
    pass


class FukujoshiTextAppendant(FukujoshiText, IKatsuyoTextAppendant["FukujoshiText"]):
    def merge(self, pre: IKatsuyoTextSource) -> "FukujoshiText":
        assert isinstance(pre, (FixedKatsuyoText, INonKatsuyoText))
        return FukujoshiText(str(pre) + self.gokan)


@attrs.define(frozen=True, slots=False)
class FukujoshiRentaiText(FukujoshiTextAppendant):
    """
    副助詞。連体形につくものをまとめる
    """

    def merge(self, pre: IKatsuyoTextSource) -> "FukujoshiText":
        if isinstance(pre, (FixedKatsuyoText, INonKatsuyoText)):
            return super().merge(pre)
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_rentai) is not None:
                return super().merge(fkt)

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


FUKUZYOSHI_BAKARI = FukujoshiRentaiText("ばかり")
FUKUZYOSHI_MADE = FukujoshiRentaiText("まで")
FUKUZYOSHI_DAKE = FukujoshiRentaiText("だけ")
FUKUZYOSHI_HODO = FukujoshiRentaiText("ほど")
FUKUZYOSHI_KURAI = FukujoshiRentaiText("くらい")


@attrs.define(frozen=True, slots=False)
class FukujoshiGokanText(FukujoshiTextAppendant):
    """
    副助詞のなかで、形容動詞を語幹で扱うもの
    """

    def merge(self, pre: IKatsuyoTextSource) -> FukujoshiText:
        if isinstance(pre, (FixedKatsuyoText, INonKatsuyoText)):
            return super().merge(pre)

        assert isinstance(pre, KatsuyoText)
        if isinstance(pre.katsuyo, k.KeiyoudoushiKatsuyo):
            assert (fkt := pre.as_fkt_gokan) is not None
            return super().merge(fkt)
        elif (fkt := pre.as_fkt_rentai) is not None:
            return super().merge(fkt)

        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )


FUKUZYOSHI_NADO = FukujoshiGokanText("など")
FUKUZYOSHI_NARI = FukujoshiGokanText("なり")
FUKUZYOSHI_YARA = FukujoshiGokanText("やら")
FUKUZYOSHI_KA = FukujoshiGokanText("か")
FUKUZYOSHI_NOMI = FukujoshiGokanText("のみ")


@attrs.define(frozen=True, slots=False)
class FukujoshiTaigenText(FukujoshiTextAppendant):
    """
    副助詞のなかでも活用形を体言的に扱う
    """

    def merge(self, pre: IKatsuyoTextSource) -> FukujoshiText:
        if isinstance(pre, TaigenText):
            return super().merge(pre)
        elif isinstance(pre, JuntaijoshiText):
            return super().merge(pre)

        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )


FUKUZYOSHI_ZUTSU = FukujoshiTaigenText("ずつ")


@attrs.define(frozen=True, slots=False)
class Kiri(FukujoshiTextAppendant):
    """
    副助詞のなかでも特殊な活用形である「きり」のクラス
    """

    def merge(self, pre: IKatsuyoTextSource) -> FukujoshiText:
        if isinstance(pre, FixedKatsuyoText):
            return super().merge(pre)
        elif isinstance(pre, TaigenText):
            return super().merge(pre)
        elif isinstance(pre, SetsuzokujoshiText):
            return super().merge(pre)
        elif isinstance(pre, JuntaijoshiText):
            return super().merge(pre)
        elif isinstance(pre, KatsuyoText):
            if isinstance(pre.katsuyo, k.TaKatsuyo):
                assert (fkt := pre.as_fkt_rentai) is not None
                return super().merge(fkt)
            elif isinstance(pre.katsuyo, k.IDoushiKatsuyo):
                assert (fkt := pre.as_fkt_renyo) is not None
                return super().merge(fkt)

        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )


FUKUZYOSHI_KIRI = Kiri("きり")

# ==============================================================================
# 接続助詞
# NOTE: 活用形が明確ではないため、用例によっては厳密な活用形とはなっていない
# ref. https://ja.wikipedia.org/wiki/助詞#接続助詞
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class SetsuzokujoshiText(INonKatsuyoText):
    """
    接続助詞
    """

    pass


class SetsuzokujoshiTextAppendant(
    SetsuzokujoshiText, IKatsuyoTextAppendant["SetsuzokujoshiText"]
):
    def merge(self, pre: IKatsuyoTextSource) -> "SetsuzokujoshiText":
        assert isinstance(pre, (FixedKatsuyoText, INonKatsuyoText))
        return SetsuzokujoshiText(str(pre) + self.gokan)


class SetuzokujoshiTeText(SetsuzokujoshiTextAppendant):
    """
    接続助詞「て」用のクラス
    """

    def __init__(self):
        super().__init__("て")

    def merge(self, pre: IKatsuyoTextSource) -> "SetsuzokujoshiText":
        if isinstance(pre, FixedKatsuyoText):
            return super().merge(pre)
        elif isinstance(pre, JuntaijoshiText):
            return super().merge(pre)
        elif isinstance(pre, KatsuyoText):
            if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
                pre.katsuyo.shushi in ["ぐ", "ぬ", "ぶ", "む"]
            ):
                raise KatsuyoTextError(
                    f"Should be 「で」: {pre} "
                    f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
                )

            if (fkt := pre.as_fkt_renyo_ta) is not None:
                return super().merge(fkt)
            elif (fkt := pre.as_fkt_renyo) is not None:
                return super().merge(fkt)

        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )


class SetuzokujoshiDeText(SetsuzokujoshiTextAppendant):
    """
    接続助詞「で」用のクラス
    """

    def __init__(self):
        super().__init__("で")

    def merge(self, pre: IKatsuyoTextSource) -> "SetsuzokujoshiText":
        if isinstance(pre, FixedKatsuyoText):
            return super().merge(pre)
        elif isinstance(pre, JuntaijoshiText):
            return super().merge(pre)
        elif isinstance(pre, KatsuyoText):
            if isinstance(pre.katsuyo, k.IDoushiKatsuyo) and (
                pre.katsuyo.shushi not in ["ぐ", "ぬ", "ぶ", "む"]
            ):
                raise KatsuyoTextError(
                    f"Should be 「て」: {pre} "
                    f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
                )
            elif isinstance(pre.katsuyo, (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo)):
                raise KatsuyoTextError(
                    f"Should be 「て」: {pre} "
                    f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
                )

            if (fkt := pre.as_fkt_renyo_ta) is not None:
                return super().merge(fkt)
            elif (fkt := pre.as_fkt_renyo) is not None:
                return super().merge(fkt)

        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )


SETSUZOKUJOSHI_TE = SetuzokujoshiTeText()
SETSUZOKUJOSHI_DE = SetuzokujoshiDeText()
SETSUZOKUJOSHI_KEREDO = SetsuzokujoshiText("けれど")


# ==============================================================================
# 終助詞
# NOTE: 活用形が明確ではないため、用例によっては厳密な活用形とはなっていない
# ref. https://ja.wikipedia.org/wiki/助詞#終助詞
# ==============================================================================


@attrs.define(frozen=True, slots=False)
class ShujoshiText(INonKatsuyoText):
    pass


class ShujoshiTextAppendant(ShujoshiText, IKatsuyoTextAppendant["ShujoshiText"]):
    def merge(self, pre: IKatsuyoTextSource) -> "ShujoshiText":
        assert isinstance(pre, (FixedKatsuyoText, INonKatsuyoText))
        return ShujoshiText(str(pre) + self.gokan)


@attrs.define(frozen=True, slots=False)
class ShujoshiYogenText(ShujoshiTextAppendant):
    """
    終助詞。連体形につくもので用言にしか紐づかないものをまとめる
    """

    def merge(self, pre: IKatsuyoTextSource) -> "ShujoshiText":
        if isinstance(pre, FixedKatsuyoText):
            return super().merge(pre)
        elif isinstance(pre, JuntaijoshiText):
            return super().merge(pre)
        elif isinstance(pre, KatsuyoText):
            if (fkt := pre.as_fkt_rentai) is not None:
                return super().merge(fkt)

        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )


SHUJOSHI_NO = ShujoshiYogenText("の")
SHUJOSHI_NONI = ShujoshiYogenText("のに")


@attrs.define(frozen=True, slots=False)
class ShujoshShushiiText(ShujoshiTextAppendant):
    """
    終助詞。終止形につくもの
    """

    def merge(self, pre: IKatsuyoTextSource) -> "ShujoshiText":
        if isinstance(pre, FixedKatsuyoText):
            return super().merge(pre)
        elif isinstance(pre, KeijoshiText):
            return super().merge(pre)
        elif isinstance(pre, SetsuzokujoshiText):
            return super().merge(pre)
        elif isinstance(pre, JuntaijoshiText):
            return super().merge(pre)
        elif isinstance(pre.katsuyo, k.ShushiMixin):
            assert isinstance(pre, KatsuyoText)
            assert (fkt := pre.as_fkt_shushi) is not None
            return super().merge(fkt)

        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )


SHUJOSHI_NA = ShujoshShushiiText("な")


@attrs.define(frozen=True, slots=False)
class ShujoshiGokanText(ShujoshiTextAppendant):
    """
    終助詞のなかで、形容動詞を語幹で扱うもの
    """

    def merge(self, pre: IKatsuyoTextSource) -> ShujoshiText:
        if isinstance(pre, (FixedKatsuyoText, INonKatsuyoText)):
            return super().merge(pre)
        else:
            assert isinstance(pre, KatsuyoText)

            if isinstance(pre.katsuyo, k.KeiyoudoushiKatsuyo):
                assert (fkt := pre.as_fkt_gokan) is not None
                return super().merge(fkt)

            if (fkt := pre.as_fkt_rentai) is not None:
                return super().merge(fkt)

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


SHUJOSHI_KA = ShujoshiGokanText("か")
# 終助詞「やら」は副助詞として取得されるため、ここでは定義しない
# SHUJOSHI_YARA = ShujoshiTaigenText("やら")
SHUJOSHI_KASHIRA = ShujoshiGokanText("かしら")

# ==============================================================================
# 準体助詞
# NOTE: 活用形が明確ではないため、用例によっては厳密な活用形とはなっていない
# ref. https://ja.wikipedia.org/wiki/助詞#準体助詞
# ==============================================================================


@attrs.define(frozen=True, slots=True)
class JuntaijoshiText(INonKatsuyoText):
    """
    準体助詞
    """

    def _merge(self, pre: IKatsuyoTextSource) -> "JuntaijoshiText":
        assert isinstance(pre, (FixedKatsuyoText, INonKatsuyoText))
        return JuntaijoshiText(str(pre) + self.gokan)

    def merge(self, pre: IKatsuyoTextSource) -> "JuntaijoshiText":
        if isinstance(pre, (FixedKatsuyoText, INonKatsuyoText)):
            return self._merge(pre)
        else:
            assert isinstance(pre, KatsuyoText)

            if (fkt := pre.as_fkt_rentai) is not None:
                return self._merge(fkt)

            raise KatsuyoTextError(
                f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
                f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
            )


JUNTAIJOSHI_NO = JuntaijoshiText("の")
JUNTAIJOSHI_NN = JuntaijoshiText("ん")
