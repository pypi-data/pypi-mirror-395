from rdkit import Chem

from abcount import ABCounter
from abcount.components import SmartsMatcher


def test_smarts_matcher_1():
    matcher = SmartsMatcher(["[OX2H]"])
    example_mol = Chem.MolFromSmiles("C(O)COCO")
    res = matcher.count_matches(example_mol)
    expected = 2
    assert res == expected


def test_smarts_matcher_2():
    matcher = SmartsMatcher(["[n;r5][nH;r5][c;r5]"])
    example_mol = Chem.MolFromSmiles("[nH]1nnnc1-c3c2[nH]ncc2ccc3")
    res = matcher.count_matches(example_mol)
    expected = 2
    assert res == expected


def test_abcounter_1():
    smiles = "[nH]1nnnc1-c3c2[nH]ncc2ccc3"
    acid_exp = 2
    base_exp = 2
    mol = Chem.MolFromSmiles(smiles)
    abc = ABCounter()
    res = abc.count_acid_and_bases(mol)
    acid_pred = res["acid"]
    base_pred = res["base"]
    assert acid_exp == acid_pred
    assert base_exp == base_pred
