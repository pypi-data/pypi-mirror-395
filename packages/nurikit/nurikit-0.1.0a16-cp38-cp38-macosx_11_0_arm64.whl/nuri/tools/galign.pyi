from __future__ import annotations
import numpy
import nuri.core._core
import typing
__all__: list[str] = ['GAlign', 'GAlignResult', 'galign']
class GAlign:
    def __init__(self, templ: nuri.core._core.Molecule, *, conf: int | None = None, vdw_scale: float = 0.8, hetero_scale: float = 0.7, dcut: int = 6) -> None:
        """
        Prepare GAlign algorithm with the given template structure.
        
        :param templ: The template structure. Must have at least 3 atoms and 3D
          coordinates.
        :param conf: The conformation index to use as the template. If not provided,
          the first conformation is used.
        :param vdw_scale: The scale factor for van der Waals radii when calculating
          shape overlap score.
        :param hetero_scale: The scale factor for atom type mismatch when calculating
          shape overlap score.
        :param dcut: The distance cutoff for neighbor search, in angstroms.
        
        :raises ValueError: If the template structure has less than 3 atoms or no 3D
          conformation, or if invalid parameters are provided (e.g., negative dcut).
        :raises IndexError: If the provided conformation index is out of range.
        """
    def align(self, query: nuri.core._core.Molecule, flexible: bool = True, max_confs: int = 1, *, conf: int | None = None, max_translation: float = 2.5, max_rotation: float = 2.0943951023931953, max_torsion: float = 2.0943951023931953, rigid_min_msd: float = 9.0, rigid_max_confs: int = 4, pool_size: int = 10, sample_size: int = 30, max_generations: int = 50, patience: int = 5, n_mutation: int = 5, p_mutation: float = 0.5, opt_ftol: float = 0.01, opt_max_iters: int = 300) -> list[GAlignResult]:
        """
        Align the given query molecule to the template structure.
        
        :param query: The query molecule to be aligned. Must have at least one 3D
          conformation.
        :param flexible: Whether to perform flexible alignment. When ``False``, only
          rigid alignment is performed and the flexible alignment parameters are ignored.
        :param max_confs: The maximum number of alignment results to return.
        :param conf: The conformation index to use as the query structure. If not
          provided, the first conformation is used.
        :param vdw_scale: The scale factor for van der Waals radii when calculating
          shape overlap score.
        :param hetero_scale: The scale factor for atom type mismatch when calculating
          shape overlap score.
        :param dcut: The distance cutoff for neighbor search, in angstroms.
        :param max_translation: The maximum translation allowed during flexible
          alignment, in angstroms.
        :param max_rotation: The maximum rotation allowed during flexible alignment,
          in radians.
        :param max_torsion: The maximum torsion angle change allowed during flexible
          alignment, in radians.
        :param rigid_min_rmsd: The minimum root-mean-squared deviation between different
          conformations to consider them as distinct during rigid alignment.
        :param rigid_max_confs: The maximum number of conformations to consider for
          initial rigid alignment. Ignored if in rigid mode; set ``max_confs`` instead.
        :param pool_size: The size of the population pool during flexible alignment.
        :param sample_size: The number of new trial conformations to sample in each
          generation.
        :param max_generations: The maximum number of generations to run.
        :param patience: The number of generations to wait for improvement before
          early stopping.
        :param n_mutation: The number of mutation operations to perform when generating
          new trial conformations.
        :param p_mutation: The probability of mutation when generating new trial
          conformations.
        :param opt_ftol: The function tolerance for the Nelder-Mead optimization.
        :param opt_max_iters: The maximum number of iterations for the Nelder-Mead
          optimization.
        
        :returns: At most ``max_confs`` alignment results as a list of
          :class:`GAlignResult` objects, sorted by their alignment scores in
          descending order.
        
        :raises ValueError: If the query molecule has no 3D conformation, or if
          invalid parameters are provided (e.g., negative max_translation).
        :raises IndexError: If the provided conformation index is out of range.
        """
class GAlignResult:
    @property
    def pos(self) -> numpy.ndarray:
        """
        A copy of the aligned conformation as a 2D numpy array of shape
        ``(N, 3)``, where ``N`` is the number of atoms in the query molecule.
        """
    @property
    def score(self) -> float:
        """
        The alignment score (shape overlap) of this result.
        """
def galign(query: nuri.core._core.Molecule, templ: nuri.core._core.Molecule, flexible: bool = True, max_confs: int = 1, *, qconf: int | None = None, tconf: int | None = None, vdw_scale: float = 0.8, hetero_scale: float = 0.7, dcut: int = 6, max_translation: float = 2.5, max_rotation: float = 2.0943951023931953, max_torsion: float = 2.0943951023931953, rigid_min_msd: float = 9.0, rigid_max_confs: int = 4, pool_size: int = 10, sample_size: int = 30, max_generations: int = 50, patience: int = 5, n_mutation: int = 5, p_mutation: float = 0.5, opt_ftol: float = 0.01, opt_max_iters: int = 300) -> list[GAlignResult]:
    """
    Align the given query molecule to the template structure.
    
    :param query: The query molecule to be aligned. Must have at least one 3D
      conformation.
    :param templ: The template structure. Must have at least 3 atoms and 3D
      coordinates.
    :param flexible: Whether to perform flexible alignment. When ``False``, only
      rigid alignment is performed and the flexible alignment parameters are ignored.
    :param max_confs: The maximum number of alignment results to return.
    :param qconf: The conformation index to use as the query structure. If not
      provided, the first conformation is used.
    :param tconf: The conformation index to use as the template structure. If not
      provided, the first conformation is used.
    :param vdw_scale: The scale factor for van der Waals radii when calculating
      shape overlap score.
    :param hetero_scale: The scale factor for atom type mismatch when calculating
      shape overlap score.
    :param dcut: The distance cutoff for neighbor search, in angstroms.
    :param max_translation: The maximum translation allowed during flexible
      alignment, in angstroms.
    :param max_rotation: The maximum rotation allowed during flexible alignment,
      in radians.
    :param max_torsion: The maximum torsion angle change allowed during flexible
      alignment, in radians.
    :param rigid_min_rmsd: The minimum root-mean-squared deviation between different
      conformations to consider them as distinct during rigid alignment.
    :param rigid_max_confs: The maximum number of conformations to consider for
      initial rigid alignment. Ignored if in rigid mode; set ``max_confs`` instead.
    :param pool_size: The size of the population pool during flexible alignment.
    :param sample_size: The number of new trial conformations to sample in each
      generation.
    :param max_generations: The maximum number of generations to run.
    :param patience: The number of generations to wait for improvement before
      early stopping.
    :param n_mutation: The number of mutation operations to perform when generating
      new trial conformations.
    :param p_mutation: The probability of mutation when generating new trial
      conformations.
    :param opt_ftol: The function tolerance for the Nelder-Mead optimization.
    :param opt_max_iters: The maximum number of iterations for the Nelder-Mead
      optimization.
    
    :returns: At most ``max_confs`` alignment results as a list of
      :class:`GAlignResult` objects, sorted by their alignment scores in
      descending order.
    
    :raises ValueError: If the query or template molecule is invalid, or if
      any of the parameters are invalid (e.g., negative max_translation).
    :raises IndexError: If the provided conformation index is out of range.
    """
