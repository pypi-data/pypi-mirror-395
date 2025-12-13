import asyncio
import importlib
import inspect
import io
import logging
import re
from contextlib import asynccontextmanager
from functools import partial
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from typing import Any, Literal
from uuid import uuid4

import pydantic
import pydantic_core
from fastapi import APIRouter, Depends, HTTPException, Request, status
from nicegui import app, run, ui
from nicegui.events import ClickEventArguments, ValueChangeEventArguments
from nicegui.observables import ObservableSet
from pydantic import ValidationError
from starlette.applications import Starlette
from xplan_tools.interface import repo_factory
from xplan_tools.interface.db import DBRepository
from xplan_tools.interface.gml import GMLRepository
from xplan_tools.model import model_factory
from xplan_tools.util import (
    cast_geom_to_multi,
    cast_geom_to_single,
    get_geometry_type_from_wkt,
)

from xmas_app.db import get_db_feature_ids, get_nodes
from xmas_app.deps.version_guard import enforce_plugin_version
from xmas_app.form import ModelForm
from xmas_app.models.crud import InsertPayload, UpdatePayload
from xmas_app.schema import ErrorDetail, ErrorResponse, SplitPayload, SplitSuccess
from xmas_app.services import crud
from xmas_app.settings import get_appschema, settings
from xmas_app.split_service import PlanSplitService, SplitValidationError


def _resolve_log_dir() -> Path:
    if settings.app_mode == "prod":
        return Path(gettempdir()) / "xmas_log"
    else:
        # dev: local repo logs
        return Path(__file__).parent.parent


log_dir = _resolve_log_dir()
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "xmas_app.log"

logger = logging.getLogger("xmas_app")
logger.propagate = False

logger.handlers.clear()
logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug(f"Writing logs to {log_file}")

ui.element.default_props("dense")

router = APIRouter()


async def get_model_for_select(
    model_select: ui.select,
    wkt: str | None = None,
    feature_regex: str | None = None,
    appschema: str = settings.appschema,
    appschema_version: str = settings.appschema_version,
) -> list[str]:
    """Populate a UI select element.

    Args:
        model_select: The ui.select input element that should be populated.
        wkt: The WKT string of the current feature geometry.
        feature_regex: A regex pattern to limit the number of models to select.
        appschema: The appschema, e.g. 'xplan'.
        appschema_version: The appschema version.
    """

    def filter_members(model: object):
        """Filters the models in the appschema according to the provided WKT geometry and the featuretype regex."""
        # Only dive into models that can be instantiated
        if (
            hasattr(model, "model_fields")
            and model.model_fields.get("id")
            and not model.abstract
        ):
            geom_types = model.get_geom_types()
            if wkt and (geom_types := model.get_geom_types()):
                # Test if the provided WKT is valid for the model and cast it to its single/multi variant otherwise
                if get_geometry_type_from_wkt(wkt) not in geom_types:
                    if not wkt.startswith("MULTI"):
                        geom = cast_geom_to_multi(wkt)
                    else:
                        geom = cast_geom_to_single(wkt)
                    if get_geometry_type_from_wkt(geom) not in geom_types:
                        return False
            if feature_regex:
                if not re.match(feature_regex, model.get_name()):
                    return False
            return True

    # update the input element options
    model_select.set_options(
        [
            model.get_name()
            for _, model in inspect.getmembers(
                importlib.import_module(
                    f"xplan_tools.model.appschema.{appschema + appschema_version.replace('.', '')}"
                ),
                filter_members,
            )
        ]
    )


@ui.page("/", dependencies=[Depends(enforce_plugin_version)])
def index():
    """
    Render the main index page of the XPlan-GUI application.
    Args:
    request (Request): The incoming HTTP request object (FastAPI).
    """
    # print(request.headers)
    ui.colors(primary="rgb(157 157 156)", secondary="rgb(229 7 126)")
    with ui.header():
        ui.label("XPlan-GUI")
    ui.button(
        "Neues Objekt", on_click=lambda: ui.navigate.to(f"/feature/{str(uuid4())}")
    )
    ui.select(
        dict(sorted(get_db_feature_ids(settings.repo).items(), key=lambda x: x[1])),
        label="Feature auswählen",
        with_input=True,
        on_change=lambda x: ui.navigate.to(f"/feature/{x.value}"),
    )


