from log import logger, setup_logging

setup_logging()

logger.info("Application started")

def cpu_category(instance_type: str) -> str:
    if instance_type in ["t2.micro"]:
        return "low"
    elif instance_type in ["t2.small"]:
        return "medium"
    else:
        return "high"
    
def select_instance(data: dict, preferences):
    for reservation in data["Reservations"]:
        for instance in reservation["Instances"]:
            try:
                # CPU check
                if cpu_category(instance["InstanceType"]) != preferences.cpu_power:
                    continue

                # Environment Tag check
                tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
                if tags.get("Environment") != preferences.environment:
                    continue

                logger.info(f"Instance selected: {instance['InstanceId']}")
                return instance

            except KeyError as e:
                logger.error(f"Missing key in instance: {e}")

    logger.warning("No matching instance found")
    return None