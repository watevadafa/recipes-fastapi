from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.database import engine
from app.models import SQLModel
from app.routers import recipe_router
from app.exceptions import custom_validation_exception_handler

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(recipe_router, prefix="/recipes", tags=["recipes"])
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
