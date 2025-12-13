from dataclasses import asdict, dataclass
from typing import Generic, TypeVar

from nasap_net.models import Reaction
from .const import Column

_T = TypeVar('_T', int, str)  # Assembly ID type
_S = TypeVar('_S', int, str)  # Component ID type
_U = TypeVar('_U', int, str)  # Site ID type
_R = TypeVar('_R', int, str)  # Reaction ID type

T = TypeVar('T', bound='ReactionRow')


@dataclass(frozen=True)
class ReactionRow(Generic[_T, _S, _U, _R]):
    init_assem_id: _T
    entering_assem_id: _T | None
    product_assem_id: _T
    leaving_assem_id: _T | None
    metal_bs_component: _S
    metal_bs_site: _U
    leaving_bs_component: _S
    leaving_bs_site: _U
    entering_bs_component: _S
    entering_bs_site: _U
    duplicate_count: int
    id_: _R | None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_reaction(cls: type[T], reaction: Reaction) -> T:
        return cls(
            init_assem_id=reaction.init_assem_id,
            entering_assem_id=reaction.entering_assem_id,
            product_assem_id=reaction.product_assem_id,
            leaving_assem_id=reaction.leaving_assem_id,
            metal_bs_component=reaction.metal_bs.component_id,
            metal_bs_site=reaction.metal_bs.site_id,
            leaving_bs_component=reaction.leaving_bs.component_id,
            leaving_bs_site=reaction.leaving_bs.site_id,
            entering_bs_component=reaction.entering_bs.component_id,
            entering_bs_site=reaction.entering_bs.site_id,
            duplicate_count=reaction.duplicate_count,
            id_=reaction.id_or_none,
        )

    @classmethod
    def from_dict(
            cls: type[T],
            data: dict,
            *,
            assembly_id_type: type[_T],
            component_id_type: type[_S],
            site_id_type: type[_U],
            reaction_id_type: type[_R],
    ) -> T:
        return cls(
            init_assem_id=assembly_id_type(data[Column.INIT_ASSEM_ID.value]),
            entering_assem_id=(
                assembly_id_type(data[Column.ENTERING_ASSEM_ID.value])
                if data[Column.ENTERING_ASSEM_ID.value] is not None else None
            ),
            product_assem_id=assembly_id_type(
                data[Column.PRODUCT_ASSEM_ID.value]
            ),
            leaving_assem_id=(
                assembly_id_type(data[Column.LEAVING_ASSEM_ID.value])
                if data[Column.LEAVING_ASSEM_ID.value] is not None else None
            ),
            metal_bs_component=component_id_type(
                data[Column.METAL_BS_COMPONENT.value]
            ),
            metal_bs_site=site_id_type(data[Column.METAL_BS_SITE.value]),
            leaving_bs_component=component_id_type(
                data[Column.LEAVING_BS_COMPONENT.value]
            ),
            leaving_bs_site=site_id_type(data[Column.LEAVING_BS_SITE.value]),
            entering_bs_component=component_id_type(
                data[Column.ENTERING_BS_COMPONENT.value]
            ),
            entering_bs_site=site_id_type(data[Column.ENTERING_BS_SITE.value]),
            duplicate_count=int(data[Column.DUPLICATE_COUNT.value]),
            id_=(
                reaction_id_type(data[Column.ID_.value])
                if data.get(Column.ID_.value) is not None else None
            ),
        )
