#!/bin/bash
# script to build a server certificate signed by a Root Certificate Authority

SCRIPT_DIR=$(dirname $0)
if [ "${SCRIPT_DIR}" == "." ]; then
    SCRIPT_DIR=$(pwd)
fi

CERTS_DIR=${SCRIPT_DIR}/certs

mkdir -p ${CERTS_DIR}

if [ -z "$1"]; then
    exit
fi

# step 1
echo ""
echo "1. Generate a public/private key for the server"
echo ""
openssl genpkey -out ${CERTS_DIR}/$1.key -algorithm RSA -pkeyopt rsa_keygen_bits:2048

echo ""
echo "2. Generate Certificate Signing Request"
echo ""
openssl req -new \
        -key ${CERTS_DIR}/$1.key \
        -out ${CERTS_DIR}/$1.csr \
        -config ${SCRIPT_DIR}/ssl.conf

echo ""
echo "3. Self signing the request with the Root CA"
echo ""
openssl x509 -req -sha256 -days 365 \
        -in ${CERTS_DIR}/$1.csr \
        -out ${CERTS_DIR}/$1.cert \
        -CA ${CERTS_DIR}/root_ca.pem \
        -CAkey ${CERTS_DIR}/root_ca.key \
        -CAcreateserial \
        -extensions req_ext -extfile ssl.conf

