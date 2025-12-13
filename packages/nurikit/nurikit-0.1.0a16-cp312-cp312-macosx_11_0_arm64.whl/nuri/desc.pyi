from __future__ import annotations
import numpy
import nuri.core._core
import typing
__all__: list[str] = ['shrake_rupley_sasa']
@typing.overload
def shrake_rupley_sasa(mol: nuri.core._core.Molecule, conf: int = 0, nprobe: int = 92, rprobe: float = 1.4) -> numpy.ndarray:
    """
    Calculate the Solvent-Accessible Surface Area (SASA) of a molecule conformation
    using the Shrake-Rupley algorithm.
    
    :param mol: The input molecule.
    :param conf: The conformation index. If not specified, uses the first
      conformation.
    :param nprobe: The number of probe spheres. Default is 92.
    :param rprobe: The radius of the probe spheres. Default is 1.4 angstroms.
    :returns: The calculated SASA values per atom (in angstroms squared).
    :raises IndexError: If the conformation index is out of range.
    :raises ValueError: If `nprobe` or `rprobe` is not positive.
    
    .. note::
      This function does not automatically handle implicit hydrogens. If the
      molecule contains implicit hydrogens, consider revealing them before calling
      this function for accurate results
      (see :func:`nuri.core.Molecule.reveal_hydrogens`).
    """
@typing.overload
def shrake_rupley_sasa(pts: typing.Any, radii: typing.Any, nprobe: int = 92, rprobe: float = 1.4) -> numpy.ndarray:
    """
    Calculate the Solvent-Accessible Surface Area (SASA) of a molecule conformation
    using the Shrake-Rupley algorithm.
    
    :param pts: The coordinates of the atoms, as a 2D array of shape ``(N, 3)``.
    :param radii: The radii of the atoms, as a 1D array of shape ``(N,)``.
    :param nprobe: The number of probe spheres. Default is 92.
    :param rprobe: The radius of the probe spheres. Default is 1.4 angstroms.
    :returns: The calculated SASA values per atom (in angstroms squared).
    :raises ValueError: If the number of `pts` and `radii` do not match, any `radii`
      are not positive, `nprobe` is not positive, or `rprobe` is not positive.
    """
