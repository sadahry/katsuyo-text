from typing import Any, Dict, Optional

from katsuyo_text.katsuyo_text import (
    IKatsuyoTextAppendant,
)
from katsuyo_text.katsuyo_text_helper import (
    IJodoushiHelper,
)
import abc


class ISentenceConverter(abc.ABC):
    def __init__(
        self,
        convertions_dict: Dict[IJodoushiHelper, Optional[IKatsuyoTextAppendant]],
    ) -> None:
        self.convertions_dict = convertions_dict

    @abc.abstractmethod
    def convert(self, sent: Any) -> str:
        raise NotImplementedError()
