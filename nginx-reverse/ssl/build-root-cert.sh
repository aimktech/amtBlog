#!/bin/bash
# script to build a root certificate for a Certificate Authority

SCRIPT_DIR=$(dirname $0)
if [ "${SCRIPT_DIR}" == "." ]; then
    SCRIPT_DIR=$(pwd)
fi

CERTS_DIR=${SCRIPT_DIR}/certs

mkdir -p ${CERTS_DIR}

# step 1
echo ""
echo "1. Generating the private key..."
echo ""
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 | \
openssl pkcs8 -topk8 -v2 des3 -out ${CERTS_DIR}/root_ca.key

# step 2
echo ""
echo "2. Generating self signed certificates"
echo "Please set the common name to your name"
echo ""
openssl req -x509 -new -nodes -sha256 \
        -key ${CERTS_DIR}/root_ca.key \
        -out ${CERTS_DIR}/root_ca.pem \
        -days 365 -config ${SCRIPT_DIR}/ssl.conf

