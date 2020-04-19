# validate a TOTP password
import sys
import time
import pathlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA1

# password parameters
password_size = 6
password_time = 30

secret_key_file = pathlib.Path("secret_key.bin")

# check for the secret key file
if not secret_key_file.exists():
    print("Please generate the secret key first.")
    sys.exit(1)

# create TOTP object
totp = TOTP(secret_key_file.read_bytes(), password_size, SHA1(), password_time, backend=default_backend())

if len(sys.argv) < 2:
    print("{} <TOTP password>".format(sys.argv[0]))
    sys.exit(1)

try:
    totp.verify(sys.argv[1].encode('utf-8'), int(time.time()))
    print("Password validated")
except:
    print("Wrong password")
