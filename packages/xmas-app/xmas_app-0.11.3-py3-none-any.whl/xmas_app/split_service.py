from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, NamedTuple, Optional
from uuid import UUID, uuid4

from xplan_tools.model.base import BaseCollection

from .db_uow import repo_uow
from .schema import (
    FeaturePatch,
    SplitPayload,
    SplitSuccess,
)

logger = logging.getLogger("xmas_app")

from xplan_tools.model import model_factory


def _uuid_str() -> str:
    return str(uuid4())


def _as_id_or_none(v):
    # Accept UUID instance, plain string, or dict with 'id' → return string id or None.
    if isinstance(v, UUID):
        return str(v)
    if isinstance(v, str) and v:
        return v
    if isinstance(v, dict) and "id" in v and isinstance(v["id"], (str, UUID)):
        return str(v["id"])
    return None


def _normalize(s: str | None) -> str:
    return (s or "").strip().lower().replace("_", "").replace("-", "")


def _normalize_appschema(s: str) -> str:
    # xplan-tools typically expects "xplan"
    s = (s or "").strip()
    return "xplan" if s.lower().startswith("xplan") else s.lower()


def _safe_model_factory(
    model_name: str, version: str, appschema: str, *, context: dict
):
    """Call model_factory with strong logging; re-raise with full context on failure."""
    norm_app = _normalize_appschema(appschema)
    logger.debug(
        "model_factory call: model=%r, version=%r, appschema(raw)=%r, appschema(norm)=%r, context=%s",
        model_name,
        version,
        appschema,
        norm_app,
        context,
    )
    try:
        ModelOrInstance = model_factory(model_name, version, norm_app)
    except Exception as e:
        # Explode with all details to see *exactly* what asked for 'section'
        raise ValueError(
            f"model_factory FAILED for model={model_name!r}, version={version!r}, appschema={norm_app!r}, context={context}"
        ) from e
    return (
        ModelOrInstance
        if isinstance(ModelOrInstance, type)
        else ModelOrInstance.__class__
    )


def _set_geometry_from_source(
    Model, dst_data: dict, src_dump: dict, new_wkt: str | None
) -> None:
    """
    Keep the source SRID; only replace the WKT for this model's geometry field.
    If the model has no geometry field, or new_wkt is None, do nothing.
    """
    gfield = Model.get_geom_field()
    if not gfield or new_wkt is None:
        return

    wkt_norm = new_wkt.strip().upper()

    src_geom = src_dump.get(gfield)  # usually {'srid': <int>, 'wkt': '...'}
    if isinstance(src_geom, dict) and "srid" in src_geom:
        srid = src_geom["srid"]
        dst_data[gfield] = {"srid": srid, "wkt": wkt_norm}
    else:
        # Fallback: preserve structure if source stored plain string/etc.
        # (XPlan models should use dict with 'srid'/'wkt', so this path is rare/just a safety)
        dst_data[gfield] = {"wkt": wkt_norm}


def _has_plan_inst(instances: list[object]) -> bool:
    """Avoid duplicating Innen/Außen plans."""
    return any(
        _is_plan_featuretype(getattr(i, "featuretype", i.__class__.__name__))
        for i in instances
    )


class ReferenceEdge(NamedTuple):
    rel: str
    src_old: str
    dst_old: str
    list_like: bool
    nullable: bool


def _clone_strip_assocs(
    src_obj,
    *,
    appschema_type: str,
    appschema_version: str,
    new_id: str,
    wkt: Optional[str],
    name_override: Optional[str] = None,
) -> tuple[object, List[ReferenceEdge], Dict[str, Any]]:
    """Clone to new instance, set geometry, strip associations collecting edges."""
    src_dump: Dict[str, Any] = (
        src_obj.model_dump() if hasattr(src_obj, "model_dump") else dict(src_obj)
    )
    ft = getattr(src_obj, "featuretype", None) or src_obj.__class__.__name__
    Model = model_factory(ft, appschema_version, appschema_type)

    data = dict(src_dump)
    data["id"] = new_id

    # Geometry
    _set_geometry_from_source(
        Model, data, src_dump, wkt.strip().upper() if wkt else None
    )

    # If plan-feature replace name with Innen/Außen
    if name_override and "name" in data and data.get("name"):
        data["name"] = name_override

    # Associations: strip and collect edges
    edges: List[ReferenceEdge] = _collect_and_strip_assocs(
        Model, data, src_id=src_dump["id"]
    )

    # Scrub meta that constructors might not accept
    for k in ("featuretype", "appschema", "version"):
        data.pop(k, None)

    return Model(**data), edges, {"featuretype": ft, "model": Model}


