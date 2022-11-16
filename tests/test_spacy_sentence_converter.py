# TODO あとで本番用に移動
import pytest
import spacy
from typing import Optional, Dict
from katsuyo_text.spacy_katsuyo_text_detector import (
    SpacyKatsuyoTextAppendantDetector,
    SpacyKatsuyoTextSourceDetector,
    ALL_APPENDANTS_DETECTOR,
)
from katsuyo_text.katsuyo_text_helper import (
    IJodoushiHelper,
    Teinei,
    Dantei,
)
from katsuyo_text.katsuyo_text import (
    KatsuyoTextError,
    INonKatsuyoText,
    IKatsuyoTextAppendant,
)


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
                prev_kt = prev_kt + convert_kt
            prev_token = token
            continue

        assert prev_kt is not None
        kt, _ = aad.try_detect(token)
        if kt is None:
            # TODO KatsuyoTextの場合、前後の活用形考慮
            assert isinstance(prev_kt, INonKatsuyoText)
            result += str(prev_kt)
            prev_kt = None
            prev_token = token
            continue

        assert kt is not None
        prev_kt = prev_kt + kt
        prev_token = token
        continue

    if prev_kt is not None:
        result += str(prev_kt)

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
            "公園へ行きました",
            {
                Teinei(): Dantei(),
            },
            "公園へ行くのだった",
        ),
    ],
)
def test_convert(nlp_ja, msg, sentence, convert_map, expected):
    sent = next(nlp_ja(sentence).sents)
    result = convert(sent, convert_map)
    assert str(result) == expected, msg
