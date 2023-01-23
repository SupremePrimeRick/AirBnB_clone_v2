#!/usr/bin/env bash
# Script that sets up webserver for the deployment of web_static

echo -e "\e[1;32m Updating and installing packages...\e[0m"

# Updating and installing packages
sudo apt-get -y update 
sudo apt-get -y install nginx
sudo apt-get -y install ufw
echo -e "\e[1;32m Package update and installation complete\e[0m"

# Configure firewall to allow NGINX HTTP
sudo ufw allow 'NGINX FULL'
echo -e "\e[1;32m Firewall access granted to nginx\e[0m"

# Creating folders
mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e "\e[1;32m Directories created\e[0m"

# Adding test string to index.html
echo "<h1>Welcome to sigmacodes</h1>" > /data/web_static/releases/test/index.html
echo -e "\e[1;32m Test string added to index.html\e[0m"

# Checking if symbolic link already exists
if [ -d '/data/web_static/current' ];
then
    echo 'Path /data/web_static/current already exists'
    rm -rf /data/web_static/current
    echo -e "\e[1;32m Existing symbolic link deleted\e[0m"
fi

# Creating symbolic link
sudo ln -s --force /data/web_static/releases/test/ /data/web_static/current
echo -e "\e[1;32m Symbolic link created\e[0m"

# Change owner and group of /data/ recursively
sudo chown -Rh ubuntu:ubuntu /data/

# Get line number to insert line
CONFIG_FILE='/etc/nginx/sites-available/default'
LINE_NO=$(wc -l $CONFIG_FILE | cut -d ' ' -f1)

sed -i "$LINE_NO i\\\tlocation /hbtn_static/ {\n\t\t\talias /data/web_static/current;\n\t\t\t}\n" $CONFIG_FILE
sudo ln -sf "/etc/nginx/sites-available/default" "/etc/nginx/sites-enabled/default"
echo -e "\e[1;32m Nginx configuration updated\e[0m"

# Restart nginx server
sudo service nginx restart
echo -e "\e[1;32m Nginx restarted OK\e[0m"
