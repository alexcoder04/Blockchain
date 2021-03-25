from blockchain import Blockchain, Socketserver, Wallet, log
import pprint
import json
import os
from datetime import datetime

ADDR = ("192.168.178.34", 8888)
TMP = "/home/alex/tmp/blockchain"

if not os.path.isdir(TMP): os.mkdir(TMP)

def save_chain(c):
    f = open(TMP + "/" + str(datetime.now()) + ".json", "w")
    json.dump(c, f)

w = Wallet.from_files("me.private.rem", "me.public.rem")
b = Blockchain(ADDR, w)
s = Socketserver(b, ADDR)

while True:
    b.mine_pending()
    save_chain(b.json())
    log.log(f"your coins: {b.get_balance(w.address)}", "external")
    log.log(f"other's coins: {b.get_balance('f5b33ff11b27d8f58f4b6b2461c6715679bab303e90fb111c6c529bd583cf50ee44a61dfb94175711a54f02519f17f27dcabcb22b7c79e42ca3208cc2663d44f')}", "external")
