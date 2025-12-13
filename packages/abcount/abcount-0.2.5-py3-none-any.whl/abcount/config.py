import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectDirs:
    package_dir: Path
    source_dir: Path
    data_dir: Path


_source_dir = os.path.dirname(__file__)
_package_dir = os.path.dirname(_source_dir)
_data_dir = os.path.join(_source_dir, "data")
dirs = ProjectDirs(
    package_dir=Path(_package_dir),
    source_dir=Path(_source_dir),
    data_dir=Path(_data_dir),
)


@dataclass
class DataFiles:
    raw_data_file: Path
    acid_defs_file: Path
    base_defs_file: Path


_files = DataFiles(
    raw_data_file=Path("raw_definitions.json"),
    acid_defs_file=Path("acid_definitions.json"),
    base_defs_file=Path("base_definitions.json"),
)


@dataclass
class DataFilePaths:
    raw_data_filepath: Path
    acid_defs_filepath: Path
    base_defs_filepath: Path


fps = DataFilePaths(
    raw_data_filepath=Path(os.path.join(dirs.data_dir, _files.raw_data_file)),
    acid_defs_filepath=Path(os.path.join(dirs.data_dir, _files.acid_defs_file)),
    base_defs_filepath=Path(os.path.join(dirs.data_dir, _files.base_defs_file)),
)
