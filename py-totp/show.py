# show the TOTP password continuously
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

# print the value every 30s
print("CTRL+C to stop")
old = 0
now = int(time.time()) // password_time
while True:
    try:
        if now != old:
            # print the new value
            print("{}".format(totp.generate(int(time.time())).decode()))
            old = now
        else:
            time.sleep(1)

        now = int(time.time()) // password_time
    except KeyboardInterrupt:
        break
