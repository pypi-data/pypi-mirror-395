# ------------------------------------------------------------
# sage_lib/visualization/PartitionProvider.py
# ------------------------------------------------------------
"""
Adapter class that wraps a `sage_lib.partition.Partition` object
to provide a uniform interface for visualization tools.

This class translates the data structures and naming conventions
used in `Partition` into a standardized protocol that
`browse_structures()` or any 3D viewer can consume directly.
"""

import numpy as np


class PartitionProvider:
    """
    Wraps your `sage_lib.partition.Partition` object to match the
    `StructureProvider` protocol expected by visualization utilities.
    """

    def __init__(self, partition):
        """
        Parameters
        ----------
        partition : sage_lib.partition.Partition
            The Partition object containing atomic configurations.
        """
        self.p = partition

    # ------------------------------------------------------------
    # Basic container interface
    # ------------------------------------------------------------
    def __len__(self) -> int:
        """Return the number of structure containers."""
        return self.p.size

    def __getitem__(self, idx: int):
        """Enable indexing: provider[i] → structure i."""
        return self.get(idx)

    # ------------------------------------------------------------
    # Data accessors
    # ------------------------------------------------------------
    def get_all_E(self):
        """Return an array of total energies for all structures."""
        return np.array(self.p.get_all_energies())

    def get_all_compositions(self):
        """Return an array of compositions for all structures."""
        return np.array(self.p.get_all_compositions())

    def get_all_Ef(self):
        """
        Compute formation energies by linear regression:
        E ≈ C·μ  →  Ef = E - C·μ
        """
        C = self.get_all_compositions()
        
        E = np.zeros( C.shape[0] )
        Eall = self.get_all_E()
        E[:Eall.shape[0]] = Eall
        if len(C) == 0 or len(E) == 0:
            return np.array([])
        mu, *_ = np.linalg.lstsq(C, E, rcond=None)  # fit chemical potentials
        E_fit = C @ mu
        Ef = E - E_fit
        return Ef

    # ------------------------------------------------------------
    # Structure-level accessor
    # ------------------------------------------------------------
    def get(self, idx: int):
        """
        Get a single structure from the partition.

        Returns
        -------
        positions : np.ndarray, shape (N, 3)
            Atomic Cartesian coordinates [Å].
        lattice : np.ndarray, shape (3, 3)
            Lattice vectors as rows [Å].
        energy : float
            Total energy (eV).
        elements : list[str]
            Element symbols corresponding to each atom.
        colors : list[str] or None
            Optional per-atom color information (can be None).
        radii : list[float] or None
            Optional atomic radii (can be None).
        """
        c = self.p.containers[idx]
        APM = c.AtomPositionManager

        lattice = np.array(APM.latticeVectors)
        positions = np.array(APM.atomPositions)
        elements = list(APM.atomLabelsList)
        energy = getattr(APM, "E", 0.0) or 0.0

        # Optional placeholders for visual styling
        colors = None
        radii = None

        return positions, lattice, float(energy), elements, colors, radii



