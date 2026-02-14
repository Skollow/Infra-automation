import json
import boto3 
from log import logger, setup_logging
from dotenv import load_dotenv
from argparse import ArgumentParser
from models import Ec2Instance, ec2_dict_to_model

load_dotenv()
setup_logging()

logger.info("Application started")

def get_ec2_instances(ec2) -> list[Ec2Instance]:
    if ec2 is None:
        with open("ec2.json") as f:
            response = json.load(f)
    else:
        response = ec2.describe_instances()

    instances = []
    for res in response["Reservations"]:
        for instance in res["Instances"]:
            instances.append(ec2_dict_to_model(instance))

    return instances

def start_instances(ec2, ids: list[str]):
    response = ec2.start_instances(InstanceIds=ids)
    logger.info(f"AWS response: {response}")

def stop_instances(ec2, ids: list[str]):
    response = ec2.stop_instances(InstanceIds=ids)
    logger.info(f"AWS response: {response}")

def is_instance_running(instance: dict) -> bool:
    return instance["State"]["Name"] == "running"

def get_running_instances(instances: list[dict]) -> dict:
    result = {
        "total": len(instances),
        "running": 0
    }
    # running = filter(is_instance_running, instances)
    # result["running"] = len(list(running))
    for instance in instances:
        if instance.state == "running":
            result["running"] += 1
    return result

def print_all_instances(instances: list[dict]):
    for number, instance in enumerate(instances):
        instance_type = instance.instance_type
        instance_id = instance.instance_id
        state = instance.state.capitalize()
        entry = f"{number + 1}. {instance_type} ({instance_id}) - {state}"
        logger.info(entry)

def flip_instance_state(instance: dict):
    if instance["State"]["Name"] == "running":
        logger.info("Stopping instance")
    else:
        logger.info("Starting instance")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--start", nargs="+")
    parser.add_argument("--stop", nargs="+")
    args = parser.parse_args()

    ec2 = boto3.client("ec2")

    # python ec2.py
    # List all the ec2 computer ids, type and their state
    # Example:
    # 1. t2.micro (i-06d82e42d46fed971) - Running
    # 2. t2.micro (i-0c5800ab649371e2c) - Stopped
    # Choose a machine to change state (from running to stopped, or from stopped to running): 1
    instances = get_ec2_instances(ec2)
    running = get_running_instances(instances)
    # before logging: print(running)
    logger.info(f"Running instances summary: {running}")
    print_all_instances(instances)
    if not args.list:
        # python ec2.py --list
        # Only print the list of states, without waiting for user input, and exit
        while True:
            user_choice = input("Choose a machine to change state (running=>stopped, or stopped=>running): ")
            try:
                user_choice = int(user_choice)
                if user_choice > len(instances) or user_choice <= 0:
                    logger.warning("User selected a number out of range")
                else:
                    break
            except ValueError:
                logger.warning("User entered non-numeric input")
        flip_instance_state(instances[user_choice - 1])

    # python ec2.py --start i-06d82e42d46fed971 i-0c5800ab649371e2c
    if args.start:
        start_instances(ec2, args.start)
    # python ec2.py --stop i-06d82e42d46fed971 i-0c5800ab649371e2c
    if args.stop:
        stop_instances(ec2, args.stop)
