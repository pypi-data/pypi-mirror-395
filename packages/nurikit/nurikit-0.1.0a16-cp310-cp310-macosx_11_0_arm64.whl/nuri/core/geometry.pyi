from __future__ import annotations
import numpy
import typing
__all__: list[str] = ['align_points', 'align_rmsd', 'transform']
def align_points(query: typing.Any, template: typing.Any, method: str = 'qcp', reflection: bool = False) -> tuple[numpy.ndarray, float]:
    """
    Find a 4x4 best-fit rigid-body transformation tensor, to align ``query`` to
    ``template``.
    
    :param query: The query points. Must be representable as a 2D numpy array of
      shape ``(N, 3)``.
    :param template: The template points. Must be representable as a 2D numpy array
      of shape ``(N, 3)``.
    :param method: The alignment method to use. Defaults to ``"qcp"``. Currently
      supported methods are:
    
      - ``"qcp"``: The Quaternion Characteristic Polynomial (QCP) method, based on
        the implementation of Liu and Theobald
        :footcite:`core:geom:qcp-2005,core:geom:qcp-2010,core:geom:qcp-2011`. Unlike
        the original implementation, this version can also handle reflection
        based on the observations of :footcite:ts:`core:geom:qcp-2004`.
    
      - ``"kabsch"``: The Kabsch algorithm.
        :footcite:`core:geom:kabsch-1976,core:geom:kabsch-1978` This implementation
        is based on the implementation in TM-align. :footcite:`tm-align`
    
    :param reflection: Whether to allow reflection in the alignment. Defaults to
      ``False``.
    
    :returns: A tuple of the transformation tensor and the RMSD of the alignment.
    """
def align_rmsd(query: typing.Any, template: typing.Any, method: str = 'qcp', reflection: bool = False) -> float:
    """
    Calculate the RMSD of the best-fit rigid-body alignment of ``query`` to
    ``template``.
    
    :param query: The query points. Must be representable as a 2D numpy array of
      shape ``(N, 3)``.
    :param template: The template points. Must be representable as a 2D numpy array
      of shape ``(N, 3)``.
    :param method: The alignment method to use. Defaults to ``"qcp"``. Currently
      supported methods are:
    
      - ``"qcp"``: The Quaternion Characteristic Polynomial (QCP) method, based on
        the implementation of Liu and Theobald
        :footcite:`core:geom:qcp-2005,core:geom:qcp-2010,core:geom:qcp-2011`. Unlike
        the original implementation, this version can also handle reflection
        based on the observations of :footcite:ts:`core:geom:qcp-2004`.
    
      - ``"kabsch"``: The Kabsch algorithm.
        :footcite:`core:geom:kabsch-1976,core:geom:kabsch-1978` This implementation
        is based on the implementation in TM-align. :footcite:`tm-align`
    
    :param reflection: Whether to allow reflection in the alignment. Defaults to
      ``False``.
    
    :returns: The RMSD of the alignment.
    """
def transform(tensor: typing.Any, pts: typing.Any) -> numpy.ndarray:
    """
    Transform a set of points using a 4x4 transformation tensor.
    
    Effectively, this function is roughly equivalent to the following Python code:
    
    .. code-block:: python
    
      def transform(tensor, pts):
          rotated = tensor[:3, :3] @ pts.T
          translated = rotated + tensor[:3, 3, None]
          return translated.T
    
    :param tensor: The transformation tensor. Must be representable as a 2D numpy
      array of shape ``(4, 4)``.
    :param pts: The points to transform. Must be representable as a 2D numpy array
      of shape ``(N, 3)``.
    :returns: The transformed points.
    
    :warning: This function does not check if the transformation tensor is a valid
      affine transformation matrix.
    """
