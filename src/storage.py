import json

CATALOG_FILE = "configs/ec2_instance_catalog.json"
STATE_FILE = "configs/instances.json"


def load_catalog():
    with open(CATALOG_FILE) as f:
        return json.load(f)["instances"]


def load_state():
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)