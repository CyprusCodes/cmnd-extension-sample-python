import logging
from .tools import tools
from pydantic import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)

async def post_run_tool(tool_name: str, props: dict):
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

    try:
        result = await tool['runCmd'](**valid_props.dict())
        return result
    except TypeError as e:
        logging.error(f"Incorrect arguments provided for {tool_name}: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error executing tool {tool_name}: {str(e)}")
        raise
