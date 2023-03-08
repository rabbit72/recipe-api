from enum import Enum


class DietKind(str, Enum):
    Diabetic = "Diabetic"
    GlutenFree = "GlutenFree"
    Halal = "Halal"
    Hindu = "Hindu"
    Kosher = "Kosher"
    LowCalorie = "LowCalorie"
    LowFat = "LowFat"
    LowLactose = "LowLactose"
    LowSalt = "LowSalt"
    Vegan = "Vegan"
    Vegetarian = "Vegetarian"
