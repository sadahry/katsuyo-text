import pytest
from katsuyo_text.katsuyo_text import (
    FUKUJOSHI_BAKARI,
    FUKUJOSHI_DAKE,
    FUKUJOSHI_HODO,
    FUKUJOSHI_KA,
    FUKUJOSHI_KIRI,
    FUKUJOSHI_KURAI,
    FUKUJOSHI_MADE,
    FUKUJOSHI_NADO,
    # FUKUJOSHI_NARI,
    FUKUJOSHI_NOMI,
    FUKUJOSHI_YARA,
    FUKUJOSHI_ZUTSU,
    SETSUZOKUJOSHI_GA,
    SETSUZOKUJOSHI_SHI,
    SETSUZOKUJOSHI_TO,
    SETSUZOKUJOSHI_DO,
    # SETSUZOKUJOSHI_NI,
    SETSUZOKUJOSHI_BA,
    SETSUZOKUJOSHI_KARA,
    SETSUZOKUJOSHI_TSUTSU,
    SETSUZOKUJOSHI_TOMO,
    SETSUZOKUJOSHI_NARI,
    SETSUZOKUJOSHI_NAGARA,
    SETSUZOKUJOSHI_KEREDO,
    SHUJOSHI_KA,
    SHUJOSHI_KASHIRA,
    SHUJOSHI_NA,
    SHUJOSHI_NO,
    KatsuyoTextError,
)
from katsuyo_text.spacy_katsuyo_text_detector import (
    SpacyKatsuyoTextAppendantDetector,
    ALL_APPENDANTS_DETECTOR,
)
from katsuyo_text.katsuyo_text_helper import (
    IKatsuyoTextHelper,
    Denbun,
    HikyoReizi,
    KakoKanryo,
    Keizoku,
    KibouOthers,
    KibouSelf,
    Suitei,
    Touzen,
    Ukemi,
    Shieki,
    Hitei,
    Youtai,
    Dantei,
    DanteiTeinei,
    Teinei,
    TeDe,
    TatteDatte,
)


@pytest.fixture(scope="session")
def spacy_appendants_detector():
    return ALL_APPENDANTS_DETECTOR


def katsuyo_texts_appendants_detector_init_validation_error():
    class UnsupportedHelper(IKatsuyoTextHelper):
        def __init__(self):
            super().__init__(bridge=lambda x: x)

        def try_merge(self, _):
            return None

    with pytest.raises(KatsuyoTextError):
        SpacyKatsuyoTextAppendantDetector((UnsupportedHelper()))
        assert False, "UnsupportedHelper should not be accepted."


@pytest.mark.filterwarnings("ignore:this object doesn't have helper")
def katsuyo_texts_appendants_detector_init_warning():
    SpacyKatsuyoTextAppendantDetector((Ukemi()))


