from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
    # example with a forward reference
    linked_items: Optional[List['Item']] = None


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, q: Optional[str] = None):
    ...


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    ...

# resolve forward references for FastApi to be able to generate OpenAPI specification
Item.update_forward_refs()