from .types import DdfLike
from .specs import AttachmentSpec
from .merger import DfMerger
from .async_enricher import AsyncDfEnricher

__all__ = [
    "DdfLike",
    "AttachmentSpec",
    "DfMerger",
    "AsyncDfEnricher",
]

"""
Usage Example

DataFrame Enricher Package
# solutions/logistics/enrichers/products_customer_enricher.py

from sibi_dst.df_enrich import AttachmentSpec, AsyncDfEnricher
from solutions.logistics.datacubes.products.product_params import ProductsCustomerCube
from solutions.logistics.tasks.helpers.product_info.attachers import (
    attachment_customer_data,
    attachment_subproduct_type_info,
)


ATTACHMENT_SPECS = [
    AttachmentSpec(
        key="cust_data",
        required_cols={"customer_id"},
        attachment_fn=attachment_customer_data,
        col_to_kwarg={"customer_id": "id__in"},
        left_on=["customer_id"],
        right_on=["temp_join_col"],
        drop_cols=["temp_join_col"],
    ),
    AttachmentSpec(
        key="subprod_data",
        required_cols={"subproduct_type_id"},
        attachment_fn=attachment_subproduct_type_info,
        col_to_kwarg={"subproduct_type_id": "id__in"},
        left_on=["subproduct_type_id"],
        right_on=["temp_join_col"],
        drop_cols=["temp_join_col"],
    ),
]


async def enrich_products_customer_cube(
    cols: list[str] = ("customer_id", "subproduct_type_id"),
):
    base = await ProductsCustomerCube().aload()
    enricher = AsyncDfEnricher(base_df=base, specs=ATTACHMENT_SPECS, debug=True)
    return await enricher.enrich(cols=cols)

"""

