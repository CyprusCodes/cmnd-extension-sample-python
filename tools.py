from pydantic import BaseModel, Field
import httpx

class ProductFinderSchema(BaseModel):
    product_name: str = Field(..., title="Product Name", description="The name of the product to find details for")

class PutUsernameSchema(BaseModel):
    username: str = Field(..., title="Username", description="The username to get details for")

class EchoUsernameSchema(BaseModel):
    pass

class GetPhoneNumberSchema(BaseModel):
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

# an example of a tool that uses the context CMND passes to every tool call
# senderPhoneNumber is only set on WhatsApp; turn on "require phone number" on the
# chatbot so it is always known
async def get_phone_number(context: dict):
    phone_number = context.get('senderPhoneNumber')
    if not phone_number:
        return {
            "responseString": "The user's phone number is not available"
        }
    return {
        "responseString": f"The user's phone number is {phone_number}"
    }

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
    },
    {
        "name": "get_phone_number",
        "description": "gets the phone number of the user the assistant is talking to",
        "parameters": custom_json_schema(GetPhoneNumberSchema),
        "runCmd": get_phone_number,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": "allowed",
        "prerequisites": [],
    }
]