@ui.page(
    "/plan-tree/{id}",
    reconnect_timeout=5,
    dependencies=[Depends(enforce_plugin_version)],
)
async def plan_tree(
    request: Request,
    id: str,
):
    async def update_nodes():
        result = await get_nodes(feature)
        if result:
            nodes, *_ = result
            nodes[0]["children"] = nodes
            tree.update()

    app.storage.client["user_agent"] = request.headers.get("user-agent", None)
    qgis = app.storage.client["user_agent"].startswith(settings.qgis_plugin_name)
    if qgis:
        ui.add_head_html('<script src="qrc:///qtwebchannel/qwebchannel.js"></script>')

    header = ui.header().classes("bg-white text-black")
    with header:
        ui.label("Feature-Baum").classes("text-h6")
        tree_filter = (
            ui.input("Baum filtern")
            .props("clearable square filled dense")
            .classes("w-full")
        )
        with tree_filter.add_slot("after"):
            ui.button(icon="refresh", on_click=update_nodes).tooltip(
                "Baum aktualisieren"
            )
        ui.separator()
    action_dialog = ui.dialog().on("hide", lambda e: e.sender.clear())

    ui.colors(primary="rgb(157 157 156)", secondary="rgb(229 7 126)")
    ui.button.default_props("flat square no-caps")
    ui.button_group.default_props("flat square no-caps")

    # # --- Create the dialog placeholder once ---
    # with ui.dialog() as confirm_removeAssociation_dialog, ui.card():
    #     removeAssociation_label = (
    #         ui.label()
    #     )  # placeholder text we can update dynamically
    #     with ui.row().classes("justify-end w-full"):
    #         cancel_removeAssociation_button = ui.button(
    #             "Abbrechen", on_click=confirm_removeAssociation_dialog.close
    #         )
    #         removeAssociation_confirm_button = ui.button("Aufheben", color="red")

    # --- Create the dialog placeholder once ---
    with ui.dialog() as confirm_deleteObject_dialog, ui.card(align_items="stretch"):
        label = ui.label(
            "Soll das Objekt wirklich gelöscht werden?"
        )  # placeholder text we can update dynamically

        confirm_button = ui.button("Löschen", color="red")
        ui.button("Abbrechen", on_click=confirm_deleteObject_dialog.close)

    # --- Function to open the dialog dynamically ---
    def confirm_delete(target):
        label.text = "Soll das Objekt wirklich gelöscht werden?"
        confirm_button.on("click", partial(delete_feature, target))
        confirm_deleteObject_dialog.open()

    # # --- Function to open the dialog dynamically ---
    # def confirm_delete_association(origin, target):
    #     removeAssociation_label.text = f"Möchten Sie diese Beziehung wirklich aufheben?"
    #     removeAssociation_confirm_button.on(
    #         "click",
    #         lambda: remove_association(origin, target),
    #         confirm_removeAssociation_dialog.close(),
    #     )
    #     confirm_removeAssociation_dialog.open()

    async def show_menu(e: ValueChangeEventArguments):
        action_dialog.clear()
        if e.value:
            path = e.value.split(".")
            if len(path) == 5:
                _, origin, _, target_featuretype, target = path
                feature = settings.repo.get(target)
                with action_dialog, ui.card():
                    ui.label(f"{target_featuretype} {target[:8]}").classes("text-bold")
                    # ui.button(
                    #     "Referenz hinzufügen", on_click=lambda: open_page_in_dialog(target)
                    # )
                    if feature.get_geom_wkt():
                        ui.button("Zum Feature springen").on(
                            "click",
                            lambda e, target=target: highlight_feature(e, str(target)),
                        )

                    ui.button("Feature selektieren").on(
                        "click",
                        lambda e, target=target: select_feature(e, str(target)),
                    )

                    ui.button("Attributformular öffnen").on(
                        "click",
                        lambda e, target=target: show_attribute_form(e, str(target)),
                    )

                    # ui.button(
                    #     "Referenz aufheben",
                    #     on_click=lambda: confirm_delete_association(origin, target),
                    # )
                    if not re.match("^.._Bereich$", target_featuretype):
                        ui.button(
                            "Feature löschen",
                            on_click=lambda e, target=target: confirm_delete(target),
                        )
            elif len(path) == 3:
                origin_featuretype, origin_id, attr = path
                with action_dialog, ui.card(align_items="stretch"):
                    ui.label(origin_featuretype + " " + origin_id[:8]).classes(
                        "text-bold"
                    )
                    if attr == "bereich":
                        ui.label(f"Keine Aktionen für Referenz {repr(attr)} verfügbar")
                    else:
                        ui.label(f"Neues Feature für Referenz {repr(attr)} erstellen")
                        feature = settings.repo.get(origin_id)
                        prop_info = feature.get_property_info(attr)
                        typename = prop_info["typename"]
                        targets = typename if isinstance(typename, list) else [typename]
                        target_select = ui.select(
                            targets,
                            label="Featuretype auswählen",
                            value=targets[0],
                            with_input=True,
                        )
                        if len(targets) == 1:
                            target_select.props("readonly")
                        with target_select.add_slot("append"):
                            ui.badge(str(len(targets))).props("floating")
                        with target_select.add_slot("after"):
                            ui.button(
                                icon="play_circle",
                                on_click=lambda _: ui.notify(
                                    "noch nicht implementiert"
                                ),
                            )

            else:
                return
            action_dialog.open()

    async def highlight_feature(e: ClickEventArguments, target: str):
        logger.debug("highlight_feature called")
        try:
            logger.info("Sending highlight_feature to QWebChannel handler")
            ui.run_javascript(f"""new QWebChannel(qt.webChannelTransport, function (channel) {{
                                        channel.objects.handler.highlight_feature("{target}")
                                }});""")
        except Exception as ex:
            logger.error(
                f"Exception while highlightFeature called: {ex}", exc_info=True
            )
        finally:
            e.sender.props(remove="loading")

    async def show_attribute_form(e: ClickEventArguments, target: str):
        logger.debug("show_attribute_form called")
        try:
            logger.info("Sending show_attribute_form to QWebChannel handler")
            ui.run_javascript(f"""new QWebChannel(qt.webChannelTransport, function (channel) {{
                                        channel.objects.handler.show_attribute_form("{target}")
                                }});""")
        except Exception as ex:
            logger.error(
                f"Exception while show_attribute_form called: {ex}", exc_info=True
            )
        finally:
            e.sender.props(remove="loading")

    async def select_feature(e: ClickEventArguments, target: str):
        logger.debug("highlight_feature called")
        try:
            logger.info("Sending select_feature to QWebChannel handler")
            ui.run_javascript(f"""new QWebChannel(qt.webChannelTransport, function (channel) {{
                                        channel.objects.handler.select_feature("{target}")
                                }});""")
        except Exception as ex:
            logger.error(f"Exception while select_feature called: {ex}", exc_info=True)
        finally:
            e.sender.props(remove="loading")

    # def remove_association(base_id, related_id):
    #     delete_db_association(base_id, related_id, settings.repo)
    #     confirm_removeAssociation_dialog.close()
    #     (
    #         ui.notify(
    #             f"Die Beziehung zwischen {base_id} und {related_id} wurde aufgehoben"
    #         ),
    #     )

    async def delete_feature(id):
        # TODO: Is cascading deletion desired?
        try:
            settings.repo.delete(id)
            ui.notify(f"Feature mit ID '{id}' wurde gelöscht", type="positive")
            await update_nodes()
            confirm_deleteObject_dialog.close()

        except Exception as e:
            print(e)
            ui.notify(f"Fehler beim Löschen vom Feature mit ID '{id}'", type="negative")

    def update_notification(e):
        notification.message = f"{len(e.sender)} Features geladen"

    if not id:
        return

    await ui.context.client.connected()
    logger.debug("Feature called by ID:")
    logger.debug(id)

    notification = ui.notification(
        "0 Features geladen",
        type="ongoing",
        spinner=True,
        timeout=None,
    )

    app.storage.client["features"] = ObservableSet(on_change=update_notification)

    result = await run.io_bound(get_nodes, id, app.storage.client["features"])
    if result:
        nodes, featuretype, id, appschema = result
    else:
        return
    tree = ui.tree(
        nodes,
        on_select=show_menu,
        tick_strategy=None,
    ).props("accordion no-transition")

    notification.spinner = False
    notification.type = "positive"
    notification.message = "Ladevorgang abgeschlossen"
    await asyncio.sleep(1)
    notification.dismiss()

    if appschema == "xplan":
        tree.expand([id, f"{featuretype}.{id}.bereich"])
    tree_filter.bind_value_to(tree, "filter")


