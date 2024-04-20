from fastapi import FastAPI
import uvicorn
from cmnd.constants.get_tools import get_tools
from cmnd.constants.run_tool import post_run_tool

app = FastAPI()

@app.get("/cmnd-tools")
async def read_cmnd_tools():
    return get_tools()

@app.post("/run-cmnd-tool")
async def run_cmnd_tool(tool_name: str, props: dict):
    return post_run_tool(tool_name, props)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
