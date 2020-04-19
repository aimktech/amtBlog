# generate the QR code secret key
import os
import pathlib

print("Generating secret key...")

# SHA1 uses 20 x 8bits = 160 bits
secret_key = os.urandom(20)

# save the file
pathlib.Path("secret_key.bin").write_bytes(secret_key)

print("Done.")
