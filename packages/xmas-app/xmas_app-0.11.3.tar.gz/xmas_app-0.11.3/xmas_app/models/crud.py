from uuid import UUID

from pydantic import BaseModel, RootModel


class InsertItem(BaseModel):
    appschema: str
    version: str
    featuretype: str
    properties: dict
    geometry: dict | None


class InsertPayload(RootModel):
    root: list[InsertItem]


class UpdateItem(BaseModel):
    properties: dict = {}
    geometry: dict | None = None


class UpdatePayload(RootModel):
    root: dict[UUID, UpdateItem]
