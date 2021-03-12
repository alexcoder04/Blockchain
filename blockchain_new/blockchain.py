from .block import Block
from .transaction import Transaction
from datetime import datetime
from Crypto.PublicKey import RSA

class Blockchain:
    def __init__(self, difficulty, rewards):
        self.pending = []
        self.difficulty = difficulty
        self.rewards = rewards
        self.chain = [self.create_genesis_block()]
    
    def mine_pending(self, miner):
        block = Block(self.pending, datetime.now(), len(self), self.last_block().hash)
        block.mine(self.difficulty)
        self.add_block(block)
        self.pending = []
        # TODO safe rewards
        self.add_transaction("reward", miner, self.rewards, None)
    
    def add_transaction(self, sender, recv, amount, sender_private_key):
        transaction = Transaction(sender, recv, amount)
        transaction.sign(sender_private_key)
        self.pending.append(transaction)
    
    def last_block(self):
        return self.chain[-1]
    
    def add_block(self, block):
        self.chain.append(block)
    
    def create_genesis_block(self):
        block = Block([], datetime.now(), 0, "NONE")
        block.mine(self.difficulty)
        return block
    
    def json(self):
        return {
            "chain": [block.json() for block in self.chain],
            "pending": [ta.json() for ta in self.pending]
        }
    
    def __len__(self):
        return len(self.chain)
    
    @staticmethod
    def generate_user():
        key = RSA.generate(bits=2048)
        return key.export_key(), key.public_key().export_key()
