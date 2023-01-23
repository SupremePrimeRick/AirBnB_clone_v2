#!/usr/bin/env bash

# Get line number to insert line
CONFIG_FILE='/etc/nginx/sites-available/default'
LINE_NO=$(wc -l $CONFIG_FILE | cut -d ' ' -f1)
echo $LINE_NO
sed -i "$LINE_NO i\\\tlocation /hbtn_static/ {\n\t\t\talias /data/web_static/current;\n\t\t\t}\n" $CONFIG_FILE

