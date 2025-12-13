from fastapi import HTTPException
from nicegui import run
from pydantic import ValidationError
from xplan_tools.model import model_factory

from xmas_app.models.crud import InsertPayload, UpdatePayload
from xmas_app.settings import settings


async def create(payload: InsertPayload):
    """Create features in the database.

    Iterates over data items in the payload and validates them with pydantic.
    If everything is valid, the features are saved to the database.
    """
    print(payload)
    features = []
    errors = []
    for item in payload.root:
        try:
            featuretype = model_factory(item.featuretype, item.version, item.appschema)
            properties = item.properties
            properties.pop("featuretype", None)
            if item.geometry:
                properties[featuretype.get_geom_field()] = item.geometry
            feature = featuretype.model_validate(properties)
            features.append(feature)
        except ValidationError as e:
            errors.append(e.errors())
    if errors:
        raise HTTPException(
            status_code=422,
            detail=errors,
        )
    try:
        await run.io_bound(settings.repo.save_all, features)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


async def update(payload: UpdatePayload):
    """Update features in the database.

    Iterates over data items in the payload and updates existing features with them.
    The update data is validated with pydantic.
    If everything is valid, the features are saved to the database.
    """
    print(payload)
    features = []
    errors = []
    for id, item in payload.root.items():
        feature = await run.io_bound(settings.repo.get, str(id))
        update = item.properties
        if item.geometry:
            update[feature.get_geom_field()] = item.geometry
        data = feature.model_dump() | update
        try:
            feature = feature.model_validate(data)
            features.append(feature)
        except ValidationError as e:
            errors.append(e.errors())
    if errors:
        raise HTTPException(
            status_code=422,
            detail=errors,
        )
    try:
        await run.io_bound(settings.repo.update_all, features)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
