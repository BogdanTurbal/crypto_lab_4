import time
import json

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, timestamp: float = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def __str__(self):
        return json.dumps(self.to_dict(), sort_keys=True)