def _apply_edges_in_place(
    instances: List[object], id_map: Dict[str, str], edges: List[ReferenceEdge]
) -> List[object]:
    """Resolve and set associations *only within* this side; drop cross-side edges."""
    # Lookup map
    rev_map = {new_id: old_id for old_id, new_id in id_map.items()}

    updated: List[object] = []
    for inst in instances:
        Model = inst.__class__
        data = inst.model_dump()
        new_id = data.get("id")
        src_old = rev_map.get(new_id)
        if src_old is None:
            updated.append(inst)
            continue

        for rel, e_src_old, e_dst_old, list_like, nullable in edges:
            if e_src_old != src_old:
                continue
            dst_new = id_map.get(e_dst_old)
            if not dst_new:
                continue
            if list_like:
                # Set a list of UUIDs / strings (pydantic will coerce to UUID)
                arr = data.get(rel)
                if not isinstance(arr, list):
                    arr = []
                arr = list(arr) + [dst_new]
                data[rel] = arr
            else:
                data[rel] = dst_new

        updated.append(Model(**data))
    return updated


def _unres(edges, id_map):
    """Return a compact list of association edges that could not be resolved on this side."""
    return [(e.rel, e.src_old, e.dst_old) for e in edges if e.dst_old not in id_map]


def _collect_and_strip_assocs(Model, data: dict, src_id: str):
    """
    Collect outgoing association references (old IDs) and strip them from 'data'.
    Handles:
      - single-valued assoc: string/UUID or {'id': ...}
      - list-valued assoc : list of the above
    Always clears the association on the clone; we reattach later if both ends exist.
    """
    edges: list[ReferenceEdge] = []

    for assoc in Model.get_associations():
        if assoc not in data:
            continue

        info = Model.get_property_info(assoc)
        list_like = bool(info["list"])
        nullable = bool(info["nullable"])
        val = data[assoc]

        if list_like:
            items = val if isinstance(val, list) else []
            for it in items:
                if isinstance(it, UUID):
                    edges.append(
                        ReferenceEdge(
                            assoc,
                            src_old=src_id,
                            dst_old=str(it),
                            list_like=True,
                            nullable=nullable,
                        )
                    )
                elif isinstance(it, dict) and "id" in it:
                    edges.append(
                        ReferenceEdge(
                            assoc,
                            src_old=src_id,
                            dst_old=str(it["id"]),
                            list_like=True,
                            nullable=nullable,
                        )
                    )
            data[
                assoc
            ] = []  # Cleared associations, filled once all features are cloned
        else:
            dst = _as_id_or_none(val)
            if dst:
                edges.append(
                    ReferenceEdge(
                        assoc,
                        src_old=str(src_id),
                        dst_old=dst,
                        list_like=False,
                        nullable=nullable,
                    )
                )
            # Clear single association
            data[assoc] = None if nullable else data.pop(assoc, None)

    return edges


# Must be a plan-feature to be able to append the plan name
def _is_plan_featuretype(ft: str) -> bool:
    ft = (ft or "").strip()
    # accepts e.g. "BP_Plan", "FPPlan", "BPPlan" …
    return ft.endswith("Plan") or ft.endswith("_Plan")


