# TODO あとで本番用に移動
import pytest
import spacy
from typing import Optional, Set, Dict
from katsuyo_text.spacy_katsuyo_text_detector import (
    SpacyKatsuyoTextAppendantDetector,
    SpacyKatsuyoTextSourceDetector,
    get_conjugation,
    ALL_APPENDANTS_DETECTOR,
)
from katsuyo_text.katsuyo_text_helper import (
    IJodoushiHelper,
    Ukemi,
    Teinei,
    Dantei,
    DanteiTeinei,
)
from katsuyo_text.katsuyo_text import (
    KatsuyoTextError,
    KatsuyoText,
    IKatsuyoTextAppendant,
    FixedKatsuyoText,
)


# 以下からleft-id.def(right-id.def)を取得し、活用形を参照して作成
# ref. https://ja.osdn.net/projects/unidic/downloads/58338/unidic-mecab-2.1.2_src.zip/
# 必要に応じて以下の辞書も参照
# ref. http://sudachi.s3-website-ap-northeast-1.amazonaws.com/sudachidict-raw/20221021/small_lex.zip
MIZEN_FORMS: Set[str] = {
    "未然形-一般",
    # 活用変形の一であるため一般変形として扱える
    "未然形-撥音便",
    # 文語のみであり置き換えられることは稀。現状対応していない
    # "未然形-補助",
    # サ行変格のみであり置き換えられることは稀。現状対応していない
    # "未然形-サ",
    # サ行変格のみであり置き換えられることは稀。現状対応していない
    # "未然形-セ",
}
RENYO_FORMS: Set[str] = {
    "連用形-一般",
    # 連用形の撥音便,促音便はKatsuyoTextで対応しているため一般変形として扱える
    "連用形-撥音便",
    # 連用形の撥音便,促音便はKatsuyoTextで対応しているため一般変形として扱える
    "連用形-促音便",
    # 活用変形の一種であるため一般変形として扱える
    "連用形-イ音便",
    # 助動詞-ダと文語助動詞-ズと文語助動詞-ナリ-断定に表れる
    # 形容動詞のrenyoMixinは「に」としており対応可能
    "連用形-ニ",
    # 文語のみであり置き換えられることは稀。現状対応していない
    # "連用形-補助",
    # 特殊な活用形であるため現状対応していない
    # "連用形-ウ音便",
    # 特殊な活用形であるため現状対応していない
    # "連用形-融合",
    # 文語助動詞-タリ-断定のみ。現状対応していない
    # "連用形-ト",
}
SHUSHI_FORMS: Set[str] = {
    "終止形-一般",
    # 助動詞「ぬ」の変形である可能性が否めず、識別困難であるため現状対応していない
    # "終止形-撥音便",
    # 口語による変形であるため一般変形として扱える
    "連用形-促音便",
    # 口語による変形であるため一般変形として扱える
    "終止形-融合",
    # 文語の特殊な活用形であるため現状対応していない
    # "終止形-ウ音便",
    # 文語の特殊な活用形であるため現状対応していない
    # "終止形-補助",
}
RENTAI_FORMS: Set[str] = {
    "連体形-一般",
    # 助動詞「ぬ」の変形である可能性が否めず、識別困難であるため現状対応していない
    # "連体形-撥音便",
    # 口語による変形であるため一般変形として扱える
    "連体形-省略",
    # 文語の特殊な活用形であるため現状対応していない
    # "連体形-ウ音便",
    # 文語の特殊な活用形であるため現状対応していない
    # "連体形-イ音便",
    # 文語の特殊な活用形であるため現状対応していない
    # "連体形-補助",
}
KATEI_FORMS: Set[str] = {
    "仮定形-一般",
    # 特殊な活用形であるため現状対応していない
    # "仮定形-融合",
}
MEIREI_FORMS: Set[str] = {
    "命令形",
}


def _bridge_by_form(
    pre: KatsuyoText,
    prev_token: spacy.tokens.Token,
) -> FixedKatsuyoText:
    # 前トークンに変更があれば、トークンの活用形からKatsuyoTextを変更する
    _, conjugation_form = get_conjugation(prev_token)
    if conjugation_form is None:
        # 活用形がなく、preがKatsuyoTextである場合には、活用形を推測できないためエラーに
        raise KatsuyoTextError(
            f"Unsupported katsuyo_text in merge of: {pre} "
            f"type: {type(pre)} katsuyo: {type(pre.katsuyo)} "
            f"prev: {prev_token} doc: {prev_token.doc} "
        )

    if conjugation_form in MIZEN_FORMS:
        fkt = pre.as_fkt_mizen
    elif conjugation_form in RENYO_FORMS:
        fkt = pre.as_fkt_renyo
    elif conjugation_form in SHUSHI_FORMS:
        fkt = pre.as_fkt_shushi
    elif conjugation_form in RENTAI_FORMS:
        fkt = pre.as_fkt_rentai
    elif conjugation_form in KATEI_FORMS:
        fkt = pre.as_fkt_katei
    elif conjugation_form in MEIREI_FORMS:
        fkt = pre.as_fkt_meirei
    # 例外パターンは概ねHelperで対応
    # fkt = pre.as_fkt_mizen_u
    # fkt = pre.as_fkt_mizen_reru
    # fkt = pre.as_fkt_mizen_rareru
    # fkt = pre.as_fkt_renyo_ta
    # fkt = pre.as_fkt_renyo_nai

    if fkt is None:
        raise KatsuyoTextError(
            f"Unsupported katsuyo_form: {conjugation_form} "
            f"pre: {pre} type: {type(pre)} katsuyo: {type(pre.katsuyo)}"
        )

    return fkt


