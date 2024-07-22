from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models import Recipe
from app.crud import (
    create_recipe,
    get_recipes,
    get_recipe,
    update_recipe,
    delete_recipe,
)
from app.database import get_session
from app.schemas import (
    RecipeCreate,
    RecipeCreateFailureResponse,
    RecipeInDBBase,
    RecipesListResponse,
    RecipeResponseWithMessage,
)
from app.services import validate_required_fields

recipe_router = APIRouter()

REQUIRED_FIELDS = ["title", "making_time", "serves", "ingredients", "cost"]


@recipe_router.post(
    "/",
    response_model=RecipeResponseWithMessage,
    responses={400: {"model": RecipeCreateFailureResponse}},
)
def create_recipe_endpoint(recipe: RecipeCreate, db: Session = Depends(get_session)):
    missing_fields = validate_required_fields(recipe.dict(), REQUIRED_FIELDS)
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Recipe creation failed!",
                "required": ", ".join(missing_fields),
            },
        )
    db_recipe = create_recipe(db, Recipe.from_orm(recipe))
    return RecipeResponseWithMessage(
        message="Recipe successfully created!",
        recipe=[RecipeInDBBase.from_orm(db_recipe)],
    )


@recipe_router.get("/", response_model=RecipesListResponse)
def read_recipes(db: Session = Depends(get_session)):
    recipes = get_recipes(db)
    return RecipesListResponse(
        recipes=[RecipeInDBBase.from_orm(recipe) for recipe in recipes]
    )


@recipe_router.get("/{recipe_id}", response_model=RecipeResponseWithMessage)
def read_recipe(recipe_id: int, db: Session = Depends(get_session)):
    recipe = get_recipe(db, recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return RecipeResponseWithMessage(
        message="Recipe details by id", recipe=[RecipeInDBBase.from_orm(recipe)]
    )


@recipe_router.patch("/{recipe_id}", response_model=RecipeResponseWithMessage)
def update_recipe_endpoint(
    recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_session)
):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    updated_recipe = update_recipe(db, recipe_id, recipe.dict(exclude_unset=True))
    return RecipeResponseWithMessage(
        message="Recipe details by id", recipe=[RecipeInDBBase.from_orm(updated_recipe)]
    )


@recipe_router.delete("/{recipe_id}", response_model=dict)
def delete_recipe_endpoint(recipe_id: int, db: Session = Depends(get_session)):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    delete_recipe(db, recipe_id)
    return {"ok": True}
