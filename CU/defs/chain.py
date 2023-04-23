

import hashlib
import random
from defs.helper import INT_BYTE_SIZE


class Block:
    def __init__(self, previous_block_hash: str, transaction_list: str):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        self.access_counter = random.randint(0, 1000)

        self.block_data = "-".join(transaction_list) + \
            "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

    def __str__(self):
        return f'\tBlock[hash={self.block_hash}, previous_hash={self.previous_block_hash}, access_counter={self.access_counter}]'

    def __sizeof__(self) -> int:
        return len(self.block_hash) + len(self.block_data) + len(self.previous_block_hash) + len(self.transaction_list) + INT_BYTE_SIZE

    def __repr__(self) -> str:
        return self.__str__()


class Ledger:
    def __init__(self, blocks: list[Block] = [], current_transactions: list[str] = []):
        self.blocks = blocks
        self.current_transactions = current_transactions

    def add_transaction(self, transaction):
        self.current_transactions.append(transaction)
        return self

    def mine(self):
        previous_block_hash = self.blocks[-1].block_hash if len(
            self.blocks) > 0 else "Initial String"

        block = Block(previous_block_hash, self.current_transactions)
        block.access_counter += 1

        self.blocks.append(block)
        self.current_transactions = []
        return block

    def get_block_range(self, start, end):
        return self.blocks[start:end]

    def sort(self):
        self.blocks.sort(key=lambda x: x.access_counter, reverse=True)

    def get_block_count(self):
        return len(self.blocks)

    def get_transaction_count(self):
        return len(self.current_transactions)

    def __str__(self):
        return f"Ledger[blocks={self.blocks}]"

    def __sizeof__(self) -> int:
        return (len(self.blocks) * Block.__sizeof__(self.blocks[0]) if self.blocks else 0) + INT_BYTE_SIZE

    def __repr__(self) -> str:
        return self.__str__()
