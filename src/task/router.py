from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import AsyncSessionDep
from src.task.models import Task
from src.task.schemas import (
    CreateTask,
    TaskResponse,
    TaskListResponse,
    UpdateTask,
    PaginationParamsDep,
)

task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.post(
    "/create_task/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def create_task(data: CreateTask, session: AsyncSessionDep):
    try:
        new_task = Task(**data.model_dump())
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return new_task
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task with this data already exists or invalid data",
        )


@task_router.get(
    "/get_task/{task_uuid}", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
async def get_task(task_uuid: int, session: AsyncSessionDep):
    query = select(Task).where(Task.uuid == task_uuid)
    data = await session.execute(query)
    task = data.scalar()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with UUID {task_uuid} not found",
        )
    return task


@task_router.get(
    "/get_task_list/", response_model=TaskListResponse, status_code=status.HTTP_200_OK
)
async def get_all_task(session: AsyncSessionDep, params: PaginationParamsDep):
    query = select(Task).limit(params.limit).offset(params.offset)
    data = await session.execute(query)
    tasks = data.scalars().all()

    return TaskListResponse(
        tasks=tasks,
    )


@task_router.patch(
    "/update_task/{task_uuid}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_uuid: int, update_data: UpdateTask, session: AsyncSessionDep
):
    try:
        query = select(Task).where(Task.uuid == task_uuid)
        data = await session.execute(query)
        task = data.scalar()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with UUID {task_uuid} not found",
            )

        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update",
            )

        for field, value in update_dict.items():
            setattr(task, field, value)

        await session.commit()
        await session.refresh(task)
        return task

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data provided for update",
        )


@task_router.delete(
    "/delete_task/{task_uuid}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_task(task_uuid: int, session: AsyncSessionDep):
    query = select(Task).where(Task.uuid == task_uuid)
    data = await session.execute(query)
    task = data.scalar()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with UUID {task_uuid} not found",
        )
    await session.delete(task)
    await session.commit()
    return task
