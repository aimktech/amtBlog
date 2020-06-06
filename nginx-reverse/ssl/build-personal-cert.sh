#!/bin/bash
# script to build a server certificate signed by a Root Certificate Authority

SCRIPT_DIR=$(dirname $0)
if [ "${SCRIPT_DIR}" == "." ]; then
    SCRIPT_DIR=$(pwd)
fi

CERTS_DIR=${SCRIPT_DIR}/certs

mkdir -p ${CERTS_DIR}

if [ -z "$1" ]; then
    exit
fi

# step 1
echo ""
echo "1. Create private key"
echo ""
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 | \
openssl pkcs8 -topk8 -v2 des3 -out ${CERTS_DIR}/$1.key

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

echo ""
echo "4. Build PKCS#12 Certificate"
echo ""
openssl pkcs12 -export \
        -out ${CERTS_DIR}/$1.pfx \
        -in ${CERTS_DIR}/$1.cert \
        -inkey ${CERTS_DIR}/$1.key

