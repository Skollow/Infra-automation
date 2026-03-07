# infra automation project 1

This project simulates a simple infrastructure automation tool that allows users to create, stop, start, and manage virtual instances.

The system also demonstrates how a Python provisioning workflow can trigger a Bash script to configure services automatically.

---

## Project Features

- Create instances based on:
  - OS
  - CPU
  - RAM
  - or by choosing a predefined instance type
- Stop running instances
- Restart stopped instances
- Display all instances and their status
- Execute a Mock Bash script after provisioning to simulate service installation (will be changed to working script in WCL if need arises)
---

## Requirements

- Python 3.10+
- Git Bash (for running the Bash script on Windows)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Skollow/Infra-automation
cd infra_automation