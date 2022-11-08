from collections.abc import Callable
from typing import Optional
import abc
import sys
import katsuyo_text.katsuyo as k
import katsuyo_text.katsuyo_text as kt


class IKatsuyoTextHelper(kt.IKatsuyoTextAppendant[kt.M]):
    """
    柔軟に活用系を変換するためのクラス
    """

    def __init__(
        self,
        bridge: Optional[Callable[[kt.IKatsuyoTextSource], kt.M]] = None,
    ) -> None:
        self.bridge: Optional[Callable[[kt.IKatsuyoTextSource], kt.M]] = bridge
        """
        文法的には不正な活用形の組み合わせを
        任意の活用形に変換して返せるようにするための関数
        """

    def merge(self, pre: kt.IKatsuyoTextSource) -> kt.M:
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


# ==============================================================================
# 助動詞::受身
# ==============================================================================


def bridge_Ukemi_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    # デフォルトでは動詞「なる」でブリッジ
    naru = kt.KatsuyoText(
        gokan="な",
        katsuyo=k.GODAN_RA_GYO,
    )

    if isinstance(pre, (kt.INonKatsuyoText)):
        return pre + kt.KAKUJOSHI_NI + naru + kt.JODOUSHI_RERU

    if isinstance(
        pre.katsuyo,
        (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
    ):
        return pre + naru + kt.JODOUSHI_RERU

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Ukemi(IKatsuyoTextHelper[kt.KatsuyoText]):
    def __init__(
        self,
        bridge: Optional[
            Optional[Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]]
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
    if isinstance(pre, kt.INonKatsuyoText):
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

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Shieki(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Optional[Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]]
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
    if isinstance(pre, kt.INonKatsuyoText):
        # TODO 助詞のハンドリング
        # TODO 「で」にも切り替えられるように
        return pre + kt.KAKUJOSHI_DE + kt.KEIJOSHI_HA + kt.HOJO_NAI

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


class Hitei(IKatsuyoTextHelper):
    # 現状、出力文字列としては「ない」のみサポート
    # TODO オプションで「ぬ」を選択できるように

    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
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


class KibouSelf(IKatsuyoTextHelper):
    def __init__(
        self,
        # デフォルトでは特に何もbridgeしない
        bridge: Optional[Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]] = None,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.IDoushiKatsuyo):
            return pre + kt.JODOUSHI_TAI

        return None


class KibouOthers(IKatsuyoTextHelper):
    def __init__(
        self,
        # デフォルトでは特に何もbridgeしない
        bridge: Optional[Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]] = None,
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


class KakoKanryo(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
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
    if isinstance(pre, kt.TaigenText):
        return pre + kt.JODOUSHI_SOUDA_YOUTAI

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Youtai(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
        ] = bridge_Youtai_default,
    ) -> None:
        super().__init__(bridge)

    def try_merge(self, pre: kt.IKatsuyoTextSource) -> Optional[kt.KatsuyoText]:
        if isinstance(pre, kt.INonKatsuyoText):
            return None
        if isinstance(pre.katsuyo, k.RenyoMixin):
            return pre + kt.JODOUSHI_SOUDA_YOUTAI

        return None


# ==============================================================================
# 助動詞::伝聞
# ==============================================================================


def bridge_Denbun_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.KAKUJOSHI_DA + kt.JODOUSHI_SOUDA_DENBUN

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Denbun(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
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


class Suitei(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
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
        return pre + kt.KAKUJOSHI_DE + kt.HOJO_ARU + kt.JODOUSHI_BEKIDA

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


class Touzen(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
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
class HikyoReizi(IKatsuyoTextHelper):
    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
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
# 助動詞::継続
# ==============================================================================


def bridge_Keizoku_default(pre: kt.IKatsuyoTextSource) -> kt.KatsuyoText:
    if isinstance(pre, kt.INonKatsuyoText):
        return pre + kt.JODOUSHI_DEIRU

    if isinstance(
        pre.katsuyo,
        (k.KeiyoushiKatsuyo, k.KeiyoudoushiKatsuyo),
    ):
        # 形容詞/形容動詞では「いる」でブリッジ
        return pre + kt.HOJO_IRU

    raise kt.KatsuyoTextError(
        f"Unsupported katsuyo_text in {sys._getframe().f_code.co_name}: {pre} "
        f"type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
    )


class Keizoku(IKatsuyoTextHelper):
    # 現状、出力文字列としては「ている」「でいる」のみサポート
    # TODO オプションで「てる」「でる」を選択できるように

    def __init__(
        self,
        bridge: Optional[
            Callable[[kt.IKatsuyoTextSource], kt.KatsuyoText]
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
