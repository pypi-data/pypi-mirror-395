import strawberry
from datetime import date
from tarandm_analytics_utils.predictive_models.model_description.sample_decription import SampleDescription as SampleDescription, SampleDescriptionType as SampleDescriptionType
from tarandm_analytics_utils.utils.base_model import BaseModel as BaseModel
from typing import Any

class AttachedImage(BaseModel):
    type: str
    filename: str
    image: bytes | None

class AttachedImageType:
    type: strawberry.auto
    filename: strawberry.auto

class PredictiveModelDescription(BaseModel):
    predictive_model_name: str | None
    predictive_model_created: date | None
    sample_metadata: list[SampleDescription] | None
    attribute_description: dict[str, str] | None
    hyperparameters: dict[str, Any] | None
    number_of_trainable_parameters: int | None
    general_notes: dict[str, str] | None
    attached_images: list[AttachedImage] | None
    def add_general_note(self, note: dict | str) -> None: ...
    def remove_general_note(self, note_key: str) -> None: ...

class AttributeDescriptionType:
    attribute_name: str
    description: str

class HyperparameterType:
    name: str
    value: str

class GeneralNoteType:
    title: str
    content: str

class PredictiveModelDescriptionType:
    predictive_model_name: strawberry.auto
    predictive_model_created: strawberry.auto
    number_of_trainable_parameters: strawberry.auto
    attached_images: list[AttachedImageType] | None
    sample_metadata: list[SampleDescriptionType] | None
    @strawberry.field
    async def attribute_description(self, parent: strawberry.Parent[PredictiveModelDescription]) -> list[AttributeDescriptionType]: ...
    @strawberry.field
    async def hyperparameters(self, parent: strawberry.Parent[PredictiveModelDescription]) -> list[HyperparameterType]: ...
    @strawberry.field
    async def general_notes(self, parent: strawberry.Parent[PredictiveModelDescription]) -> list[GeneralNoteType]: ...
    @strawberry.field
    async def eval_metric(self, parent: strawberry.Parent[PredictiveModelDescription]) -> str: ...
