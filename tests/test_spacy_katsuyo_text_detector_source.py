import pytest
from katsuyo_text.katsuyo_text import (
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
)
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
    KA_GYO_HENKAKU_KURU,
    KA_GYO_HENKAKU_KURU_KANJI,
    KAMI_ICHIDAN,
    KEIYOUSHI,
    SA_GYO_HENKAKU_SURU,
    SA_GYO_HENKAKU_ZURU,
    SHIMO_ICHIDAN,
)
from katsuyo_text.spacy_katsuyo_text_detector import (
    SpacyKatsuyoTextSourceDetector,
)


@pytest.fixture(scope="session")
def spacy_source_detector():
    return SpacyKatsuyoTextSourceDetector()


@pytest.mark.parametrize(
    "msg, text, root_text, pos, expected",
    [
        (
            "形容詞",
            "あなたは美しい",
            "美しい",
            "ADJ",
            KatsuyoText(
                gokan="美し",
                katsuyo=KEIYOUSHI,
            ),
        ),
        (
            "形容動詞",
            "あなたは傲慢だ",
            "傲慢",
            "ADJ",
            TaigenText("傲慢"),
        ),
        (
            "形容動詞",
            "あなたは傲慢で、",
            "傲慢",
            "ADJ",
            TaigenText("傲慢"),
        ),
        (
            "形容動詞",
            "あなたは傲慢です",
            "傲慢",
            "NOUN",
            TaigenText("傲慢"),
        ),
        (
            "名詞",
            "それは明日かな",
            "明日",
            "NOUN",
            TaigenText(
                gokan="明日",
            ),
        ),
        (
            "固有名詞",
            "それはステファンだ",
            "ステファン",
            "PROPN",
            TaigenText(
                gokan="ステファン",
            ),
        ),
        (
            "数詞",
            "それは230だ",
            "230",
            "NUM",
            TaigenText(
                gokan="230",
            ),
        ),
        (
            "副詞",
            "それはとてもだ",
            "とても",
            "ADV",
            FukushiText(
                gokan="とても",
            ),
        ),
        (
            "感動詞",
            "ほら",
            "ほら",
            "INTJ",
            KandoushiText(
                gokan="ほら",
            ),
        ),
        (
            "接続詞",
            "しかし",
            "しかし",
            "CCONJ",
            SetsuzokuText(
                gokan="しかし",
            ),
        ),
        (
            "記号",
            "εが",
            "ε",
            "NOUN",
            KigoText(
                gokan="ε",
            ),
        ),
        (
            "記号",
            "εが",
            "ε",
            "NOUN",
            KigoText(
                gokan="ε",
            ),
        ),
    ],
)
def test_spacy_katsuyo_text_source_detector(
    nlp_ja, spacy_source_detector, msg, text, root_text, pos, expected
):
    sent = next(nlp_ja(text).sents)
    root_token = sent.root
    assert root_token.text == root_text, "root token is not correct"
    assert root_token.pos_ == pos, "root token is not correct"
    result = spacy_source_detector.try_detect(root_token)
    assert result == expected, msg


