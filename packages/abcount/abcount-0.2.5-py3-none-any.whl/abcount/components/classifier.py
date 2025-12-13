import numpy as np

from abcount.model.classifier import ABClassData
from abcount.model.classifier import AcidType
from abcount.model.classifier import BaseType
from abcount.model.classifier import PKaAttribute
from abcount.model.classifier import Rule


def isnone(value, _):
    return value is None


class AcidRule:
    NONE = Rule(operator=isnone, type=AcidType.NONE, value=None)
    STRONG = Rule(operator=np.less, type=AcidType.STRONG, value=6.4)
    WEAK = Rule(operator=np.less, type=AcidType.WEAK, value=7.4)
    NEGLEGIBLE = Rule(operator=np.greater_equal, type=AcidType.NONE, value=7.4)


class BaseRule:
    NONE = Rule(operator=isnone, type=BaseType.NONE, value=None)
    STRONG = Rule(operator=np.greater, type=BaseType.STRONG, value=8.4)
    WEAK = Rule(operator=np.greater, type=BaseType.WEAK, value=7.4)
    NEGLEGIBLE = Rule(operator=np.less_equal, type=BaseType.NONE, value=7.4)


class ABClassBuilder:
    """Maps pKa data to acid/base classes according to
    a customisable set of rules."""

    def build(
        self, input: dict, pka_attribute_cls=PKaAttribute, num_acids=2, num_bases=2
    ):
        self.classes_obj = ABClassData()
        self.__pka_attribute_cls__ = pka_attribute_cls
        self.num_acids = num_acids
        self.num_bases = num_bases
        self._set_attribute_lists()
        self._build_attribute_map()
        self.predict_input(input)
        return self.classes_obj

    def _build_attribute_map(self) -> None:
        self.__pka_to_group_map__ = {
            self.__pka_attribute_cls__.ACID_1: ABClassData.ACID_1_FIELD,
            self.__pka_attribute_cls__.ACID_2: ABClassData.ACID_2_FIELD,
            self.__pka_attribute_cls__.BASE_1: ABClassData.BASE_1_FIELD,
            self.__pka_attribute_cls__.BASE_2: ABClassData.BASE_2_FIELD,
        }

    def _set_attribute_lists(self) -> None:
        self.acid_attribute_list = [
            self.__pka_attribute_cls__.ACID_1,
            self.__pka_attribute_cls__.ACID_2,
        ][: self.num_acids]
        self.base_attribute_list = [
            self.__pka_attribute_cls__.BASE_1,
            self.__pka_attribute_cls__.BASE_2,
        ][: self.num_bases]

    def predict_input(self, input: dict) -> str:
        self._classify_acids(input)
        self._classify_bases(input)

    def _classify_acids(self, input):
        self._classify_group(
            input,
            # ordered by priority of execution
            rules=[AcidRule.NONE, AcidRule.STRONG, AcidRule.WEAK, AcidRule.NEGLEGIBLE],
            attributes=self.acid_attribute_list,
        )

    def _classify_bases(self, input):
        self._classify_group(
            input,
            # ordered by priority of execution
            rules=[BaseRule.NONE, BaseRule.STRONG, BaseRule.WEAK, BaseRule.NEGLEGIBLE],
            attributes=self.base_attribute_list,
        )

    def _classify_group(self, input, rules, attributes) -> None:
        """Match pKa values to classes."""
        for pka_attr in attributes:
            pka_value = input[pka_attr]
            for r in rules:
                func = r.operator
                ref_value = r.value
                ion_attr = self.__pka_to_group_map__[pka_attr]
                if func(pka_value, ref_value):
                    assigned_class = r.type
                    setattr(self.classes_obj, ion_attr, assigned_class)
                    break


class PKaClassBuilder:
    @classmethod
    def build(cls, **overrides):
        """
        Return a CustomPKaAttribute class with overridden values.
        Any attributes not given in overrides will
        fall back to the parent values.
        """
        return type("CustomPKaAttribute", (PKaAttribute,), overrides)


if __name__ == "__main__":
    example = {
        "pka_acid1": 3.5,
        "pka_acid2": None,
        "pka_base1": 3.785,
        "pka_base2": None,
    }
    print(example)
    mjc = ABClassBuilder()
    mjc.predict_from_dict(example)
    mjc.get_classes_obj()
