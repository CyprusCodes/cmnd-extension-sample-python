from .tools import tools

async def post_run_tool(tool_name, props):
    tool_to_run = next((tool for tool in tools if tool.name == tool_name), None)
    if tool_to_run:
        results = await tool_to_run.run_cmd(props)
        return {'tool result': results}
    else:
        return {'error': 'Tool not found'}
