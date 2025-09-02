from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os


os.makedirs("keys", exist_ok=True)


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

with open("keys/private.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  
        )
    )


public_key = private_key.public_key()

with open("keys/public.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("RSA key pair generated in 'keys/' folder!")
