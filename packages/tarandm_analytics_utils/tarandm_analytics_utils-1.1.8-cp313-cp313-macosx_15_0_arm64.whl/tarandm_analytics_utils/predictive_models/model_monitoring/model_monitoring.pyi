from tarandm_analytics_utils.predictive_models.attribute_preprocessing.attribute_binning import AbstractAttributeBin as AbstractAttributeBin, AttributeBinCategorical as AttributeBinCategorical, AttributeBinNumerical as AttributeBinNumerical, AttributeBinning as AttributeBinning, AttributeBinningType as AttributeBinningType, AttributeDataType as AttributeDataType, PredictiveModelBinName as PredictiveModelBinName
from tarandm_analytics_utils.utils.base_model import BaseModel as BaseModel

class PredictiveModelMonitoring(BaseModel):
    binning: list[AttributeBinning]
    predictive_model_output_binning: AttributeBinning | None
    def remove_attribute_binning(self, attribute: str) -> None: ...
    def attribute_binning_exists(self, attribute: str) -> bool: ...
    def get_attribute_binning(self, attribute: str, attribute_dtype: AttributeDataType, attribute_value: str | float) -> AbstractAttributeBin | AttributeBinNumerical | AttributeBinCategorical | None: ...

class PredictiveModelMonitoringType:
    binning: list[AttributeBinningType]
    predictive_model_output_binning: AttributeBinningType | None
