import os
from pydantic import BaseModel, Field
import httpx

class ProductFinderSchema(BaseModel):
    product_name: str = Field(..., title="Product Name", description="The name of the product to find details for")

class PutUsernameSchema(BaseModel):
    username: str = Field(..., title="Username", description="The username to get details for")

class EchoUsernameSchema(BaseModel):
    pass

class SayHelloSchema(BaseModel):
    pass


# an example of a simple tool that returns the weather details of a city
async def product_finder(product_name: str):
    url = f"https://dummyjson.com/products/search?q={product_name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()   

# an example of a tool that uses the CMND's memory object feature to store some data
async def put_username(username: str, memory:dict):
    memory['username'] = username
    return {
        "responseString": f"Username {username} has been saved to memory",
        "memory": memory
    }

# an example of a tool that uses the CMND's memory object feature to retrive some data
async def echo_username(memory:dict):
    username = memory.get('username')
    if not username:
        return {
            "responseString": "No username has been found in the memory"
        }
    return {
        "responseString": f"The username found in memory is {username}"
    }

async def say_hello():
    return "Hello World!"

# DON'T TOUCH THIS FUNCTION FOR ANY REASON
def custom_json_schema(model):
    schema = model.schema()
    properties_formatted = {
        k: {
            "title": v.get("title"),
            "type": v.get("type")
        } for k, v in schema["properties"].items()
    }

    return {
        "type": "object",
        "default": {},
        "properties": properties_formatted,
        "required": schema.get("required", [])
    }

tools = [
    {
        "name": "product_finder",
        "description": "Finds and returns dummy products details based on the product name passed to it",
        "parameters": custom_json_schema(ProductFinderSchema),
        "runCmd": product_finder,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "prerequisites": [],
        "rerun": "disabled"
    },
    {
        "name": "put_username",
        "description": "saves the username to the memory",
        "parameters": custom_json_schema(PutUsernameSchema),
        "runCmd": put_username,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": "allowed",
        "prerequisites": [],

    },
    {
        "name": "echo_username",
        "description": "echos the username saved in the memory",
        "parameters": custom_json_schema(EchoUsernameSchema),
        "runCmd": echo_username,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": "allowedWithDifferentParams",
        "prerequisites": [],
    }
]
