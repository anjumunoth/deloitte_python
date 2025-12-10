from fastapi import FastAPI
import httpx
import asyncio
from typing import Annotated
from fastapi.params import Path
from enum import Enum

app = FastAPI()

@app.get("/products/allProducts")
def get_products():
    return {"products":"All Products"}


@app.get("/products/{prodId}")
def get_products(prodId: Annotated[int,Path( title="The ID of the product to get", ge=1, le=1000)]):
    return {"product_id": prodId, "name": f"Product {prodId}", "price": prodId * 10}

@app.get("/products")
def get_products():
    return {"products": "List of all products"}


#multiple path parameters
@app.get("/products/{prodId}/category/{categoryType}")
def get_product_category(
    prodId: Annotated[int,Path( title="The ID of the product to get", ge=1, le=1000)],
    categoryType: Annotated[str,Path( description="CategoryType should consist only of alphabets",title="The category type of the product",regex="^[a-zA-Z]+$",example="electronics")],
):
    return {
        "product_id": prodId,
        "category": categoryType,
        "details": f"Details of product {prodId} in category {categoryType}",
    }

#path parameter with only a set of values allowed
@app.get("/orders/{orderStatus}")
def get_orders(
    orderStatus: Annotated[str,Path( title="The status of the order",regex="^(pending|shipped|delivered|canceled)$")],
):
    return {
        "order_status": orderStatus,
        "orders": f"List of orders with status {orderStatus}",
    }


#predefined path
class PriceCategory(str,Enum):
    BUDGET = "budget"
    MIDRANGE = "midrange"
    PREMIUM = "premium"

@app.get("/products/priceCategory/{priceCategory}")
def get_products_by_price_category(
    #priceCategory: PriceCategory,
    priceCategory: Annotated[PriceCategory,Path(title="The price category of the products")],

):
    if priceCategory == PriceCategory.BUDGET:
        return {"category": priceCategory, "products": "List of budget products"}
    elif priceCategory == PriceCategory.MIDRANGE:
        return {"category": priceCategory, "products": "List of midrange products"} 
    else:
        return {"category": priceCategory, "products": "List of premium products"}
    

