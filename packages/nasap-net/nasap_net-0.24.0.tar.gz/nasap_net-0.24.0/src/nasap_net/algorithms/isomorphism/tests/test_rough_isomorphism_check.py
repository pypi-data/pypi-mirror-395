from copy import deepcopy

import pytest

from nasap_net import Assembly
from nasap_net.algorithms.isomorphism import is_roughly_isomorphic


@pytest.fixture
def assem_without_bonds() -> Assembly:
    assem = Assembly()
    assem.add_component('M1', 'M')
    assem.add_components([('L1', 'L'), ('L2', 'L')])
    assem.add_components([('X1', 'X'), ('X2', 'X')])
    return assem


@pytest.fixture
def assem1(assem_without_bonds: Assembly) -> Assembly:
    assem1_ = deepcopy(assem_without_bonds)
    assem1_.add_bonds([
        ('M1.a', 'L1.a'), ('M1.b', 'L2.a'),  # cis
        ('M1.c', 'X1.a'), ('M1.d', 'X2.a')])
    return assem1_


@pytest.fixture
def assem2(assem_without_bonds: Assembly) -> Assembly:
    assem2_ = deepcopy(assem_without_bonds)
    assem2_.add_bonds([
        ('M1.a', 'L1.a'), ('M1.c', 'L2.a'),  # trans
        ('M1.b', 'X1.a'), ('M1.d', 'X2.a')])
    return assem2_


def test_is_roughly_isomorphic_with_isomorphic_assemblies(
        assem1: Assembly) -> None:
    assem3 = deepcopy(assem1)
    assert is_roughly_isomorphic(assem1, assem3)


def test_is_roughly_isomorphic_with_clearly_non_isomorphic_assemblies(
        assem1: Assembly) -> None:
    assem2 = deepcopy(assem1)
    assem2.remove_bond('M1.a', 'L1.a')
    assert not is_roughly_isomorphic(assem1, assem2)
    

def test_is_roughly_isomorphic_with_relabelled_assemblies(
        assem1: Assembly
        ) -> None:
    # Should be roughly isomorphic
    assem2 = deepcopy(assem1)
    assem2.rename_component_ids({'M1': 'M1_'})
    assert is_roughly_isomorphic(assem1, assem2)


def test_is_roughly_isomorphic_with_stereo_isomers(
        assem1: Assembly, assem2: Assembly
        ) -> None:
    # Should be roughly isomorphic, though not isomorphic
    assert is_roughly_isomorphic(assem1, assem2)



if __name__ == '__main__':
    pytest.main(['-vv', __file__])
