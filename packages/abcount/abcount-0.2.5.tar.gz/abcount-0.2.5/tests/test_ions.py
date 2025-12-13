from abcount import IonMatcher
from abcount.components.classifier import ABClassData
from abcount.model.classifier import AcidType
from abcount.model.classifier import BaseType


ion_matcher = IonMatcher()


def test_ions_matcher_1():
    abcd = ABClassData(
        acid_1_class=AcidType.STRONG,
        acid_2_class=None,
        base_1_class=BaseType.STRONG,
        base_2_class=None,
    )
    ion_def = ion_matcher.match_class_data(abcd)
    assert ion_def.major_species_ph74_class == "zwitterion"
    assert ion_def.ion_class == "zwitterion"
    assert ion_def.explanation == "acid_1_class: strong_acid, base_1_class: strong_base"


def test_ions_matcher_json_1():
    abcd = ABClassData(
        acid_1_class=AcidType.STRONG,
        acid_2_class=None,
        base_1_class=BaseType.STRONG,
        base_2_class=None,
    )
    ion_def = ion_matcher.match_class_data(abcd).to_json()
    expected = '{"class_data": {"acid_1_class": "strong_acid", "acid_2_class": null, "base_1_class": "strong_base", "base_2_class": null}, "major_species_ph74_class": "zwitterion", "ion_class": "zwitterion", "explanation": "acid_1_class: strong_acid, base_1_class: strong_base"}'  # noqa
    assert ion_def == expected


def test_ions_matcher_ignore_nones():
    abcd = ABClassData(
        acid_1_class=AcidType.STRONG,
        acid_2_class=AcidType.NONE,  # ignored
        base_1_class=BaseType.STRONG,
        base_2_class=None,
    )
    ion_def = ion_matcher.match_class_data(abcd)
    assert ion_def.major_species_ph74_class == "zwitterion"
    assert ion_def.ion_class == "zwitterion"
    assert ion_def.explanation == "acid_1_class: strong_acid, base_1_class: strong_base"


def test_ions_matcher_undefined():
    abcd = ABClassData(
        acid_1_class=AcidType.STRONG,
        acid_2_class=None,
        base_1_class=BaseType.STRONG,
        base_2_class=BaseType.STRONG,
    )
    ion_def = ion_matcher.match_class_data(abcd)
    assert ion_def.major_species_ph74_class == "zwitterion"
    assert ion_def.ion_class == "zwitterion"
    assert (
        ion_def.explanation
        == "acid_1_class: strong_acid, base_1_class: strong_base, base_2_class: strong_base"
    )