@ui.page("/plans", dependencies=[Depends(enforce_plugin_version)])
async def plans(
    request: Request,
    appschema: str = settings.appschema,
    version: str = settings.appschema_version,
):
    """
    Render the plans overview page and configure UI settings and client storage.

    Args:
    request (Request): Incoming FastAPI HTTP request.
    appschema (str): Application schema name (default from settings).
    version (str): Schema version (default from settings).

    Raises:
    ImportError: If required modules such as `settings` or `ui` are unavailable.
    KeyError: If access to `request.headers` fails unexpectedly.
    """
    logger.info('Entered the "plans" route.')
    ui.colors(primary="rgb(157 157 156)", secondary="rgb(229 7 126)")
    ui.button.default_props("flat square no-caps")
    ui.dropdown_button.default_props("flat square no-caps")
    ui.select.default_props("square filled dense")
    app.storage.client["user_agent"] = request.headers.get("user-agent", None)
    qgis = app.storage.client["user_agent"].startswith(settings.qgis_plugin_name)
    if qgis:
        ui.add_head_html('<script src="qrc:///qtwebchannel/qwebchannel.js"></script>')

    async def update_plan_select_options():
        logger.info("Updating plan select options")
        plan_select.props("loading")
        try:
            feature_ids = await asyncio.wait_for(
                run.io_bound(
                    get_db_feature_ids,
                    settings.repo,
                    None,
                    "^.*Plan$",
                    "name",
                ),
                timeout=10,
            )
            if not feature_ids:  # Handle empty result or None
                logger.warning("No plans returned from the database.")
                ui.notify(
                    "Keine Pläne gefunden (möglicherweise keine Verbindung zur Datenbank)!",
                    type="negative",
                )
                plan_select.set_options({})
            else:
                if feature_ids is not None and feature_ids:
                    plan_select.set_options(feature_ids)
                    plan_select.set_value(list(feature_ids.keys())[0])
                else:
                    logger.warning("No plans found or database unreachable.")
        except asyncio.TimeoutError:
            logger.error("Timeout: DB connection took too long.")
            ui.notify(
                "Verbindung zur Datenbank dauert zu lange (Timeout)!", type="negative"
            )
            plan_select.set_options({})
        except Exception as e:
            print("Fehler beim Laden der Pläne:", e)
            logger.error(f"Fehler beim Laden der Pläne: {e}")
            if (
                "could not connect" in str(e).lower()
                or "connection refused" in str(e).lower()
            ):
                ui.notify("Keine Verbindung zur Datenbank!", type="negative")
            else:
                ui.notify(f"Fehler beim Laden der Pläne: {e}", type="negative")
            plan_select.set_options({})
        finally:
            plan_select.props(remove="loading")

    async def download_plan(format: Literal["gml", "jsonfg", "db"]):
        """Downloads plan in either .gml .jsonfg or as a database."""
        logger.info(
            "Starting download for plan_id=%s format=%s", plan_select.value, format
        )
        try:
            download_dropdown.props(add="loading")
            plan = await run.io_bound(settings.repo.get_plan_by_id, plan_select.value)

            appschema = plan.features[plan_select.value].get_data_type()
            version = plan.features[plan_select.value].get_version()
            logger.debug(
                "Loaded plan metadata: version=%s schema=%s", version, appschema
            )

            if format == "db":
                temp_file = NamedTemporaryFile(
                    delete=False
                )  # TODO get data from in-memory sqlite db?
                logger.debug("Using temporary sqlite file %s", temp_file.name)
                uri = f"gpkg:///{temp_file.name}"
                repo = DBRepository(uri, version, appschema)
                repo.create_tables(srid=plan.srid)
                repo.save_all(plan)
                data = Path(temp_file.name).read_bytes()
                Path(temp_file.name).unlink()
            else:
                buffer = io.BytesIO()
                logger.debug("Serializing to %s via repo_factory", format)
                repo_factory(buffer, version, appschema, repo_type=format).save_all(
                    plan
                )
                data = buffer.getvalue()

            logger.info("Prepared download payload (%d bytes)", len(data))
            await asyncio.sleep(0.1)
            ui.download.content(
                data,
                filename=f"xplan.{'gml' if format == 'gml' else 'json' if format == 'jsonfg' else 'gpkg'}",
                media_type=f"application/{'gml+xml' if format == 'gml' else 'geo+json' if format == 'jsonfg' else 'geopackage+sqlite3'}",
            )

        except Exception as e:
            logger.error(
                "Error downloading plan_id=%s", plan_select.value, exc_info=True
            )
            ui.notify(f"Failed to download plan: {e}", color="danger")
        finally:
            download_dropdown.props(remove="loading")

    async def handle_delete_plan(e: ClickEventArguments):
        """Delete plan using repository method from XPlan-Tools."""
        with ui.dialog() as dialog, ui.card():
            ui.label("Löschen bestätigen")
            with ui.row():
                ui.button(icon="check", on_click=lambda: dialog.submit(True))
                ui.button(icon="close", on_click=lambda: dialog.submit(False))
        result = await dialog
        dialog.delete()
        if not result:
            return

        e.sender.props(add="loading")
        try:
            await run.io_bound(settings.repo.delete_plan_by_id, plan_select.value)
            logging.info("Plan %s deleted successfully", plan_select.value)

            options = plan_select.options
            options.pop(plan_select.value)
            plan_select.set_options(options)

        except Exception:
            logging.exception("Failed to delete plan %s", plan_select.value)
            ui.notification.toast("Fehler beim Löschen des Plans.", severity="error")

        finally:
            e.sender.props(remove="loading")

    async def handle_load_plan(e: ClickEventArguments):
        """
        Handles loading a selected plan and sends the plan data to the QWebChannel handler.
        Fetches the selected plan, retrieves its associated 'bereiche', and passes the structured
        data to the web view. Logs key steps and errors, and provides user feedback on failure.

        Args:
            e (ClickEventArguments): The click event that triggered the plan load.
        """
        logger.info("xmas_app.handle_load_plan")
        e.sender.props(add="loading")
        try:
            logger.info(f"Attempting to load plan with ID: {plan_select.value}")
            plan = await run.io_bound(settings.repo.get, plan_select.value)
            if plan is None:
                logger.error(f"No plan found for ID: {plan_select.value}")
                ui.notify("Fehler: Plan nicht gefunden", type="negative")
                return

            bereiche = []
            if bereich_ref := getattr(plan, "bereich", None):
                logger.info(f"Found {len(bereich_ref)} bereiche for plan {plan.id}")
                for bereich_id in bereich_ref:
                    try:
                        bereich = await run.io_bound(settings.repo.get, str(bereich_id))
                        if bereich is not None:
                            bereiche.append(
                                {
                                    "id": bereich.id,
                                    "nummer": bereich.nummer,
                                    "geometry": bool(
                                        getattr(bereich, "geltungsbereich", None)
                                    ),
                                }
                            )
                        else:
                            logger.warning(f"Bereich with ID {bereich_id} not found.")
                    except Exception as ex:
                        logger.error(
                            f"Error loading bereich with ID {bereich_id}: {ex}",
                            exc_info=True,
                        )

            plan_data = {
                "plan_id": plan.id,
                "plan_name": plan.name,
                "appschema": plan.get_data_type(),
                "version": plan.get_version(),
                "plan_type": plan.get_name(),
                "bereiche": bereiche,
            }
            logger.info(f"Sending plan data to QWebChannel handler: {plan_data}")
            ui.run_javascript(f"""new QWebChannel(qt.webChannelTransport, function (channel) {{
                                        channel.objects.handler.load_plan({plan_data})
                                }});""")
        except Exception as ex:
            logger.error(f"Exception while loading plan: {ex}", exc_info=True)
            ui.notify(f"Fehler beim Laden des Plans: {ex}", type="negative")
        finally:
            e.sender.props(remove="loading")

    def handle_new_plan():
        plan_type = {"type": new_plan_select.value}
        ui.run_javascript(f"""new QWebChannel(qt.webChannelTransport, function (channel) {{
                                    channel.objects.handler.create_plan({plan_type})
                            }});""")

    async def handle_import_plan(e):
        data = io.BytesIO(e.content.read())
        try:
            repo = GMLRepository(data, data_type=appschema)
        except Exception as e:
            print(e)
            return ui.notify("Fehler beim Lesen der Datei", type="negative")
        try:
            collection = await run.io_bound(repo.get_all)
        except Exception as e:
            print(e)
            return ui.notify(
                "Fehler beim Einlesen der FeatureCollection", type="negative"
            )
        try:
            await run.io_bound(settings.repo.save_all, collection)
        except Exception as e:
            print(e)
            return ui.notify(
                "Fehler beim Speichern der FeatureCollection in der Datenbank",
                type="negative",
            )
        ui.notify("Plan wurde importiert", type="positive")
        await update_plan_select_options()

    with ui.grid(rows=2).classes("w-full"):
        with ui.column(align_items="start").classes("w-full"):
            ui.label("Vorhandene Pläne").classes("text-h6")
            plan_select = (
                ui.select({}, label="Plan auswählen", with_input=True)
                .props("loading")
                .classes("w-full")
            )
            with plan_select.add_slot("after"):
                ui.button(icon="refresh", on_click=update_plan_select_options)
            ui.button(
                text="Plan löschen", icon="delete", on_click=handle_delete_plan
            ).bind_enabled_from(plan_select, "value")
            with ui.dropdown_button(
                text="Plan herunterladen", icon="download", auto_close=True
            ).bind_enabled_from(plan_select, "value") as download_dropdown:
                with ui.item(
                    "GML", on_click=lambda format="gml": download_plan(format)
                ):
                    with ui.item_section().props("side"):
                        ui.icon("code")
                with ui.item(
                    "JSON-FG",
                    on_click=lambda format="jsonfg": download_plan(format),
                ):
                    with ui.item_section().props("side"):
                        ui.icon("data_object")
                with ui.item(
                    "GPKG",
                    on_click=lambda format="db": download_plan(format),
                ):
                    with ui.item_section().props("side"):
                        ui.icon("storage")
            if qgis:
                ui.button(
                    "Planlayer laden", icon="map", on_click=handle_load_plan
                ).bind_enabled_from(plan_select, "value")
            ui.separator()
        with ui.column(align_items="start").classes("w-full"):
            ui.label("Neuer Plan").classes("text-h6")
            if qgis:
                new_plan_select = (
                    ui.select(
                        {},
                        label=f"{get_appschema(appschema, version)} Planart auswählen",
                    )
                    .classes("w-full")
                    .props("loading")
                )
                with new_plan_select.add_slot("after"):
                    ui.button(
                        icon="play_circle",
                        on_click=handle_new_plan,
                    ).bind_enabled_from(new_plan_select, "value")
            ui.upload(
                label="GML-Datei importieren",
                on_upload=handle_import_plan,
                on_rejected=lambda: ui.notify("Falscher Dateityp", type="negative"),
                # max_file_size=1000000,
            ).props(
                "accept='text/xml,application/gml+xml,.xml,.gml' flat square bordered"
            ).classes("w-full")
    try:
        await ui.context.client.connected(timeout=10)
    except TimeoutError:
        return
    await update_plan_select_options()
    if qgis:
        await get_model_for_select(
            new_plan_select,
            feature_regex="^.*Plan$",
            appschema=appschema,
            appschema_version=version,
        )
        new_plan_select.props(remove="loading")
        new_plan_select.set_value(new_plan_select.options[0])


