from fastapi import FastAPI, HTTPException
from typing import Annotated, List, Literal
from fastapi.params import Body, Path,Query
from enum import Enum
from datetime import date

from pydantic import BaseModel, Field,field_validator,model_validator

app = FastAPI()

class Users(BaseModel):
    name:str
    email:str
    # @model_validator(mode="after")
    # def validate_email(values):
    #     #name should be there in the email id before @
    #     print(values)
    #     name= values['name']
    #     v= values['email']
    #     if name and name.replace(" ","").lower() not in v.split("@")[0].lower():
    #         raise ValueError("Email id should contain the name of the user" )
    #     return values

class GenreCategory(str,Enum):
    fiction = "fiction"
    nonfiction = "non-fiction"
    science = "science"
    biography="biography"
    history = "history"
    fantasy="fantasy"


registeredUsers: List[Users] = [
    Users(name="John", email="johnDoe@gmail.com"),
    Users(name="Jane", email="janeSmith@gmail.com"),
    Users(name="Alice", email="aliceJohnson@gmail.com")]
    

class IsbnSchema(BaseModel):
    isbn: str = Field(..., min_length=10, max_length=13)

today=date.today()
class Books(IsbnSchema):
    title: str
    authors: List[Users]
    price:int= Field(..., gt=0)
    inStock: bool = True    
    dateOfPublication: date|None=Field(...,lt=today)
    genre: GenreCategory=GenreCategory.fiction
    @field_validator('authors')
    def validate_authors(cls, v):
        if not v:
            raise ValueError('At least one author is required')
        for author in v:
            if not len(author.name)>0 or not len(author.email)>0:
                # [{name:"",email:""}] should raise error
                raise ValueError('Each author must have a non empty name and non empty email')
            # userexists =  [user for user in registeredUsers if user.name.lower() == author.name.lower()]
            # if not userexists:
            #     raise ValueError('Author is not a registered user')
        return v    

          

books=[]
books: List[Books] = [
    Books(
        title="Clean Code",
        authors=[Users(name="Robert C. Martin", email="unclebob@example.com")],
        price=500,
        inStock=True,
        dateOfPublication=date(2008, 8, 1),
        genre="non-fiction",
        isbn="9780132350884"
    ),
    Books(
        title="Fluent Python",
        authors=[Users(name="Luciano Ramalho", email="luciano@example.com")],
        price=750,
        inStock=True,
        dateOfPublication=date(2015, 8, 20),
        genre="science",
        isbn="9781491946008"
    ),
    Books(
        title="Designing Data-Intensive Applications",
        authors=[Users(name="Martin Kleppmann", email="martin@example.com")],
        price=900,
        inStock=False,
        dateOfPublication=date(2017, 3, 16),
        genre="non-fiction",
        isbn="9781449373320"
    )
]


@app.delete("/books/{isbn}")
def delete_book(
    isbn: Annotated[
        str, Path(title = "Book to delete",
                  desc = "10-13 characters",
                  min_length=10,
                  max_length=13,)
    ]
):     
    #delete book with given isbn
    for index, book in enumerate(books):
        if book.isbn == isbn:
            del books[index]
            return {"detail": f"Book with {isbn} deleted successfully"}
    raise HTTPException(
        status_code = 404,
        detail = f"Book with {isbn} not found"
    )    
    

@app.put("/books/{searchIsbn}")
def update_book(
    searchIsbn: Annotated[
        str,
        Path(
            title="The ISBN of the book to update",
            description="ISBN should be between 10 and 13 characters",
            min_length=10,
            max_length=13,
        ),
    ],
    newPrice: Annotated[int,Body(gt=0) ] ):
        for book in books:
            if book.isbn == searchIsbn:
                book.price = newPrice
                return book
        raise HTTPException(status_code=404, detail=f"Book not found with ISBN {searchIsbn}")

@app.get("/books/")
def get_books():
    return books

@app.get("/books/filter/genre/", response_model=List[Books])
def get_filtered_books(
    genre : Annotated[
        GenreCategory,
        Query(title="Genre books")
    ]
):
    """
    Docstring for get_filtered_books
    
    :param genre: Description
    :type genre: Annotated[GenreCategory, Query(title="Genre books")]
    will throw 422 error if genre not in predefined set
    :return: List of books filtered by genre
    will throw 404 error if no books found for the genre
    """
    filtered_books = [book for book in books if book.genre.lower() == genre.lower()]
    
    if not filtered_books: 
        raise HTTPException(status_code=404, detail=f"No books found for genre {genre}")
    
    return filtered_books


@app.get("/books/filter/", response_model=List[Books])
def filter_books(
    price: Annotated[int | None, Query(title="Maximum price of the books to filter", gt=0)] = None,
    author: Annotated[str | None, Query(title="Author name to filter books by")] = None,
    dateOfPublication: Annotated[date | None, Query(title="Publication date to filter books by")] = None,
):
    filtered_books = books

    if price is not None:
        filtered_books = [book for book in filtered_books if book.price <= price]

    if author is not None:
        filtered_books = [
            book
            for book in filtered_books
            if any(author.lower() in a.name.lower() for a in book.authors)
        ]

    if dateOfPublication is not None:
        filtered_books = [
            book
            for book in filtered_books
            if book.dateOfPublication == dateOfPublication
        ]

    if not filtered_books:
        raise HTTPException(
            status_code=404, detail="No books found matching the criteria"
        )

    return filtered_books
        

@app.get("/books/sort/")
def sort_books(
    sortField: str = Query(..., description="Field to sort by (any Books attribute)"),
    sortOrder: str = Query(Literal["asc","desc"], description="Sort order: asc or desc")
):
    # Get all possible attribute names from the Pydantic model
    valid_fields = Books.model_fields.keys()
    if sortField not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sortField: {sortField}")

    reverse = sortOrder.lower() == "desc"

    try:
        sorted_books = sorted(
            books,
            key=lambda book: getattr(book, sortField) if getattr(book, sortField) is not None else "",
            reverse=reverse
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Sorting failed due to invalid field or un-sortable values")

    if not sorted_books:
        raise HTTPException(status_code=404, detail="No books to sort")
    return sorted_books
    
 
@app.get("/books/{isbn}",response_model=Books)
def get_book_by_isbn(
    isbn: Annotated[
        str,
        Path(
            title="The ISBN of the book to get",
            description="ISBN should be between 10 and 13 characters",
            min_length=10,
            max_length=13,
        ),
    ],
):
    
    for book in books:
        if book.isbn == isbn:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/", response_model=Books, status_code=201)
def add_book(book: Books):
    # Check if a book with the same ISBN already exists
    for existing_book in books:
        if existing_book.isbn == book.isbn:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    books.append(book)
    return book 


