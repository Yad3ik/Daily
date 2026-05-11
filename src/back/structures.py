from pydantic import BaseModel, Field

class Task(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    is_complete: bool = Field(default=False)