@ui.page("/feature/{id}", dependencies=[Depends(enforce_plugin_version)])
async def feature(
    request: Request,
    id: str,
    planId: str | None = None,
    parentId: str | None = None,
    editable: bool = True,
    featureType: str | None = None,
    featuretypeRegex: str | None = None,
    appschema: str | None = None,
    version: str | None = None,
):
    """
    Render and manage a single feature view for the XPlan-GUI application.

    Args:
    request (Request): The incoming FastAPI HTTP request object.
    id (str): UUID or identifier of the feature to display/edit.
    planId (str | None): Optional ID of the associated plan.
    parentId (str | None): Optional ID of the parent feature.
    editable (bool): If `True`, the UI will allow editing; otherwise, it's read-only.
    featureType (str | None): Optional fixed feature type to display.
    featuretypeRegex (str | None): Optional regex to filter allowed feature types.
    appschema (str): The application schema name (defaults from settings).
    version (str): Schema version string (defaults from settings).

    """
    # async def handle_properties_received(event) -> None:
    #     form = app.storage.client["form"]
    #     # wait for form to initialize/let user choose featuretype
    #     while not getattr(form, "feature", None):
    #         await asyncio.sleep(0.5)
    #         # break endless loop if client disconnected (i.e., closed attribute form)
    #         if ui.context.client.id not in ui.context.client.instances.keys():
    #             return
    #     data = form.feature | event.args
    #     geom = data.pop("geometry", None)
    #     if model_geom := form.model.get_geom_field():
    #         data[model_geom] = geom
    #     form.feature.update(data)
    #     form._get_art_options()

    appschema = appschema or settings.appschema
    version = version or settings.appschema_version

    async def get_qgis_feature():
        return await ui.run_javascript(
            """return await new Promise((resolve, reject) => {
                    new QWebChannel(qt.webChannelTransport, function (channel) {
                        channel.objects.handler.transfer_feature().then(data => data ? resolve(data) : reject())
                    })
                });""",
            timeout=3,
        )

    def validate_feature():
        form: ModelForm = app.storage.client["form"]
        if model_instance := form.model_instance:
            feature_data = model_instance.model_dump(
                mode="json",
                exclude_none=True,
                exclude={form.model.get_geom_field()},
            ) | {"featuretype": form.model.get_name()}
            ui.run_javascript(f"""new QWebChannel(qt.webChannelTransport, function (channel) {{
                                        channel.objects.handler.receive_feature({feature_data})
                                }});""")
        else:
            form.radio_filter.set_value("mandatory")

    async def add_form(
        feature_type: str,
        feature: dict,
    ) -> None:
        content.set_visibility(False)
        spinner.set_visibility(True)
        with content:
            await asyncio.sleep(0.1)  # let spinner transfer state to client
            await app.storage.client["form"].render_form(
                editable, feature_type, feature
            )
            if settings.debug:
                with ui.row().classes("w-full"):
                    obj_log = ui.log()
                    ui.button(
                        "show model",
                        on_click=lambda: (
                            obj_log.clear(),
                            obj_log.push(
                                model.model_dump_json(indent=2)
                                if (model := app.storage.client["form"].model_instance)
                                else "No Model",
                            ),
                        ),
                    )
                    ui.button(
                        "show submodels",
                        on_click=lambda: (
                            obj_log.clear(),
                            obj_log.push(
                                "\n".join(
                                    model.model_dump_json()
                                    for model in app.storage.client[
                                        "form"
                                    ].sub_models.values()
                                )
                            ),
                        ),
                    )
        spinner.delete()
        content.set_visibility(True)

    def handle_save():
        form: ModelForm = app.storage.client["form"]
        feature = form.model_instance
        if feature:
            feature.id = id
            settings.repo.update(feature)
            ui.navigate.to(f"/?saved_feature_uuid={feature.id}")

    def handle_delete():
        form: ModelForm = app.storage.client["form"]
        feature = form.model_instance
        if feature:
            settings.repo.delete(id)
            ui.navigate.to("/")

    ui.colors(primary="rgb(157 157 156)", secondary="rgb(229 7 126)")
    app.storage.client["form"] = None
    app.storage.client["plan_id"] = planId
    app.storage.client["parent_id"] = parentId
    app.storage.client["user_agent"] = request.headers.get("user-agent", None)

    qgis = app.storage.client["user_agent"].startswith(settings.qgis_plugin_name)

    ui.colors(
        # primary=f"{'#f0f0f0' if qgis else 'rgb(157 157 156)'}",
        primary="rgb(157 157 156)",
        secondary="rgb(229 7 126)",
    )

    if qgis:
        ui.add_head_html('<script src="qrc:///qtwebchannel/qwebchannel.js"></script>')
        ui.on("validateFeature", validate_feature)

    try:
        model = settings.repo.get(id)
        feature_type = model.get_name()
        feature = model.model_dump(
            mode="json", context={"datatype": True, "file_uri": True}
        )
    except ValueError:
        feature = {"id": id}
        feature_type = featureType

    # ui.on("propertiesReceived", handle_properties_received)

    header = ui.header()  # .classes("bg-white text-black")

    if not qgis:
        with header:
            with ui.column(align_items="center").bind_visibility_from(
                app.storage.client,
                "form",
                backward=lambda form: getattr(form, "rendered", False),
            ):
                with ui.row(align_items="center"):
                    ui.button(
                        text="Speichern",
                        icon="save",
                        on_click=handle_save,
                    ).bind_enabled_from(app.storage.client, "form").props(
                        "unelevated rounded no-caps"
                    )
                    ui.button(
                        text="Löschen",
                        icon="delete",
                        on_click=handle_delete,
                    ).bind_enabled_from(app.storage.client, "form").props(
                        "unelevated rounded no-caps"
                    )
                    ui.button(
                        text="Abbrechen",
                        icon="cancel",
                        on_click=lambda: ui.navigate.to("/"),
                    ).props("unelevated rounded no-caps")
    spinner = ui.spinner(size="xl").classes("absolute-center")
    with ui.grid(columns=2 if settings.debug else 1).classes(
        "justify-center items-start"
    ) as content:
        with ui.column(align_items="center").classes(
            "justify-center"
        ):  # .classes("absolute-center"):
            with ui.row(align_items="center").classes("col-grow") as sel:
                ui.label("Objektart auswählen").classes("text-h6")
                model_select = (
                    ui.select(
                        options=[],
                        value=None,
                        label="Objektarten",
                        on_change=lambda x: add_form(x.value, feature),
                        with_input=True,
                    )
                    .props("square filled options-dense")
                    .style("width: 500px;")
                )
                # .classes("absolute-center")
            if feature_type:
                sel.set_visibility(False)
            else:
                spinner.set_visibility(False)
        app.storage.client["form"] = ModelForm(appschema, version, content, header)
        await ui.context.client.connected(
            timeout=10
        )  # see https://nicegui.io/documentation/page#wait_for_client_connection
        if qgis:
            qgis_feature = await get_qgis_feature()
            if isinstance(properties := qgis_feature.get("properties"), dict):
                feature = feature | properties
            if isinstance(geometry := qgis_feature.get("geometry"), dict):
                feature["geometry"] = geometry
        await get_model_for_select(
            model_select,
            qgis_feature.get("geometry", {}).get("wkt", None) if qgis else None,
            featuretypeRegex,
            appschema,
            version,
        )
        if feature_type:
            await add_form(feature_type, feature)


