from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from cmnd.constants.get_tools import get_tools
from cmnd.constants.run_tools import post_run_tool

app = FastAPI()

@app.get("/cmnd-tools")
async def cmnd_tools_endpoint():
    tools = await get_tools()
    return JSONResponse(content=tools)

@app.post("/run-cmnd-tool")
async def run_cmnd_tool_endpoint(request: Request):
    try:
        request_data = await request.json()
        tool_name = request_data.get('toolName')
        props = request_data.get('props', {})
        
        if not tool_name:
            raise ValueError("Tool name is required")
        
        result = await post_run_tool(tool_name, props)
        return JSONResponse(content={"result": result})
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5111)
