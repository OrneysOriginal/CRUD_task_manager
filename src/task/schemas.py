from typing import Optional, List, Annotated

from fastapi import Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.task.models import StatusEnum


class CreateTask(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    status: StatusEnum


class UpdateTask(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None


class PaginationParams(BaseModel):
    limit: int = Field(5, ge=0, le=100)
    offset: int = Field(0, ge=0)


PaginationParamsDep = Annotated[AsyncSession, Depends(PaginationParams)]


class TaskResponse(BaseModel):
    uuid: int
    name: str
    description: str
    status: str

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]

    class Config:
        from_attributes = True
