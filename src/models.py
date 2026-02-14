from pydantic import BaseModel, Field
from typing import List, Literal
from uuid import uuid4


class InstanceType(BaseModel):
    name: str
    cpu: int
    ram_gb: int
    supported_os: List[str]


class UserRequest(BaseModel):
    os_type: str
    min_cpu: int
    min_ram: int


class ProvisionedInstance(BaseModel):
    id: int
    instance_type: str
    cpu: int
    ram_gb: int
    os_type: str
    status: Literal["running", "stopped"]