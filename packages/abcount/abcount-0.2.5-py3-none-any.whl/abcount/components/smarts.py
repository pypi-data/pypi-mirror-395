import json
import logging

from rdkit import Chem


logger = logging.getLogger(__name__)


class SmartsMatcher:
    """Plain SMARTS matcher with count functionality."""

    def __init__(self, definitions_list: list):
        self._load_smarts(definitions_list)

    def _load_smarts(self, definitions_list):
        # Loaded as a tuple to retain original SMARTS for debugging
        self.definitions_tup = [(Chem.MolFromSmarts(d), d) for d in definitions_list]

    def count_matches(self, mol):
        count = 0
        for t in self.definitions_tup:
            matches = SmartsMatcher._match_smarts_to_mol(mol, t[0])
            if matches:
                logger.debug(f"SMARTS: {t[1]} - Matches: {matches}")
            count += matches
        return count

    def generate_matches_list(self, mol):
        matches_list = []
        for t in self.definitions_tup:
            matches = SmartsMatcher._match_smarts_to_mol(mol, t[0])
            if matches:
                matches_list.append((t[1], matches))
        return matches_list

    @staticmethod
    def _match_smarts_to_mol(mol, smarts):
        return len(mol.GetSubstructMatches(smarts))


class SmartsMatcherJson(SmartsMatcher):
    """Adapter for SmartsMatcher."""

    def __init__(self, definitions_fp):
        self.definitions_fp = definitions_fp
        self._load_smarts()

    def _load_smarts(self):
        definitions_dict = self._load_json()
        # Loaded as a tuple to retain original SMARTS for debugging
        self.definitions_tup = [
            (Chem.MolFromSmarts(d["smarts"]), d) for d in definitions_dict
        ]

    def _load_json(self):
        with open(self.definitions_fp) as f:
            return json.load(f)
