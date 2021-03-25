import hashlib
import time
from datetime import datetime
from .transaction import Transaction
from .log import log

class Block:
    def __init__(self, transactions, time, index, prev, difficulty, nonce=None):
        self.mined = False
        self.index = index
        self.time = time
        self.transactions = transactions
        self.prev = prev
        self.difficulty = difficulty
        self.nonce = 0
        if nonce: self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def mine(self, mining_func=None):
        if self.mined == True:
            log("block is already mined", "error")
            raise Exception("Trying to mine block is already mined")
        if mining_func:
            log("custom mining functions currently not supported", "warning")
            #self.nonce = mining_func(self.copy(), difficulty)
        start = datetime.now()
        while True:
            if self.calculate_hash().startswith("0" * self.difficulty):
                self.hash = self.calculate_hash()
                self.mined = True
                log(f"block is mined, took {str(datetime.now() - start)}")
                log(f"hash is {self.hash}")
                break
            self.nonce += 1
            time.sleep(0.05)
    
    def calculate_hash(self):
        transactions_str = ""
        for ta in self.transactions:
            transactions_str += str(ta)
        hash_str = (transactions_str + str(self.time) + self.prev + str(self.nonce)).encode()
        return hashlib.sha1(hash_str).hexdigest()
    
    def valid(self):
        # TODO implement this to check trabsactions
        #for ta in self.transactions:
        #    if not ta.valid():
        #        return False
        return self.hash == self.calculate_hash() and self.hash.startswith("0" * self.difficulty)
    
    def json(self):
        return {
            "index": self.index,
            "time": str(self.time),
            "transactions": [ta.json() for ta in self.transactions],
            "prev": self.prev,
            "hash": self.hash,
            "nonce": self.nonce,
            "difficulty": self.difficulty
        }
    
    def copy(self):
        return Block(self.transactions, self.time, self.index, self.prev)
    
    @classmethod
    def from_json(cls, json):
        log("creating block from json...")
        return cls([Transaction.from_json(ta) for ta in json["transactions"]], json["time"], json["index"], json["prev"], json["difficulty"], nonce=json["nonce"])
