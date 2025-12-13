from enum import Enum


class Column(Enum):
    """Column names for reaction data."""
    INIT_ASSEM_ID = 'init_assem_id'
    ENTERING_ASSEM_ID = 'entering_assem_id'
    PRODUCT_ASSEM_ID = 'product_assem_id'
    LEAVING_ASSEM_ID = 'leaving_assem_id'
    METAL_BS_COMPONENT = 'metal_bs_component'
    METAL_BS_SITE = 'metal_bs_site'
    LEAVING_BS_COMPONENT = 'leaving_bs_component'
    LEAVING_BS_SITE = 'leaving_bs_site'
    ENTERING_BS_COMPONENT = 'entering_bs_component'
    ENTERING_BS_SITE = 'entering_bs_site'
    DUPLICATE_COUNT = 'duplicate_count'
    ID_ = 'id'
