from copy import deepcopy

import pytest

from nasap_net.exceptions import IDNotSetError
from nasap_net.models import Assembly, BindingSite, Component, Reaction


@pytest.fixture
def MX2_plus_free_L():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MX2 = Assembly(
        id_='MX2',
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[],
    )
    free_L = Assembly(id_='free_L', components={'L0': L}, bonds=[])
    MLX = Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[],
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])

    return Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4,
    )


def test___repr__(MX2_plus_free_L):
    repr_str = repr(MX2_plus_free_L)
    assert repr_str == '<Reaction MX2 + free_L -> MLX + free_X>'


def test___repr___with_id(MX2_plus_free_L):
    reaction = MX2_plus_free_L.copy_with(id_='R1')
    repr_str = repr(reaction)
    assert repr_str == '<Reaction ID=R1 MX2 + free_L -> MLX + free_X>'


def test_equation_str(MX2_plus_free_L):
    equation = MX2_plus_free_L.equation_str
    assert equation == 'MX2 + free_L -> MLX + free_X'


def test___str__(MX2_plus_free_L):
    str_repr = str(MX2_plus_free_L)
    assert str_repr == 'MX2 + free_L -> MLX + free_X (x4)'


def test_id_property(MX2_plus_free_L):
    # Error when ID is not set
    with pytest.raises(IDNotSetError):
        _ = MX2_plus_free_L.id_

    # No error when ID is set
    reaction_with_id = MX2_plus_free_L.copy_with(id_='R1')
    assert reaction_with_id.id_ == 'R1'


def test_id_or_none_property(MX2_plus_free_L):
    assert MX2_plus_free_L.id_or_none is None

    reaction_with_id = MX2_plus_free_L.copy_with(id_='R1')
    assert reaction_with_id.id_or_none == 'R1'


def test_copy_with():
    original = Reaction(
        init_assem=Assembly(id_='init_assem_1', components={}, bonds=[]),
        entering_assem=Assembly(id_='entering_assem_1', components={}, bonds=[]),
        product_assem=Assembly(id_='product_assem_1', components={}, bonds=[]),
        leaving_assem=Assembly(id_='leaving_assem_1', components={}, bonds=[]),
        metal_bs=BindingSite('metal_1', 0),
        leaving_bs=BindingSite('leaving_1', 0),
        entering_bs=BindingSite('entering_1', 0),
        duplicate_count=1,
        id_='R_original',
    )

    original_copy = deepcopy(original)

    modified = original.copy_with(
        init_assem=Assembly(id_='init_assem_2', components={}, bonds=[]),
        entering_assem=Assembly(id_='entering_assem_2', components={},
                                bonds=[]),
        product_assem=Assembly(id_='product_assem_2', components={}, bonds=[]),
        leaving_assem=Assembly(id_='leaving_assem_2', components={}, bonds=[]),
        metal_bs=BindingSite('metal_2', 0),
        leaving_bs=BindingSite('leaving_2', 0),
        entering_bs=BindingSite('entering_2', 0),
        duplicate_count=2,
        id_='R_modified',
    )

    assert modified.init_assem == Assembly(id_='init_assem_2', components={}, bonds=[])
    assert modified.entering_assem == Assembly(id_='entering_assem_2', components={}, bonds=[])
    assert modified.product_assem == Assembly(id_='product_assem_2', components={}, bonds=[])
    assert modified.leaving_assem == Assembly(id_='leaving_assem_2', components={}, bonds=[])
    assert modified.metal_bs == BindingSite('metal_2', 0)
    assert modified.leaving_bs == BindingSite('leaving_2', 0)
    assert modified.entering_bs == BindingSite('entering_2', 0)
    assert modified.duplicate_count == 2
    assert modified.id_ == 'R_modified'

    # Ensure original is unchanged
    assert original.init_assem == original_copy.init_assem
    assert original.entering_assem == original_copy.entering_assem
    assert original.product_assem == original_copy.product_assem
    assert original.leaving_assem == original_copy.leaving_assem
    assert original.metal_bs == original_copy.metal_bs
    assert original.leaving_bs == original_copy.leaving_bs
    assert original.entering_bs == original_copy.entering_bs
    assert original.duplicate_count == original_copy.duplicate_count
    assert original.id_ == 'R_original'


def test_copy_with_no_changes(MX2_plus_free_L):
    copied = MX2_plus_free_L.copy_with()

    assert copied.init_assem == MX2_plus_free_L.init_assem
    assert copied.entering_assem == MX2_plus_free_L.entering_assem
    assert copied.product_assem == MX2_plus_free_L.product_assem
    assert copied.leaving_assem == MX2_plus_free_L.leaving_assem
    assert copied.metal_bs == MX2_plus_free_L.metal_bs
    assert copied.leaving_bs == MX2_plus_free_L.leaving_bs
    assert copied.entering_bs == MX2_plus_free_L.entering_bs
    assert copied.duplicate_count == MX2_plus_free_L.duplicate_count
    assert copied.id_or_none is None  # ID should not be copied by default


def test_override_with_none():
    reaction = Reaction(
        init_assem=Assembly(id_='init_assem', components={}, bonds=[]),
        entering_assem=Assembly(id_='entering_assem', components={}, bonds=[]),
        product_assem=Assembly(id_='product_assem', components={}, bonds=[]),
        leaving_assem=Assembly(id_='leaving_assem', components={}, bonds=[]),
        metal_bs=BindingSite('metal', 0),
        leaving_bs=BindingSite('leaving', 0),
        entering_bs=BindingSite('entering', 0),
        duplicate_count=1,
    )
    assert reaction.entering_assem is not None
    assert reaction.leaving_assem is not None

    # Overridden to None when None is explicitly provided
    modified = reaction.copy_with(
        entering_assem=None,
        leaving_assem=None,
    )
    assert modified.entering_assem is None
    assert modified.leaving_assem is None

    # Original value is used when None is not explicitly provided
    unmodified = reaction.copy_with()
    assert unmodified.entering_assem == reaction.entering_assem
    assert unmodified.leaving_assem == reaction.leaving_assem

    # Other fields cannot be set to None even when None is provided
    with pytest.raises(TypeError):
        reaction.copy_with(init_assem=None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        reaction.copy_with(product_assem=None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        reaction.copy_with(metal_bs=None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        reaction.copy_with(leaving_bs=None)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        reaction.copy_with(entering_bs=None)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        reaction.copy_with(duplicate_count=0)  # Should be positive integer
