from fastapi import FastAPI

import inventory
import ordering

app = FastAPI()
app.include_router(ordering.router)
app.include_router(inventory.router)
