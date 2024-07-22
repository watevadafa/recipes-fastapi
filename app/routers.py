from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models import Recipe
from app.crud import create_recipe, get_recipes, get_recipe, update_recipe, delete_recipe
from app.database import get_session

recipe_router = APIRouter()

@recipe_router.post("/", response_model=Recipe)
def create(recipe: Recipe, db: Session = Depends(get_session)):
    return create_recipe(db, recipe)

@recipe_router.get("/", response_model=list[Recipe])
def read_recipes(db: Session = Depends(get_session)):
    return get_recipes(db)

@recipe_router.get("/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_session)):
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@recipe_router.put("/{recipe_id}", response_model=Recipe)
def update(recipe_id: int, recipe: Recipe, db: Session = Depends(get_session)):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return update_recipe(db, recipe_id, recipe.dict(exclude_unset=True))

@recipe_router.delete("/{recipe_id}", response_model=dict)
def delete(recipe_id: int, db: Session = Depends(get_session)):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    delete_recipe(db, recipe_id)
    return {"ok": True}
