from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel


@dataclass
class TaskInfo:
    """
    Internal representation of a UAC Task.
    Used by the service layer.
    """
    name: str
    description: Optional[str]
    agent: Optional[str]
    command: Optional[str]


class TaskInfoSchema(BaseModel):
    """
    Schema used for JSON responses.
    """
    name: str
    description: Optional[str] = None
    agent: Optional[str] = None
    command: Optional[str] = None

    @classmethod
    def from_task_info(cls, task: TaskInfo) -> "TaskInfoSchema":
        return cls(
            name=task.name,
            description=task.description,
            agent=task.agent,
            command=task.command,
        )
