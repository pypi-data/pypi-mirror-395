#!/usr/bin/env bash

set -euo pipefail

echo "Starting Outline Server installation..."
sudo bash -c "$(wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh)" > ./outline-install.log
echo "Outline Server installation completed."
echo "Retrieving self-signed certificate..."
sudo cp /opt/outline/persisted-state/shadowbox-selfsigned.crt .
MYUSER=$(whoami)
sudo chown ${MYUSER}:${MYUSER} shadowbox-selfsigned.crt
echo "Done"
