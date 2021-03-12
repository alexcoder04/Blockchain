from blockchain_new import Blockchain, Block, Transaction
from datetime import datetime
import hashlib
import pprint

blockchain = Blockchain(2, 30)

chicken_private, chicken_public = blockchain.generate_user()
print(chicken_private, chicken_public)

blockchain.add_transaction("chickenking", "andreas", 10, chicken_private)

blockchain.mine_pending("andreas")

pprint.pprint(blockchain.json())

