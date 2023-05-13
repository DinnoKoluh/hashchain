from django.db import models
from django.contrib.auth.models import User, AbstractUser # user model
import sys
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from .key_generation import *

import hashlib
import time
from datetime import datetime
import math

def validate_amount(value):
    if value < 1 or not(isinstance(value, int)):
        raise ValidationError(
            gettext_lazy("%(value)s is not has to be a positive integer greater than 0!"),
            params={"value": value},
        )

class Account(User):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'address'
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account", unique=True)
    address = models.CharField(max_length=64, default="00000000000000000000000000000000", editable=False)
    balance = models.IntegerField(default='0', editable=False)
    pending_amount = models.IntegerField(default='0', editable=False) # amount to be taken out of balance when tx's is executed
    
    class Meta:
        verbose_name = "Accounts Model"

    def __str__(self):
        return self.address
    
    def get_balance(self):
        return self.balance
    
    def get_address(self):
        return self.address
    
    def increase_balance(self, amount):
        """
        Increasing account balance by amount.
        """
        self.balance = self.balance + amount
        self.save()
        return True
    
    def decrease_balance(self, amount):
        """
        Decreasing account balance by amount.
        """
        if amount > self.balance:
            raise Exception("Not enough funds!")
        self.balance = self.balance - amount
        self.save()
        return True
    
    def increase_pending_amount(self, amount):
        if self.pending_amount + amount > self.balance:
            raise Exception("Not enough funds!")
        self.pending_amount = self.pending_amount + amount
        self.save()
        return True
    
    def decrease_pending_amount(self, amount):
        self.pending_amount = self.pending_amount - amount
        self.save()
        return True
    
class Tx(models.Model):
    """
    Model that contains transaction details.
    """
    from_address = models.CharField(max_length=64, default='0000000', editable=False)
    to_address = models.CharField(max_length=64, default='0000000')
    amount = models.IntegerField(default='0', validators=[validate_amount])
    executed = models.BooleanField(default=False)
    tx_type = models.CharField(max_length=64, default='ordinary')
    message = models.TextField(max_length=512, default='None')
    fee = models.FloatField(default=0.01)
    signature = models.BinaryField(default=b'empty_signature')
    public_key = models.BinaryField(default=b'empty_pk')
    
    def __str__(self):
        return "Tx No. " + str(self.id)
    
    def execute_tx(self):
        """
        Executing a tx.
        """
        self.is_tx_valid()
        if self.tx_type == "ordinary":
            # decrease balance by amount + the fee percentage which will be added to the miner
            Account.objects.filter(address=self.from_address)[0].decrease_balance(self.amount + self.get_fee())
            # when tx is executed decrease the pending amount by that amount
            Account.objects.filter(address=self.from_address)[0].decrease_pending_amount(self.amount + self.get_fee())
            Account.objects.filter(address=self.to_address)[0].increase_balance(self.amount)
            self.executed = True
        return True
    
    def sign_tx(self, key):
        """
        Signing tx with the secret(private) key object and saving the signature.
        """
        self.signature = key.sign(
            self.get_tx_hash(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.save() # saving the signature 
        return True

    def get_tx_hash(self):
        """
        Getting the tx hash in bytes format. This will be the data that is actually being signed.
        """
        hash_data = str(self.from_address) + str(self.to_address) + str(self.amount) + str(self.message)
        return bytes(hashlib.sha256(hash_data.encode()).hexdigest(), 'utf-8')

    def is_tx_valid(self):
        """
        Check if the tx is actually valid with the use of the public key, signature and tx hash data.
        """
        try:
            publicKey = load_public_key(self.public_key)
            publicKey.verify(
                self.signature,
                self.get_tx_hash(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except:
            raise Exception(f"Invalid Signature of Transaction {self.pk}!")
        return True
    
    def is_tx_owner_valid(self, key):
        """
        Check if the owner of the transaction and the submitted private key match.
        """
        if generate_address(key) != self.from_address:
            raise Exception("Entered wrong private key!")
        return True
    
    def get_fee(self):
        # make sure that transactions under 100 have a fee of 1
        if self.amount < 100:
            return 1
        return math.floor(self.amount * self.fee) + 1

class Block(models.Model):
    total_fee = models.FloatField(default=0, editable=False)
    miner_address = models.CharField(max_length=64, default="0x0", editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=True)
    nonce = models.IntegerField(default=0, editable=False)
    previous_hash = models.CharField(max_length=64, default="GENESIS BLOCK", editable=False)
    hash = models.CharField(max_length=64, default="0x0", editable=False)
    reward = models.IntegerField(default=100, editable=False)
    txs = models.ManyToManyField(Tx, blank=True, default=None)

    def __init__(self, *args, **kwargs):
        super(Block, self).__init__(*args, **kwargs)
        if self.pk is None and Block.objects.all().last():
            self.previous_hash = Block.objects.all().last().hash # assigning the hash of the previous block
            
    def __str__(self):
        return self.hash
    
    def save(self, *args, **kwargs):
        """
        Overriding the save method, so that adding a new block is actually mining a block.
        """
        if self.pk is None:
            self.mineBlock(difficulty=5)
        return super(Block, self).save(*args, **kwargs)
    
    def add_txs(self):
        """
        Adding all the tx's which weren't executed to the block.
        """
        for tx in Tx.objects.filter(executed=False):
            self.txs.add(tx)
    
    def execute_txs(self):
        """
        Executing the pending tx's inside the block. When tx's are executed reward miner.
        """
        for tx in self.get_txs():
            self.total_fee = self.total_fee + tx.get_fee()    # calculating total fee of all tx in the block
            tx.execute_tx()
            tx.save()
        # after the txs in a block are executed reward the miner
        # when the genesis block is mined, it's reward goes to that miner
        Account.objects.filter(address=self.miner_address)[0].increase_balance(self.total_fee + self.reward) 
        return True

    
    def get_txs(self):
        """
        Return all the tx's stored in the block.
        """
        return self.txs.all()

    def calculateHash(self):
        """
        Calculating the hash of the current block based on the block attributes.
        """
        # bug using a timestamp as the block has not been saved yet so the timestamp used is the default one
        hash_data = str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(hash_data.encode()).hexdigest()
    
    def mineBlock(self, difficulty):
        """
        Mining a block based on the difficulty variable (the number of 0's at the beginning of the hash).
        """
        start_time = time.time()
        while (self.hash[0:difficulty] != str("0"*difficulty)):
            self.nonce = self.nonce + 1
            self.hash = self.calculateHash()
        end_time = time.time()
        # add final check for non executed tx so that two block cannot be mined at the same time
        print("Block has been mined successfully! \nTime taken: {}".format(end_time - start_time))
    
    def validate_block_txs(self):
        """
        Check if all tx's in a block are valid.
        """
        invalid_tx = 0
        try:
            for tx in self.get_txs():
                invalid_tx = tx.pk
                tx.is_tx_valid()
        except Exception as e:
            raise Exception("Invalid Transaction {} in Block {}!".format(invalid_tx, self.pk) + '\n' + str(e))