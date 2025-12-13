from fastapi import Header, HTTPException
from semver import format_version, parse

from xmas_app.settings import settings


async def enforce_plugin_version(
    user_agent: str = Header(...),
):
    if not user_agent.startswith(settings.qgis_plugin_name):
        return
    try:
        _, plugin_version = user_agent.split("/")
        client_v = parse(plugin_version)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {settings.qgis_plugin_name} user-agent header: '{user_agent}'",
        )

    if client_v < settings.qgis_plugin_min_version:
        # 426 Upgrade Required is appropriate
        raise HTTPException(
            status_code=426,
            detail=f"Plugin version {settings.qgis_plugin_min_version}+ required, got {format_version(**client_v)}",
        )
