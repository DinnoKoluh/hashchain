from django.db import models
import sys
# FIX: change from absolute to relative path
sys.path.append('C:\\Users\\pc\\Desktop\\MyProjects\\my_blockchain')
from BC import *
from Net import *
from Tx import *

# network = Network()
# bc = BlockChain(network)

# Create your models here.

class BlockStruct(models.Model):
    blockID = models.CharField(max_length=20)
    def __str__(self):
        return self.blockID

    class Meta:
        ordering = ('blockID',)