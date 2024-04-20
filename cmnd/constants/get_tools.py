from .tools import tools

async def get_tools():
    tools_mapped = [
        {
            "name": tool["name"],
            "description": tool["description"],
            "jsonSchema": tool["parameters"],
            "isDangerous": tool["dangerous"],
            "functionType": tool["functionType"],
            "isLongRunningTool": tool["isLongRunningTool"],
            "rerun": tool["rerun"],
            "rerunWithDifferentParameters": tool["rerunWithDifferentParameters"],
        } for tool in tools
    ]
    return {"tools": tools_mapped}