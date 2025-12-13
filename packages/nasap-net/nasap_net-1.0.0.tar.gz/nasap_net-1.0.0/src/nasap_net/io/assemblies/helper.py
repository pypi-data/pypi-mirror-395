from collections.abc import Iterator
from io import StringIO

import yaml


def split_yaml_documents(yaml_text: str) -> Iterator[str]:
    """
    Safely split YAML text into multiple documents.

    Uses PyYAML's compose_all() to parse the text document-by-document,
    then re-serializes each document and returns it as a string.

    Parameters
    ----------
    yaml_text : str
        YAML string containing multiple documents separated by '---'.

    Yields
    ------
    str
        Each document as an independent YAML string.

    Raises
    ------
    yaml.YAMLError
        If the YAML syntax is invalid.

    Example
    -------
    >>> text = '''
    ... a: 1
    ... ---
    ... b: 2
    ... '''
    >>> for doc in split_yaml_documents(text):
    ...     print('---')
    ...     print(doc.strip())
    ---
    a: 1
    ---
    b: 2
    """
    try:
        docs = yaml.compose_all(yaml_text)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to parse YAML: {e}") from e

    for node in docs:
        buffer = StringIO()
        yaml.serialize(node, stream=buffer)
        yield buffer.getvalue()
