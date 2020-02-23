#!/bin/bash

# generate the private key
echo "Generating RSA Private key:"
openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:2048 | \
openssl pkcs8 -topk8 -v2 des3 -out private.pem

# generate the public key
echo ""
echo "Generating RSA Public key:"
openssl pkey -in private.pem -pubout -out public.pem

echo "Done."