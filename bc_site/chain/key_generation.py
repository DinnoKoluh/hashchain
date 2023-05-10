import hashlib
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def generate_keys():
    """
    Generate key_pair object that contains the secret and public keys.
    """
    key_pair = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    return key_pair

def get_secret_key(key_pair):
    """
    Return secret key from a key pair.
    """
    return key_pair.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()).decode('utf-8')

def get_public_key(key_pair):
    """
    Return public key from a key pair.
    """
    return key_pair.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH).decode('utf-8')

def generate_address(key_pair):
    """
    Generate address by hashing the public key.
    """
    return hashlib.sha256(str(get_public_key(key_pair)).encode()).hexdigest()

def save_key(key_pair, filename):
    pem = key_pair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)

def load_key(filename):
    with open(filename, 'rb') as pem_in:
        pem_lines = pem_in.read()
    private_key = load_pem_private_key(pem_lines, None, default_backend())
    return private_key