import _match
import _report
import pytest

from abcount import ABCounter


abcounter = ABCounter()
validator = _match.ABValidator
entry_factory = _report.ReportEntryFactory


class SmartsMatcherMock:
    def generate_matches_list(self, mol):
        return [({"smarts": "foo", "type": "bar"}, 2)]


def test_tp_outcome_excess():
    outcome = validator.generate_outcome(expected_groups=2, predicted_groups=4)
    assert isinstance(outcome, _match.TruePositive)


def test_tp_outcome_defect():
    outcome = validator.generate_outcome(expected_groups=2, predicted_groups=1)
    assert isinstance(outcome, _match.TruePositive)


def test_fp_outcome():
    outcome = validator.generate_outcome(expected_groups=1, predicted_groups=2)
    assert isinstance(outcome, _match.FalsePositive)


def test_fn_outcome():
    outcome = validator.generate_outcome(expected_groups=1, predicted_groups=0)
    assert isinstance(outcome, _match.FalseNegative)


def test_fp_reporter():
    fp_outcome = validator.generate_outcome(expected_groups=1, predicted_groups=2)
    entry = entry_factory.generate_entry(
        SmartsMatcherMock(), fp_outcome, "FOO"
    )  # valid mock smiles
    reporter = _report.ReportGenerator()
    reporter.add(entry)
    expected = {
        "target": {0: "FOO"},
        "smarts": {0: "foo"},
        "matches": {0: 2},
        "total_expected_matches": {0: 1},
    }  # noqa
    assert reporter.fp_df.to_dict() == expected


def test_fp_runtime_error_reporter():
    with pytest.raises(RuntimeError):
        fp_outcome = validator.generate_outcome(expected_groups=1, predicted_groups=2)
        _ = entry_factory.generate_entry(
            SmartsMatcherMock(), fp_outcome, "FOOBAr"
        )  # invalid mock smiles


def test_fn_reporter():
    fn_outcome = validator.generate_outcome(expected_groups=1, predicted_groups=0)
    entry = entry_factory.generate_entry(
        SmartsMatcherMock(), fn_outcome, "FOO"
    )  # valid mock smiles
    reporter = _report.ReportGenerator()
    reporter.add(entry)
    expected = {"target": {0: "FOO"}, "total_expected_matches": {0: 1}}  # noqa
    assert reporter.fn_df.to_dict() == expected
