import hashlib
from Net import *
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Transaction:
    def __init__(self, from_address, to_address, amount, tx_type = "ordinary"):     
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.tx_type = tx_type # type of transaction (Ordinary or Mining)

    def calculateHash(self):
        """
        Hash used to sign a transaction.
        """
        # we are just going to sign the hash of our transaction (not other data)
        hash_data = str(self.from_address) + str(self.to_address) + str(self.amount) + str(self.tx_type)
        return hashlib.sha256(hash_data.encode()).hexdigest()

    def signTx(self, key_pair):
        """
        Signing a transaction using your key pair. The message to be signed is the hash of the transaction data.
        The transaction can only be signed by an account whose address matches to the "from_address" of the transaction.
        """
        # TODO don't allow signing multiple times

        # check if the address that signs the transaction is the from_address
        is_pb_key = key_pair.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH).decode('utf-8')
        is_address = hashlib.sha256(str(is_pb_key).encode()).hexdigest() 
        if (self.from_address != is_address):
            raise Exception("You cannot sign this transaction!")

        tx_hash = self.calculateHash() # message to be signed
        self.signature = key_pair.sign(
            bytes(tx_hash, 'utf-8'), # convert tx_hash to a bytes object 
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Transaction has been successfully signed!")
        self.__public_key = key_pair.public_key() # storing the public key so that the transaction can be verified/ stored as a hidden variable
        return True

    def isTxValid(self):
        """
        Check if the transaction is valid. For a transaction to be valid it has to be either a mining type transaction or 
        it has to be signed by the account from which the funds are withdrawn.
        """
        if (self.from_address == None): return True # mining transaction

        if (not(hasattr(self, "signature"))): 
            raise Exception("The transaction has not been signed yet!")

        # verifying the signature
        self.__public_key.verify(
            self.signature,
            bytes(self.calculateHash(), 'utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Transaction signature is valid!")
        return True
    
    def executeTx(self, network : Network):
        """
        Executing transaction by means of account holdings. If the transaction type is "mining" then
        the balance of miner is increased without decreasing the "from" address.
        """
        self.isTxValid() # firstly validate transaction
        if self.tx_type == "ordinary":
            network.accounts[self.from_address].decreaseBalance(self.amount)
            network.accounts[self.to_address].increaseBalance(self.amount)
            return True
        elif self.tx_type == "mining":
            network.accounts[self.to_address].increaseBalance(self.amount)
            return True
        else:
            raise Exception("Transaction type non-existent!")
    
    def printTxInfo(self):
        """
        Console info about transaction.
        """
        print("Tx type: {} \nFrom: {} \nTo: {} \nAmount: {}".format(self.tx_type, self.from_address, self.to_address, self.amount))