from sqlmodel import Session, select
from app.models import Recipe

def create_recipe(db: Session, recipe: Recipe) -> Recipe:
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def get_recipes(db: Session) -> list[Recipe]:
    return db.exec(select(Recipe)).all()

def get_recipe(db: Session, recipe_id: int) -> Recipe:
    return db.get(Recipe, recipe_id)

def update_recipe(db: Session, recipe_id: int, recipe_data: dict) -> Recipe:
    recipe = db.get(Recipe, recipe_id)
    for key, value in recipe_data.items():
        setattr(recipe, key, value)
    db.commit()
    db.refresh(recipe)
    return recipe

def delete_recipe(db: Session, recipe_id: int) -> None:
    recipe = db.get(Recipe, recipe_id)
    db.delete(recipe)
    db.commit()
