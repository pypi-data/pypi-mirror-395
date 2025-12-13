import pytest

from nasap_net.models import Assembly, Component
from nasap_net.models.component_consistency_check import \
    InconsistentComponentBetweenAssembliesError, check_component_consistency


def test_valid_case():
    L1 = Component(kind='L', sites=[0, 1])
    L2 = Component(kind='L', sites=[0, 1])
    assemblies = [
        Assembly({'L1': L1}, []),
        Assembly({'L2': L2}, []),
    ]
    # This should not raise an exception
    check_component_consistency(assemblies)


def test_invalid_case():
    L1 = Component(kind='L', sites=[0, 1])
    L2 = Component(kind='L', sites=[2, 3])  # Different
    assemblies = [
        Assembly({'L1': L1}, []),
        Assembly({'L2': L2}, []),
    ]
    with pytest.raises(InconsistentComponentBetweenAssembliesError):
        check_component_consistency(assemblies)
