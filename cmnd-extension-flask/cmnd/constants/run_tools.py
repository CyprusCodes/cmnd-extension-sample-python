import logging
from .tools import tools
from pydantic import ValidationError
import requests  # replacing httpx for synchronous operations

# Configure logging
logging.basicConfig(level=logging.INFO)

def run_tool_command(tool_function, props):
    try:
        response = tool_function(**props)
        return response
    except Exception as e:
        logging.error(f"Error executing tool: {str(e)}")
        raise

def post_run_tool(tool_name: str, props: dict):
    tool = next((t for t in tools if t['name'] == tool_name), None)
    if not tool:
        raise ValueError(f"Tool {tool_name} not found")

    model = tool['parameters']  # Getting the Pydantic class
    try:
        # Validate props with Pydantic model
        valid_props = model(**props)
    except ValidationError as ve:
        logging.error(f"Validation error for {tool_name}: {str(ve)}")
        raise ValueError(f"Parameter validation failed: {str(ve)}")

    # Run the tool's command synchronously
    return run_tool_command(tool['runCmd'], valid_props.dict())
