from models import UserRequest
from storage import load_catalog, load_state, save_state
from provisioner import find_matching_instance, create_instance, change_instance_status


def create_flow():
    catalog = load_catalog()
    state = load_state()

    os_type = input("OS (linux/windows): ").lower()
    min_cpu = int(input("Minimum CPU cores: "))
    min_ram = int(input("Minimum RAM (GB): "))

    request = UserRequest(
        os_type=os_type,
        min_cpu=min_cpu,
        min_ram=min_ram,
    )

    match = find_matching_instance(catalog, request)

    if not match:
        print("❌ No suitable instance found.")
        return

    new_instance = create_instance(match, os_type, state)
    save_state(state)

    print(f"\n✅ Instance #{new_instance.id} created.")


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
    except ValueError:
        print("Invalid input.")
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

def main():
    while True:
        print("\n==== EC2 Simulator ====")
        print("1 - Create Instance")
        print("2 - Stop Instance")
        print("3 - Start Instance")
        print("4 - Exit")

        choice = input("Choice: ")

        if choice == "1":
            create_flow()
        elif choice == "2":
            stop_flow()
        elif choice == "3":
            start_flow()
        elif choice == "4":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()