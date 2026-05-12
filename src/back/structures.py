from pydantic import BaseModel, Field

class Task(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    is_complete: bool = Field(default=False)

    def to_dict(self) -> dict:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(id=data["id"], name=data["name"], is_complete=data["is_complete"])
