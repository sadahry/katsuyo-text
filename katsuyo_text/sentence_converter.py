from typing import Any, Dict, Optional

from katsuyo_text.katsuyo_text import (
    IKatsuyoTextAppendant,
)
from katsuyo_text.katsuyo_text_helper import (
    IJodoushiHelper,
)
import abc


class ISentenceConverter(abc.ABC):
    """
    与えられた文章からHelperを探し、任意のAppendantに変換する。
    """

    def __init__(
        self,
        # 現状はIJodoushiHelperのみ対応している
        convertions_dict: Dict[IJodoushiHelper, Optional[IKatsuyoTextAppendant]],
    ) -> None:
        self.convertions_dict = convertions_dict

    @abc.abstractmethod
    def convert(self, sent: Any) -> str:
        raise NotImplementedError()
