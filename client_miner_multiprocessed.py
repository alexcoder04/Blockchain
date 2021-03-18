from blockchain import Blockchain, Wallet, Socketserver, utils
import getopt
import sys
import multiprocessing
import math

options = getopt.getopt(sys.argv, "p:w:u:n:s:c:")

def get_option(options, opt):
    for option, arg in options:
        if option == f"-{opt}":
            return arg
    return None

def get_nodes(file):
    f = open(file)
    lines = f.readlines()
    f.close()
    return [
        (line.split(":")[0], line.split(":")[1]) for line in lines
    ]

IP = utils.get_ip()
PORT = get_option(options, "p")
if not PORT: PORT = 8888
ADDR = (IP, PORT)
PRIVATE_KEY_FILE = get_option(options, "w")
PUBLIC_KEY_FILE = get_option(options, "u")
NODES = get_nodes(get_option(options, "n"))
SLEEP = float(get_option(options, "s"))
if SLEEP: from time import sleep
PROCESSES = get_option(options, "c")
if not PROCESSES: PROCESSES = 8

def mp_worker(queue, num_span, block, diff):
    for i in num_span:
        block.nonce = i
        if block.calculate_hash.startswith("0" * diff):
            queue.put({i: i})
            return
    queue.put({})

def calc_nonce(block, diff, num_span, processes=PROCESSES):
    queue = multiprocessing.Queue()
    chunks = int(math.ceil(len(num_span) / processes))
    procs = []
    for i in range(processes):
        proc = multiprocessing.Process(target=mp_worker, args=(queue, num_span[chunks * i, chunks * (i+1)], block, diff))
        procs.append(proc)
        proc.start()
    res = {}
    for i in range(processes):
        res.update(queue.get())
    for p in procs:
        p.join()
    for nonce in res:
        if res[nonce]: return res[nonce]

def mining_func(block, diff):
    i = 1
    while True:
        numbers = 100 * diff * i
        res = calc_nonce(block, diff, numbers)
        if res:
            return res
        i += 1

wallet = Wallet.from_files(PRIVATE_KEY_FILE, PUBLIC_KEY_FILE)
blockchain = Blockchain(ADDR, wallet, NODES)
server = Socketserver(blockchain, ADDR)

while True:
    try:
        blockchain.mine_pending()
        if SLEEP: time.sleep(SLEEP)
    except KeyboardInterrupt:
        # TODO create exit function
        print("EXITING")
        sys.exit()
