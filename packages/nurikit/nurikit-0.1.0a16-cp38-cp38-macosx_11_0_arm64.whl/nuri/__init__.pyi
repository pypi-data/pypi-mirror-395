"""

Project NuriKit: *the* fundamental software platform for chem- and
bio-informatics.
"""
from __future__ import annotations
from nuri import _log_adapter
import nuri.core._core
from nuri.core._core import seed_thread
from nuri.fmt import readfile
from nuri.fmt import readstring
from nuri.fmt import to_mol2
from nuri.fmt import to_pdb
from nuri.fmt import to_sdf
from nuri.fmt import to_smiles
__all__: list = ['__version__', 'periodic_table', 'readfile', 'readstring', 'seed_thread', 'to_mol2', 'to_pdb', 'to_sdf', 'to_smiles']
__full_version__: str = '0.1.0a16'
__version__: str = '0.1.0a16'
periodic_table: nuri.core._core.PeriodicTable  # value = <nuri.core._core.PeriodicTable object>
