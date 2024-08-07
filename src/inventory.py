from dataclasses import dataclass
from typing import ClassVar, Generator

from event_sourcery.aggregate import Aggregate, Repository
from event_sourcery.event_store import (
    Backend,
    Event,
    Metadata,
    Position,
    StreamId,
    StreamUUID,
)
from fastapi import APIRouter, Body, Depends

import ordering
from backend import backend


@dataclass
class Quantity(Aggregate):
    category: ClassVar[str] = "quantity"
    quantity: int = 0

    class Adjust(Event):
        quantity: int

    def adjust(self, by: int) -> None:
        self._emit(self.Adjust(quantity=self.quantity + by))

    def __apply__(self, event: Event) -> None:
        assert isinstance(event, Quantity.Adjust)
        self.quantity = event.quantity


class QuantityRepository(Repository[Quantity]):
    def process(
        self,
        order_placed: Metadata[ordering.OrderPlaced],
        stream_id: StreamId,
        position: Position | None,
    ) -> None:
        item = order_placed.event.item
        with self.aggregate(StreamUUID(name=item), Quantity()) as aggregate:
            aggregate.adjust(-order_placed.event.units)


def quantity_repository(
    backend: Backend = Depends(backend),
) -> Generator[QuantityRepository, None, None]:
    yield QuantityRepository(backend.event_store)


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
    repository: QuantityRepository = Depends(quantity_repository),
) -> None:
    with repository.aggregate(StreamUUID(name=item), Quantity()) as aggregate:
        aggregate.adjust(by=quantity)


@router.get(
    "/{item}",
    name="inventory:get_quantity",
    status_code=200,
)
def get_quantity(
    item: str,
    repository: QuantityRepository = Depends(quantity_repository),
) -> int:
    with repository.aggregate(StreamUUID(name=item), Quantity()) as aggregate:
        return aggregate.quantity
