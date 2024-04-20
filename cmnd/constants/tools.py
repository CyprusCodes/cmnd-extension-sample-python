from pydantic import BaseModel
from typing import List, Optional

# Define the Tool model with Pydantic for data validation
class Tool(BaseModel):
    name: str
    description: str
    parameters: dict
    dangerous: bool
    functionType: str
    isLongRunningTool: bool
    rerun: bool
    rerunWithDifferentParameters: bool

    async def run_cmd(self, props):
        # Placeholder for running command
        pass

# List of initialized Tool objects
tools = [
    # Initialize Tool objects here
]
