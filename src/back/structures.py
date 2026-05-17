from datetime import date, time, datetime

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


class Event(BaseModel):
    id: str = Field(..., min_length=1)
    event_date: date
    start: time
    finish: time
    description: str = Field(..., min_length=1)
    tag: str | None = None
    color: str | None = None

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        ev = data['events']
        return cls(
            id=ev['id'],
            event_date=date.fromisoformat(data['date']),
            start=datetime.fromisoformat(ev['start']),
            finish=datetime.fromisoformat(ev['finish']),
            description=ev['description'],
            tag=ev.get('tag'),
            color=ev.get('color'),
        )
