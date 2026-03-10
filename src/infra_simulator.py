import subprocess
from pathlib import Path
from log import setup_logger
from machine import UserRequest
from storage import load_catalog, load_state, save_state
from provisioner import find_matching_instance, create_instance, change_instance_status
from pydantic import ValidationError
from uuid import uuid4

logger = setup_logger()

def run_post_provision_script():
    project_root = Path(__file__).resolve().parent.parent
    script_path = project_root / "scripts" / "setup_services.sh"

    try:
        result = subprocess.run(
            ["bash", str(script_path)], 
            check=True,
            capture_output=True,
            text=True
        )

        logger.info("Post-provision script completed successfully")
        logger.debug(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        logger.error("Script failed")
        logger.error(e.stderr)
        return False

    except FileNotFoundError:
        logger.error(f"Script not found at {script_path}")
        return False

def choose_requirements_flow():
    correlation_id = str(uuid4())
    logger.info(f"[{correlation_id}] | Provisioning STARTED - User chose to create an instance by defining attributes.")

    try: 
        catalog = load_catalog()
        state = load_state()

        while True:
            allowed_os = {"linux", "windows"}
            os_type = input("OS (linux/windows): ").lower()
            if os_type not in allowed_os:
                print("❌ Please choose from the supported options.")
                logger.error(f"[{correlation_id}] | Error: unsupported OS chosen: {os_type}")
                continue 
            break
        
        while True:
            try:
                min_cpu = int(input("Minimum CPU cores (1/2):"))

                if min_cpu not in range(1, 3):
                    print("❌ Invalid selection. Please choose either 1 or 2.")
                    logger.warning(f"[{correlation_id}] | Invalid instance selection: {min_cpu}")
                    continue
                break
            except ValueError:
                print("❌ Input must be valid.")
                logger.error(f"[{correlation_id}] | Error: non-valid input (either 1 or 2).")
        
        while True:
            try:
                allowed_ram = {1, 2, 4, 8}
                min_ram = int(input("Minimum RAM (1/2/4/8): "))

                if min_ram not in allowed_ram:
                    print("❌ Invalid selection. Please choose either 1, 2, 4, 8.")
                    logger.warning(f"[{correlation_id}] | Invalid instance selection: {min_ram}")
                    continue
                break
            except ValueError:
                print("❌ Input must be valid.")
                logger.error(f"[{correlation_id}] | Error: non-valid input (either 1, 2, 4, 8).")

        request = UserRequest(
            os_type=os_type,
            min_cpu=min_cpu,
            min_ram=min_ram,
        )

        match = find_matching_instance(catalog, request)

        if not match:
            logger.error(f"[{correlation_id}] | No suitable instance found for user input. Creation proccess stopped.")
            return

        new_instance = create_instance(match, os_type, state)
        save_state(state)

        success = run_post_provision_script()

        if not success:
            print("⚠ Service setup failed. Check logs.")

        logger.info(
        f"[{correlation_id}] | Provisioning SUCCESS | "
        f"Instance created | ID={new_instance.id} | "
        f"Type={new_instance.instance_type} | "
        f"OS={new_instance.os_type}"
        )
        
        print(f"\n✅ Instance #{new_instance.id} created.")
        print(f"Type: {new_instance.instance_type}")
        print(f"Status: {new_instance.status}")

    except ValidationError as e:
        logger.error(f"[{correlation_id}] | Error: invalid input: {e}. Provisioning stopped.")

    except ValueError as e:
        logger.error(f"[{correlation_id}] | Error: non-numeric input: {e}. Provisioning stopped.")

    except Exception as e:
        logger.error(f"[{correlation_id}] | Unexpected error during provisioning process: {e}. Provisioning stopped.")

def choose_machine_flow():
    correlation_id = str(uuid4())

    logger.info(f"[{correlation_id}] | Provisioning STARTED - User chose to create an instance by choosing TYPE.")

    catalog = load_catalog()
    state = load_state()

    if not catalog:
        print("No instance types available.")
        return

    print("\nAvailable Instance Types:")

    for idx, instance in enumerate(catalog, start=1):
        print(
            f"{idx} - {instance['name']} "
            f"| CPU: {instance['cpu']} "
            f"| RAM: {instance['ram_gb']}GB "
            f"| OS: {instance['supported_os']}"
        )

    while True:
        try:
            choice = int(input("\nSelect instance number (1-4): "))

            if choice not in range(1, 5):
                print("❌ Invalid selection. Please choose a number between 1 and 4.")
                logger.warning(f"[{correlation_id}] | Invalid instance selection: {choice}")
                continue

            selected_instance = catalog[choice - 1]
            break

        except ValueError:
            print("❌ Input must be a number.")
            logger.error(f"[{correlation_id}] | Error: non-valid input (number between 1 to 4).")

    
    while True:
        print(f"\nSupported OS: {', '.join(selected_instance['supported_os'])}")

        os_type = input("Select OS: ").lower()

        if os_type not in selected_instance["supported_os"]:
            print("❌ Unsupported OS. Please choose from the supported options.")
            logger.error(f"[{correlation_id}] | Error: unsupported OS chosen: {os_type}")
            continue

        break

    new_instance = create_instance(selected_instance, os_type, state)
    save_state(state)

    success = run_post_provision_script()

    if not success:
        print("⚠ Service setup failed. Check logs.")

    print(f"\n✅ Instance #{new_instance.id} created.")
    print(f"Type: {new_instance.instance_type}")
    print(f"Status: {new_instance.status}")
    
    logger.info(
        f"[{correlation_id}] | Provisioning SUCCESS | "
    f"Instance created | ID={new_instance.id} | "
    f"Type={new_instance.instance_type} | "
    f"OS={new_instance.os_type}"
    )

def stop_flow():
    state = load_state()

    running_instances = [
        i for i in state["instances"] if i["status"] == "running"
    ]

    if not running_instances:
        print("No running instances available.")
        return

    print("\nRunning Instances:")
    for inst in running_instances:
        print(
            f"ID: {inst['id']} | {inst['instance_type']} | {inst['os_type']}"
        )

    try:
        chosen_id = int(input("Enter ID to stop: "))
    except ValidationError as e:
        print("\n❌ Invalid input:")
        print(e)
        return
    except ValueError:
        print("\n❌ Input must be numeric.")
        return

    success = change_instance_status(chosen_id, "stopped", state)

    if success:
        save_state(state)
        print(f"⏹ Instance #{chosen_id} stopped.")
    else:
        print("Instance not found.")

def start_flow():
    state = load_state()

    stopped_instances = [
        i for i in state["instances"] if i["status"] == "stopped"
    ]

    if not stopped_instances:
        print("No stopped instances available.")
        return

    print("\nStopped Instances:")
    for inst in stopped_instances:
        print(
            f"ID: {inst['id']} | {inst['instance_type']} | {inst['os_type']}"
        )

    try:
        chosen_id = int(input("Enter ID to start: "))
    except ValueError:
        print("Invalid input.")
        return

    success = change_instance_status(chosen_id, "running", state)

    if success:
        save_state(state)
        print(f"▶ Instance #{chosen_id} started.")
    else:
        print("Instance not found.")

def list_all_instances_flow():
    state = load_state()

    instances = state.get("instances", [])

    if not instances:
        print("\nNo instances found.")
        return

    print("\n==== All Provisioned Instances ====")

    for inst in instances:
        print(
            f"ID: {inst['id']} | "
            f"Type: {inst['instance_type']} | "
            f"CPU: {inst['cpu']} | "
            f"RAM: {inst['ram_gb']}GB | "
            f"OS: {inst['os_type']} | "
            f"Status: {inst['status']}"
        )

def main():
    while True:
        print("\n==== EC2 Simulator ====")
        print("Which action would you like to perform?")
        print("1 - Create an instance by defining OS, CPU, RAM")
        print("2 - Create by Instance by choosing its TYPE from a list")
        print("3 - Stopping a running Instance")
        print("4 - Starting a stopped Instance")
        print("5 - List All Instances")
        print("6 - Exit")

        choice = input("Choice: ")

        if choice == "1":
            print("You chose to create a machine by defining OS, CPU, RAM.")
            choose_requirements_flow()
        elif choice == "2":
            print("You chose to create a machine by its type.")
            choose_machine_flow()
        elif choice == "3":
            print("You chose to stop a running instance.")
            stop_flow()
        elif choice == "4":
            print("You chose to turn on an instance.")
            start_flow()
        elif choice == "5":
            list_all_instances_flow()
        elif choice == "6":
            print("Thank you for using infra-automation, bye.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()