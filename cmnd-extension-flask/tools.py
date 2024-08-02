import os
from pydantic import BaseModel, Field
import requests


class ProductFinderSchema(BaseModel):
    product_name: str = Field(..., title="Product Name", description="Product name required")

class PutUsernameSchema(BaseModel):
    username: str = Field(..., title="Username", description="The username to get details for")

class EchoUsernameSchema(BaseModel):
    pass


# an example of a simple tool that returns the weather details of a city
def product_finder(product_name: str):
    url = f"https://dummyjson.com/products/search?q={product_name}"
    response = requests.get(url)
    return response.json()


# an example of a tool that uses the CMND's memory object feature to store some data
def put_username(username: str, memory:dict):
    memory['username'] = username
    return {
        "responseString": f"Username {username} has been saved to memory",
        "memory": memory
    }

# an example of a tool that uses the CMND's memory object feature to retrive some data
def echo_username(memory:dict):
    username = memory.get('username')
    if not username:
        return {
            "responseString": "No username has been found in the memory"
        }
    return {
        "responseString": f"The username found in memory is {username}"
    }


# DONT TOUCH THIS FUNCTION FOR ANY REASON
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
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "put_username",
        "description": "saves the username to the memory",
        "parameters": custom_json_schema(PutUsernameSchema),
        "runCmd": put_username,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "echo_username",
        "description": "echos the username saved in the memory",
        "parameters": custom_json_schema(EchoUsernameSchema),
        "runCmd": echo_username,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
