"""

The core module of NuriKit.

This module contains the core classes of NuriKit. The core module is not
very useful by itself, but is a dependency of many other modules. Chemical
data structures, such as elements, isotopes, and molecules, and also the
graph structure and algorithms, are defined in this module.
"""
from __future__ import annotations
import nuri.core._core
from nuri.core._core import Atom
from nuri.core._core import AtomData
from nuri.core._core import Bond
from nuri.core._core import BondConfig
from nuri.core._core import BondData
from nuri.core._core import BondOrder
from nuri.core._core import Chirality
from nuri.core._core import Element
from nuri.core._core import Hyb
from nuri.core._core import Isotope
from nuri.core._core import Molecule
from nuri.core._core import Mutator
from nuri.core._core import Neighbor
from nuri.core._core import PeriodicTable
from nuri.core._core import ProxySubAtom
from nuri.core._core import ProxySubBond
from nuri.core._core import ProxySubNeighbor
from nuri.core._core import ProxySubstructure
from nuri.core._core import SubAtom
from nuri.core._core import SubBond
from nuri.core._core import SubNeighbor
from nuri.core._core import Substructure
from nuri.core._core import SubstructureCategory
from nuri.core._core import SubstructureContainer
from nuri.core._core import seed_thread
__all__: list = ['Atom', 'AtomData', 'Bond', 'BondConfig', 'BondData', 'BondOrder', 'Chirality', 'Element', 'Hyb', 'Isotope', 'Molecule', 'Mutator', 'Neighbor', 'PeriodicTable', 'SubAtom', 'SubBond', 'SubNeighbor', 'Substructure', 'SubstructureCategory', 'SubstructureContainer', 'seed_thread']
periodic_table: nuri.core._core.PeriodicTable  # value = <nuri.core._core.PeriodicTable object>
