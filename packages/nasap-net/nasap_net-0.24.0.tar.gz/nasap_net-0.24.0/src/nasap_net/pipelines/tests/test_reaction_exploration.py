from typing import TypeAlias

import pandas as pd
import pytest
import yaml

from nasap_net import Assembly, Component, InterReaction, IntraReaction
from nasap_net.pipelines import explore_reactions_pipeline

Reaction: TypeAlias = InterReaction | IntraReaction

def test_comprehensive_reaction_sets(tmpdir):
    components_data = {
        'component_kinds': {
        'M': Component(['a', 'b']),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
        }
    }

    id_to_assembly = {
        # MX2: X0(a)-(a)M0(b)-(a)X1
        0: Assembly(
            {'M0': 'M', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'X1.a')]
        ),
        1: Assembly({'L0': 'L'}),  # L: (a)L0(b)
        2: Assembly({'X0': 'X'}),  # X: (a)X0
        # MLX: (a)L0(b)-(a)M0(b)-(a)X0
        3: Assembly(
            {'M0': 'M', 'L0': 'L', 'X0': 'X'},
            [('L0.b', 'M0.a'), ('M0.b', 'X0.a')]
        ),
        # ML2: (a)L0(b)-(a)M0(b)-(a)L1(b)
        4: Assembly(
            {'M0': 'M', 'L0': 'L', 'L1': 'L'},
            [('L0.b', 'M0.a'), ('M0.b', 'L1.a')]
        ),
        # M2L2X: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)
        5: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 'X0': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'L1.a')]
        ),
        # M2LX2: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)X1
        6: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'X1.a')]
        ),
        # M2L2-ring: //-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)-//
        7: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L'},
            [('M0.b', 'L0.a'), ('L0.b', 'M1.a'), ('M1.b', 'L1.a'),
             ('L1.b', 'M0.a')]
        ),
    }

    config = {
        'mle_kinds': {
            'metal': 'M',
            'leaving': 'X',
            'entering': 'L',
        }
    }

    # Create input files
    assemblies_path = tmpdir / 'assemblies.yaml'
    components_path = tmpdir / 'components.yaml'
    config_path = tmpdir / 'config.yaml'
    output_path = tmpdir / 'reactions.csv'

    with open(assemblies_path, 'w') as f:
        yaml.dump(id_to_assembly, f)
    with open(components_path, 'w') as f:
        yaml.dump(components_data, f)
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    expected_csv = """\
init_assem_id,entering_assem_id,product_assem_id,leaving_assem_id,metal_bs,leaving_bs,entering_bs,duplicate_count
5,,7,2,M0.a,X0.a,L1.b,1
0,1,3,2,M0.a,X0.a,L0.a,4
0,3,6,2,M0.a,X0.a,L0.a,2
0,4,5,2,M0.a,X0.a,L0.a,4
3,1,4,2,M0.b,X0.a,L0.a,2
3,3,5,2,M0.b,X0.a,L0.a,2
6,1,5,2,M0.a,X0.a,L0.a,4
"""

    # Run the pipeline
    explore_reactions_pipeline(
        assemblies_path=assemblies_path,
        components_path=components_path,
        config_path=config_path,
        output_path=output_path,
        overwrite=True, verbose=True
    )

    # Read the output CSV
    with open(output_path, 'r') as f:
        output_csv = f.read()

    # Check if the output CSV matches the expected CSV
    assert output_csv == expected_csv


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
