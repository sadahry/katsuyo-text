from typing import Optional, List, Tuple
from itertools import dropwhile
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
    KEIYOUSHI,
    SA_GYO_HENKAKU_SURU,
    SA_GYO_HENKAKU_ZURU,
    SHIMO_ICHIDAN,
)
from katsuyo_text.katsuyo_text import (
    KatsuyoTextErrorMessage,
    KatsuyoTextHasError,
    IKatsuyoTextAppendant,
    IKatsuyoTextSource,
    KatsuyoText,
    TaigenText,
    FukushiText,
    SettoText,
    KandoushiText,
    SetsuzokuText,
    KigoText,
    KakujoshiText,
    KeijoshiText,
    FukujoshiText,
    SetsuzokujoshiText,
    ShujoshiText,
    JuntaijoshiText,
    KURU,
    KURU_KANJI,
    ALL_FUKUJOSHIS,
    ALL_SHUJOSHIS,
    ALL_SETSUZOKUJOSHIS,
    JODOUSHI_RERU,
    JODOUSHI_RARERU,
    JODOUSHI_NAI,
    JODOUSHI_TAI,
    JODOUSHI_TA,
    JODOUSHI_DA_DANTEI,
    JODOUSHI_DA_KAKO_KANRYO,
    JODOUSHI_RASHII,
    JODOUSHI_BEKIDA,
    JODOUSHI_DESU,
    JODOUSHI_MASU,
)
from katsuyo_text.katsuyo_text_helper import (
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
    ALL_JODOUSHI_HELPERS,
    ALL_SETSUZOKUJOSHI_HELPERS,
)
from katsuyo_text.katsuyo_text_detector import (
    IKatsuyoTextSourceDetector,
    IKatsuyoTextAppendantDetector,
)
import re
import warnings
import spacy


