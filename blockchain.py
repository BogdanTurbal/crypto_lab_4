import json
from typing import List, Dict, Tuple
from block import Block
from transaction import Transaction
from merkle_tree import calculate_merkle_root

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self) -> Block:
        genesis_block = Block(transactions=[])
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def add_block(self, transactions: List[Transaction]):
        prev_block = self.chain[-1]
        new_block = Block(transactions=transactions, prev_hash=prev_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.prev_hash != prev_block.hash:
                return False

            if current_block.merkle_root != calculate_merkle_root(current_block.transactions):
                return False

        return True

    def get_balances(self, block_index: int) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
        if block_index < 0 or block_index >= len(self.chain):
            return None

        balances = {}
        min_balances = {}
        max_balances = {}

        for i in range(block_index + 1):
            block = self.chain[i]
            for tx in block.transactions:
                balances[tx.sender] = balances.get(tx.sender, 0) - tx.amount
                balances[tx.receiver] = balances.get(tx.receiver, 0) + tx.amount

                min_balances[tx.sender] = min(min_balances.get(tx.sender, balances[tx.sender]), balances[tx.sender])
                min_balances[tx.receiver] = min(min_balances.get(tx.receiver, balances[tx.receiver]), balances[tx.receiver])

                max_balances[tx.sender] = max(max_balances.get(tx.sender, balances[tx.sender]), balances[tx.sender])
                max_balances[tx.receiver] = max(max_balances.get(tx.receiver, balances[tx.receiver]), balances[tx.receiver])

        return balances, min_balances, max_balances

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    @staticmethod
    def load_from_file(filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
        blockchain = Blockchain()
        blockchain.chain = [Blockchain.block_from_dict(block_dict) for block_dict in data]
        return blockchain

    @staticmethod
    def block_from_dict(block_dict: dict) -> Block:
        transactions = [Transaction(**tx_dict) for tx_dict in block_dict['transactions']]
        block = Block(transactions=transactions, prev_hash=block_dict['prev_hash'], nonce=block_dict['nonce'])
        block.timestamp = block_dict['timestamp']
        block.hash = block_dict['hash']
        block.merkle_root = block_dict['merkle_root']
        return block
