from pydantic import BaseModel
from typing import List

class Output(BaseModel):
    criteria: List[str]
