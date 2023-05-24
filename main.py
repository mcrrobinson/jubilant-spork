
# Start the network this this single CU and single node.
import math
from defs.chain import Ledger
from defs.protocol import ConcencusUnit, Network, Node, Position, generateNodeUUID, SClass
import seaborn as sns
import matplotlib.pyplot as plt


def bytes_to_mb(bytes: int) -> int:
    return bytes / 1000000


def simulation(simulated_ledger_size: int, simulated_node_count: int, new_method: bool) -> int:

    ledger = Ledger(blocks=[], current_transactions=[])
    for i in range(simulated_ledger_size):
        transaction = f"Transaction {i} - adding some extra information to see how much this affects the size of the block."
        ledger.add_transaction(transaction).mine()

    ledger.sort()
    network = Network(
        units=[ConcencusUnit([Node(
            name=generateNodeUUID(),
            position=Position(0, 0),
            lifespan=10000,
            master=True,
            s_class=SClass.Strongest,
            ledger=ledger)])],
        new_method=new_method)

    for i in range(simulated_node_count):
        network.add_node(Node(
            name=generateNodeUUID(),  # Generate random node UUID
            position=Position(0, i),  # Simulating world position.
            lifespan=i * 1000,  # Simulating lifespan for the nodes.
            master=False))

    size = network.get_network_size()
    return bytes_to_mb(size)


old_method = []
new_method = []

iteration_range = range(10000, 100000, 5000)
for i in iteration_range:
    print(f"Iteration: {i}")
    old_method.append(simulation(i, 10, new_method=False))
    new_method.append(simulation(i, 10, new_method=True))

print(old_method)
print(new_method)
print(list(iteration_range))
sns.scatterplot(x=iteration_range, y=new_method)
sns.scatterplot(x=iteration_range, y=old_method)

plt.xlabel('Ledger size (blocks)')
plt.ylabel('Network size (MB)')

plt.legend(['New method', 'Old method'])
plt.show()
