from pydantic import BaseModel, Field
import models
from fastapi import FastAPI
from routers import router
from database import engine

app = FastAPI()

app.include_router(router)

models.Base.metadata.create_all(bind=engine)


class Expression(BaseModel):
    expression: str = Field(min_length=1)
    result: float = Field(gt=-1, lt=101)
