from blockchain_new import Blockchain, Socketserver, Wallet, log
import pprint
import time

my_ADDR = ("192.168.178.34", 8888)
other_ADDR = ("192.168.178.34", 9999)

def mining_func(block, difficulty):
    while True:
        if block.calculate_hash().startswith("0" * difficulty):
            return block.nonce
        block.nonce += 1

my_wallet = Wallet.from_files("me.private.rem", "me.public.rem")
other_wallet = Wallet.from_files("you.private.rem", "you.public.rem")

my_blockchain = Blockchain(my_ADDR, my_wallet)
my_server = Socketserver(my_blockchain, my_ADDR)

other_blockchain = Blockchain(other_ADDR, other_wallet, nodes=[my_ADDR])
other_server = Socketserver(other_blockchain, other_ADDR)

other_blockchain.add_transaction(my_wallet.address, 10)

for i in range(10):
    my_blockchain.mine_pending(mining_func)
    pprint.pprint(my_blockchain.json())
    print(my_blockchain.get_balance(my_wallet.address))
    time.sleep(1)
