from config import app
from user.api import user_router
from mainapp.api import main_router

from config import metadata, engine, database

import fastapi


metadata.create_all(engine)
app.state.database = database


@app.on_event('startup')
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

app.include_router(user_router)
app.include_router(main_router)


def use_route_names_as_operation_ids(app_obj: fastapi.FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app_obj.routes:
        if isinstance(route, fastapi.routing.APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)
