import pytest
import yaml

from nasap_net.io.assemblies.helper import split_yaml_documents


def test_simple_multi_doc():
    text = """
a: 1
---
b: 2
"""
    docs = list(split_yaml_documents(text))
    assert len(docs) == 2

    data1 = yaml.safe_load(docs[0])
    data2 = yaml.safe_load(docs[1])

    assert data1 == {"a": 1}
    assert data2 == {"b": 2}


def test_block_scalar_with_dashes():
    """Check that '---' inside a block scalar does not split the document."""
    text = """
note: |
  this is part of the same block
  ---
  and should NOT split here
---
another: doc
"""
    docs = list(split_yaml_documents(text))
    assert len(docs) == 2

    data1 = yaml.safe_load(docs[0])
    data2 = yaml.safe_load(docs[1])

    assert "this is part" in data1["note"]
    assert data2 == {"another": "doc"}

    # Naive split would incorrectly produce 3 documents
    naive_docs = [d.strip() for d in text.split('---') if d.strip()]
    assert len(naive_docs) == 3


def test_comments_and_empty_lines():
    text = """
# first document
name: test

---
# second document
value: 42
...
"""
    docs = list(split_yaml_documents(text))
    assert len(docs) == 2

    data1 = yaml.safe_load(docs[0])
    data2 = yaml.safe_load(docs[1])

    assert data1 == {"name": "test"}
    assert data2 == {"value": 42}


def test_invalid_yaml_raises():
    text = """
invalid:
  - a
  - b
  - : bad
"""
    with pytest.raises(yaml.YAMLError):
        list(split_yaml_documents(text))
