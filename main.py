from fastapi import FastAPI
import sys
import datetime

dic_items = {} # Need to put it into a database


sys.path.append('./src/')

from pydantic import BaseModel

class Item(BaseModel): #Define the schema of the input
    name: str
    Category: str
    cost: float
    description: str 
    date: datetime.date
    tax_deductable: bool 


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "optional operations: /items; /deductable_items; /group_by_category"}  

@app.post("/items")
async def create_item(item: Item):
    id = item.name + str(item.date) +str(item.cost)
    dic_items[id] = item
    return(dic_items)

@app.get("/deductable_items")
async def get_deductable():
    deductable_items = {}
    for key, value in dic_items.items():
        if value.tax_deductable == True:
            deductable_items[key] = value
    return(deductable_items)

@app.get("/group_by_category")
async def get_category():
    category_items = {}
    for key, value in dic_items.items():
        if value.Category in category_items:
            category_items[value.Category].append(value)
        else:
            category_items[value.Category] = [value]
    return(category_items)