@ui.page("/feature/{id}/associations", dependencies=[Depends(enforce_plugin_version)])
def get_associations(
    request: Request,
    id: str,
    # wkbType: str | None = None,
    # planId: str | None = None,
    # parentId: str | None = None,
    # editable: bool = True,
    # featureType: str | None = None,
    # featuretypeRegex: str | None = None,
    appschema: str = settings.appschema,
    version: str = settings.appschema_version,
):
    """
    Render the associations view for a given feature in the XPlan‑GUI application.

    Args:
    request (Request): Incoming FastAPI HTTP request object.
    id (str): Identifier or UUID of the feature whose associations will be displayed.
    appschema (str): Application schema name (defaults from settings).
    version (str): Schema version string (defaults from settings).
    """

    def transfer_feature_data():
        ui.run_javascript(f"""new QWebChannel(qt.webChannelTransport, function (channel) {{
                                    channel.objects.handler.handle_feature_creation({feature_data})
                            }});""")

    def handle_assoc_select(e: ValueChangeEventArguments):
        stepper.next()
        feature_data["source"] = {
            "property": e.value,
            "value": feature[e.value],
            "list": model.get_property_info(e.value)["list"],
        }
        prop_info = model.get_property_info(e.value)
        types = prop_info["typename"]
        type_select.set_options(types if isinstance(types, list) else [types])
        if isinstance(types, str):
            type_select.set_value(types)

    def handle_geom_select(geom_regex: str):
        feature_data["geom_regex"] = geom_regex
        transfer_feature_data()

    def handle_type_select(e: ValueChangeEventArguments):
        featuretype = e.value
        feature_data["featuretype"] = featuretype
        source_prop = prop_select.value
        target_model = model_factory(featuretype, version, appschema)
        if (assoc_info := model.get_property_info(source_prop)["assoc_info"]) and (
            target_prop := assoc_info["reverse"]
        ):
            target_prop_info = target_model.get_property_info(target_prop)
            feature_data[target_prop] = [id] if target_prop_info["list"] else id
        geom_types = target_model.get_geom_types()
        if not geom_types:
            transfer_feature_data()
        else:
            geom_required = not target_model.get_property_info(
                target_model.get_geom_field()
            )["nullable"]
            type_regex_mapping = {
                geom_type.get_name(): geom_type.model_fields["wkt"].metadata[0].pattern
                for geom_type in geom_types
            }
            if not geom_required:
                type_regex_mapping["Keine Geometrie"] = "NOGEOMETRY"
            if len(geom_types) == 1 and geom_required:
                feature_data["geom_regex"] = list(type_regex_mapping.values())[0]
                transfer_feature_data()
            else:
                with stepper:
                    with ui.step("Geometrieart auswählen") as geom_step:
                        ui.label("Geometrieart des neuen Features auswählen")
                        ui.radio(
                            {
                                geom_type: geom_type.replace("PolygonObject", "Fläche")
                                .replace("PointObject", "Punkt")
                                .replace("LineObject", "Linie")
                                for geom_type in type_regex_mapping.keys()
                            },
                            on_change=lambda e: handle_geom_select(
                                type_regex_mapping[e.value]
                            ),
                        ).props("inline")
                stepper.set_value(geom_step)

    ui.colors(primary="rgb(157 157 156)", secondary="rgb(229 7 126)")
    ui.button.default_props("flat square no-caps")
    ui.dropdown_button.default_props("flat square no-caps")
    ui.select.default_props("square filled dense").default_classes("w-full")

    app.storage.client["user_agent"] = request.headers.get("user-agent", None)

    qgis = app.storage.client["user_agent"].startswith(settings.qgis_plugin_name)

    feature_data = {}

    if qgis:
        ui.add_head_html('<script src="qrc:///qtwebchannel/qwebchannel.js"></script>')

    try:
        model = settings.repo.get(id)
        # feature_type = model.get_name()
        feature = model.model_dump(mode="json")
    except ValueError:
        ui.label("Feature nicht gefunden")
        return
    assocs = model.get_associations()
    if not assocs:
        ui.label("Feature verfügt über keine Assoziationen")
        return
    with ui.stepper().props("vertical flat").classes("w-full") as stepper:
        with ui.step("Attribut auswählen"):
            ui.label(
                "Assoziationsattribut, für das ein neues Feature erzeugt werden soll, auswählen"
            )
            with ui.stepper_navigation():
                prop_select = ui.select(
                    assocs, on_change=handle_assoc_select, with_input=True
                )
        with ui.step("Featuretype auswählen"):
            ui.label("Featuretype des neuen Features auswählen")
            with ui.stepper_navigation():
                type_select = ui.select(
                    [], on_change=handle_type_select, with_input=True
                )
        # with ui.step("Bake"):
        #     ui.label("Bake for 20 minutes")
        #     with ui.stepper_navigation():
        #         ui.button("Done", on_click=lambda: ui.notify("Yay!", type="positive"))
        #         ui.button("Back", on_click=stepper.previous).props("flat")


