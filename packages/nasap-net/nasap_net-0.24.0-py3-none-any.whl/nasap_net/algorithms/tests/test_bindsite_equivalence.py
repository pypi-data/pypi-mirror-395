import pytest

from nasap_net import Assembly, Component
from nasap_net.algorithms import are_equivalent_binding_site_lists


@pytest.fixture
def component_structures():
    """Fixture for component structures."""
    return {
        'M_bi': Component(['a', 'b']),
        'M_tetra': Component(['a', 'b', 'c', 'd']),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }

@pytest.fixture
def M():
    # (a)M0(b)
    return Assembly({'M0': 'M_bi'})

@pytest.fixture
def ML2():
    # (a)L0(b)-(a)M0(b)-(a)L1(b)
    return Assembly(
        {'M0': 'M_bi', 'L0': 'L', 'L1': 'L'},
        [('L0.b', 'M0.a'), ('M0.b', 'L1.a')]
    )

@pytest.fixture
def MLX():
    # (a)L0(b)-(a)M0(b)-(a)X0
    return Assembly(
        {'M0': 'M_bi', 'L0': 'L', 'X0': 'X'},
        [('L0.b', 'M0.a'), ('M0.b', 'X0.a')]
    )

@pytest.fixture
def ML2X2():
    #              X0
    #             (a)
    #              |
    #             (c)
    # (a)L0(b)--(a)M0(b)--(a)L1(b)
    #             (d)
    #              |
    #             (a)
    #              X1

    # WITHOUT auxiliary edges

    return Assembly(
        {'M0': 'M_tetra', 'L0': 'L', 'L1': 'L', 'X0': 'X', 'X1': 'X'},
        [('M0.a', 'L0.b'), ('M0.b', 'L1.b'),
         ('M0.c', 'X0.a'), ('M0.d', 'X1.a')]
    )


def test_different_lengths_error(M):
    # Check if ValueError is raised for different lengths
    with pytest.raises(ValueError):
        are_equivalent_binding_site_lists(M, ['M0.a'], ['M0.a', 'M0.b'], {})


def test_empty_lists_error(M):
    # Check if ValueError is raised for empty lists
    with pytest.raises(ValueError):
        are_equivalent_binding_site_lists(M, [], [], {})


def test_nonexistent_binding_site_error(M, component_structures):
    # Check if ValueError is raised for nonexistent binding sites
    with pytest.raises(ValueError):
        are_equivalent_binding_site_lists(
            M, ['M0.a'], ['M0.unknown'], component_structures)
    with pytest.raises(ValueError):
        are_equivalent_binding_site_lists(
            M, ['M0.unknown'], ['M0.a'], component_structures)


def test_single_binding_site(M, component_structures):
    assert are_equivalent_binding_site_lists(
        M, ['M0.a'], ['M0.b'], component_structures)


def test_assembly_composed_of_multiple_components(
        ML2, ML2X2, component_structures):
    assert are_equivalent_binding_site_lists(
        ML2, ['L0.a'], ['L1.b'], component_structures)
    assert are_equivalent_binding_site_lists(
        ML2X2, ['L0.a', 'M0.c'], ['L1.a', 'M0.d'], component_structures)


def test_consideration_of_component_kinds(MLX, component_structures):
    # Should not be equivalent
    # because isomorphisms which maps L0 to X0 are not allowed.
    assert not are_equivalent_binding_site_lists(
        MLX, ['L0.b', 'M0.a'], ['X0.a', 'M0.b'], component_structures)


def test_self_comparison(M, ML2, MLX, component_structures):
    assert are_equivalent_binding_site_lists(
        M, ['M0.a'], ['M0.a'], component_structures)
    assert are_equivalent_binding_site_lists(
        ML2, ['L0.a', 'L0.b'], ['L0.a', 'L0.b'], component_structures)
    assert are_equivalent_binding_site_lists(
        MLX, ['L0.a', 'L0.b'], ['L0.a', 'L0.b'], component_structures)


def test_pair(ML2, component_structures):
    # Same binding sites in M
    assert are_equivalent_binding_site_lists(
        ML2, ['L0.a', 'L0.b'], ['L1.b', 'L1.a'], component_structures)
    assert not are_equivalent_binding_site_lists(
        ML2, ['L0.a', 'L0.b'], ['L1.a', 'L1.b'], component_structures)


def test_trio(ML2X2, component_structures):
    # Consider inter-molecular reactions of ML2X2 as an example.
    # trio: (metal, leaving, entering)
    assert are_equivalent_binding_site_lists(
        ML2X2, ['M0.c', 'X0.a', 'L0.a'], ['M0.d', 'X1.a', 'L1.a'],
        component_structures)


def test_auxiliary_edges():
    COMPONENT_KINDS = {
        'M_plain': Component(['a', 'b', 'c', 'd']),
        'M_aux': Component(
            ['a', 'b', 'c', 'd'],
            [('a', 'b', 'cis'), ('b', 'c', 'cis'), 
             ('c', 'd', 'cis'), ('d', 'a', 'cis')]
        ),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }

    #           X0
    #          (a)
    #           |
    #          (a)
    # X1(a)--(b)M0(d)--(a)L0(b)
    #          (c)
    #           |
    #          (a)
    #           X2
    MLX3_plain = Assembly(
        {'M0': 'M_plain', 'L0': 'L', 'X0': 'X', 'X1': 'X', 'X2': 'X'},
        [('M0.a', 'X0.a'), ('M0.b', 'X1.a'),
         ('M0.c', 'X2.a'), ('M0.d', 'L0.a')]
        )
    MLX3_aux = Assembly(
        {'M0': 'M_aux', 'L0': 'L', 'X0': 'X', 'X1': 'X', 'X2': 'X'},
        [('M0.a', 'X0.a'), ('M0.b', 'X1.a'),
         ('M0.c', 'X2.a'), ('M0.d', 'L0.a')]
        )
    
    assert are_equivalent_binding_site_lists(
        MLX3_plain, ['M0.d', 'M0.a'], ['M0.d', 'M0.b'], COMPONENT_KINDS)
    assert not are_equivalent_binding_site_lists(
        MLX3_aux, ['M0.d', 'M0.a'], ['M0.d', 'M0.b'], COMPONENT_KINDS)
    
    # Intra-molecular reaction
    assert are_equivalent_binding_site_lists(
        MLX3_plain, ['M0.a', 'X0.a', 'L0.b'], ['M0.b', 'X1.a', 'L0.b'],
        COMPONENT_KINDS)
    assert not are_equivalent_binding_site_lists(
        MLX3_aux, ['M0.a', 'X0.a', 'L0.b'], ['M0.b', 'X1.a', 'L0.b'],
        COMPONENT_KINDS)


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
