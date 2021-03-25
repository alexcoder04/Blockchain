import socket
import json
import time
from threading import Thread
from .block import Block
from .log import log

# TODO socket connection
class Network:
    def __init__(self, addr, nodes=None):
        log("initializing the network connection...")
        self.ADDR = addr
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!QUIT"
        self.nodes = []
        self.update_is_pending = False
        if nodes:
            self.nodes_to_check = nodes
        else:
            self.nodes_to_check = []
    
    def update_nodes(self, now=False):
        if not now:
            if self.update_is_pending: return
            self.update_is_pending = True
            t = Thread(target=self.nodes_updater)
            t.start()
            return
        self._update_nodes()
    
    def nodes_updater(self):
        while True:
            self._update_nodes()
            time.sleep(10)
    
    def _update_nodes(self):
        log("updating nodes...")
        # TODO add singing
        if len(self.nodes_to_check) == 0:
            print("the only node in network")
            return
        verified_nodes = []
        new_to_check = []
        for node in self.nodes_to_check:
            log(f"checking node {node[0]}...")
            # TODO check if node send a valid response
            resp = self.request(tuple(node), "CHECK", data=json.dumps(self.ADDR))
            print(resp)
            if not resp: continue
            verified_nodes.append(node)
            new_to_check.append(node)
            for node_from_other in resp:
                if node_from_other not in new_to_check:
                    new_to_check.append(node_from_other)
        self.nodes, self.nodes_to_check = verified_nodes, new_to_check
        log(f"nodes online: {self.nodes}")
        if len(self.nodes) == 0:
            log("No nodes online", "error")
            exit(1)
    
    def get_chain(self):
        log("loading current blockchain from the network...")
        max_length = 0
        chain = []
        for node in self.nodes:
            log(f"loading chain from {node[0]}...")
            new_chain = [Block.from_json(i) for i in self.request(node, "CHAIN")]
            if len(new_chain) > max_length and self.valid_chain(new_chain):
                chain = new_chain
                max_length = len(chain)
        return chain
    
    def request(self, node, command, data=""):
        print(f"request to {node}, command={command}, data={data}")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     client.connect(node)
        # except ConnectionRefusedError:
        #     log(f"node {node} unreachable", "error")
        #     return None
        client.connect(node)

        command += " " * (self.HEADER - len(command))
        length = str(len(data))
        length += (" " * (self.HEADER - len(length)))

        client.send(command.encode(self.FORMAT))
        client.send(length.encode(self.FORMAT))
        client.send(data.encode(self.FORMAT))

        length = int(client.recv(self.HEADER))
        resp = client.recv(length).decode(self.FORMAT)

        print(resp)
        
        return json.loads(resp)
    
    def get_pending(self):
        log("loading pending transactions from the network...")
        pending = []
        for node in self.nodes:
            log(f"loading transactions from {node[0]}")
            data = self.request(node, "PENDING")
            for ta in data:
                # TODO check if transaction has been already verified
                if ta not in pending:
                    pending.append(ta)
        return pending
    
    def block_mined(self, chain):
        for node in self.nodes:
            log(f"sending 'mined' message to {node[0]}")
            self.request(node, "MINED", data=json.dumps([i.json() for i in chain]))
    
    def json(self):
        return self.nodes
    
    @staticmethod
    def valid_chain(chain):
        for i in range(len(chain)):
            # TODO make that check the hash of the prev block
            if not chain[i].valid():
                return False
        return True


