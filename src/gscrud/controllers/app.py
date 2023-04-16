from typing import Union

from fastapi import FastAPI
from src.gscrud.controllers import api

app = FastAPI(title="GS-CRUD")
app.include_router(api.router)


@app.get("/")
def welcome():
    return "👋 Welcome to GS Crud"

