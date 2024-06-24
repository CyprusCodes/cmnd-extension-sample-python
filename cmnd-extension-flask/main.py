from flask import Flask, request, jsonify, abort
import os
from dotenv import load_dotenv
from flask_cors import CORS
from tools import tools

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
            "rerun": tool["rerun"],
            "rerunWithDifferentParameters": tool["rerunWithDifferentParameters"],
        } for tool in tools
    ]
    return jsonify({"tools": tools_response})

@app.route("/run-cmnd-tool", methods=['POST'])
def run_cmnd_tool_endpoint():
    data = request.json
    tool_name = data.get('toolName')
    props = data.get('props', {})
    tool = next((t for t in tools if t['name'] == tool_name), None)
    if not tool:
        abort(404, description="Tool not found")
    try:
        conversation_id = props.pop("conversationId", None)
        chatbot_conversation_id = props.pop("chatbotConversationId", None)
        result = tool["runCmd"](conversationId=conversation_id, chatbotConversationId=chatbot_conversation_id, **props)
        return jsonify(result)
    except Exception as e:
        abort(500, description=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
