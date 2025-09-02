from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

KEYS_DIR = 'keys'

def load_public_key():
	with open(f'{KEYS_DIR}/public.pem', 'rb') as f:
		return serialization.load_pem_public_key(f.read())

def load_private_key():
	with open(f'{KEYS_DIR}/private.pem', 'rb') as f:
		return serialization.load_pem_private_key(f.read(), password=None)

def encrypt_field(value):
	public_key = load_public_key()
	encrypted = public_key.encrypt(
		value.encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return base64.b64encode(encrypted).decode()

def decrypt_field(value):
	private_key = load_private_key()
	try:
		encrypted = base64.b64decode(value.encode())
		decrypted = private_key.decrypt(
			encrypted,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return decrypted.decode()
	except Exception:
		return value
