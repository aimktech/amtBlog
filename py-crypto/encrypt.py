import os
import base64
import pathlib
import argparse

from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

# read the message from the command line
parser = argparse.ArgumentParser()
parser.add_argument("message")
args = parser.parse_args()

# get default backend
backend = backends.default_backend()

# read the public key
key_bytes = pathlib.Path("public.pem").read_bytes()
public_key = serialization.load_pem_public_key(key_bytes, backend)

# encrypt the message
cipher_bytes = public_key.encrypt(args.message.encode('utf-8'), padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
) )
cipher = base64.b64encode(cipher_bytes)

print(f"Cipher: \n{cipher.decode('utf-8')}")