@pytest.mark.parametrize(
    "text, norm, pos, expected",
    [
        (
            "あなたに行動をされる",
            "れる",
            "AUX",
            [Ukemi],
        ),
        (
            "称号が与えられる",
            "られる",
            "AUX",
            [Ukemi],
        ),
        (
            "あなたを愛させる",
            "せる",
            "AUX",
            [Shieki],
        ),
        (
            "子供を寝させる",
            "させる",
            "AUX",
            [Shieki],
        ),
        (
            "子供を愛さない",
            "ない",
            "AUX",
            [Hitei],
        ),
        (
            "子供が寝ない",
            "ない",
            "AUX",
            [Hitei],
        ),
        (
            "宿題もせず",
            "ず",
            "AUX",
            [Hitei],
        ),
        (
            "子供は産まぬ",
            # 「ぬ」のnormは「ず」になる
            "ず",
            "AUX",
            [Hitei],
        ),
        (
            "子供は産まん",
            # 「ん」のnormは「ず」になる
            "ず",
            "AUX",
            [Hitei],
        ),
        # NOTE: 「仕方ない」は一つの形容詞として抽出されるが、
        #       「仕方がない」は文節を区切られ、否定として抽出される。
        #
        #       文章全体の意味を成立させるうえで問題は発生しないためBugとはしないが、
        #       否定の意味を扱ううえでは問題となるため、改善の余地がある。
        (
            "それは仕方ない",
            "仕方無い",
            "ADJ",
            [],
        ),
        (
            "それは仕方がない",
            "無い",
            "ADJ",
            [],
        ),
        (
            "あなたを愛したい",
            "たい",
            "AUX",
            [KibouSelf],
        ),
        (
            "子供が遊びたがる",
            "たがる",
            "AUX",
            [KibouOthers],
        ),
        (
            "とても歩いた",
            "た",
            "AUX",
            [KakoKanryo],
        ),
        (
            "とても走った",
            "た",
            "AUX",
            [KakoKanryo],
        ),
        (
            "とても遊んだ",
            "た",
            "AUX",
            [KakoKanryo],
        ),
        # 「そう」は「様態」「伝聞」の意味を持つためテスト追加
        (
            "とても遊びそう",
            "そう",
            "AUX",
            [Youtai],
        ),
        (
            "とてもきそう",
            "そう",
            "AUX",
            [Youtai],
        ),
        (
            "とてもしそう",
            "そう",
            "AUX",
            [Youtai],
        ),
        (
            "とても重そう",
            "そう",
            "AUX",
            [Youtai],
        ),
        # っぽい  PART    接尾辞-形容詞的
        (
            "とても保守的っぽそう",
            "そう",
            "AUX",
            [Youtai],
        ),
        (
            "とても困難そう",
            "そう",
            "AUX",
            [Youtai],
        ),
        # 辞書にある「〜的」
        (
            "その発想は保守的そう",
            "そう",
            "AUX",
            [Youtai],
        ),
        # 辞書にない「〜的」
        (
            "その発想はパリピ的そう",
            "そう",
            # ja_ginzaだとこうなっただけ。モデルに応じて変わるかも。
            "ADV",
            [Youtai],
        ),
        (
            "とても遊ぶそう",
            "そう",
            "AUX",
            [Denbun],
        ),
        (
            "とてもくるそう",
            "そう",
            "AUX",
            [Denbun],
        ),
        (
            "とてもするそう",
            "そう",
            "AUX",
            [Denbun],
        ),
        (
            "とても重いそう",
            "そう",
            "AUX",
            [Denbun],
        ),
        (
            "とても保守的っぽいそう",
            "そう",
            "AUX",
            [Denbun],
        ),
        (
            "とても困難だそう",
            "そう",
            "AUX",
            [Dantei, Denbun],
        ),
        # 辞書にある「〜的」
        (
            "その発想は保守的だそう",
            "そう",
            "AUX",
            [Dantei, Denbun],
        ),
        # 辞書にない「〜的」
        (
            "パリピ的だそう",
            "そう",
            "AUX",
            [Dantei, Denbun],
        ),
        # NOTE: 明確に意味を判別できないケースが存在するが、テストケースには追加しない
        #       たとえば「ご飯を食べたそう」において、
        #       「すでにご飯を食べてきたそうだ（過去の「た」＋伝聞の「そうだ」）」か
        #       「食べたいと思っていそうだ（希望の「たい」＋様態の「そうだ」）」の区別がつかない
        #
        #       文章全体の意味を成立させるうえで問題は発生しないためBugとはしないが、
        #       意味を扱ううえでは問題となるため、改善の余地がある。
        # (
        #     "ご飯を食べたそう",
        #     "そう",
        #     "AUX",
        #     [Union[Denbun, Youtai]],
        # ),
        (
            "とても良いらしい",
            "らしい",
            "AUX",
            [Suitei],
        ),
        (
            "とても困難らしい",
            "らしい",
            "AUX",
            [Suitei],
        ),
        (
            "するべき",
            "べし",
            "AUX",
            [Touzen],
        ),
        (
            "つくるべし",
            "べし",
            "AUX",
            [Touzen],
        ),
        (
            "遊ぶよう",
            "よう",
            "AUX",
            [HikyoReizi],
        ),
        (
            "とても良いよう",
            "よう",
            "AUX",
            [HikyoReizi],
        ),
        (
            "とても困難なよう",
            "よう",
            "AUX",
            [Dantei, HikyoReizi],
        ),
        # NOTE: 名詞として扱われる場合、「よう」がrootとなりappendantとしては
        #       何も抽出されない
        (
            "まるで宝石のよう",
            "よう",
            "NOUN",
            [],
        ),
        (
            "まるで宝石だ",
            "だ",
            "AUX",
            [Dantei],
        ),
        (
            "まるで宝石です",
            "です",
            "AUX",
            [DanteiTeinei],
        ),
        (
            "外で遊びます",
            "ます",
            "AUX",
            [Teinei],
        ),
        (
            "遊んでる",
            "てる",
            "AUX",
            [Keizoku],
        ),
        (
            "笑ってる",
            "てる",
            "AUX",
            [Keizoku],
        ),
        # TODO 複数ケースの追加
        # (
        #     # 「では」で「だ」が取れないように
        #     "あんまり成功しなそう",
        #     "無い",
        #     "AUX",
        #     [Hitei, 伝聞],
        # ),
        # (
        #     # 「で」で「だ」が取れないように
        #     "それは愛ではない",
        #     "無い",
        #     "AUX",
        #     [Hitei],
        # ),
        # (
        #     # 「て」で「た」が取れないように
        #     "それは努力してない",
        #     "ない",
        #     "AUX",
        #     [Hitei],
        # ),
    ],
)
def test_spacy_katsuyo_text_appendants_detector(
    nlp_ja, spacy_appendants_detector, text, norm, pos, expected
):
    sent = next(nlp_ja(text).sents)
    last_token = sent[-1]
    assert last_token.norm_ == norm, "last token is not correct"
    assert last_token.pos_ == pos, "last token is not correct"
    appendants, has_error = spacy_appendants_detector.detect_from_sent(sent, sent.root)
    assert not has_error, "has error in detection"
    appendant_types = [type(appendant) for appendant in appendants]
    assert appendant_types == expected