def _ensure_plan_clone_for_side(
    *,
    collection,
    plan_feature_name: str,
    appschema,
    version: str,
) -> tuple[list[object], dict[str, str], list[ReferenceEdge]]:
    # Find the original plan object once
    src_plan = next(
        (
            f
            for f in collection.features.values()
            if getattr(f, "featuretype", "").endswith("Plan")
            or f.__class__.__name__.endswith("Plan")
        ),
        None,
    )
    if src_plan is None:
        raise ValueError("Could not find source plan feature in collection")

    # If there's already a cloned plan in this side (because it was in patches), skip
    # (detect via counting clones whose class endswith('Plan'))
    # Otherwise: make a synthetic FeaturePatch for the plan with the side's plan WKT.
    # If no precomputed WKT, at least clone with original WKT so edges attach.
    orig_dump = (
        src_plan.model_dump() if hasattr(src_plan, "model_dump") else dict(src_plan)
    )
    plan_geom_field = src_plan.__class__.get_geom_field()
    plan_wkt = None
    if plan_geom_field and isinstance(orig_dump.get(plan_geom_field), dict):
        plan_wkt = orig_dump[plan_geom_field].get("wkt")

    # Fabricate a patch
    plan_patch = FeaturePatch(old_object_id=str(orig_dump["id"]), wkt=plan_wkt)

    # Reuse normal build routine but force a name override
    new_id = _uuid_str()
    cloned_plan, plan_edges, _ = _clone_strip_assocs(
        src_plan,
        appschema_type=appschema.type,
        appschema_version=version,
        new_id=new_id,
        wkt=plan_patch.wkt,  # ideally the side WKT if present
        name_override=plan_feature_name,  # “<orig> – Innen/— Außen”
    )

    return [cloned_plan], {plan_patch.old_object_id: new_id}, plan_edges


def _auto_include_missing_bereiche(
    *,
    side_name: str,
    instances: List[object],
    id_map: Dict[str, str],
    edges: List[ReferenceEdge],
    src_by_id: Dict[str, object],
    appschema_type: str,
    appschema_version: str,
) -> int:
    required = _required_bereiche_for_side(edges, src_by_id)
    missing = [old for old in required if old not in id_map]
    if not missing:
        return 0

    added = 0
    for old in missing:
        src = src_by_id.get(old)
        if not src:
            logger.error(
                "%s: required Bereich %s not found in src_by_id", side_name, old
            )
            continue
        new_id = _uuid_str()
        cloned, cloned_edges, _ = _clone_strip_assocs(
            src,
            appschema_type=appschema_type,
            appschema_version=appschema_version,
            new_id=new_id,
            wkt=None,  # keep original WKT
            name_override=None,
        )
        instances.append(cloned)
        id_map[old] = new_id
        edges.extend(cloned_edges)
        added += 1

    logger.warning(
        "%s: auto-included %d Bereich feature(s): %s", side_name, added, missing
    )
    return added


def _referenced_sides(
    old_id: str, inner_edges: list[ReferenceEdge], outer_edges: list[ReferenceEdge]
) -> set[str]:
    sides = set()
    if any(e.dst_old == old_id for e in inner_edges):
        sides.add("inner")
    if any(e.dst_old == old_id for e in outer_edges):
        sides.add("outer")
    return sides


@dataclass
class SplitViolation:
    code: str
    featuretype: str
    old_id: str
    hint: str


class SplitValidationError(Exception):
    def __init__(self, message: str, violations: List[SplitViolation]):
        super().__init__(message)
        self.message = message
        self.violations = violations


def _validate_geomless_refs(
    src_by_id: Dict[str, object],
    inner_edges: List[ReferenceEdge],
    outer_edges: List[ReferenceEdge],
    version: str,
    appschema: str,
) -> List[SplitViolation]:
    violations: List[SplitViolation] = []

    def is_geomless(obj) -> bool:
        ft = getattr(obj, "featuretype", obj.__class__.__name__)
        Model = model_factory(ft, version, appschema)
        return not bool(Model.get_geom_field())

    # Build incoming ref index (old_id -> sides referencing it)
    incoming: Dict[str, set] = {}
    for rel, src_old, dst_old, *_ in inner_edges:
        incoming.setdefault(dst_old, set()).add("inner")
    for rel, src_old, dst_old, *_ in outer_edges:
        incoming.setdefault(dst_old, set()).add("outer")

    for old_id, obj in src_by_id.items():
        if not is_geomless(obj):
            continue
        sides = incoming.get(old_id, set())
        if not sides:
            ft = getattr(obj, "featuretype", obj.__class__.__name__)
            violations.append(
                SplitViolation(
                    code="GEOMLESS_WITHOUT_INCOMING_REF",
                    featuretype=ft,
                    old_id=str(old_id),
                    hint=(
                        "Geometrieloses Objekt (Text) wird von keinem Element referenziert. "
                        "Bitte referenzieren oder entfernen, bevor gespeichert werden kann."
                    ),
                )
            )
    return violations


