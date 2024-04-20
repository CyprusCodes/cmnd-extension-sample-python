from .tools import tools

async def get_tools():
    tools_info = []
    for tool in tools:
        tool_data = {
            "name": tool["name"],
            "description": tool["description"],
            # Use the Pydantic model's .schema() method to serialize its schema to JSON, if needed
            "parameters": tool["parameters"].schema() if hasattr(tool["parameters"], 'schema') else {}
        }
        tools_info.append(tool_data)
    return {"tools": tools_info}
