from blockchain_new import Blockchain, Socketserver
import pprint

ADDR = ("192.168.178.34", 5555)

blockchain = Blockchain(ADDR, nodes=[("192.168.178.34", 8888)], difficulty=2, rewards=10)

server = Socketserver(blockchain, ADDR)

chicken_private, chicken_public = blockchain.generate_user()

blockchain.add_transaction("chickenking", "andreas", 10, chicken_private)

pprint.pprint(blockchain.json())

blockchain.mine_pending("andreas")

pprint.pprint(blockchain.json())
