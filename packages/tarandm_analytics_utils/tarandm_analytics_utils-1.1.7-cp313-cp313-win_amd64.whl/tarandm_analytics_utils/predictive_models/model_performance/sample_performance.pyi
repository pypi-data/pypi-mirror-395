import strawberry
from enum import Enum
from tarandm_analytics_utils.utils.base_model import BaseModel as BaseModel

class SampleType(str, Enum):
    TRAIN = 'TRAIN'
    VALID = 'VALID'
    TEST = 'TEST'
    OOT = 'OOT'
    CV = 'CV'

class PerformanceMetrics(str, Enum):
    AUC = 'AUC'
    GINI = 'GINI'
    LIFT = 'LIFT'
    KS = 'KS'
    TAU = 'TAR'
    RHO = 'RHO'
    ACCURACY = 'ACCURACY'

class SamplePerformance(BaseModel):
    sample: SampleType
    target: str
    performance: dict[PerformanceMetrics, float]

class SamplePerformancePerformanceType:
    metric: PerformanceMetrics
    value: float

class SamplePerformanceType:
    sample: strawberry.auto
    target: strawberry.auto
    @strawberry.field
    async def performance(self, parent: strawberry.Parent[SamplePerformance]) -> list[SamplePerformancePerformanceType]: ...
