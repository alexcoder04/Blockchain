from Crypto.PublicKey import RSA
from hashlib import sha512
from .transaction import Transaction
from .log import log

class Wallet:
    def __init__(self, private=None, public=None):
        if (not public) or (not private):
            log("generating new wallet...", "important")
            private, public = self.generate_key()
            log("your private key has been generated")
            log("SAVE IT, IT IS THE ONLY WAY YOU CAN ACCESS YOUR COINS!!!", "important")
            print(private)
            input("press [enter] to continue")
            log("your public key has been generated")
            print(public)
            input("press [enter] to continue")
        self.private = private
        self.public = public
        self.address = sha512(self.public).hexdigest()
    
    def create_send_transaction(self, recv, amount):
        ta = Transaction(self.address, recv, amount)
        ta.sign(self.private)
        return ta
    
    @staticmethod
    def generate_key():
        key = RSA.generate(bits=2048)
        return key.export_key(), key.public_key().export_key()
    
    @classmethod
    def from_files(cls, private, public):
        log(f"generating a wallet from files: {private}, {public}")
        f = open(private, "rb")
        private = f.read()
        f.close()
        f = open(public, "rb")
        public = f.read()
        f.close()
        return cls(private.replace(b"\\n", b"\n"), public.replace(b"\\n", b"\n"))