@app.get("/health_check")
def health_check() -> str:
    """
    Health check endpoint to verify that the service is running.

    Returns:
        str: A simple "OK" response indicating the application is healthy.
    """
    return "OK"


# TODO replace with QWebChannel funcionality
@app.post("/validate/{featuretype}")
def validate_featuretype(
    featuretype: str,
    featureData: dict[str, Any],
    appschema: str = settings.appschema,
    version: str = settings.appschema_version,
) -> str:
    """
    Validate feature data against the model.

    Args:
    featuretype (str): The type of the feature to validate (path parameter).
    featureData (dict[str, Any]): Raw feature data to be validated.
    appschema (str): Application schema name (default from settings).
    version (str): Schema version string (default from settings).
    """
    # print(featureData)
    featureData.pop("featuretype", None)
    try:
        model = model_factory(featuretype, version, appschema)
        if (geom_field := model.get_geom_field()) and (
            geom := featureData.pop("geometry", None)
        ):
            featureData[geom_field] = geom
        model.model_validate(featureData)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "errors": e.errors(),
            },
        )
    return "OK"


@app.post(
    "/insert-features", status_code=201, dependencies=[Depends(enforce_plugin_version)]
)
async def insert_features(payload: InsertPayload):
    """Insert a number of features."""
    await crud.create(payload)


