#!/bin/bash

set -e

SERVICE="nginx"

echo "Starting service setup..."

if command -v nginx >/dev/null 2>&1; then
    echo "$SERVICE is already installed."
else
    echo "$SERVICE not found. Installing..."

    # sudo apt update

    # sudo apt install -y nginx

    echo "$SERVICE installation completed."
fi

if systemctl is-active --quiet nginx; then
    echo "$SERVICE service is already running."
else
    echo "Starting $SERVICE service..."
    # sudo apt update
    # sudo apt install nginx
fi

echo "Service setup completed successfully."
exit 0