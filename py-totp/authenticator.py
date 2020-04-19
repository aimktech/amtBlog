# generate the QR code
import sys
import base64
import qrcode
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

# generate the qrcode
uri = totp.get_provisioning_uri("Alice Smith", "AI Mechanics & Tech")

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(uri)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.show()

# print the Base32 value for Keypass
print("Keypass Value: {}".format(base64.b32encode(secret_key_file.read_bytes()).decode()))
