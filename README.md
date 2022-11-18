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
