from django.db import models
from django.contrib.auth.models import User, AbstractUser # user model
import sys
# FIX: change from absolute to relative path
sys.path.append('C:\\Users\\pc\\Desktop\\MyProjects\\my_blockchain')
from BC import *
from Net import *
from Tx import *
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
from django.db.models.signals import post_save
from django.dispatch import receiver

# network = Network()
# bc = BlockChain(network)

# Create your models here.

# need to create user 
class AccountModel(User):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'account'
    
    # def __init__(self):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account", unique=True)
    account = Account()
    address = models.CharField(max_length=64, default=account.address, editable=True)
    test = models.CharField(max_length=5, default='a')
    
    class Meta:
        verbose_name = "Accounts Model"

    def __str__(self):
        return self.address

    # def set_password(self, raw_password):
    #     self.user.set_password(raw_password)
    #     self.user.save()
    
# @receiver(post_save, sender=User)
# def create_user_accountmodel(sender, instance, created, **kwargs):
#     if created:
#         AccountModel.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_accountmodel(sender, instance, **kwargs):
#     instance.profile.save()

# creating transactions
class TxModel(models.Model):
    """
    Model that contains transaction details
    """
    my_add = models.CharField(max_length=64, default='0000000', editable=True)
    to_address = models.CharField(max_length=64)
    amount = models.FloatField()

class BlockStruct(models.Model):
    blockID = models.CharField(max_length=20)
    def __str__(self):
        return self.blockID

    class Meta:
        ordering = ('blockID',)