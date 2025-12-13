from _typeshed import Incomplete
from pydantic import BaseModel as PydanticBaseModel

class _CyFunctionDetectorMeta(type):
    def __instancecheck__(self, instance: object) -> bool: ...

class CyFunctionDetector(metaclass=_CyFunctionDetectorMeta): ...

class BaseModel(PydanticBaseModel):
    model_config: Incomplete
