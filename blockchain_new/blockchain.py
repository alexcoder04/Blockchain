from .block import Block
from .transaction import Transaction
from .network import Network
from .log import log
from datetime import datetime
from Crypto.PublicKey import RSA

class Blockchain:
    def __init__(self, addr, nodes=None, difficulty=2, rewards=10):
        log("initializing the blockchain...")
        self.network = Network(addr, nodes)
        if not nodes:
            log("creating a new network...")
            self.difficulty = difficulty
            self.rewards = rewards
            self.pending = []
            self.chain = [self.create_genesis_block()]
        else:
            self.difficulty = difficulty
            self.rewards = rewards
            # TODO get pending, difficulty and rewards from the network
            self.pending = [Transaction.from_json(i) for i in self.network.get_pending()]
            self.chain = self.network.get_chain()
    
    def mine_pending(self, miner):
        log("creating new block...")
        block = Block(self.pending, datetime.now(), len(self), self.last_block().hash)
        block.mine(self.difficulty)
        self.add_block(block)
        self.pending = []
        # TODO safe rewards
        log("creating rewards transaction...")
        self.add_transaction("reward", miner, self.rewards, None)
        self.network.block_mined(self.chain)
    
    def add_transaction(self, sender, recv, amount, sender_private_key):
        log(f"adding a transaction from {sender} to {recv}")
        transaction = Transaction(sender, recv, amount)
        transaction.sign(sender_private_key)
        self.pending.append(transaction)
    
    def last_block(self):
        return self.chain[-1]
    
    def add_block(self, block):
        self.chain.append(block)
    
    def create_genesis_block(self):
        log("creating genesis block...")
        block = Block([], datetime.now(), 0, "NONE")
        block.mine(self.difficulty)
        return block
    
    def new_chain(self, new_chain):
        if self.valid_chain(new_chain) and len(new_chain) > len(self):
            self.chain = new_chain    
    
    def json(self):
        return {
            "chain": [block.json() for block in self.chain],
            "pending": [ta.json() for ta in self.pending],
            "nodes": self.network.json()
        }
    
    def __len__(self):
        return len(self.chain)
    
    @staticmethod
    def valid_chain(chain):
        for i in range(chain):
            if not chain[i].valid(chain[i - 1]):
                return False
        return True
    
    @staticmethod
    def generate_user():
        key = RSA.generate(bits=2048)
        return key.export_key(), key.public_key().export_key()
