from typing import Any, Optional, List, Set, Tuple, Type
from itertools import dropwhile
from katsuyo_text.katsuyo_text import (
    FukujoshiText,
    KatsuyoTextErrorMessage,
    KatsuyoTextHasError,
    IKatsuyoTextAppendant,
    KatsuyoTextError,
    ShujoshiText,
    FUKUZYOSHI_BAKARI,
    FUKUZYOSHI_MADE,
    FUKUZYOSHI_DAKE,
    FUKUZYOSHI_HODO,
    FUKUZYOSHI_KURAI,
    FUKUZYOSHI_NADO,
    FUKUZYOSHI_NARI,
    FUKUZYOSHI_KA,
    FUKUZYOSHI_ZUTSU,
    FUKUZYOSHI_NOMI,
    FUKUZYOSHI_KIRI,
    FUKUZYOSHI_YARA,
    SHUJOSHI_NO,
    SHUJOSHI_NONI,
    SHUJOSHI_NA,
    SHUJOSHI_KA,
    SHUJOSHI_KASHIRA,
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
)
import abc
import warnings
import spacy


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
    )

    def __init__(
        self,
        helpers: Set[IKatsuyoTextHelper],
        fukujoshis: Set[FukujoshiText],
        shujoshis: Set[ShujoshiText],
        allow_not_registered_fukujoshi: bool = False,
        allow_not_registered_shujoshi: bool = False,
    ) -> None:
        # validate helpers
        for helper in helpers:
            if not isinstance(helper, self.SUPPORTED_HELPERS):
                raise KatsuyoTextError(f"Unsupported appendant helper: {helper}")

        self.appendants_dict = {type(helper): helper for helper in helpers}

        # check appendants_dict
        for supported_helper in self.SUPPORTED_HELPERS:
            if not issubclass(supported_helper, tuple(self.appendants_dict.keys())):
                warnings.warn(f"this object doesn't have helper: {supported_helper}")

        self.fukujoshis_dict = {fukujoshi.gokan: fukujoshi for fukujoshi in fukujoshis}
        self.shujoshis_dict = {shujoshi.gokan: shujoshi for shujoshi in shujoshis}
        self.allow_not_registered_fukujoshi = allow_not_registered_fukujoshi
        self.allow_not_registered_shujoshi = allow_not_registered_shujoshi

    def try_get_helper(
        self, typ: Type[IKatsuyoTextHelper]
    ) -> Tuple[Optional[IKatsuyoTextHelper], Optional[KatsuyoTextErrorMessage]]:
        # TODO ignoreリストの追加
        helper = self.appendants_dict.get(typ)
        if helper is not None:
            return helper, None

        return None, KatsuyoTextErrorMessage(
            f"Unsupported type in try_get_helper: {typ}"
        )

    def try_get_fukujoshi(
        self, norm: str
    ) -> Tuple[Optional[FukujoshiText], Optional[KatsuyoTextErrorMessage]]:
        fukujoshi = self.fukujoshis_dict.get(norm)
        if fukujoshi is not None:
            return fukujoshi, None

        if self.allow_not_registered_fukujoshi:
            return FukujoshiText(norm), KatsuyoTextErrorMessage(
                f"Get Unsupported type in fukujoshi: {norm}"
            )

        # 例外が多いため、allowしない場合はwarningを出さない
        # return None, KatsuyoTextErrorMessage(
        #     f"Unsupported type in try_get_fukujoshi: {norm}"
        # )
        return None, None

    def try_get_shujoshi(
        self, norm: str
    ) -> Tuple[Optional[ShujoshiText], Optional[KatsuyoTextErrorMessage]]:
        shujoshi = self.shujoshis_dict.get(norm)
        if shujoshi is not None:
            return shujoshi, None

        if self.allow_not_registered_shujoshi:
            return ShujoshiText(norm), KatsuyoTextErrorMessage(
                f"Get Unsupported type in shujoshi: {norm}"
            )

        # 例外が多いため、allowしない場合はwarningを出さない
        # return None, KatsuyoTextErrorMessage(
        #     f"Unsupported type in try_get_shujoshi: {norm}"
        # )
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