@pytest.mark.parametrize(
    "text, norm, tag, expected",
    [
        (
            "あなたを愛するばかり",
            "ばかり",
            "助詞-副助詞",
            [FUKUJOSHI_BAKARI],
        ),
        (
            "あなたを愛するばっかり",
            "ばかり",
            "助詞-副助詞",
            [FUKUJOSHI_BAKARI],
        ),
        (
            "あなたを愛するまで",
            "まで",
            "助詞-副助詞",
            [FUKUJOSHI_MADE],
        ),
        (
            "あなたを愛するだけ",
            "だけ",
            "助詞-副助詞",
            [FUKUJOSHI_DAKE],
        ),
        (
            "あなたを愛するほど",
            "ほど",
            "助詞-副助詞",
            [FUKUJOSHI_HODO],
        ),
        (
            "あなたを愛するくらい",
            "くらい",
            "助詞-副助詞",
            [FUKUJOSHI_KURAI],
        ),
        (
            "あなたを愛するぐらい",
            "くらい",
            "助詞-副助詞",
            [FUKUJOSHI_KURAI],
        ),
        (
            "あなたを愛するなど",
            "など",
            "助詞-副助詞",
            [FUKUJOSHI_NADO],
        ),
        # 「なり」を取得できる例文がない
        # (
        #     "あなたを信じるなり",
        #     "なり",
        #     "助詞-副助詞",
        #     [FUKUJOSHI_NARI],
        # ),
        (
            "あなたを愛するやら",
            "やら",
            "助詞-副助詞",
            [FUKUJOSHI_YARA],
        ),
        (
            "あなたを愛するかどうか",
            "か",
            "助詞-副助詞",
            [FUKUJOSHI_KA],
        ),
        (
            "あなたを愛するのみ",
            "のみ",
            "助詞-副助詞",
            [FUKUJOSHI_NOMI],
        ),
        (
            "あなたを愛するひとつずつ",
            "ずつ",
            "助詞-副助詞",
            [FUKUJOSHI_ZUTSU],
        ),
        (
            "あなたに付きっきり",
            "きり",
            "助詞-副助詞",
            [FUKUJOSHI_KIRI],
        ),
        (
            "あなたはひとりきり",
            "きり",
            "助詞-副助詞",
            [FUKUJOSHI_KIRI],
        ),
    ],
)
def test_spacy_fukujoshi_appendants_detector(
    nlp_ja, spacy_appendants_detector, text, norm, tag, expected
):
    sent = next(nlp_ja(text).sents)
    last_token = sent[-1]
    assert last_token.norm_ == norm, "last token is not correct"
    assert last_token.tag_ == tag, "last token is not correct"
    appendants, has_error = spacy_appendants_detector.detect_from_sent(sent, sent.root)
    assert not has_error, "has error in detection"
    assert appendants == expected


