from collections.abc import Callable
from typing import Optional, Set, Generic, cast
import abc
import sys
import katsuyo_text.katsuyo as k
import katsuyo_text.katsuyo_text as kt


class IKatsuyoTextHelper(kt.IKatsuyoTextAppendant, Generic[kt.M]):
    """
    柔軟に活用系を変換するためのクラス
    """

    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = None,
    ) -> None:
        self.bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge
        """
        文法的には不正な活用形の組み合わせを
        任意の活用形に変換して返せるようにするための関数
        """

    def merge(self, pre: kt.IKatsuyoTextSource) -> kt.IKatsuyoTextSource:
        result = self.try_merge(pre)
        if result is not None:
            return result
        if self.bridge is not None:
            return self.bridge(pre)

        raise kt.KatsuyoTextError(
            f"Unsupported katsuyo_text in merge of {type(self)}: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )

    @abc.abstractmethod
    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.M]:
        raise NotImplementedError()

    def __eq__(self, obj):
        return hash(self) == hash(obj)

    def __hash__(self):
        return hash(self.__class__.__name__) + hash(self.bridge)


# ==============================================================================
# 助動詞
# ==============================================================================


class IJodoushiHelper(IKatsuyoTextHelper[kt.KatsuyoText]):
    pass


# ==============================================================================
# 助動詞::受身
# ==============================================================================


def bridge_Ukemi_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    # デフォルトでは動詞「なる」でブリッジ
    naru = kt.KatsuyoText(
        gokan="な",
        katsuyo=k.GODAN_RA_GYO,
    )

    if isinstance(
        pre, (kt.TaigenText, kt.KakujoshiText, kt.FukujoshiText, kt.KigoText)
    ):
        return pre + kt.KAKUJOSHI_NI + naru + kt.JODOUSHI_RERU

    if isinstance(
        pre.katsuyo,
        (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
    ):
        return pre + naru + kt.JODOUSHI_RERU

    if isinstance(pre.katsuyo, (k.TaKatsuyo, k.DesuKatsuyo, k.MasuKatsuyo)):
        # 現状は対応できない
        # NG: なる + ます + られる
        # OK: なる + られる + ます
        # TODO ヘルパー内で語順を入れ替えられるように
        raise kt.KatsuyoTextError(
            f"{type(pre)} Should be after {sys._getframe().f_code.co_name}"
        )

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Ukemi(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Optional[Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]]
        ] = bridge_Ukemi_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            # サ行変格活用のみ特殊
            if isinstance(pre.katsuyo, k.SaGyoHenkakuKatsuyo):
                # 用法的に「〜する」は「れる/られる」どちらでもよいため固定
                # 用法的に「〜ずる」は文語が多いため未然形「〜ぜ られる」を採用
                if pre.katsuyo.shushi == "する":
                    return pre + kt.JODOUSHI_RERU
                elif pre.katsuyo.shushi == "ずる":
                    return pre + kt.JODOUSHI_RARERU

            mizen = pre.katsuyo.mizen
            if mizen and mizen[-1] in k.DAN["あ"]:
                return pre + kt.JODOUSHI_RERU
            else:
                return pre + kt.JODOUSHI_RARERU

        return None


# ==============================================================================
# 助動詞::使役
# ==============================================================================


def bridge_Shieki_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(
        pre, (kt.TaigenText, kt.KakujoshiText, kt.FukujoshiText, kt.KigoText)
    ):
        # 「させる」を動詞として扱い「に」でブリッジ
        return pre + kt.KAKUJOSHI_NI + kt.SASERU

    if isinstance(
        pre.katsuyo,
        (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
    ):
        # 「させる」を動詞として扱い連用形でブリッジ
        assert isinstance(pre, kt.KatsuyoText)
        assert (fkt := pre.as_fkt_renyo) is not None
        return fkt + kt.SASERU

    if isinstance(pre.katsuyo, (k.TaKatsuyo, k.DesuKatsuyo, k.MasuKatsuyo)):
        # 現状は対応できない
        # NG: なる + ます + られる
        # OK: なる + られる + ます
        # TODO ヘルパー内で語順を入れ替えられるように
        raise kt.KatsuyoTextError(
            f"{type(pre)} Should be after {sys._getframe().f_code.co_name}"
        )

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Shieki(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Optional[Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]]
        ] = bridge_Shieki_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            # サ行変格活用のみ特殊
            if isinstance(pre.katsuyo, k.SaGyoHenkakuKatsuyo):
                # 用法的に「〜する」は「せる/させる」どちらでもよいため固定
                # 用法的に「〜ずる」は「〜じ させる」を採用
                if pre.katsuyo.shushi == "する":
                    return pre + kt.JODOUSHI_SERU
                elif pre.katsuyo.shushi == "ずる":
                    return pre + kt.JODOUSHI_SASERU

            mizen = pre.katsuyo.mizen
            if mizen and mizen[-1] in k.DAN["あ"]:
                return pre + kt.JODOUSHI_SERU
            else:
                return pre + kt.JODOUSHI_SASERU

        return None


