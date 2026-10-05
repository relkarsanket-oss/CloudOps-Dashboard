from datetime import datetime

from pydantic import BaseModel


class EC2Resource(BaseModel):
    instance_id: str | None = None
    instance_type: str | None = None
    state: str | None = None
    private_ip: str | None = None
    public_ip: str | None = None


class RDSResource(BaseModel):
    db_instance_identifier: str | None = None
    engine: str | None = None
    status: str | None = None
    instance_class: str | None = None
    endpoint: str | None = None


class S3Resource(BaseModel):
    name: str | None = None
    creation_date: datetime | str | None = None


class ResourceResponse(BaseModel):
    resources: list[EC2Resource | RDSResource | S3Resource]


class ResourceError(BaseModel):
    status: str
    message: str