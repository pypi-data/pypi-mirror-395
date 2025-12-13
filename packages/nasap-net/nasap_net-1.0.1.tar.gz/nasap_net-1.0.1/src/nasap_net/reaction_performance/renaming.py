from dataclasses import dataclass

from nasap_net.helpers import reindex_components_in_assembly
from nasap_net.models import Assembly, BindingSite, MLE
from nasap_net.types import ID


@dataclass(frozen=True)
class Renamed:
    init_assembly: Assembly
    entering_assembly: Assembly
    mle: MLE


def reindex_components_for_inter_reaction(
        init_assembly: Assembly,
        entering_assembly: Assembly,
        mle: MLE,
        *,
        init_prefix: str = 'init_',
        entering_prefix: str = 'entering_'
) -> Renamed:
    def init_reindexing_func(comp_id: ID) -> ID:
        return f'{init_prefix}{comp_id}'

    def entering_reindexing_func(comp_id: ID) -> ID:
        return f'{entering_prefix}{comp_id}'

    reindexed_init_assem = reindex_components_in_assembly(
        init_assembly, init_reindexing_func)
    reindexed_entering_assem = reindex_components_in_assembly(
        entering_assembly, entering_reindexing_func)
    reindexed_mle = MLE(
        metal=BindingSite(
            component_id=init_reindexing_func(mle.metal.component_id),
            site_id=mle.metal.site_id),
        leaving=BindingSite(
            component_id=init_reindexing_func(mle.leaving.component_id),
            site_id=mle.leaving.site_id),
        entering=BindingSite(
            component_id=entering_reindexing_func(mle.entering.component_id),
            site_id=mle.entering.site_id),
        duplication=mle.duplication_or_none
    )
    return Renamed(
        init_assembly=reindexed_init_assem,
        entering_assembly=reindexed_entering_assem,
        mle=reindexed_mle
    )
