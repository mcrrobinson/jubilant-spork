# jubilant-spork

This project is a simulation of a multi-level distributed caching system for blockchain networks.

## How does it work
Segregates nodes into CU (concencus units). Nodes within a CU contain partial information on the ledger. Within a CU, the partial ledgers from all nodes adds up to a complete ledger. The nodes contain different amounts of information based on their SV (security value). The nodes that have been in the network the longest have the highest SV and thus hold more ledger information than other nodes. One node in the CU is a master node and the master node always contains a copy of the entire ledger for availability purposes. More frequently accessed network blocks will have a higher AV (access value). High AV blocks are more commonly cloned as opposed to less frequently accessed blocks resulting in a caching strucutre.
