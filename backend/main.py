from functools import lru_cache
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from uac_client import UacClient, UacConnectionError
from task_service import TaskService
from models import TaskInfoSchema

app = FastAPI(title="Stonebranch UAC Task API")

# CORS so frontend can call backend from another port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Fine for demo; tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def get_task_service() -> TaskService:
    """
    Create and cache TaskService – we don't want to recreate
    the UAC client for every request.
    """
    try:
        client = UacClient().get_client()
        return TaskService(client)
    except UacConnectionError as ex:
        raise RuntimeError(str(ex))
    
# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Stonebranch UAC backend is running.",
        "description": "Use the endpoints below to retrieve UAC tasks.",
        "endpoints": {
            "basic_tasks": "/api/tasks/basic",
            "advanced_tasks": "/api/tasks/advanced",
            "docs": "/docs",
        },
    }
# -------------------------------------------------------
# API ENDPOINTS
# -------------------------------------------------------

@app.get("/api/tasks/basic", response_model=List[TaskInfoSchema])
def list_tasks_basic(service: TaskService = Depends(get_task_service)):
    """
    Returns tasks using list_tasks (basic summary).
    Maps name and description only; agent/command are None.
    """
    try: # Fetch tasks from service
        tasks = service.fetch_tasks_basic()
        return [TaskInfoSchema.from_task_info(t) for t in tasks]
    except Exception as ex: # Handle errors appropriately
        raise HTTPException(status_code=500, detail=f"Error fetching basic tasks: {ex}")


@app.get("/api/tasks/advanced", response_model=List[TaskInfoSchema])
def list_tasks_advanced(service: TaskService = Depends(get_task_service)):
    """
    Returns tasks using list_tasks_advanced (detailed).

    Mapping:
      name -> Task Name
      summary/description -> Task Description
      agent or agentVar -> Agent Name
      command -> Command
    """
    try: # Fetch tasks from service
        tasks = service.fetch_tasks_advanced()
        return [TaskInfoSchema.from_task_info(t) for t in tasks]
    except Exception as ex: # Handle errors appropriately
        raise HTTPException(status_code=500, detail=f"Error fetching advanced tasks: {ex}")
