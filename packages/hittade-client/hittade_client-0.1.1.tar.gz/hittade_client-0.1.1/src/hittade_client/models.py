"""Pydantic models for the Hittade API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BasicAuth(BaseModel):
    """Basic authentication credentials."""

    username: str
    password: str


class HostSchema(BaseModel):
    """Host schema."""

    id: str
    hostname: str
    model_config = ConfigDict(coerce_numbers_to_str=True)


class PagedHostSchema(BaseModel):
    """Paged host schema."""

    items: list[HostSchema]
    count: int
    limit: int
    offset: int


class HostConfigurationSchema(BaseModel):
    """Host configuration schema."""

    ctype: str
    name: str
    value: str


class HostDetailsSchema(BaseModel):
    """Host details schema."""

    time: datetime
    domain: str | None
    osname: str
    osrelease: str
    rkr: str
    cosmosrepourl: str
    ipv4: str | None
    ipv6: str | None
    fail2ban: bool


class PackageSchema(BaseModel):
    """Package schema."""

    id: int
    name: str
    version: str


class ServerContainerSchema(BaseModel):
    """Server container schema."""

    image: str
    imageid: str


class CombinedHostSchema(BaseModel):
    """Combined host schema."""

    host: HostSchema
    details: HostDetailsSchema
    packages: list[PackageSchema]
    containers: list[ServerContainerSchema]
    configs: list[HostConfigurationSchema]
