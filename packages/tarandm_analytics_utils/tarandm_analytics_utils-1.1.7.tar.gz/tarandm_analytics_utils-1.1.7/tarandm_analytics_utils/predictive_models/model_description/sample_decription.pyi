import strawberry
from datetime import date
from tarandm_analytics_utils.predictive_models.model_performance.sample_performance import SampleType as SampleType
from tarandm_analytics_utils.utils.base_model import BaseModel as BaseModel
from typing import Any

class ClassFrequency(BaseModel):
    label_class: Any
    number_of_observations: int | None

class ClassFrequencyType:
    number_of_observations: strawberry.auto
    @strawberry.field
    def label_class(self, parent: strawberry.Parent[ClassFrequency]) -> str: ...

class SampleDescription(BaseModel):
    sample_type: SampleType | None
    first_date: date | None
    last_date: date | None
    number_of_observations: int | None
    label_class_frequency: list[ClassFrequency] | None

class SampleDescriptionType:
    sample_type: strawberry.auto
    first_date: strawberry.auto
    last_date: strawberry.auto
    number_of_observations: strawberry.auto
    label_class_frequency: list[ClassFrequencyType] | None
