from dataclasses import dataclass
from enum import Enum
from typing import Callable
from typing import Optional

from dataclasses_json import dataclass_json


class PKaAttribute:
    ACID_1 = "pka_acid1"
    BASE_1 = "pka_base1"
    ACID_2 = "pka_acid2"
    BASE_2 = "pka_base2"


class AcidType(Enum):
    STRONG = "strong_acid"
    WEAK = "weak_acid"
    NONE = "no_acid"


class BaseType(Enum):
    STRONG = "strong_base"
    WEAK = "weak_base"
    NONE = "no_base"


@dataclass_json
@dataclass
class ABClassData:
    """Class for tracking the types of Acid/Base groups in a molecule."""

    acid_1_class: Optional[Enum] = None
    acid_2_class: Optional[Enum] = None
    base_1_class: Optional[Enum] = None
    base_2_class: Optional[Enum] = None

    # references to own field names
    ACID_1_FIELD = "acid_1_class"
    ACID_2_FIELD = "acid_2_class"
    BASE_1_FIELD = "base_1_class"
    BASE_2_FIELD = "base_2_class"

    def convert_nones_to_nulls(self) -> None:
        """Utility method to convert AcidType.NONE and BaseType.NONE to None."""
        for k in self.__dict__.keys():
            if getattr(self, k) in (AcidType.NONE, BaseType.NONE):
                setattr(self, k, None)


@dataclass
class Rule:
    """Rule to determine a class."""

    operator: Callable
    type: Enum
    value: Optional[float]
