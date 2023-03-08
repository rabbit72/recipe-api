from bson import ObjectId
from pydantic import BaseModel, Field

from src.enumirations import DietKind

from .instruction_step import InstructionStep
from .nutrition_information import NutritionInformation
from .yield_information import YieldInformation


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Recipe(BaseModel):
    id_: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cook_time_sec: int  # TODO use appropriate type with encoding to BSON
    cooking_method: str
    nutrition: NutritionInformation
    recipe_category: str
    recipe_cuisine: str
    recipe_instructions: list[InstructionStep]
    recipe_yield: YieldInformation
    suitable_for_diet: list[DietKind]

    class Config:
        json_encoders = {ObjectId: str}
