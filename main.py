from http.client import HTTPException
from fastapi import  FastAPI,Header
from typing import Optional
from pydantic import BaseModel


app = FastAPI()




books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "price": 450
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "price": 500
    }
]




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
async def get_headers(accept: str = Header(None), content_type: str = Header(None), user_agent: str = Header(None),host:str=Header(None)):
    request_headers = {
        "accept": accept,

    }
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    return request_headers







# ---------------- Schema ----------------
class Book(BaseModel):
    title: str
    author: str
    price: int

# ---------------- CRUD APIs ----------------

# READ all books
@app.get("/books", response_model=List[dict])
async def get_books():
    return books

# READ single book
@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# CREATE book
@app.post("/books", status_code=201)
async def create_book(book: Book):
    new_id = books[-1]["id"] + 1 if books else 1
    new_book = {
        "id": new_id,
        **book.dict()
    }
    books.append(new_book)
    return new_book

# UPDATE book
@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = {"id": book_id, **updated_book.dict()}
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            deleted_book = books.pop(index)
            return {"message": "Book deleted", "book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")
