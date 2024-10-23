#!/bin/bash

readonly KEY_PATH=.cache/keys

openssl req -new -x509 -days 365 -nodes -out ${KEY_PATH}/server.pem -keyout ${KEY_PATH}/server.pem
