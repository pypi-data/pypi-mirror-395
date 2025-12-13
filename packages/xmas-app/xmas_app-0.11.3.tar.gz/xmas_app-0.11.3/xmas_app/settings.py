import os
from typing import Any, Dict, List, Literal, Optional, TypedDict

from pydantic import HttpUrl
from pydantic_extra_types.semver import _VersionPydanticAnnotation
from pydantic_settings import BaseSettings, SettingsConfigDict
from semver import Version
from xplan_tools.interface.db import DBRepository


class AppSchema(TypedDict):
    type: str
    versions: List[str]


APPSCHEMAS: Dict[str, AppSchema] = {
    "XPlanung": {"type": "xplan", "versions": ["5.4", "6.0"]},
    "XTrasse": {"type": "xtrasse", "versions": ["2.0"]},
}


def get_appschema(schema_type: str, version: str):
    try:
        name = next(
            filter(
                lambda key: APPSCHEMAS[key]["type"] == schema_type, APPSCHEMAS.keys()
            )
        )
        if version not in APPSCHEMAS[name]["versions"]:
            raise ValueError(f"Invalid version for Appschema {name}")
    except (StopIteration, ValueError):
        return None
    else:
        return f"{name} {version}"


class Settings(BaseSettings):
    debug: bool = False

    PGUSER: Optional[str] = None
    PGPASSWORD: Optional[str] = None
    PGHOST: Optional[str] = None
    PGPORT: Optional[str] = None
    PGDATABASE: Optional[str] = None
    PGSERVICE: Optional[str] = None

    appschema: Literal["xplan", "xtrasse"]
    appschema_version: Literal["2.0", "5.4", "6.0"]
    app_port: int
    db_type: str = "postgres"  # defaulting to postgres
    app_mode: Literal["dev", "prod"] = "prod"
    srid: int = 25832
    repo: DBRepository | None = None
    codelist_repo: HttpUrl = HttpUrl(
        "https://registry.gdi-de.org/codelist/de.xleitstelle.xplanung"
    )
    qgis_plugin_name: str = "XMAS-Plugin"
    qgis_plugin_min_version: _VersionPydanticAnnotation = Version(major=0, minor=10)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def model_post_init(self, context: Any):
        """Set environment variables and initialize repo at startup."""
        os.environ.update(
            self.model_dump(
                include={
                    "PGUSER",
                    "PGHOST",
                    "PGPASSWORD",
                    "PGPORT",
                    "PGDATABASE",
                    "PGSERVICE",
                },
                exclude_none=True,
            )
        )
        self.repo = DBRepository(
            "postgresql://",
            self.appschema_version,
            self.appschema,
            srid=self.srid,
            with_views=True,
        )


settings = Settings()
