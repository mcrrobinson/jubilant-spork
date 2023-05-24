import hashlib
from pprint import pprint
import random


class Kademlia:
    def __init__(self, k=20, alpha=3):
        self.k = k
        self.alpha = alpha
        self.node_id = self.generate_node_id()
        self.routing_table = {}

    # Generate a random 160-bit node ID
    def generate_node_id(self):
        return hashlib.sha1(str(random.random()).encode()).hexdigest()

    # Calculate the distance between two nodes
    def distance(self, a, b):
        return int(a, 16) ^ int(b, 16)

    # Add a node to the routing table
    def add_node(self, node_id, node):
        if node_id not in self.routing_table:
            self.routing_table[node_id] = node

    # Remove a node from the routing table
    def remove_node(self, node_id):
        if node_id in self.routing_table:
            del self.routing_table[node_id]

    # Find the k closest nodes to a given ID
    def find_closest_nodes(self, target_id):
        nodes = sorted(self.routing_table.values(),
                       key=lambda node: self.distance(node.node_id, target_id))
        return nodes[:self.k]

    # Find the node responsible for a given ID
    def find_node(self, target_id):
        nodes = self.find_closest_nodes(target_id)
        for node in nodes:
            if node.node_id == target_id:
                return node
        return None

    # Lookup a key in the network
    def lookup_key(self, key):
        nodes = self.routing_table.values()
        contacted = []
        while len(nodes) > 0 and len(contacted) < self.k:
            node = nodes.pop(0)
            contacted.append(node)
            nodes.extend(self.find_closest_nodes(key) - set(contacted))
        return contacted

# Define the Node class


class Node:
    def __init__(self, node_id):
        self.node_id = node_id

    def __repr__(self):
        return f'Node[node_id={self.node_id}]'


# Example usage
kademlia = Kademlia()
node1 = Node(kademlia.generate_node_id())
node2 = Node(kademlia.generate_node_id())
node3 = Node(kademlia.generate_node_id())
node4 = Node(kademlia.generate_node_id())
kademlia.add_node(node1.node_id, node1)
kademlia.add_node(node2.node_id, node2)
kademlia.add_node(node3.node_id, node3)
kademlia.add_node(node4.node_id, node4)
closest_nodes = kademlia.find_closest_nodes(node1.node_id)

pprint(kademlia.routing_table)
pprint(closest_nodes)
