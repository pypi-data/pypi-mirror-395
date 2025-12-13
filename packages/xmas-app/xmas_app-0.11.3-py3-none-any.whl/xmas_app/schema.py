from typing import Dict, List, Literal, Optional

from pydantic import BaseModel


class AppSchema(BaseModel):
    """Schema for app schema and version"""

    type: str
    version: str


class FeaturePatch(BaseModel):
    old_object_id: str
    wkt: Optional[str] = None


class SideSpec(BaseModel):
    group_name: str
    items: List[FeaturePatch]


class SplitPayload(BaseModel):
    """Schema for split tool post request payload"""

    schema_version: Literal["split-import-v1-min"]
    src_plan_group: Optional[str] = None
    src_plan_id: str
    crs: Optional[str] = None
    appschema: AppSchema
    inner: SideSpec
    outer: SideSpec


class BereichDescriptor(BaseModel):
    id: str
    nummer: str  # label in layer tree
    featuretype: str  # e.g. "Bereichsobjekt"
    geometry: bool = True  # for plugin's plan manager nogem vs geom check


class PlanDescriptor(BaseModel):
    plan_id: str
    plan_name: str
    plan_type: str
    appschema: str
    version: str
    bereiche: list[BereichDescriptor] = []


class SplitSuccess(BaseModel):
    status: Literal["ok"] = "ok"
    src_plan_id: str
    inner: Optional[PlanDescriptor] = None
    outer: Optional[PlanDescriptor] = None


class ErrorDetail(BaseModel):
    code: Optional[str] = None  # machine-readable code
    message: str  # human-readable message
    violations: Optional[List[Dict]] = None  # optional list of offending items


class ErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    detail: ErrorDetail
