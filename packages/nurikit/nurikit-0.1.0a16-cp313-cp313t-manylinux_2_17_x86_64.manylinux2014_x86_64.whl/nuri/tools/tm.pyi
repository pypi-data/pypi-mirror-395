from __future__ import annotations
import numpy
import typing
__all__: list[str] = ['TMAlign', 'tm_align', 'tm_score']
class TMAlign:
    @staticmethod
    def from_alignment(query: typing.Any, templ: typing.Any, alignment: typing.Any = None) -> TMAlign:
        """
        Prepare TM-align algorithm with the given structures and user-provided alignment.
        
        :param query: The query structure, in which each residue is represented by a
          single atom (usually ``CA``). Must be representable as a 2D numpy array of
          shape ``(N, 3)``, where ``N`` is the number of residues.
        :param templ: The template structure, in which each residue is represented by a
          single atom (usually ``CA``). Must be representable as a 2D numpy array of
          shape ``(M, 3)``, where ``M`` is the number of residues.
        :param alignment: Pairwise alignment of the query and template structures. Must
          be in a form representable as a 2D numpy array of shape ``(L, 2)``, in which
          rows must contain (query index, template index) pairs. If not provided, query
          and template must have same length and assumed to be aligned in order.
        :returns: A :class:`TMAlign` object initialized with the given alignment.
        
        :raises ValueError: If:
        
          - The query or template structure has less than 5 residues.
          - The alignment contains out-of-range indices.
          - Alignment is not provided and the query and template structures have
            different lengths.
          - The initialization fails (for any other reason).
        
        .. tip::
          When initialized by this method, the result is equivalent to the "TM-score"
          program in the TM-tools suite.
        
        .. note::
          Duplicate values in ``alignment`` are not checked and may result in invalid
          alignment.
        """
    def __init__(self, query: typing.Any, templ: typing.Any, query_ss: str | None = None, templ_ss: str | None = None, *, gapless: bool = True, sec_str: bool = True, local_sup: bool = True, local_with_ss: bool = True, fragment_gapless: bool = True) -> None:
        """
        Prepare TM-align algorithm with the given structures.
        
        :param query: The query structure, in which each residue is represented by a
          single atom (usually ``CA``). Must be representable as a 2D numpy array of
          shape ``(N, 3)``, where ``N`` is the number of residues.
        :param templ: The template structure, in which each residue is represented by a
          single atom (usually ``CA``). Must be representable as a 2D numpy array of
          shape ``(M, 3)``, where ``M`` is the number of residues.
        :param query_ss: The secondary structure of the query structure. When provided,
          must be an ASCII string of length ``N``.
        :param templ_ss: The secondary structure of the template structure. When
          provided, must be an ASCII string of length ``M``.
        :param gapless: Enable gapless threading.
        :param sec_str: Enable secondary structure assignment.
        :param local_sup: Enable local superposition. Note that this is the most
          expensive initialization method due to the exhaustive pairwise distance
          calculation. Consider disabling this flag if alignment takes too long.
        :param local_with_ss: Enable local superposition with secondary structure-based
          alignment.
        :param fragment_gapless: Enable fragment gapless threading.
        
        :raises ValueError: If:
        
          - The query or template structure has less than 5 residues.
          - The secondary structure of the query or template structure has a different
            length than the structure.
          - No initialization flag is set.
          - The initialization fails (for any other reason).
        
        .. note::
          If the secondary structure is not provided, it will be assigned using the
          approximate secondary structure assignment algorithm defined in the TM-align
          code. When both ``sec_str`` and ``local_with_ss`` flags are not set, the
          secondary structures are ignored.
        """
    def aligned_pairs(self) -> numpy.ndarray:
        """
        Get pairwise alignment of the query and template structures.
        
        :returns: A 2D numpy array of shape ``(L, 2)``, where ``L`` is the number of
          aligned pairs. Each row is a (query index, template index) pair.
        
        .. tip::
          This will always return the same alignment once the :class:`TMAlign` object is
          created.
        
        .. note::
          Even if the :class:`TMAlign` object is created with :meth:`from_alignment`,
          the returned pairs from this method may not be the same as the input
          alignment. This is because the TM-align algorithm filters out far-apart pairs
          when calculating the final alignment.
        """
    def rmsd(self) -> float:
        """
        The RMSD of the aligned pairs.
        """
    def score(self, l_norm: int | None = None, *, d0: float | None = None) -> tuple[numpy.ndarray, float]:
        """
        Calculate TM-score using the current alignment.
        
        :param l_norm: Length normalization factor. If not specified, the length of the
          template structure is used.
        :param d0: Distance scale factor. If not specified, calculated based on the
          length normalization factor.
        
        :returns: A pair of the transformation tensor and the TM-score of the alignment.
        """
