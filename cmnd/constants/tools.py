import httpx
import json
from pydantic import BaseModel, Field
from urllib.parse import quote

# Pydantic models for validation
class NoParamsSchema(BaseModel):
    pass

class WeatherCitySchema(BaseModel):
    city: str = Field(..., description="City name required")

class GetProductSchema(BaseModel):
    product: str = Field(..., description="Product name required")

class GetFilePathSchema(BaseModel):
    filePath: str = Field(..., description="File path required")

# Function to convert Pydantic models to JSON schema
def pydantic_to_json_schema(model_class):
    return model_class.schema()

# Generating JSON schema from Pydantic models
no_params_json_schema = pydantic_to_json_schema(NoParamsSchema)
weather_city_json_schema = pydantic_to_json_schema(WeatherCitySchema)
get_products_json_schema = pydantic_to_json_schema(GetProductSchema)
get_file_path_json_schema = pydantic_to_json_schema(GetFilePathSchema)

# Function definitions
async def run_product_finder(product):
    url = f"https://dummyjson.com/products/search?q={httpx.utils.quote(product)}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return json.dumps(response.json())
        except httpx.HTTPError as error:
            return f"Error trying to execute the tool: {str(error)}"

async def run_weather_from_location(city):
    api_key = "8f0eec2086ed5576e96eaf5ab22c889e"
    print(f"Original city: {city}")  # Print the original city name received
    encoded_city = quote(city)  # Encoding the city to ensure it's URL-safe
    print(f"Encoded city: {encoded_city}")  # Print the encoded city name

    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&units=metric&appid={api_key}"
    print(f"Request URL: {url}")  # Print the final URL to be requested

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                return json.dumps({"error": "API call failed", "status_code": response.status_code, "message": response.json().get('message', 'No error message provided')})
            return json.dumps(response.json())
        except httpx.HTTPError as error:
            return json.dumps({"error": f"HTTP error occurred: {str(error)}"})
        except Exception as e:
            return json.dumps({"error": f"An unexpected error occurred: {str(e)}"})

def run_json_file_reader(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return json.dumps(data)
    except Exception as error:
        return f"An error occurred while looking for the file content: {str(error)}"

# Tool definitions
PRODUCT_FINDER = {
    "name": "product_finder",
    "description": "Finds and returns dummy product details based on the product name passed to it",
    "category": "communication",
    "subcategory": "hackathon",
    "functionType": "backend",
    "dangerous": False,
    "associatedCommands": [],
    "prerequisites": [],
    "parameters": get_products_json_schema,
    "rerun": True,
    "rerunWithDifferentParameters": True,
    "isLongRunningTool": False,
    "runCmd": run_product_finder
}

WEATHER_FROM_LOCATION = {
    "name": "city_weather_data",
    "description": "Gets the weather details from a given city name",
    "category": "communication",
    "subcategory": "hackathon",
    "functionType": "backend",
    "dangerous": False,
    "associatedCommands": [],
    "prerequisites": [],
    "parameters": weather_city_json_schema,
    "rerun": True,
    "rerunWithDifferentParameters": True,
    "isLongRunningTool": False,
    "runCmd": run_weather_from_location
}

JSON_FILE_READER = {
    "name": "json_file_reader",
    "description": "Gets the contents of the file given a filepath in the repository",
    "category": "communication",
    "subcategory": "hackathon",
    "functionType": "backend",
    "dangerous": False,
    "associatedCommands": [],
    "prerequisites": [],
    "parameters": get_file_path_json_schema,
    "rerun": True,
    "rerunWithDifferentParameters": True,
    "isLongRunningTool": False,
    "runCmd": run_json_file_reader
}

tools = [JSON_FILE_READER, PRODUCT_FINDER, WEATHER_FROM_LOCATION]
