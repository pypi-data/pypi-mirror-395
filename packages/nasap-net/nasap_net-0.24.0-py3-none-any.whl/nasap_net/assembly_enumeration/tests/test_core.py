from nasap_net.assembly_enumeration import enumerate_assemblies


def test_M4L4(M4L4, M4L4_symmetry_operations, X):
    assemblies = enumerate_assemblies(
        M4L4,
        leaving_ligand=X,
        leaving_ligand_site=0,
        metal_kinds=['M'],
        symmetry_operations=list(M4L4_symmetry_operations.values())
    )
    assert len(assemblies) == 14


def test_M2L4(M2L4, M2L4_symmetry_operations, X):
    assemblies = enumerate_assemblies(
        M2L4,
        leaving_ligand=X,
        leaving_ligand_site=0,
        metal_kinds=['M'],
        symmetry_operations=list(M2L4_symmetry_operations.values())
    )
    assert len(assemblies) == 29


def test_M9L6(M9L6, M9L6_symmetry_operations, X):
    assemblies = enumerate_assemblies(
        M9L6,
        leaving_ligand=X,
        leaving_ligand_site=0,
        metal_kinds=['M'],
        symmetry_operations=list(M9L6_symmetry_operations.values())
    )
    assert len(assemblies) == 505


def test_without_specifying_leaving_site(M4L4, M4L4_symmetry_operations, X):
    assemblies = enumerate_assemblies(
        M4L4,
        leaving_ligand=X,
        leaving_ligand_site=None,
        metal_kinds=['M'],
        symmetry_operations=list(M4L4_symmetry_operations.values())
    )
    assert len(assemblies) == 14