@pytest.mark.parametrize(
    "tag, text, target_i, target_text, target_pos, expected",
    [
        (
            "接尾辞-名詞的-一般",
            "田中さん",
            -1,
            "さん",
            "NOUN",
            TaigenText(
                gokan="さん",
            ),
        ),
        (
            "接尾辞-形容詞的",
            "田中っぽい",
            -1,
            "っぽい",
            "PART",
            KatsuyoText(
                gokan="っぽ",
                katsuyo=KEIYOUSHI,
            ),
        ),
        (
            "接尾辞-形状詞的",
            "田中げ",
            -1,
            "げ",
            "PART",
            TaigenText(
                gokan="げ",
            ),
        ),
        (
            "接尾辞-動詞的",
            "汗ばむ",
            -1,
            "ばむ",
            "NOUN",
            KatsuyoText(
                gokan="ば",
                katsuyo=GODAN_MA_GYO,
            ),
        ),
        (
            "連体詞",
            "あの惣菜",
            0,
            "あの",
            "DET",
            SettoText(
                gokan="あの",
            ),
        ),
        (
            "接頭辞",
            "お惣菜",
            0,
            "お",
            "NOUN",
            SettoText(
                gokan="お",
            ),
        ),
        (
            "補助記号-句点",
            "これは。",
            -1,
            "。",
            "PUNCT",
            KigoText(
                gokan="。",
            ),
        ),
        (
            "補助記号-読点",
            "これは、",
            -1,
            "、",
            "PUNCT",
            KigoText(
                gokan="、",
            ),
        ),
        (
            "補助記号-ＡＡ-顔文字",
            "これですm(__)m",
            -1,
            "m(__)m",
            "PUNCT",
            KigoText(
                gokan="m(__)m",
            ),
        ),
    ],
)
def test_spacy_katsuyo_text_source_detector_detail(
    nlp_ja,
    spacy_source_detector,
    tag,
    text,
    target_i,
    target_text,
    target_pos,
    expected,
):
    sent = next(nlp_ja(text).sents)
    target_token = sent[target_i]
    assert target_token.text == target_text, "target_token is not correct"
    assert target_token.pos_ == target_pos, "target_token is not correct"
    assert target_token.tag_ == tag, "target_token is not correct"
    result = spacy_source_detector.try_detect(target_token)
    assert result == expected, tag


@pytest.mark.parametrize(
    "tag, text, target_i, target_text, expected",
    [
        (
            "助詞-格助詞",
            "田中さんの",
            -1,
            "の",
            KakujoshiText("の"),
        ),
        (
            "助詞-係助詞",
            "田中さんこそ",
            -1,
            "こそ",
            KeijoshiText("こそ"),
        ),
        (
            "助詞-副助詞",
            "田中さんばかり",
            -1,
            "ばかり",
            FukujoshiText("ばかり"),
        ),
        (
            "助詞-接続助詞",
            "田中さんだけど",
            -1,
            "けど",
            SetsuzokujoshiText("けど"),
        ),
        (
            "助詞-終助詞",
            "田中さんなの",
            -1,
            "の",
            ShujoshiText("の"),
        ),
        (
            "助詞-準体助詞",
            "田中さんなので",
            -2,
            "の",
            JuntaijoshiText("の"),
        ),
    ],
)
def test_spacy_katsuyo_text_source_detector_joshi(
    nlp_ja,
    spacy_source_detector,
    tag,
    text,
    target_i,
    target_text,
    expected,
):
    sent = next(nlp_ja(text).sents)
    target_token = sent[target_i]
    assert target_token.text == target_text, "target_token is not correct"
    assert target_token.tag_ == tag, "target_token is not correct"
    result = spacy_source_detector.try_detect(target_token)
    assert result == expected, tag


