from pydantic import BaseModel

class TodoSchema(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    priority: str = "Medium"

class UpdateTodoSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: str | None = None