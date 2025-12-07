from typing import List
from models import TaskInfo


class TaskService:
    """
    Service for extracting exactly the required fields:
    - Task Name     -> name
    - Task Description -> description or summary
    - Agent Name    -> agent
    - Command       -> command
    """

    def __init__(self, uac_client):
        self.uac = uac_client

    # -------------------------------------------------------
    # BASIC API: list_tasks()
    # -------------------------------------------------------
    def fetch_tasks_basic(self) -> List[TaskInfo]:
        payload = {
            "name": "*",
            "type": "",
            "updatedTimeType": "Offset",
            "updatedTime": "-30d",
        }

        try:
            response = self.uac.tasks.list_tasks(payload=payload)
        except Exception as ex:
            raise RuntimeError(f"Failed to retrieve tasks (basic): {ex}")

        raw_tasks = response if isinstance(response, list) else response.get("data", [])

        results = []

        for t in raw_tasks:
            name = t.get("name")
            description = t.get("description") or t.get("summary")
            agent = t.get("agent")           
            command = t.get("command")       

            results.append(
                TaskInfo(
                    name=name,
                    description=description,
                    agent=agent,
                    command=command,
                )
            )

        return results

    # -------------------------------------------------------
    # ADVANCED API: list_tasks_advanced()
    # -------------------------------------------------------
    def fetch_tasks_advanced(self) -> List[TaskInfo]:
        try:
            response = self.uac.tasks.list_tasks_advanced()
        except Exception as ex:
            raise RuntimeError(f"Failed to retrieve tasks (advanced): {ex}")

        raw_tasks = response if isinstance(response, list) else response.get("data", [])

        results = []

        for t in raw_tasks:
            name = t.get("name")
            description = t.get("description") or t.get("summary")
            agent = t.get("agent")          
            command = t.get("command")       

            results.append(
                TaskInfo(
                    name=name,
                    description=description,
                    agent=agent,
                    command=command,
                )
            )

        return results
