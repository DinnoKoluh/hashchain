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

def get_secret_key_as_bytes(key_pair):
    """
    Return secret key from a key pair.
    """
    return key_pair.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption())

def get_public_key_as_bytes(key_pair):
    """
    Return public key from a key pair.
    """
    return key_pair.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

def generate_address(key_pair):
    """
    Generate address by hashing the public key.
    """
    return hashlib.sha256(str(get_public_key_as_bytes(key_pair)).encode()).hexdigest()

def save_key(key_pair, filename):
    pem = key_pair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)

def load_secret_key(data):
    """
    Loads secret key as corresponding class object from given given path or bytes object.
    """
    if type(data) is str:
        with open(data, 'rb') as pem_in:
            pem_lines = pem_in.read()
        private_key = load_pem_private_key(pem_lines, None, default_backend())
    elif type(data) is bytes:
        private_key = load_pem_private_key(data, None, default_backend())
    else:
        raise Exception("Wrong input!")
    return private_key

def load_public_key(data):
    """
    Loads public key as corresponding class object from given given path or bytes object.
    """
    if type(data) is str:
        with open(data, 'rb') as pem_in:
            pem_lines = pem_in.read()
        public_key = serialization.load_pem_public_key(pem_lines, backend=default_backend())
    elif type(data) is bytes:
        public_key = serialization.load_pem_public_key(data, backend=default_backend())
    else:
        raise Exception("Wrong input!")
    return public_key