class SpacyKatsuyoTextSourceDetector(IKatsuyoTextSourceDetector):
    VERB_KATSUYOS_BY_CONJUGATION_TYPE = {
        "五段-カ行": GODAN_KA_GYO,
        "五段-ガ行": GODAN_GA_GYO,
        "五段-サ行": GODAN_SA_GYO,
        "五段-タ行": GODAN_TA_GYO,
        "五段-ナ行": GODAN_NA_GYO,
        "五段-バ行": GODAN_BA_GYO,
        "五段-マ行": GODAN_MA_GYO,
        "五段-ラ行": GODAN_RA_GYO,
        "五段-ワア行": GODAN_WAA_GYO,
        "上一段-ア行": KAMI_ICHIDAN,
        "上一段-カ行": KAMI_ICHIDAN,
        "上一段-ガ行": KAMI_ICHIDAN,
        "上一段-ザ行": KAMI_ICHIDAN,
        "上一段-タ行": KAMI_ICHIDAN,
        "上一段-ナ行": KAMI_ICHIDAN,
        "上一段-バ行": KAMI_ICHIDAN,
        "上一段-マ行": KAMI_ICHIDAN,
        "上一段-ラ行": KAMI_ICHIDAN,
        "下一段-ア行": SHIMO_ICHIDAN,
        "下一段-カ行": SHIMO_ICHIDAN,
        "下一段-ガ行": SHIMO_ICHIDAN,
        "下一段-サ行": SHIMO_ICHIDAN,
        "下一段-ザ行": SHIMO_ICHIDAN,
        "下一段-タ行": SHIMO_ICHIDAN,
        "下一段-ダ行": SHIMO_ICHIDAN,
        "下一段-ナ行": SHIMO_ICHIDAN,
        "下一段-ハ行": SHIMO_ICHIDAN,
        "下一段-バ行": SHIMO_ICHIDAN,
        "下一段-マ行": SHIMO_ICHIDAN,
        "下一段-ラ行": SHIMO_ICHIDAN,
    }
    JODOUSHI_BY_LEMMA = {
        "れる": JODOUSHI_RERU.katsuyo_text,
        "られる": JODOUSHI_RARERU.katsuyo_text,
        # "せる" -> KatsuyoText
        # "させる" -> KatsuyoText
        "ない": JODOUSHI_NAI.katsuyo_text,
        "ず": JODOUSHI_NAI.katsuyo_text,
        "ぬ": JODOUSHI_NAI.katsuyo_text,
        "たい": JODOUSHI_TAI.katsuyo_text,
        # "たがる" -> KatsuyoText
        "た": JODOUSHI_TA.katsuyo_text,
        # "だ" -> 例外的に区別
        # "そう" -> TaigenText|FukushiText
        "らしい": JODOUSHI_RASHII.katsuyo_text,
        "べし": JODOUSHI_BEKIDA.katsuyo_text,
        # "よう" -> TaigenText
        "です": JODOUSHI_DESU.katsuyo_text,
        "ます": JODOUSHI_MASU.katsuyo_text,
        # "てる" -> KatsuyoText
    }
    DOUSHI_PATTERN = re.compile(r"(動詞|.*動詞的)")
    JODOUSHI_PATTERN = "助動詞"
    KEIYOUSHI_PATTERN = re.compile(r"(形容詞|.*形容詞的)")
    # 「形状詞」=「形容動詞の語幹」
    # universaldependenciesのADJは形状詞を形容動詞として扱うが、KatsuyoTextとしては形状詞は名詞として扱う
    # ref. https://universaldependencies.org/treebanks/ja_gsd/ja_gsd-pos-ADJ.html
    # 「記号」e.g., 「ε」
    MEISHI_PATTERN = re.compile(r"(名詞|.*名詞的|形状詞|.*形状詞的)")
    FUKUSHI_PATTERN = "副詞"
    KANDOUSHI_PATTERN = "感動詞"
    SETSUZOKU_PATTERN = "接続詞"
    SETTOU_PATTERN = re.compile(r"(接頭辞|連体詞)")
    KIGO_PATTERN = re.compile(r"(記号|補助記号)")
    KAKUJOSHI_PATTERN = "助詞-格助詞"
    KEIJOSHI_PATTERN = "助詞-係助詞"
    FUKUJOSHI_PATTERN = "助詞-副助詞"
    SETSUZOKUJOSHI_PATTERN = "助詞-接続助詞"
    SHUJOSHI_PATTERN = "助詞-終助詞"
    JUNTAIJOSHI_PATTERN = "助詞-準体助詞"

    def try_detect(self, src: spacy.tokens.Token) -> Optional[IKatsuyoTextSource]:
        # spacy.tokens.Tokenから抽出される活用形の特徴を表す変数
        tag = src.tag_
        lemma = src.lemma_
        norm = src.norm_
        conjugation_type, _ = get_conjugation(src)

        # There is no VBD tokens in Japanese
        # ref. https://universaldependencies.org/treebanks/ja_gsd/index.html#pos-tags
        # if pos_tag == "VBD":

        if self.DOUSHI_PATTERN.match(tag):
            # ==================================================
            # 動詞の判定
            # ==================================================
            # 「行く」は特殊な変形
            if lemma in ["ゆく"]:
                # 「ゆく」も「いく」に含める（過去・完了「た」を「ゆった」「ゆいた」とはできないため）
                return KatsuyoText(gokan="い", katsuyo=GODAN_IKU)
            if norm in ["行く", "逝く"]:
                return KatsuyoText(gokan=lemma[:-1], katsuyo=GODAN_IKU)

            # 活用タイプを取得して判定に利用
            assert conjugation_type is not None, f"inflection is not empty: {src}"

            # 活用形の判定
            katsuyo = self.VERB_KATSUYOS_BY_CONJUGATION_TYPE.get(conjugation_type)
            if katsuyo:
                return KatsuyoText(gokan=lemma[:-1], katsuyo=katsuyo)

            # 例外的な活用形の判定
            if conjugation_type == "カ行変格":
                # カ変「くる」「来る」を別途ハンドリング
                if lemma == "来る":
                    return KURU_KANJI
                elif lemma == "くる":
                    return KURU
            elif conjugation_type == "サ行変格":
                # サ変「する」「ずる」を別途ハンドリング
                if lemma[-2:] == "する":
                    return KatsuyoText(gokan=lemma[:-2], katsuyo=SA_GYO_HENKAKU_SURU)
                elif lemma[-2:] == "ずる":
                    return KatsuyoText(gokan=lemma[:-2], katsuyo=SA_GYO_HENKAKU_ZURU)

            warnings.warn(
                f"Unsupported conjugation_type of VERB: {conjugation_type}", UserWarning
            )
            return None
        elif tag.startswith(self.JODOUSHI_PATTERN):
            # 活用タイプを取得して判定に利用
            assert conjugation_type is not None, f"inflection is not empty: {src}"

            # 活用形の判定
            katsuyo = self.VERB_KATSUYOS_BY_CONJUGATION_TYPE.get(conjugation_type)
            if katsuyo:
                return KatsuyoText(gokan=lemma[:-1], katsuyo=katsuyo)

            # 例外的な活用形の判定
            # 過去完了「だ」と断定「だ」の区別
            if lemma == "だ":
                if norm == "た":
                    return JODOUSHI_DA_KAKO_KANRYO.katsuyo_text
                else:
                    assert norm == "だ"
                    return JODOUSHI_DA_DANTEI.katsuyo_text

            jodoushi = self.JODOUSHI_BY_LEMMA.get(lemma)
            if jodoushi:
                return jodoushi

            warnings.warn(
                f"Unsupported conjugation_type of AUX: {conjugation_type}", UserWarning
            )
            return None
        elif self.KEIYOUSHI_PATTERN.match(tag):
            # ==================================================
            # 形容詞の変形
            # ==================================================
            # e.g. 楽しい -> gokan=楽し + katsuyo=い
            return KatsuyoText(gokan=lemma[:-1], katsuyo=KEIYOUSHI)
        elif self.MEISHI_PATTERN.match(tag):
            return TaigenText(gokan=src.text)
        elif tag.startswith(self.FUKUSHI_PATTERN):
            return FukushiText(gokan=src.text)
        elif self.SETTOU_PATTERN.match(tag):
            return SettoText(gokan=src.text)
        elif tag.startswith(self.KANDOUSHI_PATTERN):
            return KandoushiText(gokan=src.text)
        elif tag.startswith(self.SETSUZOKU_PATTERN):
            return SetsuzokuText(gokan=src.text)
        elif self.KIGO_PATTERN.match(tag):
            return KigoText(gokan=src.text)
        elif tag.startswith(self.KAKUJOSHI_PATTERN):
            return KakujoshiText(gokan=src.text)
        elif tag.startswith(self.KEIJOSHI_PATTERN):
            return KeijoshiText(gokan=src.text)
        elif tag.startswith(self.FUKUJOSHI_PATTERN):
            return FukujoshiText(gokan=src.text)
        elif tag.startswith(self.SETSUZOKUJOSHI_PATTERN):
            return SetsuzokujoshiText(gokan=src.text)
        elif tag.startswith(self.SHUJOSHI_PATTERN):
            return ShujoshiText(gokan=src.text)
        elif tag.startswith(self.JUNTAIJOSHI_PATTERN):
            return JuntaijoshiText(gokan=src.text)

        return None


