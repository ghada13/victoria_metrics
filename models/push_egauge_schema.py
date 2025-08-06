from pydantic import BaseModel
from typing import List

class Register(BaseModel):
    name: str
    type: str  # or just str if it's not always "V"
    did: int

class Range(BaseModel):
    ts: int
    delta: float
    rows: List[List[str]]  # Strings that will likely need to be casted to float/int

class BulkPushRequest(BaseModel):
    registers: List[Register]
    ranges: List[Range]
