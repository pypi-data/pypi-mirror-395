from nasap_net.io.assemblies.semi_light_assembly import SemiLightAssembly
from nasap_net.models import Bond


def test___repr__():
    assembly = SemiLightAssembly(
        components={'X0': 'X'},
        bonds=[],
    )
    repr_str = repr(assembly)
    expected_str = (
        "<SemiLightAssembly components={'X0': 'X'}, bonds=[]>"
    )
    assert repr_str == expected_str


def test___repr___with_id():
    assembly = SemiLightAssembly(
        id_='free_X',
        components={'X0': 'X'},
        bonds=[],
    )
    repr_str = repr(assembly)
    expected_str = (
        "<SemiLightAssembly id_='free_X', components={'X0': 'X'}, bonds=[]>"
    )
    assert repr_str == expected_str


def test___repr___with_bonds():
    assembly = SemiLightAssembly(
        components={'X0': 'X', 'M0': 'M', 'X1': 'X'},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'X1', 0),
        ],
    )
    repr_str = repr(assembly)
    expected_str = (
        "<SemiLightAssembly components={'X0': 'X', 'M0': 'M', 'X1': 'X'}, "
        "bonds=[('M0', 0, 'X0', 0), ('M0', 1, 'X1', 0)]>"
    )
    assert repr_str == expected_str