@pytest.mark.parametrize(
    "msg, text, last_text, last_pos, expected",
    [
        # ref, https://ja.wikipedia.org/wiki/五段活用
        (
            "五段活用",
            "あなたと歩く",
            "歩く",
            "VERB",
            KatsuyoText(
                gokan="歩",
                katsuyo=GODAN_KA_GYO,
            ),
        ),
        (
            "五段活用",
            "あなたと稼ぐ",
            "稼ぐ",
            "VERB",
            KatsuyoText(
                gokan="稼",
                katsuyo=GODAN_GA_GYO,
            ),
        ),
        (
            "五段活用",
            "あなたと話す",
            "話す",
            "VERB",
            KatsuyoText(
                gokan="話",
                katsuyo=GODAN_SA_GYO,
            ),
        ),
        (
            "五段活用",
            "あなたと待つ",
            "待つ",
            "VERB",
            KatsuyoText(
                gokan="待",
                katsuyo=GODAN_TA_GYO,
            ),
        ),
        (
            "五段活用",
            "あなたと死ぬ",
            "死ぬ",
            "VERB",
            KatsuyoText(
                gokan="死",
                katsuyo=GODAN_NA_GYO,
            ),
        ),
        (
            "五段活用",
            "あなたと遊ぶ",
            "遊ぶ",
            "VERB",
            KatsuyoText(
                gokan="遊",
                katsuyo=GODAN_BA_GYO,
            ),
        ),
        (
            "五段活用",
            "本を読む",
            "読む",
            "VERB",
            KatsuyoText(
                gokan="読",
                katsuyo=GODAN_MA_GYO,
            ),
        ),
        (
            "五段活用",
            "あなたと帰る",
            "帰る",
            "VERB",
            KatsuyoText(
                gokan="帰",
                katsuyo=GODAN_RA_GYO,
            ),
        ),
        (
            "五段活用",
            "あなたと買う",
            "買う",
            "VERB",
            KatsuyoText(
                gokan="買",
                katsuyo=GODAN_WAA_GYO,
            ),
        ),
        # 「いく」のみ特殊
        (
            "五段活用",
            "あなたと行く",
            "行く",
            "VERB",
            KatsuyoText(
                gokan="行",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "五段活用",
            "あなたと往く",
            "往く",
            "VERB",
            KatsuyoText(
                gokan="往",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "五段活用",
            "あなたと逝く",
            "逝く",
            "VERB",
            KatsuyoText(
                gokan="逝",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "五段活用",
            "あなたといく",
            "いく",
            "VERB",
            KatsuyoText(
                gokan="い",
                katsuyo=GODAN_IKU,
            ),
        ),
        (
            "五段活用",
            "あなたとゆく",
            "ゆく",
            "VERB",
            KatsuyoText(
                # 「ゆく」は「いく」に
                gokan="い",
                katsuyo=GODAN_IKU,
            ),
        ),
        # ref, https://ja.wikipedia.org/wiki/上一段活用
        (
            "上一段活用",
            "あなたと老いる",
            "老いる",
            "VERB",
            KatsuyoText(
                gokan="老い",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "あなたと居る",
            "居る",
            "VERB",
            KatsuyoText(
                gokan="居",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "あなたといる",
            "いる",
            "VERB",
            KatsuyoText(
                gokan="い",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "あなたと起きる",
            "起きる",
            "VERB",
            KatsuyoText(
                gokan="起き",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "あなたと着る",
            "着る",
            "VERB",
            KatsuyoText(
                gokan="着",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "過ぎる",
            "過ぎる",
            "VERB",
            KatsuyoText(
                gokan="過ぎ",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "あなたと閉じる",
            "閉じる",
            "VERB",
            KatsuyoText(
                gokan="閉じ",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "あなたと落ちる",
            "落ちる",
            "VERB",
            KatsuyoText(
                gokan="落ち",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "野菜を煮る",
            "煮る",
            "VERB",
            KatsuyoText(
                gokan="煮",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "日差しを浴びる",
            "浴びる",
            "VERB",
            KatsuyoText(
                gokan="浴び",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "目に染みる",
            "染みる",
            "VERB",
            KatsuyoText(
                gokan="染み",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "目を見る",
            "見る",
            "VERB",
            KatsuyoText(
                gokan="見",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        (
            "上一段活用",
            "下に降りる",
            "降りる",
            "VERB",
            KatsuyoText(
                gokan="降り",
                katsuyo=KAMI_ICHIDAN,
            ),
        ),
        # ref, https://ja.wikipedia.org/wiki/下一段活用
        (
            "下一段活用",
            "下に見える",
            "見える",
            "VERB",
            KatsuyoText(
                gokan="見え",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "報酬を得る",
            "得る",
            "VERB",
            KatsuyoText(
                gokan="得",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "罰を受ける",
            "受ける",
            "VERB",
            KatsuyoText(
                gokan="受け",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "宣告を告げる",
            "告げる",
            "VERB",
            KatsuyoText(
                gokan="告げ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "映像を見せる",
            "見せる",
            "VERB",
            KatsuyoText(
                gokan="見せ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "小麦粉を混ぜる",
            "混ぜる",
            "VERB",
            KatsuyoText(
                gokan="混ぜ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "小麦粉を捨てる",
            "捨てる",
            "VERB",
            KatsuyoText(
                gokan="捨て",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "うどんを茹でる",
            "茹でる",
            "VERB",
            KatsuyoText(
                gokan="茹で",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "出汁が出る",
            "出る",
            "VERB",
            KatsuyoText(
                gokan="出",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "親戚を尋ねる",
            "尋ねる",
            "VERB",
            KatsuyoText(
                gokan="尋ね",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "すぐに寝る",
            "寝る",
            "VERB",
            KatsuyoText(
                gokan="寝",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "時を経る",
            "経る",
            "VERB",
            KatsuyoText(
                gokan="経",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "ご飯を食べる",
            "食べる",
            "VERB",
            KatsuyoText(
                gokan="食べ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "ご飯を求める",
            "求める",
            "VERB",
            KatsuyoText(
                gokan="求め",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        (
            "下一段活用",
            "麺を入れる",
            "入れる",
            "VERB",
            KatsuyoText(
                gokan="入れ",
                katsuyo=SHIMO_ICHIDAN,
            ),
        ),
        # ref. https://ja.wikipedia.org/wiki/カ行変格活用
        (
            "カ行変格活用",
            "家にくる",
            "くる",
            "VERB",
            KatsuyoText(
                gokan="",
                katsuyo=KA_GYO_HENKAKU_KURU,
            ),
        ),
        (
            "カ行変格活用",
            "家に来る",
            "来る",
            "VERB",
            KatsuyoText(
                gokan="来",
                katsuyo=KA_GYO_HENKAKU_KURU_KANJI,
            ),
        ),
        # ref. https://ja.wikipedia.org/wiki/サ行変格活用
        (
            "サ行変格活用",
            "軽くウォーキングする",
            "する",
            # rootが「ウォーキング」であるため「する」は助動詞的な扱い
            "AUX",
            KatsuyoText(
                gokan="",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
        ),
        (
            "サ行変格活用",
            "フライパンを熱する",
            "熱する",
            "VERB",
            KatsuyoText(
                gokan="熱",
                katsuyo=SA_GYO_HENKAKU_SURU,
            ),
        ),
        (
            "サ行変格活用",
            "影響が生ずる",
            "生ずる",
            "VERB",
            KatsuyoText(
                gokan="生",
                katsuyo=SA_GYO_HENKAKU_ZURU,
            ),
        ),
        # サ行変格活用と間違える可能性がある動詞
        (
            "サ行変格活用と間違われる可能性がある動詞",
            "ひざをずる",
            "ずる",
            "VERB",
            KatsuyoText(
                gokan="ず",
                katsuyo=GODAN_RA_GYO,
            ),
        ),
        (
            "サ行変格活用と間違われる可能性がある動詞",
            "ひざを擦る",
            "擦る",
            "VERB",
            KatsuyoText(
                gokan="擦",
                katsuyo=GODAN_RA_GYO,
            ),
        ),
        # この活用判別は困難なため、現状は未対応
        # (
        #    "サ行変格活用と間違われる可能性がある動詞",
        #     "ひざをする",
        #     "する",
        #     "VERB",
        #     KatsuyoText(
        #         gokan="す",
        #         katsuyo=GODAN_RA_GYO,
        #     ),
        # ),
    ],
)
def test_spacy_katsuyo_text_source_detector_verb(
    nlp_ja, spacy_source_detector, msg, text, last_text, last_pos, expected
):
    sent = next(nlp_ja(text).sents)
    root_token = sent[-1]
    assert root_token.text == last_text, "last token is not correct"
    assert root_token.pos_ == last_pos, "last token is not correct"
    result = spacy_source_detector.try_detect(root_token)
    assert result == expected, msg
