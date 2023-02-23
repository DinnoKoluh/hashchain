import hashlib
import time
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

class Account:
    def __init__(self):
        self.secret_key, self.public_key = self.generateKeys()
        self.address = hashlib.sha256(str(self.public_key).encode()).hexdigest() # account address
        self.balance = 0

    def generateKeys(self):
        key_pair = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=512
        )
        secret_key = key_pair.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()).decode('utf-8')
        
        public_key = key_pair.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH).decode('utf-8')
        return secret_key, public_key
    
    def increaseBalance(self, amount):
        self.balance = self.balance + amount
        return True
    
    def decreaseBalance(self, amount):
        if amount > self.balance:
            print("Not enough funds!")
            return False
        self.balance = self.balance - amount
        return True

class Network:
    def __init__(self):
        self.accounts = {}

    def addAccount(self, account: Account):
        """
        Add a new account to the network. Accounts are found via their address.
        """
        self.accounts[account.address] = account

class Transaction:
    def __init__(self, from_address, to_address, amount, tx_type = "ordinary"):     
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.tx_type = tx_type # type of transaction (Ordinary or Mining)
    
    def executeTx(self, network : Network):
        """
        Executing transaction by means of account holdings. If the transaction type is "mining" then
        the balance of miner is increased without decreasing the "from" address.
        """
        if self.tx_type == "ordinary":
            network.accounts[self.from_address].decreaseBalance(self.amount)
            network.accounts[self.to_address].increaseBalance(self.amount)
        elif self.tx_type == "mining":
            network.accounts[self.to_address].increaseBalance(self.amount)
    
    def printTxInfo(self):
        """
        Console info about transaction.
        """
        print("Tx type: {} \nFrom: {} \nTo: {} \nAmount: {}".format(self.tx_type, self.from_address, self.to_address, self.amount))