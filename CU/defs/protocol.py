from enum import Enum
import hashlib
import random
import uuid

from defs.helper import INT_BYTE_SIZE, convert_size

server = 'pool.ntp.org'


def generateNodeUUID() -> str:
    return str(uuid.uuid4())


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
        return len(self.block_hash) + len(self.previous_block_hash) + len(self.transaction_list)

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
        return sum([block.__sizeof__() for block in self.blocks]) + INT_BYTE_SIZE

    def __repr__(self) -> str:
        return self.__str__()


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Position[X={self.x}, Y={self.y}]'


class SClass(Enum):
    Weakest = 4
    Weak = 3
    Strong = 2
    Strongest = 1

    def __repr__(self):
        return self.__str__()


class Node:
    def __init__(
            self,
            name: str,
            position: Position,
            lifespan: int,
            master: bool = False,
            s_class: SClass = None,
            ledger: Ledger = None):
        self.name = name
        self.position = position
        self.simulated_lifespan = lifespan
        self.master = master
        self.s_class = s_class
        self.ledger = ledger

    def __str__(self):
        return f"\nNode[id={self.name}, lifespan={self.simulated_lifespan}, s_class={self.s_class}, ledger={self.ledger is not None}, blocks={self.ledger.get_block_count()}]"

    def __repr__(self) -> str:
        return self.__str__()


class ConcencusUnit:
    def __init__(self, nodes: list[Node], full: bool = False):
        self.nodes = nodes
        self.full = full

    def add_node(self, node: Node):
        if self.full:
            raise Exception("Concencus unit is full")

        self.nodes.append(node)

        if len(self.nodes) == 4:
            self.full = True

        # If node needs reshuffling, do it...

    def remove_node(self, node: Node):
        if len(self.nodes) == 0:
            raise Exception("Concencus unit is empty")

        self.nodes.remove(node)

        if len(self.nodes) == 3:
            self.full = False

    def nodes_needed(self) -> list:
        if self.full:
            return []

        types = [SClass.Weakest, SClass.Weak, SClass.Strong, SClass.Strongest]
        for node in self.nodes:
            if node.s_class in types:
                types.remove(node.s_class)

        return types

    def __str__(self):
        return f"\nConcencusUnit[nodes={self.nodes}]"

    def __repr__(self) -> str:
        return self.__str__()


class Network:
    def __init__(self, units: list[ConcencusUnit], new_method: bool):
        self.units = units
        self.lifespans = self.update_lifespans()
        self.new_method = new_method

    def add_node(self, node: Node):

        # Update lifespans each time.
        self.lifespans = self.update_lifespans()

        for unit in self.units:

            nodes_needed = unit.nodes_needed()
            if node.s_class:
                if node.s_class in nodes_needed:
                    unit.add_node(node)
                    return
            else:
                self.update_lifespans()
                if node.simulated_lifespan <= self.lifespans[0]:
                    node.s_class = SClass.Weakest
                elif node.simulated_lifespan <= self.lifespans[1]:
                    node.s_class = SClass.Weak
                elif node.simulated_lifespan <= self.lifespans[2]:
                    node.s_class = SClass.Strong
                elif node.simulated_lifespan <= self.lifespans[3]:
                    node.s_class = SClass.Strongest
                else:
                    raise Exception("Node lifespan is too high")

                # Simulate traversing and downloading the ledger from another node.

                if self.new_method:
                    for c_node in unit.nodes:

                        # Add ledger info...
                        if c_node.s_class == SClass.Strongest:
                            node.ledger = Ledger(
                                c_node.ledger.get_block_range(
                                    0, c_node.ledger.get_block_count() // node.s_class.value))
                            break
                else:
                    for c_node in unit.nodes:
                        if c_node.s_class != None:
                            node.ledger = Ledger(
                                c_node.ledger.get_block_range(
                                    0, c_node.ledger.get_block_count()))
                            break
                if node.s_class in nodes_needed:
                    unit.add_node(node)
                    return

        self.units.append(ConcencusUnit([node]))

    def update_lifespans(self):
        shortest = int(1e9)
        largest = 0
        for unit in self.units:
            for node in unit.nodes:
                if node.simulated_lifespan < shortest:
                    shortest = node.simulated_lifespan
                if node.simulated_lifespan > largest:
                    largest = node.simulated_lifespan

        # This isn't right, but works for now.

        difference = largest - shortest

        if difference == 0:
            increment = largest / 4
        else:
            increment = difference / 4
        self.lifespans = [increment, increment * 2, increment * 3, largest]

    def get_concencus_units(self):
        return self.units

    def get_network_size(self) -> int:
        return sum([
            sum([node.ledger.__sizeof__() for node in unit.nodes
                 ]) for unit in self.units])


# print(network.get_concencus_units())


# Upon connecting, nodes need to syncronise their availability clocks.
# Every X minutes (configurable) the nodes collectively decide which SC layer they belong to.
# If there is a change in SC layer, the nodes need to adjust resources they are holding.


# Miner validates new transactions. Doing proof of work.

# Once they verify most recent block is valid. Try create candidate block by adding uncomfirmed transactions from the pool.
