from collections import Counter
from collections.abc import Sequence

from nasap_net.models import Assembly


def generate_composition_formula(
        assembly: Assembly,
        *,
        order: Sequence[str] | None = None,
) -> str:
    """Generate a composition formula string for the given assembly.

    You can specify the order of component kinds in the formula.
    Components not specified in `comp_kind_order` will appear at the end of
    the formula sorted alphabetically.

    Parameters
    ----------
    assembly : Assembly
        The assembly for which to generate the composition formula.
    order : Sequence[str]
        The order of component kinds to use in the formula.

    Returns
    -------
    str
        The composition formula string.
    """
    kind_counter: Counter[str] = Counter(
        comp.kind for comp in assembly.components.values()
    )
    if order is None:
        full_kind_order = sorted(kind_counter.keys())
    else:
        unspecified_kinds = kind_counter.keys() - set(order)
        sorted_unspecified_kinds = sorted(unspecified_kinds)
        full_kind_order = list(order) + sorted_unspecified_kinds

    formula_parts = []
    for kind in full_kind_order:
        if kind not in kind_counter:
            continue
        count = kind_counter[kind]
        formula_parts.append(_composition_to_str(kind, count))

    return ''.join(formula_parts)


def _composition_to_str(
        kind: str,
        count: int,
) -> str:
    """Convert a component kind and its count to a string representation."""
    if count == 1:
        return kind
    return f'{kind}{count}'
