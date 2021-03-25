from blockchain import Blockchain, Wallet, Socketserver, utils, log
import getopt
import sys
from time import sleep

options = getopt.getopt(sys.argv[1:], "p:w:u:n:s:")[0]

def get_option(options, opt):
    for option, arg in options:
        if option == f"-{opt}":
            return arg

def get_nodes(file):
    f = open(file)
    lines = f.readlines()
    f.close()
    return [
        (line.split(":")[0], int(line.split(":")[1])) for line in lines
    ]

IP = "192.168.178.34" #utils.get_ip()
PORT = int(get_option(options, "p"))
if not PORT: PORT = 8888
ADDR = (IP, PORT)
PRIVATE_KEY_FILE = get_option(options, "w")
PUBLIC_KEY_FILE = get_option(options, "u")
NODES = get_nodes(get_option(options, "n"))
SLEEP = get_option(options, "s")
if SLEEP: SLEEP = float(SLEEP)

wallet = Wallet.from_files(PRIVATE_KEY_FILE, PUBLIC_KEY_FILE)
blockchain = Blockchain(ADDR, wallet, NODES)
server = Socketserver(blockchain, ADDR)
blockchain.network.update_nodes(now=True)
blockchain.load()

while True:
    try:
        blockchain.mine_pending()
        log.log(f"your coins: {blockchain.get_balance(wallet.address)}", "external")
        log.log(f"other's coins: {blockchain.get_balance('3423cf3bad6272395f7717f1e12059dfb6e26adcb463ee85586020da9614391df184de17a83289ab700bba60e853c1c36ae3e4e513315f5f45c0d5c0364e8b80')}", "external")
        if SLEEP: sleep(SLEEP)
    except KeyboardInterrupt:
        # TODO create exit function
        server.close()
        break

sys.exit()
