#!/bin/ash

echo ""
echo "-----------------------------------------------------------"
echo ""
echo "Starting 'user' service on (internal) port 8000"
echo "         ... but it will be binded to external port 7070"
echo ""

ping -c 2 www.google.com

ping -c 3 registrator

python /app-src/user-service.py -p 8000
