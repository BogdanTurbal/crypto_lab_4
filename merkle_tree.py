import hashlib
from typing import List
from transaction import Transaction

def calculate_merkle_root(transactions: List[Transaction]) -> str:
    if len(transactions) == 0:
        return ''

    tx_hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in transactions]

    while len(tx_hashes) > 1:
        new_level = []
        for i in range(0, len(tx_hashes), 2):
            left = tx_hashes[i]
            right = tx_hashes[i + 1] if i + 1 < len(tx_hashes) else left
            new_level.append(hashlib.sha256((left + right).encode()).hexdigest())
        tx_hashes = new_level

    return tx_hashes[0]