def _is_bereich_ft(ft: str) -> bool:
    ft = (ft or "").strip()
    return ("Bereich" in ft) or ft.endswith("_Bereich")


def _required_bereiche_for_side(
    edges: List[ReferenceEdge], src_by_id: Dict[str, object]
) -> set[str]:
    req: set[str] = set()
    for rel, _src_old, dst_old, *_ in edges:
        if rel not in ("bereich", "gehoertZuBereich"):
            continue
        tgt = src_by_id.get(dst_old)
        if not tgt:
            continue
        ft = getattr(tgt, "featuretype", tgt.__class__.__name__)
        if _is_bereich_ft(ft):
            req.add(dst_old)
    return req


def _ensure_side_minimum(
    side_name: str,
    rows: List[object],
    id_map: Dict[str, str],
    edges: List[ReferenceEdge],
    src_by_id: Dict[str, object],
):
    fts = [getattr(x, "featuretype", x.__class__.__name__) for x in rows]
    has_plan = any(ft.endswith("Plan") or ft.endswith("_Plan") for ft in fts)
    has_bereich = any(_is_bereich_ft(ft) for ft in fts)

    violations: List[SplitViolation] = []
    if not has_plan:
        violations.append(
            SplitViolation(
                "SIDE_MISSING_PLAN",
                "—",
                side_name,
                f"{side_name}: Es muss genau ein Plan vorhanden sein.",
            )
        )
    if not has_bereich:
        violations.append(
            SplitViolation(
                "SIDE_MISSING_BEREICH",
                "—",
                side_name,
                f"{side_name}: Mindestens ein Bereich erforderlich (Bitte Bereich in die {side_name}-Auswahl aufnehmen).",
            )
        )

    required = _required_bereiche_for_side(edges, src_by_id)
    missing = [old for old in required if old not in id_map]
    for old in missing:
        tgt = src_by_id.get(old)
        ft = getattr(tgt, "featuretype", tgt.__class__.__name__) if tgt else "BPBereich"
        violations.append(
            SplitViolation(
                "MISSING_REFERENCED_BEREICH",
                ft,
                str(old),
                f"{side_name}: Bereich wird referenziert (z. B. über 'gehoertZuBereich'), ist aber nicht in den {side_name}-Patches enthalten.",
            )
        )

    if violations:
        raise SplitValidationError(
            f"Seite '{side_name}' unvollständig/inkonsistent.", violations
        )


def _must_have_no_unresolved_bereich(
    edges: List[ReferenceEdge], id_map: Dict[str, str]
):
    unresolved = [
        (e.rel, e.src_old, e.dst_old)
        for e in edges
        if e.rel in ("bereich", "gehoertZuBereich") and e.dst_old not in id_map
    ]
    if unresolved:
        raise SplitValidationError(
            "Bereich-Referenzen konnten nicht aufgelöst werden.",
            [
                SplitViolation(
                    "UNRESOLVED_BEREICH",
                    "BPBereich",
                    d,
                    f"Unresolved edge {r} from {s} to {d}",
                )
                for (r, s, d) in unresolved
            ],
        )


def _is_plan_inst(obj) -> bool:
    ft = getattr(obj, "featuretype", obj.__class__.__name__)
    return "Plan" in ft or ft.endswith("_Plan") or ft.lower().endswith("plan")


def _get_id(obj) -> str | None:
    for attr in ("id", "gml_id", "identifier"):
        v = getattr(obj, attr, None)
        if isinstance(v, str) and v:
            return v
    return None


def _get_name(obj, default_name: str) -> str:
    for attr in ("name", "bezeichnung", "titel", "plan_name"):
        v = getattr(obj, attr, None)
        if isinstance(v, str) and v.strip():
            return v
    return default_name


