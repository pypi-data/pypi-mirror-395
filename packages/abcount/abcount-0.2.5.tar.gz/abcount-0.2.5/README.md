![ABCount logo](https://github.com/ghiander/abcount/blob/main/docs/static/logo.png?raw=true)

## Introduction
**ABCount** is an extended cheminformatics package to work with acidic and basic groups in molecules. The package includes the following functionalities:
- `ABCounter`: SMARTS-based matcher to determine the number of acidic and basic groups in molecules.
- `ABClassBuilder`: Converter that accepts a dictionary of pKa numerical values and yields an `ABClassData` object with their corresponding classes such as `STRONG`, `WEAK`, and `NONE`.
- `IonMatcher`: Matcher that accepts an `ABClassData` object and yields an `IonDefinition` containing information about the major species at pH 7.4 and its corresponding ionic class and explanation.

## How to install the tool
ABCount can be installed from pypi (https://pypi.org/project/abcount).
```bash
pip install abcount
```

## Usage
### `ABCounter`
```python
from rdkit import Chem
from abcount import ABCounter

# Use the tool out of the box with default definitions.
mol = Chem.MolFromSmiles("[nH]1nnnc1-c3c2[nH]ncc2ccc3")
abc = ABCounter()
abc.count_acid_and_bases(mol)
```
```python
{'acid': 2, 'base': 2}
```

```python
from rdkit import Chem
from abcount import ABCounter

# Point the tool to using your own definitions.
# The format is JSON and attributes must be consistent to those in
# acid_definitions.json and base_definitions.json in abcount/data.
mol = Chem.MolFromSmiles("[nH]1nnnc1-c3c2[nH]ncc2ccc3")
abc = ABCounter(acid_defs_filepath="/my/path/acid_defs.json", base_defs_filepath="/my/path/base_defs.json")
abc.acid_matcher.definitions_fp
```
```python
PosixPath('/my/path/acid_defs.json')
```

### `ABClassBuilder` and `ABClassData`
```python
from abcount import ABClassBuilder

abcb = ABClassBuilder()
# The builder expects two acidic and two basic groups with these key names.
predictions = {"pka_acid1": 3.5, "pka_acid2": None, "pka_base1": 9.785, "pka_base2": None}
abcb.build(predictions)
```
```python
ABClassData(acid_1_class=<AcidType.STRONG: 'strong_acid'>, acid_2_class=<AcidType.NONE: 'no_acid'>, base_1_class=<BaseType.STRONG: 'strong_base'>, base_2_class=<BaseType.NONE: 'no_base'>)
```
```python
# to_dict() can be used to obtain a dictionary containing a mix of objects.
# Alternatively, the output can also be serialised using to_json()
abcb.build(predictions).to_json()
```
```python
'{"acid_1_class": "strong_acid", "acid_2_class": "no_acid", "base_1_class": "strong_base", "base_2_class": "no_base"}'
```

```python
from abcount import ABClassBuilder, PKaClassBuilder

abcb = ABClassBuilder()
# Custom names can be passed but these need to be
# configured in a `CustomPKaAttribute` class.
predictions = {"my_pka_acid1": 3.5, "my_pka_acid2": None, "my_pka_base1": 9.785, "my_pka_base2": None}
CustomPKaAttribute = PKaClassBuilder.build(ACID_1="my_pka_acid1", BASE_1="my_pka_base1", ACID_2="my_pka_acid2", BASE_2="my_pka_base2")

# The `CustomPKaAttribute` can then be passed to the builder
# which will map the new data to the rules.
abcb.build(predictions, CustomPKaAttribute)
```
```python
ABClassData(acid_1_class=<AcidType.STRONG: 'strong_acid'>, acid_2_class=<AcidType.NONE: 'no_acid'>, base_1_class=<BaseType.STRONG: 'strong_base'>, base_2_class=<BaseType.NONE: 'no_base'>)
```

```python
from abcount import ABClassBuilder

abcb = ABClassBuilder()
# It is possible to work with fewer acidic or basic groups
# These can be set as arguments in the builder
predictions = {"pka_acid1": 3.5, "pka_acid2": 7.5, "pka_base1": 9.785}
abcb.build(predictions, num_acids=2, num_bases=1)
```
```python
# Note that despite passing only one basic group, the builder still 
# returns `base_2_class` but associating that with a None instead of BaseType.NONE.
ABClassData(acid_1_class=<AcidType.STRONG: 'strong_acid'>, acid_2_class=<AcidType.NONE: 'no_acid'>, base_1_class=<BaseType.STRONG: 'strong_base'>, base_2_class=None)
```

### `IonMatcher`
```python
from abcount import ABClassBuilder, IonMatcher

abcb = ABClassBuilder()
predictions = {"pka_acid1": 3.5, "pka_acid2": 7.5, "pka_base1": 9.785}
abcd = abcb.build(predictions, num_acids=2, num_bases=1)

ion_matcher = IonMatcher()
ion_matcher.match_class_data(abcd)
```
```python
# Note that IonMatcher ignores AcidType.NONE and BaseType.NONE - treats them as None.
IonDefinition(class_data=ABClassData(acid_1_class=<AcidType.STRONG: 'strong_acid'>, acid_2_class=None, base_1_class=<BaseType.STRONG: 'strong_base'>, base_2_class=None), major_species_ph74_class='zwitterion', ion_class='zwitterion', explanation='acid_1_class: strong_acid, base_1_class: strong_base')
```
```python
# to_json() can also be applied to `IonDefinition`
# to yield a fully serialised representation.
# Alternatively, to_dict() can be used to obtain 
# a dictionary containing a mix of objects.
ion_matcher.match_class_data(abcd).to_dict()
```
```
{'class_data': {'acid_1_class': <AcidType.STRONG: 'strong_acid'>, 'acid_2_class': None, 'base_1_class': <BaseType.STRONG: 'strong_base'>, 'base_2_class': None}, 'major_species_ph74_class': 'zwitterion', 'ion_class': 'zwitterion', 'explanation': 'acid_1_class: strong_acid, base_1_class: strong_base'}
```

## SMARTS definitions source for `ABCounter`
The SMARTS patterns used in this project were obtained from the following sources. Note that definitions are not deduplicated, hence require curation to avoid redundant matching.

* Pan, X.; Wang, H.; Li, C.; Zhang, J. Z. H.; Ji, C., **MolGpka: A Web Server for Small Molecule pKa Prediction Using a Graph-Convolutional Neural Network**
*Journal of Chemical Information and Modeling* **2021**, *61* (7), 3159–3165. DOI: [10.1021/acs.jcim.1c00075](https://doi.org/10.1021/acs.jcim.1c00075)
* Wu, J.; Wan, Y.; Wu, Z.; Zhang, S.; Cao, D.; Hsieh, C.-Y.; Hou, T., **MF-SuP-pKa: Multi-fidelity modeling with subgraph pooling mechanism for pKa prediction** *Acta Pharmaceutica Sinica B* **2023**, *13* (6). DOI: [10.26434/chemrxiv-2022-t6q61](https://doi.org/10.26434/chemrxiv-2022-t6q61)
* Some manually curated definitions.

## Some useful commands
- Generate acidic and basic definitions from aggregated data: `python abcount/_definitions.py`. A follow up on how definitions can be curated will be provided.
- Run tests: `pytest -vss tests/test.py`
- Run validation: `cd tests && validation.py`. This will also generate four CSV files listing out false positives and negatives for the test data.

## For developers
- The package was created using `uv` (https://docs.astral.sh/uv/).
- The package can be installed from the wheel in the `dist/` folder. When a new version needs to be released, a new wheel must be built. That can be done by changing the version of the package inside `pyproject.toml` then calling `uv build` which will create a new build.
- The code can be automatically tested using `pytest -vss tests/test.py` which requires `pytest` to be installed.
- The `Makefile` can also be used for building (`make build`) or testing (`make test`).
- Before committing new code, please always check that the style and syntax are compliant using `pre-commit`.

### Setting up your development environment
The `pyproject.toml` already contains the optional dependencies needed for development. Follow these steps to set up the environment.
```bash
# Make sure you have got Python >= 3.10
python --version
> Python 3.12.7

# Installs `abcount` in editable mode and with dev dependencies
pip install -e .[dev]
> ...
> Successfully installed abcount ...

# Setup pre-commit hooks
pre-commit install
> pre-commit installed at .git/hooks/pre-commit
```
