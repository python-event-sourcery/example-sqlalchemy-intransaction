from event_sourcery.event_store import TransactionalBackend
from fastapi import Depends, FastAPI

import inventory
import ordering
from backend import backend


def in_transaction_subscriptions(
    pyes_backend: TransactionalBackend = Depends(backend),
    quantity: inventory.QuantityRepository = Depends(inventory.quantity_repository),
) -> None:
    pyes_backend.in_transaction.register(quantity.process, to=ordering.OrderPlaced)


app = FastAPI(dependencies=[Depends(in_transaction_subscriptions)])
app.include_router(ordering.router)
app.include_router(inventory.router)
