# Assuming post_run_tool is meant to delegate to the specific tool functions
from .tools import tools

async def post_run_tool(tool_name: str, props: dict):
    tool_to_run = next((tool for tool in tools if tool["name"] == tool_name), None)
    if not tool_to_run:
        return "Tool not found"

    try:
        if tool_name == "city_weather_data":
            # Ensure that we pass only the city name
            city = props['city']
            return await tool_to_run["runCmd"](city)
    except Exception as e:
        return str(e)
import logging
from .tools import run_weather_from_location, run_product_finder, run_json_file_reader

# Configure logging
logging.basicConfig(level=logging.INFO)

async def post_run_tool(tool_name: str, props: dict):
    # Mapping tool names to their corresponding functions
    tool_mapping = {
        "city_weather_data": run_weather_from_location,
        "product_finder": run_product_finder,
        "json_file_reader": run_json_file_reader
    }

    tool_function = tool_mapping.get(tool_name)
    if not tool_function:
        logging.error(f"Tool not found: {tool_name}")
        return {"error": "Tool not found"}

    try:
        # Validate properties based on tool requirements
        if tool_name == "city_weather_data" and 'city' not in props:
            logging.error("Missing city parameter for weather data tool")
            return {"error": "Missing city parameter"}

        # Dynamically call the appropriate function with **props if valid
        result = await tool_function(**props)
        logging.info(f"Successfully executed tool {tool_name}")
        return result
    except TypeError as e:
        # Catching errors related to incorrect function arguments or missing expected keys in props
        logging.error(f"Incorrect arguments provided for {tool_name}: {str(e)}")
        return {"error": f"Incorrect arguments: {str(e)}"}
    except Exception as e:
        # General exception handling
        logging.error(f"Error executing tool {tool_name}: {str(e)}")
        return {"error": str(e)}