@app.post("/update-features", dependencies=[Depends(enforce_plugin_version)])
async def update_features(payload: UpdatePayload):
    """Update a number of features."""
    await crud.update(payload)


@app.post(
    "/split-tool",
    response_model=SplitSuccess,
    status_code=status.HTTP_201_CREATED,  # semantically 'created'
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
        500: {"model": ErrorResponse, "description": "Server Error"},
    },
    dependencies=[Depends(enforce_plugin_version)],
)
async def receive_split_plans(payload: SplitPayload) -> SplitSuccess:
    logger.info("Split plans endpoint reached.")

    API_VERSION = "split-import-v1-min"

    # Lightweight contract check up front
    if payload.schema_version != API_VERSION:
        logger.error("Payload api schema version incorrect.")
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail(
                code="invalid_schema_version", message="Invalid schema_version"
            ).model_dump(),
        )

    # Early existence check to short-circuit before the service
    try:
        source_plan = settings.repo.get_plan_by_id(payload.src_plan_id)
        if source_plan is None:
            logger.error("Couldn't load plan from database with provided id.")
            raise HTTPException(
                status_code=400,
                detail=ErrorDetail(
                    code="plan_not_found", message="Plan not found"
                ).model_dump(),
            )
    except (pydantic.ValidationError, pydantic_core.ValidationError) as e:
        logger.error(f"Plan validation failed: {e}")
        raise HTTPException(
            status_code=422,
            detail=ErrorDetail(code="validation_error", message=str(e)).model_dump(),
        )

    service = PlanSplitService(settings.repo)

    try:
        return service.apply_split_import(payload, source_plan)
    except SplitValidationError as e:
        logger.warning("Split validation failed with %d violations", len(e.violations))
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail(
                code="validation_failed",
                message=e.message,
                violations=[
                    {
                        "code": v.code,
                        "featuretype": v.featuretype,
                        "old_id": v.old_id,
                        "hint": v.hint,
                    }
                    for v in e.violations
                ],
            ).model_dump(),
        )
    except ValueError as e:
        logger.error("Domain error during split: %s", e)
        raise HTTPException(
            status_code=400,
            detail=ErrorDetail(code="domain_error", message=str(e)).model_dump(),
        )
    except Exception as e:
        logger.exception(
            "Unhandled split processing error. "
            "Likely dangling association reference. "
            "Check for edges whose dst_old not in id_map."
        )
        raise HTTPException(
            status_code=500,
            detail=ErrorDetail(
                code="server_error", message=f"Processing error: {e}"
            ).model_dump(),
        ) from e