def _build_plan_descriptor(
    instances: list[object], *, default_name: str, appschema: str, version: str
) -> dict | None:
    plan_inst = next((x for x in instances if _is_plan_inst(x)), None)
    plan_type = getattr(plan_inst, "featuretype", plan_inst.__class__.__name__)
    plan_id = _get_id(plan_inst) or ""
    plan_name = _get_name(plan_inst, default_name=default_name)
    return {
        "plan_id": plan_id,
        "plan_name": plan_name,
        "plan_type": plan_type,
        "appschema": appschema,
        "version": version,
        "bereiche": _collect_bereiche(instances),
    }


def _is_bereich_inst(x) -> bool:
    ft = getattr(x, "featuretype", x.__class__.__name__)
    return "Bereich" in ft


def _collect_bereiche(instances: list[object]) -> list[dict]:
    out: list[dict] = []
    for obj in instances:
        ft = getattr(obj, "featuretype", obj.__class__.__name__)
        if "Bereich" not in ft:
            continue

        bid = _get_id(obj)
        if not bid:
            continue

        # 0 is valid -> check against None, not truthiness
        nummer = getattr(obj, "nummer", None)
        if nummer is None:
            logger.warning("Bereich %s (%s) has no 'nummer' after clone", bid, ft)
            continue

        out.append(
            {
                "id": bid,
                "featuretype": ft,
                "nummer": str(nummer),  # stringify for UI safety
                "geometry": True,
            }
        )
    return out


