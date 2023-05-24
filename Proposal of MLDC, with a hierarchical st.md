Proposal of MLDC, with a hierarchical structure of distributed caching for blockchain that effectively reduces the storage costs with minimal network overhead without any centralised components. MLDC maintains blockchain hash consistency even when partial data is unavailable


Nodes in control unit store partial data of blockchain ledger and each CU maintains at least one copy of full ledger.

When block requested, navigate through headers of nodes in CU to get it. This increases query time. Block assignment optimisation (BAO) (heuristic algorithms) used to determine optimal assignment to decrease query cost. Reduces replication.

Storage Class (SC) : A storage class represents a group
of nodes with similar node availability levels


Proposals:
# IPFS but with forced smart caching... using access frequency.
# Blockchain with CU's.

- We divide nodes into SC groups based on node availability.
- Each SC group has access frequency level
- AF determined by number of accesses and threshold time.
- Nodes in SC group with higher AF are assigned more blocks.
- Highest SC group has all blocks.
- Each node removes an object when the access time exceeds the threshold time.
-  Every content and node are uniquely identified by their hash value and a distance between them is calculated by XOR of their hash.
- 