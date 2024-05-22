from transaction import Transaction
from blockchain import Blockchain

# creating blockchain and adding blocks
blockchain = Blockchain()

# adding transactions
transactions = [
    Transaction(sender="Alice", receiver="Bob", amount=10),
    Transaction(sender="Bob", receiver="Charlie", amount=5)
]

# adding a block
blockchain.add_block(transactions)

# checking blockchain validity
print("Is blockchain valid?", blockchain.is_chain_valid())

# saving blockchain to file
blockchain.save_to_file('blockchain.json')

# loading blockchain from file
loaded_blockchain = Blockchain.load_from_file('blockchain.json')
print("Is loaded blockchain valid?", loaded_blockchain.is_chain_valid())

# get balances for a given block
balances, min_balances, max_balances = blockchain.get_balances(1)
print("Balances:", balances)
print("Min Balances:", min_balances)
print("Max Balances:", max_balances)
