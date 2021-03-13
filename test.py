from blockchain_new import Blockchain, Socketserver
import pprint

ADDR = ("192.168.178.34", 8888)

blockchain = Blockchain(ADDR)

server = Socketserver(blockchain, ADDR)

chicken_private, chicken_public = blockchain.generate_user()

blockchain.add_transaction("chickenking", "andreas", 10, chicken_private)

blockchain.mine_pending("andreas")

pprint.pprint(blockchain.json())
