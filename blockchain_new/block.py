import hashlib

class Block:
    def __init__(self, transactions, time, index, prev):
        self.mined = False
        self.index = index
        self.time = time
        self.transactions = transactions
        self.prev = prev
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def mine(self, difficulty):
        if self.mined == True:
            raise Exception("Trying to mine block is already mined")
        while True:
            if self.calculate_hash().startswith("0" * difficulty):
                self.hash = self.calculate_hash()
                self.mined = True
                break
            self.nonce += 1
    
    def calculate_hash(self):
        transactions_str = ""
        for ta in self.transactions:
            transactions_str += str(ta)
        hash_str = (transactions_str + str(self.time) + self.prev + str(self.nonce)).encode()
        return hashlib.sha1(hash_str).hexdigest()
    
    def json(self):
        return {
            "index": self.index,
            "time": str(self.time),
            "transactions": [ta.json() for ta in self.transactions],
            "prev": self.prev,
            "hash": self.hash
        }
