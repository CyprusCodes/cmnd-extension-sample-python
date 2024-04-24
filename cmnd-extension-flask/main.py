from flask import Flask, request, jsonify, abort, Response
import json
from collections import OrderedDict
import os
from dotenv import load_dotenv
from tools import tools, product_finder, weather_from_location, file_reader

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/cmnd-tools", methods=['GET'])
def cmnd_tools_endpoint():
    tools_response = [
    OrderedDict([
        ("name", tool["name"]),
        ("description", tool["description"]),
        ("jsonSchema", tool["parameters"]),
        ("isDangerous", tool.get("isDangerous", False)),
        ("functionType", tool["functionType"]),
        ("rerun", tool["rerun"]),
        ("rerunWithDifferentParameters", tool["rerunWithDifferentParameters"]),
    ]) for tool in tools
    ]
    json_data = json.dumps({"tools": tools_response})

    response_data = Response(json_data, content_type="application/json")

    return response_data

@app.route("/run-cmnd-tool", methods=['POST'])
def run_cmnd_tool_endpoint():
    data = request.json
    tool_name = data.get('toolName')
    props = data.get('props', {})
    tool = next((t for t in tools if t['name'] == tool_name), None)
    if not tool:
        abort(404, description="Tool not found")
    try:
        result = tool["runCmd"](**props)
        return jsonify(result)
    except Exception as e:
        abort(500, description=str(e))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888, debug=True)
