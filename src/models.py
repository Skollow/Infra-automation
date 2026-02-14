from pydantic import BaseModel
from typing import Optional 

class Ec2Instance(BaseModel):
    instance_id: str
    instance_type: str
    state: str
    name: Optional[str] = None

def extract_name_from_tags(instance_dict: dict) -> Optional[str]:
    tags = instance_dict.get("Tags", [])
    for tag in tags:
        if tag.get("Key") == "Name":
            return tag.get("Value")
    return None

def ec2_dict_to_model(instance_dict: dict) -> Ec2Instance:
    return Ec2Instance(
        instance_id=instance_dict["InstanceId"],
        instance_type=instance_dict["InstanceType"],
        state=instance_dict["State"]["Name"],
        name=extract_name_from_tags(instance_dict),
    )
