# =============================
# graph_builder.py
# =============================

import numpy as np
from ase.neighborlist import neighbor_list
import networkx as nx
from ase.data import atomic_numbers
from ase import Atoms

element_props = {
    "Ni": {"Z": 28}, "Fe": {"Z": 26}, "V": {"Z": 23},
    "O": {"Z": 8}, "H": {"Z": 1}, "K": {"Z": 19}
}

class GraphBuilder:
    def __init__(self, cutoffs):
        self.cutoffs = cutoffs

    def build(self, container):
        graphs = {}
        positions = container.AtomPositionManager.atomPositions
        symbols = container.AtomPositionManager.atomLabelsList
        cell = container.AtomPositionManager.latticeVectors
        Zs = [atomic_numbers[s] for s in symbols]

        atoms = Atoms(
		    symbols=symbols,
		    positions=positions,
		    cell=cell,
		    pbc=True    # or [True, True, False] as needed
		)
        
        for c in self.cutoffs:
            i_idx, j_idx, _, dist = neighbor_list("ijDd", atoms, c)
            G = nx.Graph()
            for i, s in enumerate(symbols):
                G.add_node(i, element=s, Z=Zs[i])
            for i, j, d in zip(i_idx, j_idx, dist):
                if i < j:
                    G.add_edge(i, j, weight=float(d))
            graphs[c] = G
        return graphs

