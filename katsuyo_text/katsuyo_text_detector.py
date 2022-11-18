from typing import Any, Optional, List, Set, Tuple, Type
from katsuyo_text.katsuyo_text import (
    IKatsuyoTextSource,
    KatsuyoTextErrorMessage,
    KatsuyoTextHasError,
    IKatsuyoTextAppendant,
    FukujoshiTextAppendant,
    SetsuzokujoshiTextAppendant,
    ShujoshiTextAppendant,
)
from katsuyo_text.katsuyo_text_helper import (
    IKatsuyoTextHelper,
    Denbun,
    HikyoReizi,
    Hitei,
    KakoKanryo,
    Keizoku,
    KibouSelf,
    Shieki,
    Suitei,
    Touzen,
    Ukemi,
    KibouOthers,
    Youtai,
    Dantei,
    DanteiTeinei,
    Teinei,
    TeDe,
    TatteDatte,
)
import abc
import warnings


class IKatsuyoTextSourceDetector(abc.ABC):
    @abc.abstractmethod
    def try_detect(self, src: Any) -> Optional[IKatsuyoTextSource]:
        """
        不適切な値が代入された際は、Noneを返却する。
        """
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__


class IKatsuyoTextAppendantDetector(abc.ABC):
    SUPPORTED_HELPERS = (
        Ukemi,
        Shieki,
        Hitei,
        KibouSelf,
        KibouOthers,
        KakoKanryo,
        Youtai,
        Denbun,
        Suitei,
        Touzen,
        HikyoReizi,
        Keizoku,
        Dantei,
        DanteiTeinei,
        Teinei,
        TeDe,
        TatteDatte,
    )

    def __init__(
        self,
        helpers: Set[IKatsuyoTextHelper] = set(),
        fukujoshis: Set[FukujoshiTextAppendant] = set(),
        setsuzokujoshis: Set[SetsuzokujoshiTextAppendant] = set(),
        shujoshis: Set[ShujoshiTextAppendant] = set(),
        log_warning: bool = True,
    ) -> None:
        # validate helpers
        for helper in helpers:
            if not isinstance(helper, self.SUPPORTED_HELPERS):
                raise ValueError(f"Unsupported appendant helper: {helper}")

        self.helpers_dict = {type(helper): helper for helper in helpers}

        # check helpers_dict
        if log_warning and len(self.helpers_dict) > 0:
            for supported_helper in self.SUPPORTED_HELPERS:
                if not issubclass(supported_helper, tuple(self.helpers_dict.keys())):
                    warnings.warn(
                        f"this object doesn't have helper: {supported_helper}"
                    )

        self.fukujoshis_dict = {fukujoshi.gokan: fukujoshi for fukujoshi in fukujoshis}
        self.setsuzokujoshis_dict = {
            setsuzokujoshi.gokan: setsuzokujoshi for setsuzokujoshi in setsuzokujoshis
        }
        self.shujoshis_dict = {shujoshi.gokan: shujoshi for shujoshi in shujoshis}
        self.log_warning = log_warning

    def try_get_helper(
        self, typ: Type[IKatsuyoTextHelper]
    ) -> Tuple[Optional[IKatsuyoTextHelper], Optional[KatsuyoTextErrorMessage]]:
        # TODO ignoreリストの追加
        helper = self.helpers_dict.get(typ)
        if helper is not None:
            return helper, None

        if self.log_warning:
            return None, KatsuyoTextErrorMessage(
                f"Unsupported type in try_get_helper: {typ}"
            )

        return None, None

    def try_get_fukujoshi(
        self, norm: str
    ) -> Tuple[Optional[FukujoshiTextAppendant], Optional[KatsuyoTextErrorMessage]]:
        fukujoshi = self.fukujoshis_dict.get(norm)
        if fukujoshi is not None:
            return fukujoshi, None

        if self.log_warning:
            return None, KatsuyoTextErrorMessage(
                f"Unsupported type in try_get_fukujoshi: {norm}"
            )

        return None, None

    def try_get_setsuzokujoshi(
        self, lemma: str
    ) -> Tuple[
        Optional[SetsuzokujoshiTextAppendant], Optional[KatsuyoTextErrorMessage]
    ]:
        setsuzokujoshi = self.setsuzokujoshis_dict.get(lemma)
        if setsuzokujoshi is not None:
            return setsuzokujoshi, None

        if self.log_warning:
            return None, KatsuyoTextErrorMessage(
                f"Unsupported type in try_get_setsuzokujoshi: {lemma}"
            )

        return None, None

    def try_get_shujoshi(
        self, norm: str
    ) -> Tuple[Optional[ShujoshiTextAppendant], Optional[KatsuyoTextErrorMessage]]:
        shujoshi = self.shujoshis_dict.get(norm)
        if shujoshi is not None:
            return shujoshi, None

        if self.log_warning:
            return None, KatsuyoTextErrorMessage(
                f"Unsupported type in try_get_shujoshi: {norm}"
            )

        return None, None

    @abc.abstractmethod
    def detect_from_sent(
        self, sent: Any, src: Any
    ) -> Tuple[List[IKatsuyoTextAppendant], KatsuyoTextHasError]:
        """
        detectされなかった場合は、空のListを返却する。
        意図しない値が代入された際は、KatsuyoTextHasError=Trueを返却する。
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def try_detect(
        self, candidate: Any
    ) -> Tuple[Optional[IKatsuyoTextAppendant], Optional[KatsuyoTextErrorMessage]]:
        """
        detectされなかった場合は、IKatsuyoTextAppendant=Noneを返却する。
        意図しない値が代入された際は、KatsuyoTextErrorMessageを返却する。
        """
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__
