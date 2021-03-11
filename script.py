from blockchain_core import Blockchain

blockchain = Blockchain(
    address="1234567890123456",
    directory="data",
    tmp_dir="/home/alex/tmp/blockchain",
    queue="/home/alex/tmp/blockchain/queue"
)

blockchain.mine(
    efficiency=0.005
)