def convert(
    sent: spacy.tokens.Span,
    convert_map: Dict[IJodoushiHelper, Optional[IKatsuyoTextAppendant]],
) -> str:
    sd = SpacyKatsuyoTextSourceDetector()
    ad = SpacyKatsuyoTextAppendantDetector(
        helpers=set(convert_map.keys()),
        log_warning=False,
    )
    aad = ALL_APPENDANTS_DETECTOR

    result = ""
    prev_token = None
    prev_kt = None
    for token in sent:
        # at first
        if prev_token is None:
            prev_token = token
            continue

        if prev_kt is None:
            kt, _ = ad.try_detect(token)
            if kt is None:
                result += prev_token.text
                prev_token = token
                continue
            prev_kt = sd.try_detect(prev_token)
            if prev_kt is None:
                raise KatsuyoTextError(
                    f"Unsupported token: {prev_token} tag: {prev_token.tag_} doc: {prev_token.doc}"
                )
            convert_kt = convert_map.get(kt)
            if convert_kt is not None:
                prev_kt += convert_kt
            prev_token = token
            continue

        assert prev_kt is not None
        kt, _ = aad.try_detect(token)
        if kt is None:
            if isinstance(prev_kt, KatsuyoText):
                prev_kt = _bridge_by_form(prev_kt, prev_token)
            result += str(prev_kt)
            prev_kt = None
            prev_token = token
            continue

        assert kt is not None
        prev_kt += kt
        prev_token = token
        continue

    if prev_kt is not None:
        result += str(prev_kt)
    else:
        assert prev_token is not None
        result += prev_token.text

    return result


@pytest.mark.parametrize(
    "msg, sentence, convert_map, expected",
    [
        (
            "Teinei->None",
            "公園を見ました",
            {
                Teinei(): None,
            },
            "公園を見た",
        ),
        (
            "Teinei->None",
            "公園へ行きました",
            {
                Teinei(): None,
            },
            "公園へ行った",
        ),
        (
            "Teinei->None",
            "公園へ行かれますか",
            {
                Teinei(): None,
            },
            "公園へ行かれるか",
        ),
        (
            "Teinei->None",
            "すみません",
            {
                Teinei(): None,
            },
            "すまない",
        ),
        (
            "Teinei->Dantei",
            "公園へ行きまして",
            {
                Teinei(): None,
            },
            "公園へ行って",
        ),
        (
            "Teinei->Dantei",
            "公園へ行きました",
            {
                Teinei(): Dantei(),
            },
            "公園へ行くのだった",
        ),
        # TODO 接続助詞「て」のHelper実装
        # (
        #     "Teinei->Dantei",
        #     "そう言われましても",
        #     {
        #         Teinei(): Dantei(),
        #     },
        #     "そう言われるのであっても",
        # ),
    ],
)
def test_convert_teinei(nlp_ja, msg, sentence, convert_map, expected):
    sent = next(nlp_ja(sentence).sents)
    result = convert(sent, convert_map)
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, sentence, convert_map, expected",
    [
        (
            "DanteiTeinei->Dantei",
            "誕生日でした",
            {
                DanteiTeinei(): Dantei(),
            },
            "誕生日だった",
        ),
        (
            "DanteiTeinei->Dantei",
            "大丈夫ですかね",
            {
                DanteiTeinei(): Dantei(),
            },
            "大丈夫かね",
        ),
    ],
)
def test_convert_dantei_teinei(nlp_ja, msg, sentence, convert_map, expected):
    sent = next(nlp_ja(sentence).sents)
    result = convert(sent, convert_map)
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, sentence, convert_map, expected",
    [
        (
            "Contexual IJodoushiHelper",
            "怒られに行く",
            {
                Ukemi(): None,
            },
            "怒りに行く",
        ),
        (
            "Contexual Suffix",
            "怒られまくれ",
            {
                Ukemi(): None,
            },
            "怒りまくれ",
        ),
        (
            "Contexual Suffix",
            "怒られた",
            {
                Ukemi(): None,
            },
            "怒った",
        ),
    ],
)
def test_convert_contextual(nlp_ja, msg, sentence, convert_map, expected):
    sent = next(nlp_ja(sentence).sents)
    result = convert(sent, convert_map)
    assert str(result) == expected, msg
