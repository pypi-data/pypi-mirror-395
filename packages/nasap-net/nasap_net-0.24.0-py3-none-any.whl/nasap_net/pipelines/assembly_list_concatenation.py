import os
from collections.abc import Mapping, Sequence
from typing import Any, Literal, overload

from nasap_net import Assembly, Component, group_assemblies_by_isomorphism
from nasap_net.pipelines.lib import read_file, write_output


@overload
def concatenate_assemblies_pipeline(
        assemblies_path_list: Sequence[os.PathLike | str],
        components_path: None,
        resulting_assems_path: os.PathLike | str,
        *,
        skip_isomorphism_checks: Literal[True] = True,
        start: int = 0,
        overwrite: bool = False,
        verbose: bool = False,
        ) -> None: ...
@overload
def concatenate_assemblies_pipeline(
        assemblies_path_list: Sequence[os.PathLike | str],
        components_path: os.PathLike | str,
        resulting_assems_path: os.PathLike | str,
        *,
        already_unique_within_files: bool = False,
        skip_isomorphism_checks: Literal[False] = False,
        start: int = 0,
        overwrite: bool = False,
        verbose: bool = False,
        ) -> None: ...
def concatenate_assemblies_pipeline(
        assemblies_path_list: Sequence[os.PathLike | str],
        components_path: os.PathLike | str | None,
        resulting_assems_path: os.PathLike | str,
        *,
        already_unique_within_files: bool = False,
        skip_isomorphism_checks: bool = False,
        start: int = 0,
        overwrite: bool = False,
        verbose: bool = False,
        ) -> None:
    """Concatenate a list of assemblies into a single list excluding duplicates.
    
    Concatenates a list of assemblies from different files into a single 
    list. The IDs of the assemblies are reindexed starting from the given
    start value.

    Parameters
    ----------
    assemblies_path_list : Sequence[os.PathLike | str]
        List of paths to the files containing the assemblies.
        Each file should contain a dictionary with the assembly IDs as keys
        and the Assembly objects as values.
    components_path : os.PathLike | str | None
        Path to the file containing the component kinds. 
        None is allowed only if `skip_isomorphism_checks` is True.
    resulting_assems_path : os.PathLike | str
        Path to the file to save the concatenated list of assemblies.
    already_unique_within_files : bool, optional
        Whether the assemblies in each file are already unique, 
        by default False. If True, the isomorphism checks are skipped 
        for the assemblies within each file. The parameter will be 
        ignored if `exclude_duplicates` is False.
    skip_isomorphism_checks : bool, optional
        Whether to skip all isomorphism checks, by default False.
        If True, the assemblies are concatenated without checking for
        isomorphism. The resulting list may contain duplicate assemblies.
    start : int, optional
        Starting index for the reindexing of the assemblies, by default 0.
    overwrite : bool, optional
        Whether to overwrite the file if it already exists, by default False.
    verbose : bool, optional
        Whether to print the process steps, by default False
    
    Notes
    -----
    The reindexing order is determined by the order of the input files and 
    the order of the assemblies in each file, not by their alphabetical 
    order.

    Output file contains a dictionary with the reindexed IDs as keys and the
    Assembly objects as values.
    """
    if skip_isomorphism_checks:
        concatenate_assemblies_without_isom_checks(
            assemblies_path_list, resulting_assems_path,
            start=start, overwrite=overwrite, verbose=verbose)
        return
    if components_path is None:
        raise ValueError(
            'The parameter `components_path` is required if '
            '`skip_isomorphism_checks` is False.')
    
    # Input
    list_of_id_to_assembly: Sequence[Mapping[Any, Assembly]] = [
        read_file(path, verbose=verbose)
        for path in assemblies_path_list]
    
    components: Mapping[str, Component] = read_file(
        components_path, verbose=verbose)['component_kinds']
    
    # Main process
    if verbose:
        print('Concatenating assembly lists...')

    assemblies: list[Assembly] = []
    for id_to_assembly in list_of_id_to_assembly:
        assemblies.extend(id_to_assembly.values())
    
    reindexed_with_dup = {
        new_id: assembly for new_id, assembly 
        in enumerate(assemblies, start=start)
    }

    if verbose:
        print('Concatenation completed.')
    if verbose:
        print('Excluding duplicate assemblies...')
    
    if already_unique_within_files:
        non_isomorphic_groups = [
            set(id_to_assembly.keys())
            for id_to_assembly in list_of_id_to_assembly
        ]
    else:
        non_isomorphic_groups = None
    
    isom_group = group_assemblies_by_isomorphism(
        reindexed_with_dup, components,
        non_isomorphic_groups=non_isomorphic_groups)
    
    reindexed_without_dup = {
        id_: reindexed_with_dup[id_] for id_ in isom_group.keys()}
    
    if verbose:
        print('Duplicate exclusion completed.')

    # Save reindexed assemblies
    write_output(
        resulting_assems_path, reindexed_without_dup,
        overwrite=overwrite, verbose=verbose,
        header='Concatenated list of assemblies')


def concatenate_assemblies_without_isom_checks(
        assemblies_path_list: Sequence[os.PathLike | str],
        resulting_assems_path: os.PathLike | str,
        *,
        start: int = 0,
        overwrite: bool = False,
        verbose: bool = False,
        ) -> None:
    """Concatenate a list of assemblies into a single list.
    
    Concatenates a list of assemblies from different files into a single 
    list. The IDs of the assemblies are reindexed starting from the given
    start value.

    Parameters
    ----------
    assemblies_path_list : Sequence[os.PathLike | str]
        List of paths to the files containing the assemblies.
        Each file should contain a dictionary with the assembly IDs as keys
        and the Assembly objects as values.
    resulting_assems_path : os.PathLike | str
        Path to the file to save the concatenated list of assemblies.
    exclude_duplicates : bool, optional
        Whether to exclude duplicate assemblies, by default False.
        If True, isomorphism checks are performed to group the assemblies
        by isomorphism. The resulting list contains only the unique
        assemblies.
    already_unique_within_files : bool, optional
        Whether the assemblies in each file are already unique, 
        by default False. If True, the isomorphism checks are skipped 
        for the assemblies within each file. The parameter will be 
        ignored if `exclude_duplicates` is False.
    start : int, optional
        Starting index for the reindexing of the assemblies, by default 0.
    overwrite : bool, optional
        Whether to overwrite the file if it already exists, by default False.
    verbose : bool, optional
        Whether to print the process steps, by default False
    
    Notes
    -----
    The reindexing order is determined by the order of the input files and 
    the order of the assemblies in each file, not by their alphabetical 
    order.

    Output file contains a dictionary with the reindexed IDs as keys and the
    Assembly objects as values.
    """
    # Input
    list_of_id_to_assembly: Sequence[Mapping[Any, Assembly]] = [
        read_file(path, verbose=verbose)
        for path in assemblies_path_list]
    
    # Main process
    if verbose:
        print('Concatenating assembly lists...')

    assemblies: list[Assembly] = []
    for id_to_assembly in list_of_id_to_assembly:
        assemblies.extend(id_to_assembly.values())
    
    reindexed = {
        new_id: assembly for new_id, assembly 
        in enumerate(assemblies, start=start)
    }

    if verbose:
        print('Concatenation completed.')

    # Save reindexed assemblies
    write_output(
        resulting_assems_path, reindexed,
        overwrite=overwrite, verbose=verbose,
        header='Concatenated list of assemblies')
