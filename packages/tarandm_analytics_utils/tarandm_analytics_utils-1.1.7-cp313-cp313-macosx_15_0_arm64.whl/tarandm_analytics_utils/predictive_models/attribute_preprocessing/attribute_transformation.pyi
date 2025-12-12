import strawberry
from tarandm_analytics_utils.utils.base_model import BaseModel as BaseModel

class AttributeTransformation(BaseModel):
    attribute: str
    transformation: str
    transformed_attribute_name: str | None

class AttributeTransformationType:
    attribute: strawberry.auto
    transformation: strawberry.auto
    transformed_attribute_name: strawberry.auto
