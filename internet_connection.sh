#!/bin/bash

echo -e "GET https://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Online" $(date)
else
    echo "Offline" $(date)
    systemctl reboot -i
fi
