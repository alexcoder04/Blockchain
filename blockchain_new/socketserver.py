import socket
from threading import Thread
import json

class Socketserver:
    def __init__(self, blockchain, addr):
        self.blockchain = blockchain
        self.ADDR = addr
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!QUIT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(self.ADDR)
        except OSError:
            print("[ERROR] The port you chose is already used")
            print("[INFO] Maybe another program runs on that port, you already started the blockchain or it just crashed")
            exit(1)
        else:
            server_thread = Thread(target=self.run)
            server_thread.start()
    
    def run(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            t = Thread(target=self.handle, args=(conn, addr))
            t.start()
    
    def send(self, msg, conn):
        print(f"Sending message: {msg}")
        msg = msg.encode(self.FORMAT)
        length = str(len(msg))
        length += (" " * (self.HEADER - len(length)))
        conn.send(length.encode(self.FORMAT))
        conn.send(msg)
        conn.close()
        
    def handle(self, conn, addr):
        print(f"Connected to {addr}")
        command = conn.recv(self.HEADER).decode(self.FORMAT).strip()
        length = int(conn.recv(self.HEADER).decode(self.FORMAT))
        data = conn.recv(length)
        print(f"{addr}: {command}")
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
            print("[INFO] SOMEONE ELSE MINED A BLOCK!!!")
            print(self.blockchain.json())
            return
