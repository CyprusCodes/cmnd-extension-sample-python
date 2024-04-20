from flask import Flask, request, jsonify
from cmnd.constants.get_tools import get_tools
from cmnd.constants.run_tools import post_run_tool

app = Flask(__name__)

@app.route("/cmnd-tools", methods=["GET"])
def cmnd_tools_endpoint():
    tools = get_tools()
    return jsonify(tools)

@app.route("/run-cmnd-tool", methods=["POST"])
def run_cmnd_tool_endpoint():
    try:
        request_data = request.json
        tool_name = request_data.get('toolName')
        props = request_data.get('props', {})

        if not tool_name:
            raise ValueError("Tool name is required")

        result = post_run_tool(tool_name, props)
        return jsonify({"result": result})
    except ValueError as ve:
        return jsonify({"detail": str(ve)}), 400
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5222, debug=True)
