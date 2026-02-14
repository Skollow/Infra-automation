import json
from log import logger, setup_logging
from models import ec2_dict_to_model

setup_logging()

logger.info("Application started")

#code to check that models.py works as intended
with open("configs\ec2.json") as f:
    response = json.load(f)

first_instance = response["Reservations"][0]["Instances"][0]

model = ec2_dict_to_model(first_instance)
# before logging: print(model.model_dump_json(indent=2))
logger.info("Pydantic model output:\n%s", model.model_dump_json(indent=2))