from nasap_net.models import Assembly, Component
from nasap_net.utils import deduplicate_ids


def test():
    X = Component(kind='X', sites=[0])

    assemblies = [
        Assembly(id_='freeX', components={'X0': X}, bonds=[]),
        Assembly(id_='freeX', components={'X1': X}, bonds=[]),
    ]

    deduplicated = deduplicate_ids(assemblies)

    assert deduplicated == [
        Assembly(id_='freeX', components={'X0': X}, bonds=[]),
        Assembly(id_='freeX_2', components={'X1': X}, bonds=[]),
    ]


def test_keep_order():
    X = Component(kind='X', sites=[0])

    assemblies = [
        Assembly(id_='freeX', components={'X0': X}, bonds=[]),
        Assembly(id_='freeX', components={'X2': X}, bonds=[]),
        Assembly(id_='freeX', components={'X1': X}, bonds=[]),
    ]

    deduplicated = deduplicate_ids(assemblies)

    assert deduplicated == [
        Assembly(id_='freeX', components={'X0': X}, bonds=[]),
        Assembly(id_='freeX_2', components={'X2': X}, bonds=[]),
        Assembly(id_='freeX_3', components={'X1': X}, bonds=[]),
    ]
