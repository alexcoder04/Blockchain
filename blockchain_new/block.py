import hashlib
from .transaction import Transaction
from .log import log

class Block:
    def __init__(self, transactions, time, index, prev):
        log("creating a block...")
        self.mined = False
        self.index = index
        self.time = time
        self.transactions = transactions
        self.prev = prev
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def mine(self, difficulty):
        if self.mined == True:
            log("block is already mined", "error")
            raise Exception("Trying to mine block is already mined")
        while True:
            if self.calculate_hash().startswith("0" * difficulty):
                self.hash = self.calculate_hash()
                self.mined = True
                log("block is mined!")
                break
            self.nonce += 1
    
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
        return self.hash == self.calculate_hash()
    
    def json(self):
        return {
            "index": self.index,
            "time": str(self.time),
            "transactions": [ta.json() for ta in self.transactions],
            "prev": self.prev,
            "hash": self.hash
        }
    
    @classmethod
    def from_json(cls, json):
        return cls([Transaction.from_json(ta) for ta in json["transactions"]], json["time"], json["index"], json["prev"])
