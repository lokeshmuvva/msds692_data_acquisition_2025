
from fastapi import FastAPI

# 1. Create a FastAPI App Instance
app = FastAPI()

# 2. Define a function and associate with a route.


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item_w_path_param(item_id: int):
    return {"item_id": item_id}


@app.get("/items/")
def read_item_w_query_param(item_id: int | None = None, ct: int = 0):
    return {"item_id": item_id, "count": ct}


# TODO: CREATE /name route and return {"name": val}

@app.get("/")
def intro():
    return {"message": "hello"}


@app.get("/hello")
def custom_intro(name: str | None = None):
    if name:
        return {"message": f"Hello {name}"}
    return {"message": "Hello nobody"}

# requests.get("url/hello?name=Lokesh")
# requests.get("url/hello", params={"name":"Lokesh"})


@app.get("/hello/{name}")
def custom_intro_w(name: str):
    return {"message": f"Hello {name}"}

# requests.get("url/hello/Lokesh")
