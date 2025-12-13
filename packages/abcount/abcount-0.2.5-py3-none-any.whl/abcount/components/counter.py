import logging

import rdkit
from rdkit import Chem

from abcount.components.smarts import SmartsMatcherJson
from abcount.config import fps
from abcount.model.counter import GroupTypeAttribute


logger = logging.getLogger(__name__)


class ABCounter:
    def __init__(
        self,
        acid_defs_filepath=fps.acid_defs_filepath,
        base_defs_filepath=fps.base_defs_filepath,
    ):
        """
        Counts acidic and basic functional groups in a molecule using SMARTS pattern matching.

        Args:
            acid_defs_filepath (str): Path to custom acidic SMARTS definitions (optional).
            base_defs_filepath (str): Path to custom basic SMARTS definitions (optional).

        Attributes:
            acid_matcher (SmartsMatcherJson): Matcher for acidic functional group patterns.
            base_matcher (SmartsMatcherJson): Matcher for basic functional group patterns.
        """
        self.acid_defs_filepath = acid_defs_filepath
        self.base_defs_filepath = base_defs_filepath
        logger.debug(f"Loading Acidic SMARTS from path: {self.acid_defs_filepath}")
        logger.debug(f"Loading Basic SMARTS from path: {self.base_defs_filepath}")
        self.acid_matcher = SmartsMatcherJson(self.acid_defs_filepath)
        self.base_matcher = SmartsMatcherJson(self.base_defs_filepath)

    def count_acid_and_bases(self, mol: rdkit.Chem.Mol):
        """
        Count acidic and basic groups in the given molecule.

        Args:
            mol (rdkit.Chem.Mol): An RDKit molecule object.

        Returns:
            dict: A dictionary with counts keyed by GroupTypeAttribute.ACID and
                  GroupTypeAttribute.BASE.
        """
        acid_count = self.acid_matcher.count_matches(mol)
        base_count = self.base_matcher.count_matches(mol)
        return {
            GroupTypeAttribute.ACID: acid_count,
            GroupTypeAttribute.BASE: base_count,
        }


if __name__ == "__main__":
    # Test
    smiles = "OC(CC)(C)C#C"
    acid_exp = 0
    base_exp = 3
    mol = Chem.MolFromSmiles(smiles)
    abc = ABCounter()
    print(abc.count_acid_and_bases(mol))
