import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate


async def initialize_database(max_attempts: int = 15) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except SQLAlchemyError:
            if attempt == max_attempts:
                raise
            await asyncio.sleep(2)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await initialize_database()
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/health/live", tags=["health"])
def liveness() -> dict[str, str]:
    return {"status": "alive", "version": settings.app_version}


@app.get("/health/ready", tags=["health"])
def readiness(db: DbSession) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is not ready") from exc
    return {"status": "ready", "version": settings.app_version}


@app.get("/metrics", response_class=PlainTextResponse, tags=["monitoring"])
def metrics(db: DbSession) -> str:
    total = db.scalar(select(func.count()).select_from(Task)) or 0
    completed = (
        db.scalar(select(func.count()).select_from(Task).where(Task.completed.is_(True))) or 0
    )
    return (
        "# HELP task_app_info Static application information.\n"
        "# TYPE task_app_info gauge\n"
        f'task_app_info{{version="{settings.app_version}"}} 1\n'
        "# HELP task_app_tasks_total Number of tasks.\n"
        "# TYPE task_app_tasks_total gauge\n"
        f"task_app_tasks_total {total}\n"
        "# HELP task_app_tasks_completed Number of completed tasks.\n"
        "# TYPE task_app_tasks_completed gauge\n"
        f"task_app_tasks_completed {completed}\n"
    )


@app.get("/api/tasks", response_model=list[TaskRead], tags=["tasks"])
def list_tasks(db: DbSession) -> list[Task]:
    return list(db.scalars(select(Task).order_by(Task.id.desc())))


@app.post(
    "/api/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED, tags=["tasks"]
)
def create_task(payload: TaskCreate, db: DbSession) -> Task:
    task = Task(title=payload.title.strip())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.patch("/api/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate, db: DbSession) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    changes = payload.model_dump(exclude_unset=True)
    if "title" in changes and changes["title"] is not None:
        changes["title"] = changes["title"].strip()
    for key, value in changes.items():
        if value is not None:
            setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int, db: DbSession) -> Response:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
