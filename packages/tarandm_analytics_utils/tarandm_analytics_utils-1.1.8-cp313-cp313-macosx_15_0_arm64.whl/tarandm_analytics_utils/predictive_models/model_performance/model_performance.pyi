import strawberry
from tarandm_analytics_utils.predictive_models.model_performance.sample_performance import PerformanceMetrics as PerformanceMetrics, SamplePerformance as SamplePerformance, SamplePerformanceType as SamplePerformanceType
from tarandm_analytics_utils.utils.base_model import BaseModel as BaseModel
from typing import Any

class PredictiveModelPerformance(BaseModel):
    sample_performance: list[SamplePerformance]
    performance_metrics: list[PerformanceMetrics]
    @classmethod
    def validate_performance_metric_str(cls, metric: str) -> PerformanceMetrics: ...
    @classmethod
    def validate_performance_metrics(cls, data: Any) -> Any: ...

class PredictiveModelPerformanceType:
    sample_performance: list[SamplePerformanceType]
    performance_metrics: strawberry.auto
