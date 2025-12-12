import strawberry
from _typeshed import Incomplete
from abc import ABC
from enum import Enum
from tarandm_analytics_utils.utils.base_model import BaseModel as BaseModel
from typing import Any, Literal

logger: Incomplete

class AttributeDataType(str, Enum):
    CATEGORICAL = 'CATEGORICAL'
    NUMERICAL = 'NUMERICAL'

class PredictiveModelBinName(str, Enum):
    DEFAULT = '0_default'
    DEFINED_DEFAULT = '0_defined_default'
    SYSTEM_DEFAULT = '0_system_default'
    NULL = '1_null'

class AbstractAttributeBin(BaseModel, ABC):
    name: str
    value: float | None
    frequency: float | None
    target_rate: float | None
    id: int
    def __init__(self, **kwargs: Any) -> None: ...

class AttributeBinCategorical(AbstractAttributeBin):
    type: Literal[AttributeDataType.CATEGORICAL]
    categories: list[str] | None
    def __init__(self, **kwargs: Any) -> None: ...

class AttributeBinNumerical(AbstractAttributeBin):
    type: Literal[AttributeDataType.NUMERICAL]
    lower_bound: float | None
    upper_bound: float | None
    def __init__(self, **kwargs: Any) -> None: ...

AttributeBin: Incomplete

class AbstractAttributeBinType:
    name: strawberry.auto
    value: strawberry.auto
    frequency: strawberry.auto
    target_rate: strawberry.auto
    id: strawberry.auto
    @strawberry.field
    async def type(self, parent: strawberry.Parent[AttributeBin]) -> AttributeDataType: ...

class AttributeBinCategoricalType(AbstractAttributeBinType):
    categories: strawberry.auto

class AttributeBinNumericalType(AbstractAttributeBinType):
    lower_bound: strawberry.auto
    upper_bound: strawberry.auto
    @strawberry.field
    async def formatted_lower_bound(self, parent: strawberry.Parent[AttributeBinNumerical]) -> str | None: ...
    @strawberry.field
    async def formatted_upper_bound(self, parent: strawberry.Parent[AttributeBinNumerical]) -> str | None: ...

class AttributeBinning(BaseModel):
    attribute: str
    attribute_data_type: AttributeDataType
    attribute_binning: list[AttributeBin]
    binned_attribute_name: str | None
    def bin_numeric_attribute(self, value: int | float | None) -> float | None: ...
    def bin_categoric_attribute(self, value: str | None) -> float | None: ...

class AttributeBinningType:
    attribute: strawberry.auto
    @strawberry.field
    async def attribute_binning(self, parent: strawberry.Parent[AttributeBinning]) -> list[AttributeBinNumericalType | AttributeBinCategoricalType]: ...
