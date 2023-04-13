import hashlib
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Account:
    def __init__(self):
        self.username = ""
        self.key_pair = self.generateKeys()

        self.secret_key = self.key_pair.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()).decode('utf-8')
        
        self.public_key = self.key_pair.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH).decode('utf-8')
        
        self.address = hashlib.sha256(str(self.public_key).encode()).hexdigest() # account address
        self.__balance = 0

    def generateKeys(self):
        """
        Generate key_pair object that contains the secret and public keys.
        """
        key_pair = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=512
        )
        return key_pair
    
    def increaseBalance(self, amount):
        """
        Increasing account __balance by amount.
        """
        self.__balance = self.__balance + amount
        return True
    
    def decreaseBalance(self, amount):
        """
        Decreasing account __balance by amount.
        """
        if amount > self.__balance:
            raise Exception("Not enough funds!")
        self.__balance = self.__balance - amount
        return True

    def getBalance(self):
        """
        Return account balance
        """
        return self.__balance

    def getKeys(self):
        """
        Return object containing secret and public key.
        """
        return self.key_pair

class Network:
    def __init__(self):
        self.accounts = {}

    def addAccount(self, account: Account):
        """
        Add a new account to the network. Accounts stored as a dictionary where the key is the account address.
        """
        self.accounts[account.address] = account