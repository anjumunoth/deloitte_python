from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}  # dict 



# request headers, response haeders, status code -- not setup
# response -- dict in python
# REST api -- content type -- json
#run with: uvicorn firstProject.main:app --reload
# fast api automatically converts dict to json response with 200 response code and content type

itemsArr:list=[]
#


@app.get("/items/{prod_id}") #path definition decorator
def read_item(prod_id: int):
    for i in range (len(itemsArr)):
        if itemsArr[i]['prod_id']==prod_id:
            return itemsArr[i]
    return {"prod_id": prod_id} 



@app.post("/items/")
def create_item(item: dict):# data in request body is converted to dict and stored in item
    itemsArr.append(item)
    return item
# POST request with body

#kebab case python prod_id
#json camel case prodId