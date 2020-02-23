import os
import base64
import pathlib
import argparse

from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

# retrieve the cipher from the command line
parser = argparse.ArgumentParser()
parser.add_argument("cipher")
parser.add_argument("password")
args = parser.parse_args()

# get default backend
backend = backends.default_backend()

# read the private key
key_bytes = pathlib.Path("private.pem").read_bytes()
private_key = serialization.load_pem_private_key(key_bytes, password=args.password.encode('utf-8'), backend=backend)

# decrypt the cipher
cipher_bytes = base64.b64decode(args.cipher)
message = private_key.decrypt(cipher_bytes, padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
) )

print(f"Message: \n{message.decode('utf-8')}")