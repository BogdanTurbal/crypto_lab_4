import hashlib
import time
from typing import List
from transaction import Transaction
from merkle_tree import calculate_merkle_root

class Block:
    def __init__(self, transactions: List[Transaction], prev_hash: str = '', nonce: int = 0):
        self.transactions = transactions
        self.timestamp = time.time()
        self.prev_hash = prev_hash
        self.hash = ''
        self.nonce = nonce
        self.merkle_root = calculate_merkle_root(transactions)

    def calculate_hash(self) -> str:
        block_string = str(self.merkle_root) + str(self.timestamp) + self.prev_hash + str(self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        return {
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'prev_hash': self.prev_hash,
            'hash': self.hash,
            'nonce': self.nonce,
            'merkle_root': self.merkle_root
        }

    def __str__(self):
        return json.dumps(self.to_dict(), sort_keys=True)
