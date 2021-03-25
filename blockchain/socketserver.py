import socket
from threading import Thread
import json
from .log import log
from .block import Block

class Socketserver:
    def __init__(self, blockchain, addr):
        log("initializing socket server...")
        self.blockchain = blockchain
        self.ADDR = addr
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!QUIT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server.bind(self.ADDR)
        except OSError:
            log("the port you chose is already used", "error")
            log("Maybe another program runs on that port, you already started the blockchain or it just crashed")
            self.blockchain.shutdown()
            exit(1)
        else:
            log("creating and starting new thread...")
            server_thread = Thread(target=self.run)
            server_thread.start()
    
    def run(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            log(f"{addr} connected")
            log("creating and starting new thread to handle the connection...")
            t = Thread(target=self.handle, args=(conn, addr))
            t.start()
    
    def send(self, msg, conn):
        msg = msg.encode(self.FORMAT)
        length = str(len(msg))
        length += (" " * (self.HEADER - len(length)))
        conn.send(length.encode(self.FORMAT))
        conn.send(msg)
        conn.close()
        
    def handle(self, conn, addr):
        command = conn.recv(self.HEADER).decode(self.FORMAT).strip()
        length = int(conn.recv(self.HEADER).decode(self.FORMAT))
        data = conn.recv(length)
        log(f"{addr} sent command: {command}")
        if command == "CHECK":
            self.blockchain.network.nodes_to_check.append(json.loads(data))
            resp_data = self.blockchain.network.json()
            resp_data.append(self.ADDR)
            print(resp_data)
            resp = json.dumps(resp_data)
            print(resp)
            self.send(resp, conn)
            #self.blockchain.network.update_nodes()
            return
        if command == "CHAIN":
            self.send(json.dumps([i.json() for i in self.blockchain.chain]), conn)
            return
        if command == "PENDING":
            self.send(json.dumps([i.json() for i in self.blockchain.pending]), conn)
            return
        if command == "MINED":
            self.send("{}", conn)
            log(f"{addr} MINED A BLOCK!!!")
            chain = []
            for b in json.loads(data):
                chain.append(Block.from_json(b))
            self.blockchain.new_chain(chain)
            return
        log(f"{addr} sent an invalid command", "warning")
        self.send("{}", conn)
        return
    
    def close(self):
        self.blockchain.shutdown()
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        exit(1)
