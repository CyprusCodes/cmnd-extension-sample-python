import json
import asyncio
from inspect import signature
from tools import tools

def handler(event, context):
    try:
        path = event.get('path')
        http_method = event.get('httpMethod')

        if path == "/cmnd-tools" and http_method == "GET":
            return get_tools(event, context)

        if path == "/run-cmnd-tool" and http_method == "POST":
            return run_cmnd_tool(event, context)

        # Default response for unsupported paths/methods
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Endpoint not found"}),
            "headers": {"Content-Type": "application/json"}
        }
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
            "headers": {"Content-Type": "application/json"}
        }

def get_tools(event, context):
    tools_response = [
        {
            "name": tool["name"],
            "description": tool["description"],
            "jsonSchema": tool["parameters"],
            "isDangerous": tool.get("isDangerous", False),
            "functionType": tool["functionType"],
            "isLongRunningTool": tool.get("isLongRunningTool", False),
            "postCallPrompt": tool.get("postCallPrompt"),
            "prerequisites": tool.get("prerequisites"),
            "rerun": tool["rerun"],
        } for tool in tools
    ]
    return {
        "statusCode": 200,
        "body": json.dumps({"tools": tools_response}),
        "headers": {"Content-Type": "application/json"}
    }

def run_cmnd_tool(event, context):
    try:
        body = json.loads(event['body'])
        tool_name = body.get('toolName')
        props = body.get('props', {})
        memory = body.get('memory')
        
        tool = next((t for t in tools if t['name'] == tool_name), None)
        if not tool:
            return {
                "statusCode": 404,
                "body": json.dumps({"detail": "Tool not found"}),
                "headers": {"Content-Type": "application/json"}
            }

        conversation_id = props.pop("conversationId", None)
        chatbot_conversation_id = props.pop("chatbotConversationId", None)
        organization_id = props.pop("organizationId", None)

        run_cmd_params = signature(tool["runCmd"]).parameters

        if 'memory' in run_cmd_params:
            result = asyncio.run(tool["runCmd"](**props, memory=memory))
        else:
            result = asyncio.run(tool["runCmd"](**props))
        
        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"detail": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
