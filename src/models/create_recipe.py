from pydantic import BaseModel, constr, validator

from src.enumirations import DietKind

from .instruction_step import InstructionStep
from .nutrition_information import NutritionInformation
from .yield_information import YieldInformation


class CreateRecipe(BaseModel):
    cook_time_sec: int  # TODO use appropriate type with encoding to BSON
    cooking_method: constr(min_length=1, strip_whitespace=True, to_lower=True)
    nutrition: NutritionInformation
    recipe_category: constr(min_length=1, strip_whitespace=True, to_lower=True)
    recipe_cuisine: constr(min_length=1, strip_whitespace=True, to_lower=True)
    recipe_instructions: list[InstructionStep]
    recipe_yield: YieldInformation
    suitable_for_diet: list[DietKind]

    @validator("recipe_instructions")
    def at_least_one_step(cls, v):
        if len(v) < 1:
            raise ValueError("Must contain at least one step")
        return v
