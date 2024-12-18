from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=2000, lt=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2024,
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2024),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2024),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A very nice book!', 5, 2023),
    Book(4, 'HP1', 'codingwithroby', 'A very nice book!', 2, 2022),
    Book(5, 'HP2', 'codingwithroby', 'A very nice book!', 3, 2024),
    Book(6, 'HP3', 'codingwithroby', 'A very nice book!', 1, 2023),
]

@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get('/books/{book_id}')
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

@app.get('/books/')
async def read_book_by_rating(book_rating: int=Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get('/books/by/published_date/')
async def select_book_by_published_date(published_date: int=Query(gt=2000, lt=2025)):
    books_to_return = list(filter(lambda book: book.published_date == published_date, BOOKS))
    return books_to_return

@app.post('/create-book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put('/books/update_book')
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

@app.delete('/book/{book_id}')
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')