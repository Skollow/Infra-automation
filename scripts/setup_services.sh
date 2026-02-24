#!/bin/bash

set -e

echo "Starting service configuration..."

install_if_missing() {
    PACKAGE=$1

    if dpkg -s "$PACKAGE" &> /dev/null; then
        echo "$PACKAGE already installed."
    else
        echo "Installing $PACKAGE..."
        sudo apt-get update -y
        sudo apt-get install -y "$PACKAGE"
    fi
}

install_if_missing nginx
install_if_missing curl

echo "Service configuration completed."