from datetime import datetime
from pydantic import BaseModel
from typing import List


class RecipeBase(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int


class RecipeCreate(RecipeBase):
    pass


class RecipeInDBBase(RecipeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeResponseWithMessage(BaseModel):
    message: str
    recipe: List[RecipeInDBBase]


class RecipesListResponse(BaseModel):
    recipes: List[RecipeInDBBase]


class RecipeCreateFailureResponse(BaseModel):
    message: str
    required: str
