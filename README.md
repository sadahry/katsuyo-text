# Katsuyo Text

日本語の活用変換器  
A Japanese conjugation form converter

## Motivation

日本語文法における活用変形をロジックに落とし込めるかの試み

## ⚠CAUTION

現状、挙動は不安定です。必要に応じてアップデートしたいです。

## How to Use
### 追加

```python
from katsuyo_text.katsuyo_text_helper import (
    Hitei,
    KakoKanryo,
    DanteiTeinei,
)
from katsuyo_text.spacy_katsuyo_text_detector import SpacyKatsuyoTextSourceDetector
import spacy


nlp = spacy.load("ja_ginza")
src_detector = SpacyKatsuyoTextSourceDetector()


doc = nlp("今日は旅行に行く")
sent = next(doc.sents)
katsuyo_text = src_detector.try_detect(sent[-1])

katsuyo_text
# => KatsuyoText(gokan='行', katsuyo=GodanKatsuyo(renyo_ta='っ', mizen_u='こ', meirei='け', katei='け', rentai='く', shushi='く', renyo='き', mizen='か'))

print(katsuyo_text + Hitei())
# => 行かない
print(katsuyo_text + Hitei() + KakoKanryo())
# => 行かなかった
print(katsuyo_text + Hitei() + KakoKanryo() + DanteiTeinei())
# => 行かなかったです
```

### 変換

```python
from katsuyo_text.katsuyo_text_helper import (
    Teinei,
    Dantei,
    DanteiTeinei,
)
from katsuyo_text.spacy_sentence_converter import SpacySentenceConverter
import spacy


nlp = spacy.load("ja_ginza")
converter = SpacySentenceConverter(
    conversions_dict={
        Teinei(): None,
        DanteiTeinei(): Dantei(),
    }
)


doc = nlp("今日は旅行に行きました")
sent = next(doc.sents)
print(converter.convert(sent))
# => 今日は旅行に行った

doc = nlp("今日は最高の日でした")
sent = next(doc.sents)
print(converter.convert(sent))
# => 今日は最高の日だった
```

### カスタマイズ

文法的に成立しない活用変形を `bridge` で実現している
```python
from katsuyo_text.katsuyo_text import TaigenText, JODOUSHI_NAI

TaigenText("大丈夫") + JODOUSHI_NAI
# error => katsuyo_text.katsuyo_text.KatsuyoTextError: Unsupported katsuyo_text in merge of <class 'katsuyo_text.katsuyo_text.Nai'>: 大丈夫 type: <class 'katsuyo_text.katsuyo_text.TaigenText'>

from katsuyo_text.katsuyo_text_helper import Hitei
TaigenText("大丈夫") + Hitei()
# => KatsuyoText(gokan='大丈夫ではな', katsuyo=KeiyoushiKatsuyo(katei='けれ', rentai='い', shushi='い', renyo_ta='かっ', renyo='く', mizen='かろ'))

TaigenText("大丈夫") + Hitei() == Hitei().bridge(TaigenText("大丈夫"))
# => True
```

`bridge` はカスタマイズ可能
```python
from katsuyo_text.katsuyo_text import KatsuyoText, TaigenText, KAKUJOSHI_GA
from katsuyo_text.katsuyo import KEIYOUSHI

nai = KatsuyoText(gokan="な", katsuyo=KEIYOUSHI)
custom_hitei = Hitei(bridge=lambda src: src + KAKUJOSHI_GA + nai)

TaigenText("耐性") + custom_hitei
# => KatsuyoText(gokan='耐性がな', katsuyo=KeiyoushiKatsuyo(katei='けれ', rentai='い', shushi='い', renyo_ta='かっ', renyo='く', mizen='かろ'))
```

`IKatsuyoTextHelper` で独自の活用変形を実装可能
```python
from typing import Optional
from katsuyo_text.katsuyo_text_helper import IKatsuyoTextHelper
from katsuyo_text.katsuyo_text import (
    TaigenText,
    KatsuyoTextError,
    IKatsuyoTextSource,
    SetsuzokujoshiText,
    KURU,
    SETSUZOKUJOSHI_KARA,
    JUNTAIJOSHI_NO,
    JODOUSHI_DA_DANTEI,
)


class JunsetsuKakutei(IKatsuyoTextHelper[SetsuzokujoshiText]):
    def try_merge(self, pre: IKatsuyoTextSource) -> Optional[SetsuzokujoshiText]:
        try:
            pre + SETSUZOKUJOSHI_KARA
        except KatsuyoTextError as e:
            # Handle error
            return None


KURU
# => KatsuyoText(gokan='', katsuyo=KaGyoHenkakuKatsuyo(meirei='こい', katei='くれ', rentai='くる', shushi='くる', renyo='き', mizen='こ'))
KURU + JunsetsuKakutei()
# => SetsuzokujoshiText(gokan='くるから', katsuyo=None)

custom_junsetsu_kakutei = JunsetsuKakutei(bridge=lambda src: src + JODOUSHI_DA_DANTEI + SETSUZOKUJOSHI_KARA)

TaigenText("症状") + JunsetsuKakutei()
# error => katsuyo_text.katsuyo_text.KatsuyoTextError: Unsupported katsuyo_text in merge of <class '__main__.JunsetsuKakutei'>: 症状 type: <class 'katsuyo_text.katsuyo_text.TaigenText'> katsuyo: <class 'NoneType'>
TaigenText("症状") + custom_junsetsu_kakutei
# => SetsuzokujoshiText(gokan='症状だから', katsuyo=None)
```