@pytest.mark.parametrize(
    "text, lemma, tag, expected",
    [
        (
            "あなたを愛するが、",
            "が",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_GA,
        ),
        (
            "あなたを愛するし、",
            "し",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_SHI,
        ),
        (
            "あなたを愛して、",
            "て",
            "助詞-接続助詞",
            TeDe(),
        ),
        (
            "あなたと遊んで、",
            "で",
            "助詞-接続助詞",
            TeDe(),
        ),
        (
            "あなたを愛すると、",
            "と",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_TO,
        ),
        (
            "あなたを愛すれど、",
            "ど",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_DO,
        ),
        # 用例がないためスキップ
        # (
        #     "あなたは要するに、",
        #     "に",
        #     "助詞-接続助詞",
        #     SETSUZOKUJOSHI_NI,
        # ),
        (
            "あなたを愛すれば、",
            "ば",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_BA,
        ),
        (
            "あなたを愛するから、",
            "から",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_KARA,
        ),
        (
            "あなたを愛しつつ、",
            "つつ",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_TSUTSU,
        ),
        (
            "あなたを愛するとも、",
            "とも",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_TOMO,
        ),
        (
            "あなたを愛するなり大切にするなり、",
            "なり",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_NARI,
        ),
        (
            "あなたを愛したって、",
            "たって",
            "助詞-接続助詞",
            TatteDatte(),
        ),
        (
            "あなたが遊んだって、",
            # "だって", # sudachiの辞書の正規形が正しくない「たって」となるためlemmaで対応
            "だって",
            "助詞-接続助詞",
            TatteDatte(),
        ),
        (
            "あなたと遊びながら、",
            "ながら",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_NAGARA,
        ),
        (
            "あなたと遊ぶけれど、",
            "けれど",
            "助詞-接続助詞",
            SETSUZOKUJOSHI_KEREDO,
        ),
    ],
)
def test_spacy_setsuzokujoshi_appendants_detector(
    nlp_ja, spacy_appendants_detector, text, lemma, tag, expected
):
    sent = next(nlp_ja(text).sents)
    last_token = sent[-2]
    assert last_token.lemma_ == lemma, "last token is not correct"
    assert last_token.tag_ == tag, "last token is not correct"
    appendants, has_error = spacy_appendants_detector.try_detect(last_token)
    assert not has_error, "has error in detection"
    assert appendants == expected


@pytest.mark.parametrize(
    "text, norm, tag, expected",
    [
        (
            "あなたを愛するの",
            "の",
            "助詞-終助詞",
            [SHUJOSHI_NO],
        ),
        (
            "きっと泣くな",
            "な",
            "助詞-終助詞",
            [SHUJOSHI_NA],
        ),
        (
            "あなたを愛するのか",
            "か",
            "助詞-終助詞",
            [SHUJOSHI_KA],
        ),
        (
            "あなたを愛するか",
            "か",
            "助詞-終助詞",
            [SHUJOSHI_KA],
        ),
        (
            "あなたを愛せるかしら",
            "かしら",
            "助詞-終助詞",
            [SHUJOSHI_KASHIRA],
        ),
    ],
)
def test_spacy_shujoshi_appendants_detector(
    nlp_ja, spacy_appendants_detector, text, norm, tag, expected
):
    sent = next(nlp_ja(text).sents)
    last_token = sent[-1]
    assert last_token.norm_ == norm, "last token is not correct"
    assert last_token.tag_ == tag, "last token is not correct"
    appendants, has_error = spacy_appendants_detector.detect_from_sent(sent, sent.root)
    assert not has_error, "has error in detection"
    assert appendants == expected


@pytest.mark.parametrize(
    "text, norm, pos",
    [
        (
            "嫉妬しちゃう",
            "ちゃう",
            "AUX",
        ),
        (
            "悲しんじゃう",
            # 「ちゃう」になる
            "ちゃう",
            "AUX",
        ),
        (
            "嫉妬しやがる",
            "やがる",
            "AUX",
        ),
        # TODO 副助詞, 終助詞, 接続助詞
    ],
)
@pytest.mark.filterwarnings("ignore:Unsupported")
def test_spacy_katsuyo_text_appendants_detector_warning(
    nlp_ja, spacy_appendants_detector, text, norm, pos
):
    sent = next(nlp_ja(text).sents)
    last_token = sent[-1]
    assert last_token.norm_ == norm, "last token is not correct"
    assert last_token.pos_ == pos, "last token is not correct"
    appendants, has_error = spacy_appendants_detector.detect_from_sent(sent, sent.root)
    assert has_error, "has error in detection"
    assert appendants == [], f"{norm} will be ignored"


@pytest.mark.parametrize(
    "text, norm, pos",
    [
        (
            "嫉妬しちゃう",
            "ちゃう",
            "AUX",
        ),
        (
            "悲しんじゃう",
            # 「ちゃう」になる
            "ちゃう",
            "AUX",
        ),
        (
            "嫉妬しやがる",
            "やがる",
            "AUX",
        ),
        # TODO 副助詞, 終助詞, 接続助詞
    ],
)
@pytest.mark.filterwarnings("ignore:Unsupported")
def test_spacy_katsuyo_text_appendants_detector_ignore_warning(nlp_ja, text, norm, pos):
    spacy_appendants_detector_ignore_warning = SpacyKatsuyoTextAppendantDetector(
        log_warning=False
    )
    sent = next(nlp_ja(text).sents)
    last_token = sent[-1]
    assert last_token.norm_ == norm, "last token is not correct"
    assert last_token.pos_ == pos, "last token is not correct"
    appendants, has_error = spacy_appendants_detector_ignore_warning.detect_from_sent(
        sent, sent.root
    )
    assert not has_error, "has error in detection"
    assert appendants == [], f"{norm} will be ignored"
