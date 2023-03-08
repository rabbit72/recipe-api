from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from src.collections import recipes
from src.models.create_recipe import CreateRecipe
from src.models.recipe import PyObjectId, Recipe

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    # dependencies=[Depends(has_active_session_in_cookies)],
)


@router.get("/", response_model=list[Recipe])
async def get_all_recipes():
    return await recipes.get_all()


@router.post("/", response_model=Recipe, status_code=status.HTTP_201_CREATED)
async def create_new_recipe(new_recipe: CreateRecipe):
    new_recipe_id = await recipes.create_new(new_recipe.dict())
    recipe = await recipes.find_one(new_recipe_id)
    return recipe


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: PyObjectId):
    recipe = await recipes.find_one(recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return recipe


@router.put("/{recipe_id}", status_code=status.HTTP_200_OK)
async def update_or_create_recipe(
    recipe_id: PyObjectId, new_recipe: CreateRecipe, response: Response
):
    new_recipe_from_model = new_recipe.dict()
    is_recipe_updated = await recipes.replace_if_exists(
        recipe_id, new_recipe_from_model
    )

    if is_recipe_updated:
        return {"recipe_id": str(recipe_id)}

    new_recipe_from_model_with_id = {
        **new_recipe_from_model,
        **{"_id": recipe_id},
    }
    new_recipe_id = await recipes.create_new(new_recipe_from_model_with_id)
    response.status_code = status.HTTP_201_CREATED
    return {"recipe_id": str(new_recipe_id)}


@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: PyObjectId):
    is_recipe_deleted = await recipes.delete_one_if_exists(recipe_id)
    if not is_recipe_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"recipe_id": str(recipe_id)}
