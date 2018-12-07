#!/bin/bash
read -p "username: " username
read -s -p "password: " password

curl -i -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}' -c cookie-jar -k https://info3103.cs.unb.ca:36479/signin
