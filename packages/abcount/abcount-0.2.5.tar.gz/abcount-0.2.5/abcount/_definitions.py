import json
from pathlib import Path

from rdkit import Chem

from abcount.config import fps
from abcount.model.counter import DefinitionAttribute
from abcount.model.counter import GroupTypeAttribute


class RawDefinitionAttribute:
    SMARTS = "SMARTS"
    TYPE = "type"
    ACIDIC_TYPE = "A"
    BASIC_TYPE = "B"


def _validate_smarts(smarts: str) -> None:
    """Raise an error if the SMARTS pattern is invalid."""
    Chem.MolFromSmarts(smarts)


def preprocess_definition(def_dict: dict) -> dict:
    """
    Normalize and validate a SMARTS definition.
    The function will fail loudly on malformed input.
    """
    smarts = def_dict[RawDefinitionAttribute.SMARTS]
    raw_type = def_dict[RawDefinitionAttribute.TYPE]

    if raw_type == RawDefinitionAttribute.ACIDIC_TYPE:
        def_type = GroupTypeAttribute.ACID
    elif raw_type == RawDefinitionAttribute.BASIC_TYPE:
        def_type = GroupTypeAttribute.BASE
    else:
        def_type = raw_type  # Already normalized

    _validate_smarts(smarts)

    return {DefinitionAttribute.SMARTS: smarts, DefinitionAttribute.TYPE: def_type}


class SmartsStore:
    """Stores and organizes SMARTS definitions by type."""

    def __init__(self):
        self._acid_defs = []
        self._base_defs = []

    def add(self, definition: dict) -> None:
        def_type = definition[DefinitionAttribute.TYPE]
        if def_type == GroupTypeAttribute.ACID:
            self._acid_defs.append(definition)
        elif def_type == GroupTypeAttribute.BASE:
            self._base_defs.append(definition)
        else:
            raise ValueError(f"Unknown group type: {def_type}")

    @property
    def acid_defs(self) -> list:
        return self._acid_defs

    @property
    def base_defs(self) -> list:
        return self._base_defs


class SmartsDump:
    """Utility for writing SMARTS definitions to disk."""

    @staticmethod
    def save_definitions_to_json(defs: list, filepath: Path) -> None:
        with open(filepath, "w") as f:
            json.dump(defs, f, indent=4)


if __name__ == "__main__":
    with open(fps.raw_data_filepath) as f:
        definitions = json.load(f)

    store = SmartsStore()

    for raw_def in definitions:
        processed_def = preprocess_definition(raw_def)
        store.add(processed_def)

    SmartsDump.save_definitions_to_json(store.acid_defs, fps.acid_defs_filepath)
    SmartsDump.save_definitions_to_json(store.base_defs, fps.base_defs_filepath)
