from blockchain_new import Blockchain, Socketserver
import pprint
import time

ADDR = ("192.168.178.34", 8888)

blockchain = Blockchain(ADDR)

server = Socketserver(blockchain, ADDR)

chicken_private, chicken_public = blockchain.generate_user()

blockchain.add_transaction("chickenking", "andreas", 10, chicken_private)

for i in range(10):
    blockchain.mine_pending("andreas")
    print(blockchain.json())
    time.sleep(1)

