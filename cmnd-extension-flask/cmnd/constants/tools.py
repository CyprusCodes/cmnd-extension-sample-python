import requests
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

# Function definitions
def run_product_finder(product):
    url = f"https://dummyjson.com/products/search?q={quote(product)}"
    try:
        response = requests.get(url)
        return json.dumps(response.json())
    except requests.RequestException as error:
        return f"Error trying to execute the tool: {str(error)}"

def run_weather_from_location(city):
    api_key = "8f0eec2086ed5576e96eaf5ab22c889e"
    encoded_city = quote(city)  # Encoding the city to ensure it's URL-safe

    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&units=metric&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return json.dumps({"error": "API call failed", "status_code": response.status_code, "message": response.json().get('message', 'No error message provided')})
        return json.dumps(response.json())
    except requests.RequestException as error:
        return json.dumps({"error": f"HTTP error occurred: {str(error)}"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occurred: {str(e)}"})

def run_json_file_reader(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return json.dumps(data)
    except Exception as error:
        return f"An error occurred while reading the file: {str(error)}"

# Tool definitions with direct Pydantic model references for parameter validation
tools = [
    {
        "name": "product_finder",
        "description": "Finds and returns dummy product details based on the product name passed to it",
        "parameters": GetProductSchema,
        "runCmd": run_product_finder
    },
    {
        "name": "city_weather_data",
        "description": "Gets the weather details from a given city name",
        "parameters": WeatherCitySchema,
        "runCmd": run_weather_from_location
    },
    {
        "name": "json_file_reader",
        "description": "Reads JSON file content",
        "parameters": GetFilePathSchema,
        "runCmd": run_json_file_reader
    }
]
