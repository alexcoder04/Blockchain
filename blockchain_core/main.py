import os
import time
import random
import hashlib

class Blockchain:
    first_block = "2911"

    def __init__(self, address, directory="blockchain", tmp_dir=".blockchain", queue=".blockchain/queue"):
        self.address = address
        if not os.path.isdir(directory):
            os.mkdir(directory)
        if not os.path.isfile(directory + "/0"):
            f = open(directory + "/0", "w")
            f.write(self.first_block)
            f.close()
        self.directory = directory
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)
        self.tmp_dir = tmp_dir
        f = open(tmp_dir + "/current", "w")
        f.write(str(self.get_last_block_number()))
        f.close()
        if not os.path.isfile(queue):
            f = open(queue, "w")
            f.close()
        self.queue_file = queue

    def mine(self, efficiency=0.1):
        old_block = self.get_last_block()
        new_block = ""
        transactions = self.get_transactions()
        for i in range(len(transactions)):
            if i != 0:
                new_block += "\n"
            new_block += transactions[i]
        new_block += f"\n0000000000000000:00000000000000000000000000000001:{self.address}"
        new_block += f"\n{self.hash(old_block)}"
        nonce_len = 1024 - len(new_block)
        for number in range((10 ** (nonce_len + 1)) - 1):
            print(number)
            if self.hash(new_block + f"\n{'0' * (nonce_len - len(str(number))) + str(number)}").startswith("00"):
                print(number)
                #print(self.hash(new_block + f"\n{'0' * (nonce_len - len(str(number))) + str(number)}"))
                #print(new_block + f"\n{'0' * (nonce_len - len(str(number))) + str(number)}")
                print("         BLOCK FOUND          ")
                self.commit_block(new_block + f"\n{'0' * (nonce_len - len(str(number)) - 1) + str(number)}")
                print(f"Your current balance: {self.calc_money()}  ")
                break
            time.sleep(efficiency)

    def commit_block(self, block):
        current_file = open(self.tmp_dir + "/current", "r+")
        current_number = int(current_file.read())
        block_file = open(self.directory + "/" + str(current_number + 1), "w")
        block_file.write(block)
        block_file.close()
        current_file.write(str(current_number + 1))
        current_file.close()

    def hash(self, string):
        return hashlib.sha1(string.encode("utf8")).hexdigest()

    def get_last_block(self):
        f = open(self.tmp_dir + "/current", "r")
        last_number = f.read()
        f.close()
        f = open(self.directory + "/" + last_number, "r")
        block = f.read()
        f.close()
        return block

    def get_last_block_number(self):
        i = 0
        while True:
            if not os.path.isfile(self.directory + "/" + str(i)):
                return i - 1
            i += 1

    def get_transactions(self, number=9):
        transactions = []
        while True:
            if os.path.exists(self.queue_file + ".lock"):
                time.sleep(0.5)
            else:
                lock = open(self.queue_file + ".lock", "w")
                f = open(self.queue_file, "r+")
                transactions_in_queue = f.readlines()
                if len(transactions_in_queue) < number:
                    for _ in range(number - len(transactions_in_queue)):
                        transactions_in_queue.append(f"{self.address}:{'0' * 32}:{self.address}")
                random.shuffle(transactions_in_queue)
                new_queue = []
                for i in range(len(transactions_in_queue)):
                    if i < number and transactions_in_queue[i]:
                        transactions.append(transactions_in_queue[i])
                    elif transactions_in_queue[i] != "":
                        new_queue.append(transactions_in_queue[i])
                f.write("\n".join(new_queue))
                f.close()
                lock.close()
                os.remove(self.queue_file + ".lock")
                break
        return transactions

    def calc_money(self):
        balance = 0
        for block in os.listdir(self.directory):
            f = open(self.directory + "/" + block)
            for line in f.readlines():
                if line.strip().endswith(self.address):
                    balance += int(line.split(":")[1])
        return balance
