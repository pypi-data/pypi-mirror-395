from nasap_net.utils.default import MISSING, default_if_missing


def test_with_value():
    result = default_if_missing('value', 'default')
    assert result == 'value'


def test_with_missing():
    result = default_if_missing(MISSING, 'default')
    assert result == 'default'


def test_no_fallback_for_none():
    result = default_if_missing(None, 'default')
    assert result is None
