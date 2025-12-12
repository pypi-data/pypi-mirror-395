from __future__ import annotations

from pydantic import BaseModel
from typing import Any, Literal


class ProjectResourceStatus(BaseModel):
    kind: Literal["Database", "StorageBucket", "Secret"]
    name: str
    status: Literal["Pending", "Available", "Error"] = "Pending"
    aws_id: str | None = None
    description: str | None = None


class ProjectRunningStatus(BaseModel):
    current: Literal["Pending", "Running", "Stopped", "Error"] = "Pending"
    deployment_revision: int | None = None
    last_updated: str | None = None
    public_ip: str | None = None

    port_mappings: list[PortMapping] | None = None
    cpu: str | None = None
    memory: str | None = None


class ProviderConfig(BaseModel):
    provider: Literal["aws"] = "aws"
    region: str | None = "eu-west-2"


class PortMapping(BaseModel):
    container_port: int
    host_port: int
    protocol: Literal["tcp", "udp"] = "tcp"


class GetHealthResponse(BaseModel):
    status: str
    details: dict[str, Any] = {}


class PutProjectResponse(BaseModel):
    deployment_id: str
    status: str


class PutSecretValueRequest(BaseModel):
    secret_name: str
    secret_string: str


class PostDeploymentResponse(BaseModel):
    revision: int
    image: str
    status: str
    push_token: str | None = None


class GetProjectResponse(BaseModel):
    name: str
    kind: Literal["Service"] = "Service"
    provisioning_state: str
    running_status: ProjectRunningStatus
    resources: list[ProjectResourceStatus]
    port_mappings: list[PortMapping]
    cloud_provider: ProviderConfig
    cpu: str
    memory: str


class ListProjectsResponse(BaseModel):
    projects: list[GetProjectResponse]


class PutProjectRequest(BaseModel):
    kind: Literal["Service"]
    name: str
    resources: list[DatabaseResource | StorageBucketResource | SecretResource] = []
    cloud_provider: ProviderConfig = ProviderConfig()
    port_mappings: list[PortMapping] = [
        PortMapping(container_port=8080, host_port=8080)
    ]
    cpu: str = "256"
    memory: str = "512"


class DatabaseResource(BaseModel):
    kind: Literal["Database"]
    name: str


class StorageBucketResource(BaseModel):
    kind: Literal["StorageBucket"]
    name: str


class SecretResource(BaseModel):
    kind: Literal["Secret"]
    name: str
    value_string: str | None = None


class GetLogsResponse(BaseModel):
    logs: list[str]


class ListBucketKeysResponse(BaseModel):
    keys: list[str]


class GetDatabaseConnectionInfoResponse(BaseModel):
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_mode: str = "require"
