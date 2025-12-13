from enum import Enum

from abcount.components.classifier import ABClassData
from abcount.model.classifier import AcidType
from abcount.model.classifier import BaseType
from abcount.model.ions import IonDefinition


class IonMatcher:
    """Matches AB data to the ion and species definitions."""

    def match_class_data(self, class_data: ABClassData) -> IonDefinition:
        # ignore difference AcidType.NONE | BaseType.NONE and None
        class_data.convert_nones_to_nulls()
        for ion_definition in IonRules:
            ion_obj = ion_definition.value
            if class_data == ion_obj.class_data:
                ion_obj.explanation = self._explanation_from_class_data(class_data)
                return ion_obj

        # If no definition is matched, it's likely a unbalanced zwitterion
        return IonDefinition(
            class_data=class_data,
            major_species_ph74_class="zwitterion",
            ion_class="zwitterion",
            explanation=self._explanation_from_class_data(class_data),
        )

    def _explanation_from_class_data(self, class_data):
        return ", ".join(self._get_list_of_defined_groups(class_data))

    def _get_list_of_defined_groups(self, class_data):
        class_data_dict = class_data.to_dict()
        return [f"{k}: {v.value}" for k, v in class_data_dict.items() if v]


class IonRules(Enum):
    I1 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.STRONG,
            acid_2_class=None,
            base_1_class=BaseType.STRONG,
            base_2_class=None,
        ),
        major_species_ph74_class="zwitterion",
        ion_class="zwitterion",
    )

    I2 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.STRONG,
            acid_2_class=None,
            base_1_class=BaseType.WEAK,
            base_2_class=None,
        ),
        major_species_ph74_class="zwitterion",
        ion_class="zwitterion",
    )

    I3 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.STRONG,
            acid_2_class=AcidType.STRONG,
            base_1_class=None,
            base_2_class=None,
        ),
        major_species_ph74_class="dianion",
        ion_class="diacid",
    )

    I4 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.STRONG,
            acid_2_class=AcidType.WEAK,
            base_1_class=None,
            base_2_class=None,
        ),
        major_species_ph74_class="dianion",
        ion_class="diacid",
    )

    I5 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.STRONG,
            acid_2_class=None,
            base_1_class=None,
            base_2_class=None,
        ),
        major_species_ph74_class="anion",
        ion_class="acid",
    )

    I6 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.WEAK,
            acid_2_class=None,
            base_1_class=None,
            base_2_class=None,
        ),
        major_species_ph74_class="anion",
        ion_class="weak acid",
    )

    I7 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.WEAK,
            acid_2_class=AcidType.WEAK,
            base_1_class=None,
            base_2_class=None,
        ),
        major_species_ph74_class="dianion",
        ion_class="weak diacid",
    )

    I8 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=None,
            acid_2_class=None,
            base_1_class=BaseType.STRONG,
            base_2_class=None,
        ),
        major_species_ph74_class="cation",
        ion_class="base",
    )

    I9 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=None,
            acid_2_class=None,
            base_1_class=BaseType.STRONG,
            base_2_class=BaseType.STRONG,
        ),
        major_species_ph74_class="dication",
        ion_class="dibase",
    )

    I10 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=None,
            acid_2_class=None,
            base_1_class=BaseType.WEAK,
            base_2_class=None,
        ),
        major_species_ph74_class="cation",
        ion_class="weak base",
    )

    I11 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=None,
            acid_2_class=None,
            base_1_class=BaseType.WEAK,
            base_2_class=BaseType.WEAK,
        ),
        major_species_ph74_class="dication",
        ion_class="weak dibase",
    )

    I12 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=None,
            acid_2_class=None,
            base_1_class=BaseType.STRONG,
            base_2_class=BaseType.WEAK,
        ),
        major_species_ph74_class="dication",
        ion_class="dibase",
    )

    I13 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.WEAK,
            acid_2_class=None,
            base_1_class=BaseType.WEAK,
            base_2_class=None,
        ),
        major_species_ph74_class="zwitterion",
        ion_class="weak zwitterion",
    )

    I14 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=AcidType.WEAK,
            acid_2_class=None,
            base_1_class=BaseType.STRONG,
            base_2_class=None,
        ),
        major_species_ph74_class="zwitterion",
        ion_class="zwitterion",
    )

    I15 = IonDefinition(
        class_data=ABClassData(
            acid_1_class=None, acid_2_class=None, base_1_class=None, base_2_class=None
        ),
        major_species_ph74_class="neutral",
        ion_class="neutral",
    )
