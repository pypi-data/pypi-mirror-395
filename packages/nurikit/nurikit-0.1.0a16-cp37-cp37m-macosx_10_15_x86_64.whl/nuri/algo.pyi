from __future__ import annotations
import nuri.core._core
import typing
__all__: list[str] = ['find_all_rings', 'find_relevant_rings', 'find_sssr', 'generate_coords', 'guess_all_types', 'guess_connectivity', 'guess_everything']
@typing.overload
def find_all_rings(mol: nuri.core._core.Molecule, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find all rings (a.k.a. elementary circuits) in a molecule.
    
    :param mol: The molecule to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    :raises ValueError: If the molecule has too many rings to find. Currently, this
      will fail if and only if any atom is a member of more than 100 rings.
    """
@typing.overload
def find_all_rings(sub: nuri.core._core.Substructure, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find all rings (a.k.a. elementary circuits) in a substructure.
    
    :param sub: The substructure to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    :raises ValueError: If the substructure has too many rings to find. Currently,
      this will fail if and only if any atom is a member of more than 100 rings.
    """
@typing.overload
def find_all_rings(sub: nuri.core._core.ProxySubstructure, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find all rings (a.k.a. elementary circuits) in a substructure.
    
    :param sub: The substructure to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    :raises ValueError: If the substructure has too many rings to find. Currently,
      this will fail if and only if any atom is a member of more than 100 rings.
    
    This is based on the algorithm by :cite:t:`algo:all-rings`.
    
    .. note::
      The time complexity of this function is inherently exponential, but it is
      expected to run in a reasonable time for most molecules in practice. See the
      reference for more details.
    """
@typing.overload
def find_relevant_rings(mol: nuri.core._core.Molecule, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find union of all SSSR (smallest set of smallest rings) in a molecule.
    
    :param mol: The molecule to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    """
@typing.overload
def find_relevant_rings(sub: nuri.core._core.Substructure, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find union of all SSSR (smallest set of smallest rings) in a substructure.
    
    :param sub: The substructure to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    """
@typing.overload
def find_relevant_rings(sub: nuri.core._core.ProxySubstructure, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find union of all SSSR (smallest set of smallest rings) in a substructure.
    
    :param sub: The substructure to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    """
@typing.overload
def find_sssr(mol: nuri.core._core.Molecule, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find a SSSR (smallest set of smallest rings) in a molecule.
    
    :param mol: The molecule to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    """
@typing.overload
def find_sssr(sub: nuri.core._core.Substructure, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find a SSSR (smallest set of smallest rings) in a substructure.
    
    :param sub: The substructure to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    """
@typing.overload
def find_sssr(sub: nuri.core._core.ProxySubstructure, max_size: int | None = None) -> list[nuri.core._core.Substructure]:
    """
    Find a SSSR (smallest set of smallest rings) in a substructure.
    
    :param sub: The substructure to find rings in.
    :param max_size: The maximum size of rings to find. If not specified, all rings
      are found.
    :return: A list of substructures, each representing a ring.
    :rtype: list[nuri.core.Substructure]
    
    .. note::
      This function does not guarantee that the returned set is unique, nor that the
      result is reproducible even for the same molecule.
    """
def generate_coords(mol: nuri.core._core.Molecule, method: str = 'DG', max_trial: int = 10) -> None:
    """
    Generate 3D coordinates of a molecule. The generated coordinates are stored in
    the last conformer of the molecule if the generation is successful.
    
    :param mol: The molecule to generate coordinates.
    :param method: The method to use for coordinate generation (case insensitive).
      Currently, only ``DG`` (distance geometry) is supported.
    :param max_trial: The maximum number of trials to generate trial distances.
    :raises ValueError: If the generation fails. On exception, the molecule is left
      unmodified.
    """
def guess_all_types(mol: nuri.core._core.Molecule, conf: int = 0) -> None:
    """
    Guess types of atoms and bonds, and number of hydrogens of a molecule.
    
    :param mol: The molecule to be guessed.
    :param conf: The index of the conformation used for guessing.
    :raises IndexError: If the conformer index is out of range.
    :raises ValueError: If the guessing fails. The state of molecule is not
      guaranteed to be preserved in this case. If you want to preserve the state,
      copy the molecule before calling this function using
      :meth:`~nuri.core.Molecule.copy`.
    
    .. tip::
      If want to find extra bonds that are not in the input molecule, consider using
      :func:`guess_everything()`.
    """
def guess_connectivity(mutator: nuri.core._core.Mutator, conf: int = 0, threshold: float = 0.5) -> None:
    """
    Guess connectivity information of a molecule.
    
    :param mutator: The mutator of the molecule to be guessed.
    :param conf: The index of the conformation used for guessing.
    :param threshold: The threshold for guessing connectivity. Will be added to the
      sum of two covalent radii of the atoms to determine the maximum distance
      between two atoms to be considered as bonded.
    :raises IndexError: If the conformer index is out of range. This function never
      fails otherwise.
    
    This function find extra bonds that are not in the input molecule. Unlike
    :func:`guess_everything()`, this function does not touch other information
    present in the molecule.
    
    .. tip::
      If want to guess types of atoms and bonds as well, consider using
      :func:`guess_everything()`.
    """
def guess_everything(mutator: nuri.core._core.Mutator, conf: int = 0, threshold: float = 0.5) -> None:
    """
    Guess connectivity information of a molecule, then guess types of atoms and
    bonds, and number of hydrogens of a molecule.
    
    :param mutator: The mutator of the molecule to be guessed.
    :param conf: The index of the conformation used for guessing.
    :param threshold: The threshold for guessing connectivity. Will be added to the
      sum of two covalent radii of the atoms to determine the maximum distance
      between two atoms to be considered as bonded.
    :raises IndexError: If the conformer index is out of range.
    :raises ValueError: If the guessing fails. The state of molecule is not
      guaranteed to be preserved in this case. If you want to preserve the state,
      copy the molecule before calling this function using
      :meth:`~nuri.core.Molecule.copy`.
    
    This function is functionally equivalent to calling :func:`guess_connectivity()`
    and :func:`guess_all_types()` in sequence, except that it is (slightly) more
    efficient.
    
    .. tip::
      If connectivity information is already present and is correct, consider using
      :func:`guess_all_types()`.
    
    .. warning::
      The information present in the molecule is overwritten by this function.
    """
