from .block import Block
from .transaction import Transaction
from .network import Network
from .log import log
from .wallet import Wallet
from datetime import datetime

class Blockchain:
    def __init__(self, addr, wallet=None, nodes=None, difficulty=2, rewards=10):
        log("initializing the blockchain...")
        self.network = Network(addr, nodes)
        if wallet:
            self.wallet = wallet
            log("wallet loaded")
        else:
            log("creating a new wallet...")
            self.wallet = Wallet()
        if not nodes:
            log("creating a new network...", "important")
            self.difficulty = difficulty
            self.rewards = rewards
            self.pending = []
            self.chain = [self.create_genesis_block()]
        else:
            self.buffer = {}
            self.buffer["difficulty"] = difficulty
            self.buffer["rewards"] = rewards
    
    def load(self):
        self.difficulty = self.buffer["difficulty"]
        self.rewards = self.buffer["rewards"]
        # TODO get pending, difficulty and rewards from the network
        self.pending = [Transaction.from_json(i) for i in self.network.get_pending()]
        self.chain = self.network.get_chain()
    
    def mine_pending(self, mining_func=None):
        log("creating new block...")
        block = Block(self.pending, datetime.now(), len(self), self.last_block().hash, self.difficulty)
        block.mine(mining_func=mining_func)
        self.add_block(block)
        self.pending = []
        # TODO safe rewards
        log("creating rewards transaction...")
        self.pending.append(Transaction("reward", self.wallet.address, self.rewards, signature="REWARDS"))
        self.network.block_mined(self.chain)
    
    def add_transaction(self, recv, amount):
        log(f"adding a transaction from {self.wallet.address} to {recv}")
        self.pending.append(self.wallet.create_send_transaction(recv, amount))
    
    def last_block(self):
        return self.chain[-1]
    
    def add_block(self, block):
        self.chain.append(block)
    
    def create_genesis_block(self):
        log("creating genesis block...")
        block = Block([], datetime.now(), 0, "NONE", self.difficulty)
        block.mine()
        return block
    
    def new_chain(self, new_chain):
        if self.valid_chain(new_chain) and len(new_chain) > len(self):
            log("a new chain was accepted")
            self.chain = new_chain

    def get_balance(self, user):
        log(f"checking balance for {user}...")
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.recv == user:
                    balance += transaction.amount
        return balance
    
    def shutdown(self, code=0):
        log("shutting down...")
    
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
        for i in range(len(chain)):
            # TODO validate prev block
            #if not chain[i].valid(chain[i - 1]):
            if not chain[i].valid():
                return False
        return True
