from bson import ObjectId
from pydantic import parse_obj_as

from src.db import database_connection
from src.models.recipe import Recipe

collection = database_connection["recipe"]


async def get_all() -> list[Recipe]:
    cursor = collection.find({})
    recipes = await cursor.to_list(length=100)
    return parse_obj_as(list[Recipe], list(recipes))


async def find_one(recipe_id: ObjectId) -> Recipe | None:
    recipe = await collection.find_one(ObjectId(recipe_id))
    if not recipe:
        return None
    return Recipe(**recipe)


async def create_new(new_recipe: dict) -> ObjectId:
    insert_one_result = await collection.insert_one(new_recipe)
    return insert_one_result.inserted_id


async def delete_one_if_exists(recipe_id: ObjectId) -> bool:
    delete_result = await collection.delete_one({"_id": recipe_id})
    return delete_result.deleted_count != 0


async def replace_if_exists(recipe_id: ObjectId, new_recipe: dict) -> bool:
    update_result = await collection.replace_one({"_id": recipe_id}, new_recipe)
    return update_result.modified_count != 0
