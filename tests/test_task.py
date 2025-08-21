import pytest
from httpx import AsyncClient

from tests.conftest import async_client


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, status_code",
    [
        (
            {"name": "cool1", "description": "Cool", "status": "created"},
            201,
        ),
        (
            {"name": "cool", "description": "Cool", "status": "in_work"},
            400,
        ),
        (
            {"name": "", "description": "Cool", "status": "in_work"},
            422,
        ),
    ],
)
async def test_create_task(async_client: AsyncClient, data: dict, status_code: int):
    response = await async_client.post("/task/create_task/", json=data)
    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_uuid, status_code",
    [
        (0, 200),
        (10, 404),
    ],
)
async def test_get_task(async_client: AsyncClient, task_uuid: int, status_code: int):
    response = await async_client.get(f"/task/get_task/{task_uuid}")
    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code",
    [
        (200),
    ],
)
async def test_get_all_task(async_client: AsyncClient, status_code: int):
    response = await async_client.get("/task/get_task_list/")
    assert response.status_code == status_code


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_uuid, data, status_code",
    [
        (0, {"description": "Cool111"}, 200),
    ],
)
async def test_update_task(
    async_client: AsyncClient, task_uuid: int, data: dict, status_code: int
):
    response = await async_client.patch(f"/task/update_task/{task_uuid}", json=data)
    assert response.status_code == status_code
    assert response.json().get("description") == data.get("description")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_uuid, status_code, data",
    [
        (1, 200, {"name": "cool1", "description": "Cool", "status": "created"}),
        (1, 404, {}),
    ],
)
async def test_delete_task(
    async_client: AsyncClient, task_uuid: int, status_code: int, data: dict
):
    await async_client.post("/task/create_task/", json=data)
    response = await async_client.delete(f"/task/delete_task/{task_uuid}")
    assert response.status_code == status_code
