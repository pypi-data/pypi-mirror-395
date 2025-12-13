"""
Test .export construct

We are testing ROUND-TRIP properties of the export,
within the limites of the format.
"""
import io
from pathlib import Path

import pytest

from yamlpp import Interpreter
from yamlpp.error import YAMLppError, YAMLValidationError
from yamlpp.util import print_yaml, deserialize, FILE_FORMATS


EXPORT_COMBINATIONS = [(fmt, explicit) for fmt in FILE_FORMATS 
                                       for explicit in (True, False)]


@pytest.mark.parametrize("fmt, explicit", EXPORT_COMBINATIONS)
def test_handle_export(tmp_path:str, fmt:str, explicit:bool):
    """
    Test the handle_export() method, specifically with the format argument.

    It tests both the explicit case (where the format is specified), and not explicit.
    """
    
    # Arrange: create interpreter with tmp_path as source_dir
    interpreter = Interpreter(source_dir=tmp_path)

    entry = {
        ".filename": f"export.{fmt}",
        ".do": {"server": {"foo": "bar", "baz": 5}},
        ".format": fmt if explicit else None,
    }
    # Act: call the real handle_export
    interpreter.handle_export(entry)

    # Assert: file exists
    full_path = tmp_path / f"export.{fmt}"
    assert full_path.exists(), f"Export file for {fmt} should be created"

    # Assert: round-trip content with yamlpp
    content = full_path.read_text(encoding="utf-8")
    print("Read-back:\n---", content)
    parsed = deserialize(content, format=fmt)
    assert parsed["server"]["foo"] == "bar"
    assert parsed["server"]["baz"] == 5


# -------------------------
# Full Chain
# -------------------------

# Arrange
CURRENT_DIR = Path(__file__).parent 
EXPORT = "_export" 

SOURCE_DIR = CURRENT_DIR / 'source'

EXPORT_DIR = SOURCE_DIR / EXPORT
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def test_export_enviroment():
    assert SOURCE_DIR.is_dir()
    assert EXPORT_DIR.is_dir()
    print("Export dir: ", EXPORT_DIR)


def test_export_yaml():
    """
    Test YAMLpp export, with the full chain
    """
    
    SOURCE_FILENAME = SOURCE_DIR / 'test1.yaml'
    EXPORT_FILENAME = f'{EXPORT}/export1.yaml' # relative

    # Act
    i = Interpreter()
    i.load(SOURCE_FILENAME)
    
    # Replace the accounts in the source file by an export clause
    accounts = i.initial_tree.pop('accounts')
    block = {'.filename': EXPORT_FILENAME, 
             '.do' : {'accounts': accounts},
             '.args':
                {'allow_unicode': False} # will not make any difference here for the round trip
             }
    i.initial_tree['.export'] = block
    print("Destination:")
    print_yaml(i.yaml)

    # Assert
    exported = SOURCE_DIR / EXPORT_FILENAME
    assert exported.is_file()
    print("Reloading...")
    i2 = Interpreter()
    i2.load(exported)
    tree = i2.initial_tree
    print("Reloaded YAML (as 'YAMLpp'):")
    print_yaml(i2.yamlpp, filename=EXPORT_FILENAME)
    print("Reprocessed YAML:")
    print_yaml(i2.yaml, filename=EXPORT_FILENAME)
    len(tree) == 4
    tree.accounts[1].name = 'bob'
    tree.accounts[2].name = 'charlie'
    # this is pure YAML:
    assert i2.yamlpp == i2.yaml, "YAML produced should be identical to YAMLpp source"



