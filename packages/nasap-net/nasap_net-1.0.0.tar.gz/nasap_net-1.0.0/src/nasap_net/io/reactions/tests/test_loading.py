import pandas as pd
import pytest

from nasap_net.io import load_reactions
from nasap_net.models import Assembly, BindingSite, Bond, Component, Reaction


@pytest.fixture
def M():
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L():
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X():
    return Component(kind='X', sites=[0])

@pytest.fixture
def MX2(M, X):
    return Assembly(
        id_='MX2',
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )

@pytest.fixture
def free_L(L):
    return Assembly(id_='free_L', components={'L0': L}, bonds=[])

@pytest.fixture
def MLX(M, L, X):
    return Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[],
    )

@pytest.fixture
def free_X(X):
    return Assembly(id_='free_X', components={'X0': X}, bonds=[])


def test_basic(tmp_path, MX2, free_L, MLX, free_X):
    df = pd.DataFrame([{
        'init_assem_id': 'MX2',
        'entering_assem_id': 'free_L',
        'product_assem_id': 'MLX',
        'leaving_assem_id': 'free_X',
        'metal_bs_component': 'M0',
        'metal_bs_site': 0,
        'leaving_bs_component': 'X0',
        'leaving_bs_site': 0,
        'entering_bs_component': 'L0',
        'entering_bs_site': 0,
        'duplicate_count': 4,
    }])

    reaction_file = tmp_path / 'reactions.csv'
    df.to_csv(reaction_file, index=False)

    imported_reactions = load_reactions(
        reaction_file,
        assemblies=[MX2, free_L, MLX, free_X],
        assembly_id_type='str',
        component_id_type='str',
        site_id_type='str',
    )

    assert len(imported_reactions) == 1
    assert imported_reactions[0] == Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', '0'),
        leaving_bs=BindingSite('X0', '0'),
        entering_bs=BindingSite('L0', '0'),
        duplicate_count=4,
    )


def test_index_column(tmp_path, MX2, free_L, MLX, free_X):
    df = pd.DataFrame([{
        'init_assem_id': 'MX2',
        'entering_assem_id': 'free_L',
        'product_assem_id': 'MLX',
        'leaving_assem_id': 'free_X',
        'metal_bs_component': 'M0',
        'metal_bs_site': 0,
        'leaving_bs_component': 'X0',
        'leaving_bs_site': 0,
        'entering_bs_component': 'L0',
        'entering_bs_site': 0,
        'duplicate_count': 4,
    }])
    reaction_file = tmp_path / 'reactions_with_index.csv'
    df.to_csv(reaction_file, index_label='index_column')

    imported_reactions = load_reactions(
        reaction_file,
        assemblies=[MX2, free_L, MLX, free_X],
        assembly_id_type='str',
        component_id_type='str',
        site_id_type='str',
        has_index_column=True,
    )

    assert len(imported_reactions) == 1
    assert imported_reactions[0] == Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', '0'),
        leaving_bs=BindingSite('X0', '0'),
        entering_bs=BindingSite('L0', '0'),
        duplicate_count=4,
    )


def test_with_id_column(tmp_path, MX2, free_L, MLX, free_X):
    df = pd.DataFrame([{
        'init_assem_id': 'MX2',
        'entering_assem_id': 'free_L',
        'product_assem_id': 'MLX',
        'leaving_assem_id': 'free_X',
        'metal_bs_component': 'M0',
        'metal_bs_site': 0,
        'leaving_bs_component': 'X0',
        'leaving_bs_site': 0,
        'entering_bs_component': 'L0',
        'entering_bs_site': 0,
        'duplicate_count': 4,
        'id': 'R1',
    }])
    reaction_file = tmp_path / 'reactions_with_id.csv'
    df.to_csv(reaction_file, index=False)

    imported_reactions = load_reactions(
        reaction_file,
        assemblies=[MX2, free_L, MLX, free_X],
        assembly_id_type='str',
        component_id_type='str',
        site_id_type='str',
        reaction_id_type='str',
    )

    assert len(imported_reactions) == 1
    assert imported_reactions[0] == Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', '0'),
        leaving_bs=BindingSite('X0', '0'),
        entering_bs=BindingSite('L0', '0'),
        duplicate_count=4,
        id_='R1',
    )
