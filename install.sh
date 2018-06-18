#!/usr/bin/env bash

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
COLOR_OFF='\033[0m'

echo -e "${YELLOW}Welcome to operative framework HD installation script ${COLOR_OFF}"
echo "Making directory ~/.operative_framework ..."
mkdir ~/.operative_framework
echo "Moving framework, client folder to '~/.operative_framework' ..."
cp -R framework/ ~/.operative_framework/framework
cp -R client/ ~/.operative_framework/client
cp bin/opf_client.py /usr/local/bin/opf_client
cp bin/opf_console.py /usr/local/bin/opf_console
cp bin/opf_server.py /usr/local/bin/opf_server
cp bin/opf_users.py /usr/local/bin/opf_users
echo "operative framework binary copied."
echo "installation if python dependency ..."
pip install -r requirements.txt
echo "installation of npm dependency ..."
npm install --prefix "~/.operative_framework/client/"
echo -e "${GREEN}Installation successfully terminated,  start cmd 'opf_console' from new shell.${COLOR_OFF}"