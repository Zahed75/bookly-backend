from fastapi import  FastAPI,Header
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}



@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0):
    return {
        "message": f"Hello, {name}",
        "age": age
    }



class BookCreateModel(BaseModel):
    title: str
    author: str
    description: Optional[str] = None


@app.post('/create_book')
async def create_book(book: BookCreateModel):
    return {
        "title": book.title,
        "author": book.author,
        "description": book.description
    }


@app.get("/get_headers")
async def get_headers(accept: str = Header(None), content_type: str = Header(None)):
    request_headers = {
        "accept": accept,

    }
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    return request_headers