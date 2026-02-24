from pydantic import BaseModel
from typing import List, Literal


class InstanceType(BaseModel):
    name: str
    cpu: int
    ram_gb: int
    supported_os: List[Literal["linux", "windows"]]


class UserRequest(BaseModel):
    os_type: Literal["linux", "windows"]
    min_cpu: int
    min_ram: int


class ProvisionedInstance(BaseModel):
    id: int
    instance_type: str
    cpu: int
    ram_gb: int
    os_type: Literal["linux", "windows"]
    status: Literal["running", "stopped"]