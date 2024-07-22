from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
