from fastapi import FastAPI
from pydantic import BaseModel


# 1. Create a FastAPI App Instance
app = FastAPI()
items = {}  # In-memory database


class Item(BaseModel):
    # 3. Define Pydantic Model
    name: str
    price: float | None = None
    instock_qt: int = 0


@app.post("/add_items/")
def create_item(item: Item):
    # 2. Define a function and associate with a route.
    items[item.name] = item
    return {"message": "Item added successfully", "items": items}


@app.post("/add_items/")
def create_item_1(name: str, price: float, instock_qt: int = 10):
    items[name] = {}


@app.get("/list_items/")
def list_all():
    return {"items": items}
