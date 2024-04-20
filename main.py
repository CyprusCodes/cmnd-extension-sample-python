# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from cmnd.constants.get_tools import get_tools
from cmnd.constants.run_tools import post_run_tool

app = FastAPI()

@app.get("/cmnd-tools")
async def cmnd_tools_endpoint():
    tools = await get_tools()
    return JSONResponse(content={"tools": tools})

@app.post("/run-cmnd-tool")
async def run_cmnd_tool_endpoint(request: Request):
    try:
        request_data = await request.json()
    except Exception as e:
        return JSONResponse(content={"error": f"Invalid JSON data: {str(e)}"}, status_code=400)

    tool_name = request_data.get('toolName')
    props = request_data.get('props', {})

    if tool_name != "city_weather_data" or 'city' not in props:
        return JSONResponse(content={"error": "Missing or incorrect toolName or props."}, status_code=400)

    city = props['city']  # Directly extracting the city value
    if not isinstance(city, str):
        return JSONResponse(content={"error": "City must be a string."}, status_code=400)

    try:
        result = await post_run_tool(tool_name, {'city': city})  # Pass the corrected city value
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5111)
