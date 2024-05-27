#!/bin/bash
exec 2>> /tmp/debug-ovpn

PATH=$PATH:/usr/local/bin
set -e

env

auth_usr=$(head -1 "$1")
auth_passwd=$(tail -1 "$1")

if [ $common_name = "$auth_usr" ]; then
  result=$(curl -X GET -H "Content-type: application/json" -d "{\"username\":\"${auth_usr}\",\"password\":\"${auth_passwd}\"}" http://openvpn-ui-api:8080/auth)
  echo "$result"
  if [ "$result" = '"Authorized"' ]; then
    echo "Authorization succeeded"
    exit 0
  else
    echo "Authorization failed"
    exit 1
  fi
else
  echo "Authorization failed"
  exit 1
fi