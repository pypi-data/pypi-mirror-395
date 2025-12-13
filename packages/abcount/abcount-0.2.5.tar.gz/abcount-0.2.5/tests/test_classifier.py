import pytest

from abcount import ABClassBuilder
from abcount import PKaClassBuilder
from abcount.components.classifier import ABClassData
from abcount.components.classifier import AcidType
from abcount.components.classifier import BaseType


@pytest.mark.parametrize(
    "input_dict,expected",
    [
        (
            {
                "pka_acid1": 3.5,
                "pka_acid2": None,
                "pka_base1": 3.785,
                "pka_base2": None,
            },
            ABClassData(
                acid_1_class=AcidType.STRONG,
                acid_2_class=AcidType.NONE,
                base_1_class=BaseType.NONE,
                base_2_class=BaseType.NONE,
            ),
        ),
        (
            {"pka_acid1": 3.5, "pka_acid2": 4.5, "pka_base1": 3.785, "pka_base2": None},
            ABClassData(
                acid_1_class=AcidType.STRONG,
                acid_2_class=AcidType.STRONG,
                base_1_class=BaseType.NONE,
                base_2_class=BaseType.NONE,
            ),
        ),
        (
            {"pka_acid1": 6.3, "pka_acid2": 7.3, "pka_base1": 3.785, "pka_base2": None},
            ABClassData(
                acid_1_class=AcidType.STRONG,
                acid_2_class=AcidType.WEAK,
                base_1_class=BaseType.NONE,
                base_2_class=BaseType.NONE,
            ),
        ),
        (
            {"pka_acid1": 6.4, "pka_acid2": 7.4, "pka_base1": 3.785, "pka_base2": None},
            ABClassData(
                acid_1_class=AcidType.WEAK,
                acid_2_class=AcidType.NONE,
                base_1_class=BaseType.NONE,
                base_2_class=BaseType.NONE,
            ),
        ),
        (
            {
                "pka_acid1": None,
                "pka_acid2": 7.3,
                "pka_base1": 7.785,
                "pka_base2": None,
            },
            ABClassData(
                acid_1_class=AcidType.NONE,
                acid_2_class=AcidType.WEAK,
                base_1_class=BaseType.WEAK,
                base_2_class=BaseType.NONE,
            ),
        ),
        (
            {
                "pka_acid1": None,
                "pka_acid2": 7.3,
                "pka_base1": 9.785,
                "pka_base2": None,
            },
            ABClassData(
                acid_1_class=AcidType.NONE,
                acid_2_class=AcidType.WEAK,
                base_1_class=BaseType.STRONG,
                base_2_class=BaseType.NONE,
            ),
        ),
        (
            {"pka_acid1": None, "pka_acid2": 7.3, "pka_base1": 9.785, "pka_base2": 7.7},
            ABClassData(
                acid_1_class=AcidType.NONE,
                acid_2_class=AcidType.WEAK,
                base_1_class=BaseType.STRONG,
                base_2_class=BaseType.WEAK,
            ),
        ),
        (
            {"pka_acid1": None, "pka_acid2": 7.3, "pka_base1": 9.785, "pka_base2": 7.7},
            ABClassData(
                acid_1_class=AcidType.NONE,
                acid_2_class=AcidType.WEAK,
                base_1_class=BaseType.STRONG,
                base_2_class=BaseType.WEAK,
            ),
        ),
        (
            {
                "pka_acid1": None,
                "pka_acid2": None,
                "pka_base1": 7.785,
                "pka_base2": 7.7,
            },
            ABClassData(
                acid_1_class=AcidType.NONE,
                acid_2_class=AcidType.NONE,
                base_1_class=BaseType.WEAK,
                base_2_class=BaseType.WEAK,
            ),
        ),
    ],
)
def test_abclass_prediction(input_dict, expected):
    classes_obj = ABClassBuilder().build(input_dict)
    assert classes_obj == expected


@pytest.mark.parametrize(
    "input_dict,expected",
    [
        (
            {"my_pkaa1": 3.5, "pka_acid2": None, "my_pkab_1": 3.785, "pka_base2": None},
            ABClassData(
                acid_1_class=AcidType.STRONG,
                acid_2_class=AcidType.NONE,
                base_1_class=BaseType.NONE,
                base_2_class=BaseType.NONE,
            ),
        )
    ],
)
def test_abclass_custom_builder(input_dict, expected):
    CustomPKaAttribute = PKaClassBuilder.build(ACID_1="my_pkaa1", BASE_1="my_pkab_1")
    classes_obj = ABClassBuilder().build(
        input_dict, pka_attribute_cls=CustomPKaAttribute
    )
    assert classes_obj == expected


@pytest.mark.parametrize(
    "input_dict,expected",
    [
        (
            {"my_pkaa1": 3.5, "my_pkab_1": 9.785},
            ABClassData(acid_1_class=AcidType.STRONG, base_1_class=BaseType.STRONG),
        )
    ],
)
def test_abclass_custom_builder_and_groups(input_dict, expected):
    CustomPKaAttribute = PKaClassBuilder.build(ACID_1="my_pkaa1", BASE_1="my_pkab_1")
    classes_obj = ABClassBuilder().build(
        input_dict, pka_attribute_cls=CustomPKaAttribute, num_acids=1, num_bases=1
    )
    assert classes_obj == expected


@pytest.mark.parametrize(
    "input_dict,expected",
    [
        (
            {"my_pkaa_1": 3.5, "my_pkaa_2": 7.5, "my_pkab_1": 9.785},
            ABClassData(acid_1_class=AcidType.STRONG, base_1_class=BaseType.STRONG),
        )
    ],
)
def test_abclass_json(input_dict, expected):
    CustomPKaAttribute = PKaClassBuilder.build(
        ACID_1="my_pkaa_1", ACID_2="my_pkaa_2", BASE_1="my_pkab_1"
    )
    classes_obj = ABClassBuilder().build(
        input_dict, pka_attribute_cls=CustomPKaAttribute, num_acids=2, num_bases=1
    )
    expected = '{"acid_1_class": "strong_acid", "acid_2_class": "no_acid", "base_1_class": "strong_base", "base_2_class": null}'  # noqa
    assert classes_obj.to_json() == expected
