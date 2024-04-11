from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Action(BaseModel):
    name: str = Field(description="ToolsOrFunctions")
    args: Optional[Dict[str, Any]] = Field(description="ToolsOrFunctions Params, with fields and values")
