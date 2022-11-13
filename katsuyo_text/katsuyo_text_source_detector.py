from typing import Any, Optional
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
    KURU,
    KURU_KANJI,
    IKatsuyoTextSource,
    KatsuyoText,
    TaigenText,
    FukushiText,
    SettoText,
    KandoushiText,
    SetsuzokuText,
    KigoText,
)
import abc
import re
import warnings
import spacy


class IKatsuyoTextSourceDetector(abc.ABC):
    @abc.abstractmethod
    def try_detect(self, src: Any) -> Optional[IKatsuyoTextSource]:
        """
        不適切な値が代入された際は、Noneを返却する。
        """
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__


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
    DOUSHI_PATTERN = re.compile(r"(動詞|.*動詞的)")
    KEIYOUSHI_PATTERN = re.compile(r"(形容詞|.*形容詞的)")
    # 「形状詞」=「形容動詞の語幹」
    # universaldependenciesのADJは形状詞を形容動詞として扱うが、KatsuyoTextとしては形状詞は名詞として扱う
    # ref. https://universaldependencies.org/treebanks/ja_gsd/ja_gsd-pos-ADJ.html
    # 「記号」e.g., 「ε」
    MEISHI_PATTERN = re.compile(r"(名詞|.*名詞的|形状詞|.*形状詞的)")
    FUKUSHI_PATTERN = re.compile(r"副詞")
    KANDOUSHI_PATTERN = re.compile(r"感動詞")
    SETSUZOKU_PATTERN = re.compile(r"接続詞")
    SETTOU_PATTERN = re.compile(r"(接頭辞|連体詞)")
    KIGO_PATTERN = re.compile(r"(記号|補助記号)")

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
        elif self.KEIYOUSHI_PATTERN.match(tag):
            # ==================================================
            # 形容詞の変形
            # ==================================================
            # e.g. 楽しい -> gokan=楽し + katsuyo=い
            return KatsuyoText(gokan=lemma[:-1], katsuyo=KEIYOUSHI)
        elif self.MEISHI_PATTERN.match(tag):
            return TaigenText(gokan=src.text)
        elif self.FUKUSHI_PATTERN.match(tag):
            return FukushiText(gokan=src.text)
        elif self.SETTOU_PATTERN.match(tag):
            return SettoText(gokan=src.text)
        elif self.KANDOUSHI_PATTERN.match(tag):
            return KandoushiText(gokan=src.text)
        elif self.SETSUZOKU_PATTERN.match(tag):
            return SetsuzokuText(gokan=src.text)
        elif self.KIGO_PATTERN.match(tag):
            return KigoText(gokan=src.text)

        return None


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
