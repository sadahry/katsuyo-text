import pytest
from katsuyo_text.katsuyo_text_helper import (
    Ukemi,
    Teinei,
    Dantei,
    DanteiTeinei,
)
from katsuyo_text.spacy_sentence_converter import (
    SpacySentenceConverter,
)


@pytest.mark.parametrize(
    "msg, sentence, convertions_dict, expected",
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
            "Teinei->None",
            "公園へ行きまして",
            {
                Teinei(): None,
            },
            "公園へ行って",
        ),
        (
            "Teinei->None",
            "公園で遊びまして",
            {
                Teinei(): None,
            },
            "公園で遊んで",
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
def test_convert_teinei(nlp_ja, msg, sentence, convertions_dict, expected):
    sent = next(nlp_ja(sentence).sents)
    converter = SpacySentenceConverter(convertions_dict)
    result = converter.convert(sent)
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, sentence, convertions_dict, expected",
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
def test_convert_dantei_teinei(nlp_ja, msg, sentence, convertions_dict, expected):
    sent = next(nlp_ja(sentence).sents)
    converter = SpacySentenceConverter(convertions_dict)
    result = converter.convert(sent)
    assert str(result) == expected, msg


@pytest.mark.parametrize(
    "msg, sentence, convertions_dict, expected",
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
        (
            "Contexual Suffix",
            "怒られろ",
            {
                Ukemi(): None,
            },
            "怒れ",
        ),
    ],
)
def test_convert_contextual(nlp_ja, msg, sentence, convertions_dict, expected):
    sent = next(nlp_ja(sentence).sents)
    converter = SpacySentenceConverter(convertions_dict)
    result = converter.convert(sent)
    assert str(result) == expected, msg