# ==============================================================================
# 助動詞::否定
# ==============================================================================


def bridge_Hitei_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    # 細かくハンドリング
    # 無理やり「〜ない」を付与
    # kt.HOJO_NAIを使えば「〜でない」にできるが「〜ではない」としたい
    nai = kt.KatsuyoText(gokan="な", katsuyo=k.KEIYOUSHI)

    if isinstance(
        pre,
        (
            kt.TaigenText,
            kt.FukushiText,
            kt.SettoText,
            kt.KigoText,
            kt.FukujoshiText,
            kt.ShujoshiText,
            kt.JuntaijoshiText,
        ),
    ):
        return pre + kt.KAKUJOSHI_DE + kt.KEIJOSHI_HA + nai
    elif isinstance(pre, (kt.SetsuzokuText, kt.SetsuzokujoshiText)):
        return pre + kt.KEIJOSHI_HA + nai
    elif isinstance(pre, (kt.KandoushiText, kt.KakujoshiText, kt.KeijoshiText)):
        return pre + nai

    if isinstance(pre.katsuyo, (k.TaKatsuyo, k.DesuKatsuyo, k.MasuKatsuyo)):
        # 現状は対応できない
        # NG: なる + ます + られる
        # OK: なる + られる + ます
        # TODO ヘルパー内で語順を入れ替えられるように
        raise kt.KatsuyoTextError(
            f"{type(pre)} Should be after {sys._getframe().f_code.co_name}"
        )

    if isinstance(
        pre.katsuyo,
        (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
    ):
        # 「ない」を補助形容詞としてブリッジ
        return pre + kt.HOJO_NAI

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Hitei(IJodoushiHelper):
    # 現状、出力文字列としては「ない」のみサポート
    # TODO オプションで「ぬ」を選択できるように

    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Hitei_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None

        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            return pre + kt.JODOUSHI_NAI

        return None


# ==============================================================================
# 助動詞::希望
# ==============================================================================


class KibouSelf(IJodoushiHelper):
    def __init__(
        self,
        # デフォルトでは特に何もbridgeしない
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = None,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            return pre + kt.JODOUSHI_TAI

        return None


class KibouOthers(IJodoushiHelper):
    def __init__(
        self,
        # デフォルトでは特に何もbridgeしない
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = None,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            return pre + kt.JODOUSHI_TAGARU

        return None


# ==============================================================================
# 助動詞::過去/完了/存続/確認
# ==============================================================================


def bridge_KakoKanryo_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        # TODO 助詞のハンドリング
        da = kt.KatsuyoText(
            gokan="",
            katsuyo=k.KEIYOUDOUSHI,
        )
        return pre + da + kt.JODOUSHI_TA

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class KakoKanryo(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_KakoKanryo_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.RenyoMixin):
            if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
                pre.katsuyo.shushi in ["ぐ", "ぬ", "ぶ", "む"]
            ):
                return pre + kt.JODOUSHI_DA_KAKO_KANRYO

            return pre + kt.JODOUSHI_TA

        return None


# ==============================================================================
# 助動詞::様態
# ==============================================================================


def bridge_Youtai_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.JODOUSHI_SOUDA_YOUTAI

    # TODO 意志推量「う」の実装
    # if isinstance(pre.katsuyo, k.DesuKatsuyo):
    #     return "でしょう"
    # if isinstance(pre.katsuyo, k.MasuKatsuyo):
    #     return "ましょう"

    if isinstance(pre.katsuyo, (k.TaKatsuyo)):
        # 現状は対応できない
        # NG: なる + た + そうだ
        # OK: なる + そうだ + た
        # TODO ヘルパー内で語順を入れ替えられるように
        raise kt.KatsuyoTextError(
            f"{type(pre)} Should be after {sys._getframe().f_code.co_name}"
        )

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Youtai(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Youtai_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None

        if isinstance(pre.katsuyo, (k.DesuKatsuyo, k.MasuKatsuyo)):
            return None

        if isinstance(pre.katsuyo, k.RenyoMixin):
            return pre + kt.JODOUSHI_SOUDA_YOUTAI

        return None


# ==============================================================================
# 助動詞::伝聞
# ==============================================================================


def bridge_Denbun_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.JODOUSHI_DA_DANTEI + kt.JODOUSHI_SOUDA_DENBUN

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Denbun(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Denbun_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.ShushiMixin):
            return pre + kt.JODOUSHI_SOUDA_DENBUN

        return None


# ==============================================================================
# 助動詞::伝聞
# ==============================================================================


def bridge_Suitei_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    # TODO 文法的にも体言に紐づけることができるため
    #      try_mergeにこのロジックを移植できるようにする
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.JODOUSHI_RASHII

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Suitei(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Suitei_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.ShushiMixin):
            return pre + kt.JODOUSHI_RASHII

        return None


# ==============================================================================
# 助動詞::当然
# ==============================================================================


def bridge_Touzen_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.HOJO_ARU + kt.JODOUSHI_BEKIDA

    if isinstance(
        pre.katsuyo,
        (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
    ):
        # 補助動詞「ある」でブリッジ
        return pre + kt.HOJO_ARU + kt.JODOUSHI_BEKIDA

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Touzen(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Touzen_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            return pre + kt.JODOUSHI_BEKIDA

        return None


# ==============================================================================
# 助動詞::比況 例示 推定
# ==============================================================================


def bridge_HikyoReizi_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.KAKUJOSHI_NO + kt.JODOUSHI_YOUDA

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


# NOTE: 文法的には連体詞「この」等に紐づけることができるが
#       文末表現として「このようだ」となる際はrootに「よう」がつくため
#       文末の品詞を分解する機能として扱ううえでは
#       「比況」にて連体詞を扱うロジックはIKatsuyoTextHelperに含めない
class HikyoReizi(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_HikyoReizi_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.RentaiMixin):
            return pre + kt.JODOUSHI_YOUDA

        return None


# ==============================================================================
# 助動詞::断定
# ==============================================================================


def bridge_Dantei_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.KatsuyoText):
        if isinstance(pre.katsuyo, k.KeiyoudoushiKatsuyo):
            # 変形しない
            return pre
        return pre + kt.KAKUJOSHI_NO + kt.JODOUSHI_DA_DANTEI

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Dantei(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Dantei_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return pre + kt.JODOUSHI_DA_DANTEI

        return None


def bridge_DanteiTeinei_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre.katsuyo, (k.DesuKatsuyo, k.MasuKatsuyo)):
        # そのまま返す
        return cast(kt.KatsuyoText, pre)

    if isinstance(pre, kt.KatsuyoText):
        return pre + kt.KAKUJOSHI_NO + kt.JODOUSHI_DESU

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class DanteiTeinei(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_DanteiTeinei_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return pre + kt.JODOUSHI_DESU

        if isinstance(
            pre.katsuyo, (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo, k.TaKatsuyo)
        ):
            return pre + kt.JODOUSHI_DESU

        return None


# ==============================================================================
# 助動詞::丁寧
# ==============================================================================


def bridge_Teinei_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.JODOUSHI_DESU

    if isinstance(pre.katsuyo, (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo)):
        return pre + kt.JODOUSHI_DESU

    return bridge_DanteiTeinei_default(pre)


class Teinei(IJodoushiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Teinei_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            return pre + kt.JODOUSHI_MASU

        return None


# ==============================================================================
# 助動詞::継続
# ==============================================================================


def bridge_Keizoku_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(
        pre,
        (
            kt.TaigenText,
            kt.FukushiText,
            kt.KakujoshiText,
            kt.JuntaijoshiText,
            kt.FukujoshiText,
            kt.KandoushiText,
            kt.SetsuzokuText,
            kt.SettoText,
            kt.KigoText,
        ),
    ):
        return pre + kt.JODOUSHI_DEIRU

    if isinstance(
        pre.katsuyo,
        (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
    ):
        # 形容詞/形容動詞では「いる」でブリッジ
        return pre + kt.HOJO_IRU

    if isinstance(pre.katsuyo, (k.TaKatsuyo, k.DesuKatsuyo, k.MasuKatsuyo)):
        # 現状は対応できない
        # NG: なる + ます + ている
        # OK: なる + ている + ます
        # TODO ヘルパー内で語順を入れ替えられるように
        raise kt.KatsuyoTextError(
            f"{type(pre)} Should be after {sys._getframe().f_code.co_name}"
        )

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Keizoku(IJodoushiHelper):
    # 現状、出力文字列としては「ている」「でいる」のみサポート
    # TODO オプションで「てる」「でる」を選択できるように

    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_Keizoku_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
                pre.katsuyo.shushi in ["ぐ", "ぬ", "ぶ", "む"]
            ):
                return pre + kt.JODOUSHI_DEIRU

            return pre + kt.JODOUSHI_TEIRU

        return None


ALL_JODOUSHI_HELPERS: Set[IKatsuyoTextHelper] = {
    Ukemi(),
    Shieki(),
    Hitei(),
    KibouSelf(),
    KibouOthers(),
    KakoKanryo(),
    Youtai(),
    Denbun(),
    Suitei(),
    Touzen(),
    HikyoReizi(),
    Keizoku(),
    Dantei(),
    DanteiTeinei(),
    Teinei(),
}

# ==============================================================================
# 接続助詞
# ==============================================================================


class ISetsuzokujoshiHelper(IKatsuyoTextHelper[kt.SetsuzokujoshiText]):
    pass


# ==============================================================================
# 「て」「で」「たって」「だって」
# ==============================================================================


def bridge_TeDe_default(pre: kt.IKatsuyoTextSource) -> kt.IKatsuyoTextSource:
    if isinstance(
        pre,
        (
            kt.KandoushiText,
            kt.SetsuzokuText,
            kt.SettoText,
            kt.KigoText,
            kt.SetsuzokujoshiText,
            kt.KeijoshiText,
        ),
    ):
        return pre + kt.FUKUJOSHI_TTE
    elif isinstance(pre, kt.INonKatsuyoText):
        # 断定の「だ」でブリッジ。次に連用形が来ることを想定
        return pre + kt.JODOUSHI_DA_DANTEI

    if isinstance(pre.katsuyo, k.TaKatsuyo):
        return pre + kt.FUKUJOSHI_TTE

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class TeDe(ISetsuzokujoshiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_TeDe_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.SetsuzokujoshiText]:
        if isinstance(pre, kt.KatsuyoText):
            if isinstance(pre.katsuyo, k.TaKatsuyo):
                return None
            if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
                pre.katsuyo.shushi in ["ぐ", "ぬ", "ぶ", "む"]
            ):
                return pre + kt.SETSUZOKUJOSHI_DE

            return pre + kt.SETSUZOKUJOSHI_TE

        return None


def bridge_TatteDatte_default(pre: kt.IKatsuyoTextSource) -> kt.IKatsuyoTextSource:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.FUKUJOSHI_TTE

    if isinstance(pre.katsuyo, k.TaKatsuyo):
        return pre + kt.FUKUJOSHI_TTE

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class TatteDatte(ISetsuzokujoshiHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.IKatsuyoTextSource]
        ] = bridge_TatteDatte_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.SetsuzokujoshiText]:
        if isinstance(pre, kt.KatsuyoText):
            if isinstance(pre.katsuyo, k.TaKatsuyo):
                return None
            if isinstance(pre.katsuyo, k.GodanKatsuyo) and (
                pre.katsuyo.shushi in ["ぐ", "ぬ", "ぶ", "む"]
            ):
                return pre + kt.SETSUZOKUJOSHI_DATTE

            return pre + kt.SETSUZOKUJOSHI_TATTE

        return None


ALL_SETSUZOKUJOSHI_HELPERS: Set[IKatsuyoTextHelper] = {
    TeDe(),
    TatteDatte(),
}