class SpacyKatsuyoTextAppendantDetector(IKatsuyoTextAppendantDetector):
    def detect_from_sent(
        self, sent: spacy.tokens.Span, src: spacy.tokens.Token
    ) -> Tuple[List[IKatsuyoTextAppendant], KatsuyoTextHasError]:
        assert src in sent

        appendants: List[IKatsuyoTextAppendant] = []
        has_error = False

        # NOTE: srcに紐づくトークンを取得するのに、依存関係を見ずにsrcトークンのindex以降のトークンすべてを見る
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
        lemma = candidate.lemma_

        if pos_tag == "AUX" or tag == "助動詞":
            # ==================================================
            # 助動詞の判定
            # ==================================================
            # NOTE: inflectionの情報のみでは、助動詞の活用形を判定できない
            #       e.g. せる -> Inf=下一段-サ行,終止形-一般 となる

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
            elif norm in ["ます"]:
                return self.try_get_helper(Teinei)
            elif norm in ["てる"]:
                return self.try_get_helper(Keizoku)

            if self.log_warning:
                return None, KatsuyoTextErrorMessage(f"Unsupported AUX: {norm}")

            return None, None
        elif pos_tag == "ADJ":
            # 形容詞「ない」はIJodoushiHelperの対象外とする
            # NOTE: 必ずしも正確に否定表現を解析できるとは限らない
            #       @see: https://github.com/sadahry/spacy-dialog-reflection/blob/17507db530da24c11816374d6caa4766e4614f69/tests/lang/ja/test_katsuyo_text_detector.py#L676-L693
            # if norm in ["無い"]:
            #     return self.try_get_helper(Hitei)

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
        elif tag == "助詞-接続助詞":
            # ==================================================
            # 接続助詞の判定
            # ==================================================
            # sudachiの辞書のnorm「だって」が正しくないためlemmaで対応
            if lemma in ["たって", "だって"]:
                return self.try_get_helper(TatteDatte)
            elif lemma in ["て", "で"]:
                return self.try_get_helper(TeDe)
            return self.try_get_setsuzokujoshi(lemma)
        elif tag == "助詞-終助詞":
            # ==================================================
            # 終助詞の判定
            # ==================================================
            return self.try_get_shujoshi(norm)

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


def get_conjugation(token):
    # sudachiの形態素解析結果(part_of_speech)5つ目以降(活用タイプ、活用形)が格納される
    # 品詞によっては活用タイプ、活用形が存在しないため、ここでは配列の取得のみ行う
    # e.g. 動詞
    # > m.part_of_speech() # => ['動詞', '一般', '*', '*', '下一段-バ行', '連用形-一般']
    # ref. https://github.com/explosion/spaCy/blob/v3.4.1/spacy/lang/ja/__init__.py#L102
    # ref. https://github.com/WorksApplications/SudachiPy/blob/v0.5.4/README.md
    # > Returns the part of speech as a six-element tuple. Tuple elements are four POS levels, conjugation type and conjugation form.
    # ref. https://worksapplications.github.io/sudachi.rs/python/api/sudachipy.html#sudachipy.Morpheme.part_of_speech
    inflection = token.morph.get("Inflection")
    if not inflection:
        return None, None
    inflection = inflection[0].split(";")
    conjugation_type = inflection[0]
    conjugation_form = inflection[1]
    return conjugation_type, conjugation_form


ALL_APPENDANTS_DETECTOR = SpacyKatsuyoTextAppendantDetector(
    helpers=ALL_JODOUSHI_HELPERS | ALL_SETSUZOKUJOSHI_HELPERS,
    fukujoshis=ALL_FUKUJOSHIS,
    setsuzokujoshis=ALL_SETSUZOKUJOSHIS,
    shujoshis=ALL_SHUJOSHIS,
)