@asynccontextmanager
async def lifespan(starlette_app):
    msg = (
        f"XMAS-App is running on port {settings.app_port} in {settings.app_mode} mode."
    )
    logger.info(msg)
    print(msg)
    yield
    logger.info("XMAS-App is shutting down.")
    print("XMAS-App is shutting down.")


starlette_app = Starlette(
    debug=settings.debug,
    routes=None,
    lifespan=lifespan,
)
ui.run_with(starlette_app)


def create_app() -> Starlette:
    """Factory for the plugin: return the ASGI app, without asyncio or uvicorn."""

    # os.environ["PYGEOAPI_CONFIG"] = str(Path(__file__).parent / "pygeoapi" / "config.yaml")
    # os.environ["PYGEOAPI_OPENAPI"] = str(
    #     Path(__file__).parent / "pygeoapi" / "openapi.yaml"
    # )
    # from pygeoapi.starlette_app import APP as pygeoapi_app

    # starlette.mount("/oapi", pygeoapi_app)

    return starlette_app


def run_server():
    import uvicorn

    print("Starting server in stand alone mode.")
    logger.info("Starting server in stand alone mode.")

    try:
        uvicorn.run(
            "xmas_app.main:starlette_app",
            host="0.0.0.0",
            port=settings.app_port,
            reload=settings.app_mode == "dev",
            log_config=None,  # avoids isatty() issue
        )
    except Exception as e:
        msg = f"Failed to start server: {e}"
        print(msg)
        logger.error(msg)


if __name__ == "__main__":
    run_server()
