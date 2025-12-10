from fastapi import FastAPI
from typing import Annotated, Literal
from fastapi.params import Path,Query
from enum import Enum
from datetime import date

from pydantic import BaseModel, Field

app = FastAPI()


#pageNo is an optional query parameter with default value 1 and ignore any other query params
@app.get("/users/")
def get_users(pageNo:int=1):
    return {"users": f"List of users on page {pageNo}"}

#multiple query parameters
#name and age are mandatory query parameters
@app.get("/users/search/")
def search_users(
    name: Annotated[str,Query( title="Name of the user to search")],
    age: Annotated[int,Query( title="Age of the user to search", ge=1, le=120)],
):
    return {
        "name": name,
        "age": age,
        "results": f"Search results for users with name {name} and age {age}",
    }

#query params with some optional(city) and some mandatory
@app.get("/users/filter/")
def filter_users(      
    country: Annotated[str,Query( title="Country of the user to filter")],
    city: Annotated[str | None,Query( title="City of the user to filter")] = None,
):
    if city is None:
        return {
            "country": country,
            "results": f"Filtered users from country {country}",
        }
    return {
        "country": country,
        "city": city,
        "results": f"Filtered users from country {country} and city {city}",
    }   

#optional int query param with default value

@app.get("/users/paginate/")
def paginate_users(
    pageSize: Annotated[int | None,Query( title="Number of users per page", ge=1, le=100)] =None,
):
    if pageSize is None:
        pageSize = 10
    return {
        "page_size": pageSize,
        "results": f"List of users with page size {pageSize}",
    }

#query param as a pydantic model
class ProductSchemaForQueryParams(BaseModel):
    brand: str#mandatory
    color: str | None = None#optional
    price: float= Field(..., gt=0)#mandatory greater than 0
    storageSize:Literal["128gb","256gb","512gb","1tb"]="128gb"#mandatory with predefined values
    inStock: bool = True#optional with default value
    manufactureDate:date|None=None#optional date field
    

@app.get("/products/search/")
def search_products(
    productDetails: Annotated[ProductSchemaForQueryParams,Query( title="Details of the product to search")],
):
    return {
        "product_details": productDetails,
        "results": f"Search results for products with details {productDetails}",
    }



    