from nasap_net.isomorphism.utils import reverse_mapping_seq


def test_basic():
    # [2, 0, 1] means: 0->2, 1->0, 2->1
    # So the reverse mapping is: 0->1, 1->2, 2->0  => [1, 2, 0]
    assert reverse_mapping_seq([2, 0, 1]) == [1, 2, 0]
