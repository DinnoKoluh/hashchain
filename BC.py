import hashlib
import time

class Block:
    def __init__(self, data, previousTimestamp = " ", previousHash = " "):
        self.index = 0 # block index
        self.timestamp = time.time() # timestamp of current block i.e. when it was created (not included in the hash)
        self.previousTimestamp = previousTimestamp
        self.data = data # data included inside the block (e.g. the transaction)
        self.nonce = 0
        self.previousHash = previousHash # hash of previous block
        self.hash = self.calculateHash()
    
    def calculateHash(self):
        """
        Calculating the hash of the current block based on the block attributes.
        """
        #hash_data = str(self.index) + "-" + "-".join(self.data) + "-" + self.previousHash
        hash_data = str(self.index) + "-" + "-" + str(self.data) + "-" + str(self.previousTimestamp) + "-" + self.previousHash + "-" + str(self.nonce)
        return hashlib.sha256(hash_data.encode()).hexdigest()

    def getBlockInfo(self):
        """
        Printing out block information.
        """
        print("Index: {} \nData: {} \nTimestamp: {} \nPrevious Timestamp: {} \nPrevious Hash: {} \nBlock Hash: {}".format(self.index, 
        self.data, self.timestamp, self.previousTimestamp, self.previousHash, self.hash))

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

class BlockChain:
    def __init__(self):
        """
        Chain is constructed as a list of Block objects where the first block is the genesis block.
        """
        self.difficulty = 3 # how many 0's are at the beginning of the hash
        gen_block = Block("GENESIS BLOCK", time.time(), "0x000") # creating genesis block
        gen_block.mineBlock(self.difficulty)
        self.chain = [gen_block] # creating the chain
        
    def getLatestBlock(self):
        """
        Get the latest block in the cain.
        """
        return self.chain[-1]
    
    def addNewBlock(self, new_block: Block):
        """
        Adding a new block to the chain. Function expects Block object. It makes sure that the indices will be consecutive.
        """
        new_block.previousHash = self.getLatestBlock().hash
        new_block.previousTimestamp = self.getLatestBlock().timestamp # getting the timestamp of the previous block as it is needed in the hashing
        new_block.index = self.getLatestBlock().index + 1 # making sure that the block indices are consecutive
        #new_block.hash = new_block.calculateHash()
        new_block.mineBlock(self.difficulty) # mining a block
        new_block.timestamp = time.time() # timestamp of current block is defined as the time the block was mined
        self.chain.append(new_block)

    def isChainValid(self):
        """
        Checking if the chain is valid by traversing through it and checking connections.
        """
        for i in range(1, len(self.chain)):
            currBlock = self.chain[i]
            prevBlock = self.chain[i-1]
            # case when block hash is wrong
            if (currBlock.hash != currBlock.calculateHash()):
                return False
            # case when current block has wrong hash of previous block
            if (currBlock.previousHash != prevBlock.hash):
                return False
        return True

        
        