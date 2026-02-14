from models import ProvisionedInstance

def find_matching_instance(catalog, request):
    for instance in catalog:
        if (
            instance["cpu"] >= request.min_cpu
            and instance["ram_gb"] >= request.min_ram
            and request.os_type in instance["supported_os"]
        ):
            return instance
    return None


def create_instance(instance_type, os_type, state_data):
    new_id = state_data["last_id"] + 1
    state_data["last_id"] = new_id

    new_instance = ProvisionedInstance(
        id=new_id,
        instance_type=instance_type["name"],
        cpu=instance_type["cpu"],
        ram_gb=instance_type["ram_gb"],
        os_type=os_type,
        status="running",
    )

    state_data["instances"].append(new_instance.model_dump())
    return new_instance

def change_instance_status(instance_id, new_status, state_data):
    for instance in state_data["instances"]:
        if instance["id"] == instance_id:
            instance["status"] = new_status
            return True
    return False