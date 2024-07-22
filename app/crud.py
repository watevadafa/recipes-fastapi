from sqlmodel import Session
from app.models import Recipe


def create_recipe(db: Session, recipe: Recipe):
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


def get_recipes(db: Session):
    return db.query(Recipe).all()


def get_recipe(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def update_recipe(db: Session, recipe_id: int, recipe_data: dict):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    for key, value in recipe_data.items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    db.delete(db_recipe)
    db.commit()