class SpacyKatsuyoTextAppendantDetector(IKatsuyoTextAppendantDetector):
    def detect_from_sent(
        self, sent: spacy.tokens.Span, src: spacy.tokens.Token
    ) -> Tuple[List[IKatsuyoTextAppendant], KatsuyoTextHasError]:
        assert src in sent

        appendants: List[IKatsuyoTextAppendant] = []
        has_error = False

        # NOTE: srcに紐づくトークンを取得するのに、依存関係を見ずにsrcトークンのindex以降のトークンを見る
        #       これは、srcがrootとなるとは限らないことと、sentをあらかじめ必要な長さに分割していることを前提としている
        candidates = dropwhile(lambda t: t.i <= src.i, sent)
        for candidate in candidates:
            appendant, warning_msg = self.try_detect(candidate)
            if warning_msg:
                has_error = True
                warnings.warn(f"{warning_msg} src: {src} sent: {sent}", UserWarning)
            if appendant is None:
                continue
            appendants.append(appendant)

        return appendants, KatsuyoTextHasError(has_error)

    def try_detect(
        self, candidate: spacy.tokens.Token
    ) -> Tuple[Optional[IKatsuyoTextAppendant], Optional[KatsuyoTextErrorMessage]]:
        pos_tag = candidate.pos_
        tag = candidate.tag_
        norm = candidate.norm_

        if pos_tag == "AUX":
            # ==================================================
            # 助動詞の判定
            # ==================================================
            # NOTE: inflectionの情報のみでは、助動詞の活用形を判定できない
            #       e.g. せる -> Inf=下一段-サ行,終止形-一般 となる

            # TODO 無視する助動詞のリスト化
            if norm in {
                "ます",
                "ちゃう",
                "やがる",
                # 「する」の助動詞はSpacyKatsuyoTextSourceDetectorで対処されるので
                # ここでは無視する
                "為る",
            }:
                return None, None

            if norm in ["れる", "られる"]:
                return self.try_get_helper(Ukemi)
            elif norm in ["せる", "させる"]:
                return self.try_get_helper(Shieki)
            elif norm in ["ない", "ず"]:
                # 「ず」も「ない」として扱う
                return self.try_get_helper(Hitei)
            elif norm in ["たい"]:
                return self.try_get_helper(KibouSelf)
            elif norm in ["たがる"]:
                return self.try_get_helper(KibouOthers)
            elif norm in ["た"]:
                return self.try_get_helper(KakoKanryo)
            elif norm in ["そう"]:
                return self._detect_appendant_sou(candidate)
            elif norm in ["らしい"]:
                return self.try_get_helper(Suitei)
            elif norm in ["べし"]:
                return self.try_get_helper(Touzen)
            elif norm in ["よう"]:
                return self.try_get_helper(HikyoReizi)
            elif norm in ["だ"]:
                return self.try_get_helper(Dantei)
            elif norm in ["です"]:
                return self.try_get_helper(DanteiTeinei)
            elif norm in ["てる"]:
                return self.try_get_helper(Keizoku)

            return None, KatsuyoTextErrorMessage(f"Unsupported AUX: {norm}")
        elif pos_tag == "ADJ":
            # 「ない」のみ対応
            # NOTE: 必ずしも正確に否定表現を解析できるとは限らない
            #       @see: https://github.com/sadahry/spacy-dialog-reflection/blob/17507db530da24c11816374d6caa4766e4614f69/tests/lang/ja/test_katsuyo_text_detector.py#L676-L693
            if norm in ["無い"]:
                return self.try_get_helper(Hitei)

            return None, None
        elif pos_tag == "ADV":
            # 「そう」のみ対応
            if norm in ["そう"]:
                return self._detect_appendant_sou(candidate)

            return None, None
        elif tag == "助詞-副助詞":
            # ==================================================
            # 副助詞の判定
            # ==================================================
            return self.try_get_fukujoshi(norm)
        elif tag == "助詞-終助詞":
            # ==================================================
            # 終助詞の判定
            # ==================================================
            return self.try_get_shujoshi(norm)
        elif pos_tag == "ADP":
            # 「のに」のみ対応
            if norm in ["に"]:
                return self._try_detect_noni(candidate)

            return None, None

        return None, None

    def _detect_appendant_sou(
        self, candidate: spacy.tokens.Token
    ) -> Tuple[Optional[IKatsuyoTextAppendant], Optional[KatsuyoTextErrorMessage]]:
        # 「様態」「伝聞」の判別
        left = candidate.doc[candidate.i - 1]
        # 動詞判定
        if left.tag_.startswith("動詞"):
            # @ref: https://github.com/sadahry/spacy-dialog-reflection/blob/6a56bd3378daee41a30bc7bb50b8de6c063a8437/spacy_dialog_reflection/lang/ja/katsuyo_text_detector.py#L136-L144
            inflection = left.morph.get("Inflection")[0].split(";")
            katsuyo_type = inflection[1]
            if "連用形" in katsuyo_type:
                return self.try_get_helper(Youtai)
            elif "終止形" in katsuyo_type or "連体形" in katsuyo_type:
                return self.try_get_helper(Denbun)
        # 形容詞判定
        if "形容詞" in left.tag_:
            # @ref: https://github.com/sadahry/spacy-dialog-reflection/blob/6a56bd3378daee41a30bc7bb50b8de6c063a8437/spacy_dialog_reflection/lang/ja/katsuyo_text_detector.py#L136-L144
            inflection = left.morph.get("Inflection")[0].split(";")
            katsuyo_type = inflection[1]
            if "語幹" in katsuyo_type:
                return self.try_get_helper(Youtai)
            elif "終止形" in katsuyo_type or "連体形" in katsuyo_type:
                return self.try_get_helper(Denbun)
        # 形容動詞判定
        if left.pos_ == "AUX" and left.text == "だ":
            # 形容動詞の基本形(終止or連体)が取れていると判断する
            return self.try_get_helper(Denbun)
        elif "形状詞" in left.tag_:
            # e.g.,
            # 困難    ADJ     名詞-普通名詞-形状詞可能
            # 的      PART    接尾辞-形状詞的
            return self.try_get_helper(Youtai)
        elif left.pos_ == "ADJ" and left.tag_.startswith("名詞"):
            # 形状詞可能ではない形容動詞の語幹が取れていると判断する
            return self.try_get_helper(Youtai)

        return None, KatsuyoTextErrorMessage(f"Unexpected {candidate.norm_} no matched")

    def _try_detect_noni(
        self, candidate: spacy.tokens.Token
    ) -> Tuple[Optional[IKatsuyoTextAppendant], Optional[KatsuyoTextErrorMessage]]:
        """
        「のに」の判定
        係り受けでは識別できないため、直接文法を読み込んで判定
        ユーザー辞書での対応も可能
        """
        assert candidate.norm_ == "に"
        left = candidate.doc[candidate.i - 1]
        if left.norm_ not in ["の"]:
            return None, None

        no_left = left.doc[left.i - 1]
        inflection = no_left.morph.get("Inflection")
        if len(inflection) == 0:
            return None, None

        inflection = inflection[0].split(";")
        conjugation_form = inflection[1]
        if not conjugation_form.startswith("連体形") and (
            not conjugation_form.startswith("終止形")
        ):
            return None, None

        return self.try_get_shujoshi("のに")


DEFAULT_APPENDANTS_DETECTOR = SpacyKatsuyoTextAppendantDetector(
    helpers={
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
        # TODO 丁寧を足す
    },
    fukujoshis={
        FUKUZYOSHI_BAKARI,
        FUKUZYOSHI_MADE,
        FUKUZYOSHI_DAKE,
        FUKUZYOSHI_HODO,
        FUKUZYOSHI_KURAI,
        FUKUZYOSHI_NADO,
        FUKUZYOSHI_NARI,
        FUKUZYOSHI_KA,
        FUKUZYOSHI_ZUTSU,
        FUKUZYOSHI_NOMI,
        FUKUZYOSHI_KIRI,
        FUKUZYOSHI_YARA,
    },
    shujoshis={
        SHUJOSHI_NO,
        SHUJOSHI_NONI,
        SHUJOSHI_NA,
        SHUJOSHI_KA,
        SHUJOSHI_KASHIRA,
    },
)
