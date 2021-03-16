import socket
from threading import Thread
import json
from .log import log

class Socketserver:
    def __init__(self, blockchain, addr):
        log("initializing socket server...")
        self.blockchain = blockchain
        self.ADDR = addr
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!QUIT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(self.ADDR)
        except OSError:
            log("the port you chose is already used", "error")
            log("Maybe another program runs on that port, you already started the blockchain or it just crashed")
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
            self.send(json.dumps(self.blockchain.network.json()), conn)
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
            print(self.blockchain.json())
            return
        log(f"{addr} sent an invalid command", "warning")
        self.send("{}", conn)
        return