class PlanSplitService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def apply_split_import(
        self, payload: SplitPayload, source_plan: BaseCollection
    ) -> SplitSuccess:
        # Load BaseCollection to access original plan and source features
        source_plan_collection = source_plan
        if not hasattr(source_plan_collection, "features"):
            raise ValueError(
                "Expected BaseCollection with .features from get_plan_by_id"
            )

        src_by_id: Dict[str, object] = getattr(source_plan_collection, "features", {})

        def build_side(
            patches: List[FeaturePatch], *, side_group_name: str
        ) -> tuple[List[object], Dict[str, str], List[ReferenceEdge]]:
            cloned_instances: List[object] = []
            old_to_new_id_map: Dict[str, str] = {}
            reference_edges: List[ReferenceEdge] = []

            for patch in patches:
                source_instance = src_by_id.get(patch.old_object_id)
                if not source_instance:
                    logger.error(
                        "Unknown source id=%s (not in plan features). Side=%s",
                        patch.old_object_id,
                        side_group_name,
                    )
                    continue

                ft = (
                    getattr(source_instance, "featuretype", None)
                    or source_instance.__class__.__name__
                )
                name_override = side_group_name if _is_plan_featuretype(ft) else None

                new_id = _uuid_str()
                cloned_instance, cloned_edges, _metadata = _clone_strip_assocs(
                    source_instance,
                    appschema_type=payload.appschema.type,
                    appschema_version=payload.appschema.version,
                    new_id=new_id,
                    wkt=patch.wkt,
                    name_override=name_override,
                )
                cloned_instances.append(cloned_instance)
                old_to_new_id_map[patch.old_object_id] = new_id
                reference_edges.extend(cloned_edges)

            logger.debug(
                "build_side('%s'): instances=%d edges=%d",
                side_group_name,
                len(cloned_instances),
                len(reference_edges),
            )
            return cloned_instances, old_to_new_id_map, reference_edges

        inner_instances, inner_id_map, inner_edges = build_side(
            payload.inner.items, side_group_name=payload.inner.group_name
        )
        if not _has_plan_inst(inner_instances):
            plan_insts, plan_map, plan_edges = _ensure_plan_clone_for_side(
                collection=source_plan_collection,
                plan_feature_name=payload.inner.group_name,
                appschema=payload.appschema,
                version=payload.appschema.version,
            )
            inner_instances = plan_insts + inner_instances
            inner_id_map.update(plan_map)
            inner_edges.extend(plan_edges)

        outer_instances, outer_id_map, outer_edges = build_side(
            payload.outer.items, side_group_name=payload.outer.group_name
        )
        if not _has_plan_inst(outer_instances):
            plan_insts, plan_map, plan_edges = _ensure_plan_clone_for_side(
                collection=source_plan_collection,
                plan_feature_name=payload.outer.group_name,
                appschema=payload.appschema,
                version=payload.appschema.version,
            )
            outer_instances = plan_insts + outer_instances
            outer_id_map.update(plan_map)
            outer_edges.extend(plan_edges)

        violations = _validate_geomless_refs(
            src_by_id,
            inner_edges,
            outer_edges,
            version=payload.appschema.version,
            appschema=payload.appschema.type,
        )
        if violations:
            raise SplitValidationError(
                "Geometriefreie Objekte ohne eingehende Referenz gefunden.", violations
            )

        def _debug_edge_targets(edges, src_by_id, label):
            rows = []
            for rel, src_old, dst_old, *_ in edges:
                tgt = src_by_id.get(dst_old)
                ft = (
                    getattr(tgt, "featuretype", tgt.__class__.__name__)
                    if tgt
                    else "<?>"
                )
                rows.append((rel, dst_old, ft))
            logger.debug("%s edge targets (first 20): %s", label, rows[:20])

        _debug_edge_targets(inner_edges, src_by_id, "INNER")
        _debug_edge_targets(outer_edges, src_by_id, "OUTER")

        added_in = _auto_include_missing_bereiche(
            side_name="INNER",
            instances=inner_instances,
            id_map=inner_id_map,
            edges=inner_edges,
            src_by_id=src_by_id,
            appschema_type=payload.appschema.type,
            appschema_version=payload.appschema.version,
        )
        added_out = _auto_include_missing_bereiche(
            side_name="OUTER",
            instances=outer_instances,
            id_map=outer_id_map,
            edges=outer_edges,
            src_by_id=src_by_id,
            appschema_type=payload.appschema.type,
            appschema_version=payload.appschema.version,
        )

        if added_in or added_out:
            logger.info(
                "Auto-included Bereich: INNER=%d, OUTER=%d", added_in, added_out
            )

        _must_have_no_unresolved_bereich(inner_edges, inner_id_map)
        _must_have_no_unresolved_bereich(outer_edges, outer_id_map)

        # Resolve associations per side (only if both ends were cloned into that side)
        inner_resolved = _apply_edges_in_place(
            inner_instances, inner_id_map, inner_edges
        )
        outer_resolved = _apply_edges_in_place(
            outer_instances, outer_id_map, outer_edges
        )

        logger.debug("INNER unresolved edges: %s", _unres(inner_edges, inner_id_map))
        logger.debug("OUTER unresolved edges: %s", _unres(outer_edges, outer_id_map))

        def _count_by_ft(rows):
            from collections import Counter

            c = Counter(getattr(r, "featuretype", r.__class__.__name__) for r in rows)
            return ", ".join(f"{k}={v}" for k, v in c.items())

        logger.debug(
            "INNER: %d instances; %s", len(inner_resolved), _count_by_ft(inner_resolved)
        )
        logger.debug(
            "OUTER: %d instances; %s", len(outer_resolved), _count_by_ft(outer_resolved)
        )

        def _fts(rows):
            return [getattr(x, "featuretype", x.__class__.__name__) for x in rows]

        logger.debug("INNER featuretypes: %s", _fts(inner_instances))
        logger.debug("OUTER featuretypes: %s", _fts(outer_instances))
        logger.debug("INNER_RESOLVED featuretypes: %s", _fts(inner_resolved))
        logger.debug("OUTER_RESOLVED featuretypes: %s", _fts(outer_resolved))

        # Validate both sides
        _ensure_side_minimum(
            "INNER", inner_resolved, inner_id_map, inner_edges, src_by_id
        )
        _ensure_side_minimum(
            "OUTER", outer_resolved, outer_id_map, outer_edges, src_by_id
        )

        # Persist in one go
        with repo_uow(self.repo):
            self.repo.save_all(inner_resolved + outer_resolved)

        # Build response
        apps = payload.appschema.type
        ver = payload.appschema.version

        inner_desc = _build_plan_descriptor(
            inner_resolved,
            default_name=payload.inner.group_name,
            appschema=apps,
            version=ver,
        )
        outer_desc = _build_plan_descriptor(
            outer_resolved,
            default_name=payload.outer.group_name,
            appschema=apps,
            version=ver,
        )

        result = {
            "status": "ok",
            "src_plan_id": _get_id(
                getattr(source_plan_collection, "plan", source_plan_collection)
            )
            or "",
            "inner": inner_desc,
            "outer": outer_desc,
        }

        return SplitSuccess(**result)
