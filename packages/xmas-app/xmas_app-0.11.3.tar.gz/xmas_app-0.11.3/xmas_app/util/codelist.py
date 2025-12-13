import logging

import httpx
from nicegui import app

from xmas_app.settings import settings

logger = logging.getLogger("xmas_app")

app.storage.general.setdefault("codelists", {})

CODELIST_CACHE = app.storage.general["codelists"]


async def get_codelist_options(
    values: str | list[str], codelist: str
) -> dict[str, str] | list[str]:
    CODELIST_URL = f"{settings.codelist_repo}/{codelist}"
    if not CODELIST_CACHE.get(codelist):
        async with httpx.AsyncClient(timeout=1.0) as client:
            try:
                response = await client.get(f"{CODELIST_URL}/{codelist}.de.json")
                response.raise_for_status()
            except httpx.RequestError as e:
                logger.error(f"Network error while fetching codelist: {e}")
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error {e.response.status_code} while fetching codelist"
                )
            except Exception:
                logger.exception("unknown error while loading codelist")
            else:
                CODELIST_CACHE[codelist] = response.json()
    content = CODELIST_CACHE.get(codelist, {})
    options = {}
    try:
        for item in content.get("de.xleitstelle.xplanung", {}).get(
            "containeditems", []
        ):
            value = item["value"]
            options[value["id"]] = (
                f"{value['label']['text']} ({value['CodeListValue_Local_Id']['text']})"
            )
    except Exception:
        logger.exception("error during parsing of codelist values")
    if isinstance(values, str):
        values = [values]
    if values:
        keys = options.keys()
        for value in values:
            if value not in keys:
                try:
                    code = value.split("/")[-1]
                except Exception:
                    code = value
                options[value] = f"{code} (lokaler Code)"
    return options
