from datetime import datetime
import hashlib
from Crypto.PublicKey import RSA

class Transaction:
    def __init__(self, sender, recv, amount, signature=None, time=None):
        self.sender = sender
        self.recv = recv
        self.amount = amount
        if time:
            self.time = time
        else:
            self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.signature = signature
    
    def sign(self, sender_private_key):
        if self.sender == "reward":
            self.signature = "REWARD"
            return
        key = RSA.import_key(sender_private_key)
        msg_hash = int.from_bytes(hashlib.sha512(str(self).encode()).digest(), byteorder="big")
        self.signature = pow(msg_hash, key.d, key.n)
    
    def valid(self, sender_public_key):
        if self.sender == self.recv:
            return False
        if not self.signature:
            return False
        msg_hash = int.from_bytes(hashlib.sha512(str(self).encode()).digest(), byteorder="big")
        key = RSA.import_key(sender_public_key)
        return pow(self.signature, key.e, key.n) == msg_hash
    
    def __str__(self):
        return f"{self.sender}:{self.recv}:{self.amount}:{self.time}"
    
    def json(self):
        return {
            "sender": self.sender,
            "recv": self.recv,
            "amount": self.amount,
            "time": self.time,
            "signature": self.signature
        }
    
    @classmethod
    def from_json(cls, json):
        return cls(json["sender"], json["recv"], json["amount"], json["signature"], json["time"])

