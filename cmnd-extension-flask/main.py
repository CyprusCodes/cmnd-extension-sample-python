from flask import Flask, request, jsonify, abort
import os
from dotenv import load_dotenv
from flask_cors import CORS
from tools import tools
import traceback
from inspect import signature

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/cmnd-tools", methods=['GET'])
def cmnd_tools_endpoint():
    tools_response = [
        {
            "name": tool["name"],
            "description": tool["description"],
            "jsonSchema": tool["parameters"],
            "isDangerous": tool.get("isDangerous", False),
            "functionType": tool["functionType"],
            "isLongRunningTool": tool.get("isLongRunningTool", False),
            "postCallPrompt": tool.get("postCallPrompt"),
            "rerun": tool["rerun"],
            "prerequisites": tool.get("prerequisites"),
        } for tool in tools
    ]
    return jsonify({"tools": tools_response})

@app.route("/run-cmnd-tool", methods=['POST'])
def run_cmnd_tool_endpoint():
    try:
        data = request.json
        tool_name = data.get('toolName')
        props = data.get('props', {})
        memory = data.get('memory')
        tool = next((t for t in tools if t['name'] == tool_name), None)
        if not tool:
            abort(404, description="Tool not found")
        
        props.pop("conversationId", None)
        props.pop("chatbotConversationId", None)
        
        run_cmd_params = signature(tool["runCmd"]).parameters
        
        if 'memory' in run_cmd_params:
            result = tool["runCmd"](**props, memory=memory)
        else:
            result = tool["runCmd"](**props)
        
        return jsonify(result)
    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details)
        abort(500, description=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
