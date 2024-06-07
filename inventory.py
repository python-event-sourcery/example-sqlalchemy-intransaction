from fastapi import APIRouter, Body

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)


@router.post(
    "/",
    name="inventory:create_item",
    status_code=201,
)
def create_item(
    item: str = Body(...),
    quantity: int = Body(...),
) -> None:
    raise NotImplementedError


@router.get(
    "/{item}",
    name="inventory:get_quantity",
    status_code=200,
)
def get_quantity(item: str) -> int:
    raise NotImplementedError