def tm_align(query: typing.Any, templ: typing.Any, l_norm: int | None = None, query_ss: str | None = None, templ_ss: str | None = None, *, d0: float | None = None, gapless: bool = True, sec_str: bool = True, local_sup: bool = True, local_with_ss: bool = True, fragment_gapless: bool = True) -> tuple[numpy.ndarray, float]:
    """
    Run TM-align algorithm with the given structures and parameters.
    
    :param query: The query structure, in which each residue is represented by a
      single atom (usually ``CA``). Must be representable as a 2D numpy array of
      shape ``(N, 3)``, where ``N`` is the number of residues.
    :param templ: The template structure, in which each residue is represented by a
      single atom (usually ``CA``). Must be representable as a 2D numpy array of
      shape ``(M, 3)``, where ``M`` is the number of residues.
    :param l_norm: Length normalization factor. If not specified, the length of the
      template structure is used.
    :param query_ss: The secondary structure of the query structure. When provided,
      must be an ASCII string of length ``N``.
    :param templ_ss: The secondary structure of the template structure. When
      provided, must be an ASCII string of length ``M``.
    :param d0: Distance scale factor. If not specified, calculated based on the
      length normalization factor.
    :param gapless: Enable gapless threading.
    :param sec_str: Enable secondary structure assignment.
    :param local_sup: Enable local superposition. Note that this is the most
      expensive initialization method due to the exhaustive pairwise distance
      calculation. Consider disabling this flag if alignment takes too long.
    :param local_with_ss: Enable local superposition with secondary structure-based
      alignment.
    :param fragment_gapless: Enable fragment gapless threading.
    :returns: A pair of the transformation tensor and the TM-score of the alignment.
    
    :raises ValueError: If:
    
      - The query or template structure has less than 5 residues.
      - The secondary structure of the query or template structure has a different
        length than the structure.
      - No initialization flag is set.
      - The initialization fails (for any other reason).
    
    .. tip::
      If want to calculate TM-score for multiple ``l_norm`` or ``d0`` values, or
      want more details such as RMSD or aligned pairs, consider using the
      :class:`TMAlign` object directly.
    
    .. note::
      If the secondary structure is not provided, it will be assigned using the
      approximate secondary structure assignment algorithm defined in the TM-align
      code. When both ``sec_str`` and ``local_with_ss`` flags are not set, the
      secondary structures are ignored.
    
    .. seealso::
      :class:`TMAlign`, :meth:`TMAlign.__init__`, :meth:`TMAlign.score`
    """
def tm_score(query: typing.Any, templ: typing.Any, alignment: typing.Any = None, l_norm: int | None = None, *, d0: float | None = None) -> tuple[numpy.ndarray, float]:
    """
    Run TM-align algorithm with the given structures and alignment. This is also
    known as the "TM-score" program in the TM-tools suite, from which the function
    got its name.
    
    :param query: The query structure, in which residues are represented by a single
      atom (usually ``CA``). Must be representable as a 2D numpy array of shape
      ``(N, 3)`` where ``N`` is the number of residues.
    :param templ: The template structure, in which residues are represented by a
      single atom (usually ``CA``). Must be representable as a 2D numpy array of
      shape ``(M, 3)`` where ``M`` is the number of residues.
    :param alignment: Pairwise alignment of the query and template structures. Must
      be in a form representable as a 2D numpy array of shape ``(L, 2)``, in which
      rows must contain (query index, template index) pairs. If not provided, query
      and template must have same length and assumed to be aligned in order.
    :param l_norm: Length normalization factor. If not specified, the length of the
      template structure is used.
    :param d0: Distance scale factor. If not specified, calculated based on the
      length normalization factor.
    :returns: A pair of the transformation tensor and the TM-score of the alignment.
    
    :raises ValueError: If:
    
      - The query or template structure has less than 5 residues.
      - The alignment contains out-of-range indices.
      - Alignment is not provided and the query and template structures have
        different lengths.
      - The initialization fails (for any other reason).
    
    
    .. tip::
      If want to calculate TM-score for multiple ``l_norm`` or ``d0`` values, or
      want more details such as RMSD or aligned pairs, consider using the
      :class:`TMAlign` object directly.
    
    .. note::
      Duplicate values in ``alignment`` are not checked and may result in invalid
      alignment.
    
    .. seealso::
      :class:`TMAlign`, :meth:`TMAlign.from_alignment`, :meth:`TMAlign.score`
    """
