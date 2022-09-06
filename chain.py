#!/usr/bin/env python3

import sys
import time
import hashlib

difficulty = 5

class Block():
    def __init__(self, data, previous_hash) -> None:
        self.data = data
        self.previous_hash = previous_hash
        # get timestamp in ms as whole number
        self.timestamp = time.time_ns() // 10**6
        self.nonce = 0
        self.hash = self.get_hash()

    def get_hash(self):
        payload = self.previous_hash + str(self.timestamp) + str(self.nonce) + self.data
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def mine(self, difficulty):
        target = difficulty * '0'

        while(self.hash[:difficulty] != target):
            self.nonce += 1
            self.hash = self.get_hash()

    def __str__(self):
        return 'Block: ' + str(self.__dict__)


def is_chain_valid(chain):
    previous = None
    hash_target = difficulty * '0'

    for i, current in enumerate(chain):
        if i == 0:
            continue
        previous = chain[i-1]

        if current.hash != current.get_hash():
            print('Block ' + str(i) + ': current hashes not equal')
            return False

        if previous.hash != current.previous_hash:
            print('Block ' + str(i) + ': previous hashes not equal')
            return False

        if current.hash[:difficulty] != hash_target:
            print('Block ' + str(i) + ': this block hasn\'t been mined')
            return False

    return True

def main():
    blockchain = []

    blockchain.append(Block('Hi im the first block', '0'))
    print('mining block 0...')
    blockchain[0].mine(difficulty)

    blockchain.append(Block('Yo im the second block', blockchain[-1].hash))
    print('mining block 1...')
    blockchain[1].mine(difficulty)

    blockchain.append(Block('Hey im the third block', blockchain[-1].hash))
    print('mining block 2...')
    blockchain[2].mine(difficulty)

    print('Blockchain is valid: ' + str(is_chain_valid(blockchain)))

    for b in blockchain:
        print(b)

    return 0

if __name__ == '__main__':
    sys.exit(main())