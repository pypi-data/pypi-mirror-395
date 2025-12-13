from dataclasses import dataclass

from dataclasses_json import dataclass_json

from abcount.model.classifier import ABClassData


@dataclass_json
@dataclass
class IonDefinition:
    """Class for storing class conditions and ionic definitions."""

    class_data: ABClassData
    major_species_ph74_class: str
    ion_class: str
    explanation: str = None  # gets calculated rather than defined
