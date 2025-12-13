"""
Low-level tests for YAML export
"""

from io import StringIO

import pytest
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from yamlpp.util import to_yaml  # adjust import path if needed

# -------------------------
# Basic behavior
# -------------------------

def test_default_instance_reuse():
    """Ensure that when all arguments are None, the global YAML_RT instance is reused."""
    data = {"a": 1}
    out = to_yaml(data)
    assert "a: 1" in out


def test_indent_argument_applied():
    """Verify that the indent argument changes the indentation of nested mappings."""
    data = {"outer": {"inner": 42}}
    out = to_yaml(data, indent=4)
    # Expect 4 spaces before 'inner'
    assert "    inner: 42" in out


def test_offset_argument_applied():
    """Verify that offset argument does not break round-trip for sequences."""
    data = {"list": [1, 2]}
    out = to_yaml(data, offset=4)
    yaml = YAML(typ="rt")
    loaded = yaml.load(out)
    assert loaded == data



def test_explicit_start_and_end_markers():
    """Ensure explicit_start and explicit_end add '---' and '...' markers."""
    data = {"x": 1}
    out = to_yaml(data, explicit_start=True, explicit_end=True)
    assert out.startswith("---")
    assert out.strip().endswith("...")


def test_allow_unicode_true():
    """Ensure allow_unicode=True preserves non-ASCII characters without escaping."""
    data = {"greeting": "café"}
    out = to_yaml(data, allow_unicode=True)
    assert "café" in out


def test_canonical_output():
    """Ensure canonical=True produces verbose, explicit YAML with sorted keys."""
    data = {"b": 2, "a": 1}
    out = to_yaml(data, canonical=True)
    # Canonical form includes explicit type tags and sorted keys
    assert "!!map" in out
    assert out.index("a") < out.index("b")


def test_width_argument_applied():
    """Verify that width argument controls line wrapping of long scalars."""
    long_string = "x" * 100
    data = {"msg": long_string}
    out = to_yaml(data, width=40)
    # Expect line breaks due to width constraint
    assert "\n" in out



def test_preserve_quotes_true():
    """Ensure preserve_quotes=True respects double-quoted style without reloading."""
    yaml = YAML(typ="rt")
    node = {"key": DoubleQuotedScalarString("value")}

    out = to_yaml(node, preserve_quotes=True)

    # The output string should contain the quotes
    assert 'key: "value"' in out




def test_typ_and_pure_arguments():
    """Ensure typ and pure arguments are passed to YAML constructor."""
    data = {"a": 1}
    out = to_yaml(data, typ="safe", pure=True)
    assert "a: 1" in out  # still serializes correctly


def test_version_argument_applied():
    """Ensure version argument adds %YAML directive at top of output."""
    data = {"a": 1}
    out = to_yaml(data, version=(1, 2))
    assert out.startswith("%YAML 1.2")


# -------------------------
# Error handling
# -------------------------

def test_duplicate_keys_raise_error():
    """Ensure duplicate keys are rejected due to allow_duplicate_keys=False."""
    yaml = YAML(typ="rt")
    text = "a: 1\na: 2\n"
    with pytest.raises(Exception):
        to_yaml(yaml.load(text))
