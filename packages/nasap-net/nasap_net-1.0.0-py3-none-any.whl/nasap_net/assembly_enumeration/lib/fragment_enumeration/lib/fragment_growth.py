from collections.abc import Iterator

from ..models import Fragment, GrowingStep


def enumerate_one_step_grown_fragments(
        fragment: Fragment
) -> Iterator[Fragment]:
    for growing_step in fragment.enumerate_possible_growing_steps():
        yield grow_fragment(fragment, growing_step)


def grow_fragment(
        fragment: Fragment, step: GrowingStep
) -> Fragment:
    if step.component_to_add is None:
        new_components = fragment.components
    else:
        new_components = fragment.components | {step.component_to_add}
    new_bonds = fragment.bonds | {step.bond_to_add}
    return fragment.copy_with(components=new_components, bonds=new_bonds)
