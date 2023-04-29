import hashlib
import time
from Net import *
from Tx import *

class Block:
    def __init__(self, data, previous_timestamp = "0", previous_hash = " "):
        self.timestamp = time.time() # timestamp of current block i.e. when it was created (not included in the hash)
        self.previous_timestamp = previous_timestamp
        self.data = data # data included inside the block (e.g. the transaction)
        self.nonce = 0
        self.previous_hash = previous_hash # hash of previous block
        self.hash = self.calculateHash()
    
    def calculateHash(self):
        """
        Calculating the hash of the current block based on the block attributes.
        """
        hash_data = str(self.data) + "-" + str(self.previous_timestamp) + "-" + self.previous_hash + "-" + str(self.nonce)
        return hashlib.sha256(hash_data.encode()).hexdigest()

    def getBlockInfo(self):
        """
        Printing out block information.
        """
        print("Data: {} \nTimestamp: {} \nPrevious Timestamp: {} \nPrevious Hash: {} \nBlock Hash: {}".format(self.data, 
            self.timestamp, self.previous_timestamp, self.previous_hash, self.hash))

    def mineBlock(self, difficulty):
        """
        Mining a block based on the difficulty variable (the number of 0's at the beginning of the hash).
        """
        start_time = time.time()
        while (self.hash[0:difficulty] != str("0"*difficulty)):
            self.nonce = self.nonce + 1
            self.hash = self.calculateHash()
        end_time = time.time()
        print("Block has been mined successfully! \nTime taken: {}".format(end_time - start_time))
    
    # TODO: still change to accommodate tx validation if the from account doesn't have enough funds
    def hasValidTx(self):
        """
        Check if the transactions contained inside a block are valid.
        """
        for tx in self.data:
            if not(tx.isValid()):
                return False
        return True

class BlockChain:
    def __init__(self, network:Network):
        """
        Chain is constructed as a list of Block objects where the first block is the genesis block.
        """
        self.difficulty = 3 # how many 0's are at the beginning of the hash
        gen_block = Block("GENESIS BLOCK", time.time(), "0x000") # creating genesis block
        gen_block.mineBlock(self.difficulty)

        self.chain = [gen_block] # creating the chain
        self.pending_txs = [] # where transactions are stored while a new block is being mined 
        # TODO reward to be regarded as a percentage of transaction amount
        self.reward = 100 # mining reward given to miner if a block is successfully mined
        self.network = network # network of accounts 
        # TODO add system of a master account from where the rewards are given
        self.supply = 10000 # total supply blockchain supply
        
    def getLatestBlock(self):
        """
        Get the latest block in the cain.
        """
        return self.chain[-1]
    
    def addNewBlock(self, new_block: Block):
        """
        Adding a new block to the chain. Function expects Block object.
        """
        new_block.previous_hash = self.getLatestBlock().hash
        new_block.previous_timestamp = self.getLatestBlock().timestamp # getting the timestamp of the previous block as it is needed in the hashing
        new_block.mineBlock(self.difficulty) # mining a block
        new_block.timestamp = time.time() # timestamp of current block is defined as the time the block was mined
        self.chain.append(new_block)
        print("New block with ID:{} has been added to the blockchain!".format(len(self.chain)-1))

    def minePendingTransaction(self, miner_address):
        """
        Function to mine new blocks by a miner.
        If a miner successfully mines a new block, send reward to his address and add mined block to the blockchain.
        """
        block = Block(self.pending_txs) # in reality not all pending transactions can be added to a block due to block size limitations
        self.addNewBlock(block) # adding (mining) the block
        self.executePendingTxs() # executing pending transactions
        self.addTransaction(Transaction(None, miner_address, self.reward, tx_type = "mining")) # appending the reward transaction to the list

    def executePendingTxs(self):
        """
        After a block has been successfully mined execute all the transaction inside of it.
        """
        for tx in self.pending_txs:
            tx.executeTx(self.network)
        self.pending_txs = [] # after executing all txs restore pending txs

    def addTransaction(self, transaction: Transaction):
        """
        Add a new transaction to the transaction list.
        """
        self.pending_txs.append(transaction)
        print("Transaction successfully added! \nTx type {}".format(transaction.tx_type))
        return True

    def printPendingTxInfo(self):
        """
        Function to print pending transaction info.
        """
        for tx in self.pending_txs:
            tx.printTxInfo()
    
    def isChainValid(self):
        """
        Checking if the chain is valid by traversing through it and checking connections.
        """
        for i in range(1, len(self.chain)):
            currBlock = self.chain[i]
            prevBlock = self.chain[i-1]
            # check if all tx in the block are valid
            if (not(currBlock.hasValidTx())):
                return False
            # case when block hash is wrong
            if (currBlock.hash != currBlock.calculateHash()):
                return False
            # case when current block has wrong hash of previous block
            if (currBlock.previous_hash != prevBlock.hash):
                return False
        return True

        