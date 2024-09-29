#!/bin/bash

readonly KEY_PATH=.cache/keys
readonly CONFIG_PATH=.cache/configurations
readonly CERTIFICATE_PATH=.cache/certificates

mkdir -p ${KEY_PATH}
mkdir -p ${CERTIFICATE_PATH}

if [[ -f "${KEY_PATH}/server.key" && -f "${CERTIFICATE_PATH}/server.crt" ]]; then
    echo "Key and certificate already exist"
else
    echo "Generating key and certificate"
    openssl genrsa -out ${KEY_PATH}/server.key 2048
    openssl req -new -key ${KEY_PATH}/server.key -out ${CERTIFICATE_PATH}/server.csr -config ${CONFIG_PATH}/localhost.conf
    openssl x509 -req -days 365 -in ${CERTIFICATE_PATH}/server.csr -signkey ${KEY_PATH}/server.key -out ${CERTIFICATE_PATH}/server.crt -extensions v3_req -extfile ${CONFIG_PATH}/localhost.conf
    echo "Key and certificate generated"
fi
