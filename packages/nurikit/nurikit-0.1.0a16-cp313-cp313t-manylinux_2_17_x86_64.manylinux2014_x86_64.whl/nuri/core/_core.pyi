from __future__ import annotations
import numpy
import typing
__all__: list[str] = ['Atom', 'AtomData', 'Bond', 'BondConfig', 'BondData', 'BondOrder', 'Chirality', 'Element', 'Hyb', 'Isotope', 'Molecule', 'Mutator', 'Neighbor', 'PeriodicTable', 'ProxySubAtom', 'ProxySubBond', 'ProxySubNeighbor', 'ProxySubstructure', 'SubAtom', 'SubBond', 'SubNeighbor', 'Substructure', 'SubstructureCategory', 'SubstructureContainer', 'periodic_table', 'seed_thread']
class Atom:
    """
    
    An atom of a molecule.
    
    This is a proxy object to the :class:`AtomData` of the atom in a molecule. The
    proxy object is invalidated when any changes are made to the molecule. If
    underlying data must be kept alive, copy the data first with :meth:`copy_data`
    method.
    
    We only document the differences from the original class. Refer to the
    :class:`AtomData` class for common properties and methods.
    
    .. note:: Unlike the underlying data object, the atom cannot be created
      directly. Use the :meth:`Mutator.add_atom` method to add an atom to a
      molecule.
    """
    def __contains__(self, idx: int) -> bool:
        ...
    def __getitem__(self, idx: int) -> Neighbor:
        ...
    def __iter__(self) -> _NeighborIterator:
        ...
    def __len__(self) -> int:
        ...
    def copy_data(self) -> AtomData:
        """
        Copy the underlying :class:`AtomData` object.
        
        :returns: A copy of the underlying :class:`AtomData` object.
        """
    def count_heavy_neighbors(self) -> int:
        """
        Count heavy neighbors connected to the atom. A heavy atom is an atom that is not
        hydrogen.
        """
    def count_hydrogens(self) -> int:
        """
        Count hydrogen atoms connected to the atom. Includes both explicit and implicit
        hydrogens.
        """
    def count_neighbors(self) -> int:
        """
        Count connected atoms to the atom. Includes both explicit and implicit
        neighbors.
        
        .. note::
          This is *not* same with ``len(atom)``. The length of the atom is the number of
          explicit neighbors, or, the iterable neighbors of the atom. Implicit hydrogens
          could not be iterated, thus not counted in the length.
        """
    def get_isotope(self, explicit: bool = False) -> Isotope:
        """
        Get the isotope of the atom.
        
        :param explicit: If True, returns the explicit isotope of the atom. Otherwise,
          returns the isotope of the atom. Defaults to False.
        
        :returns: The isotope of the atom. If the atom does not have an explicit
          isotope,
        
          * If ``explicit`` is False, the representative isotope of the element is
            returned.
          * If ``explicit`` is True, None is returned.
        """
    def get_pos(self, conf: int = 0) -> numpy.ndarray:
        """
        Get the position of the atom.
        
        :param conf: The index of the conformation to get the position from. Defaults to
          0.
        :returns: The position of the atom.
        
        .. note::
          The position could not be directly set from Python. Use the :meth:`set_pos`
          method to set the position.
        """
    @typing.overload
    def set_element(self, atomic_number: int) -> Atom:
        """
        Set the element of the atom.
        
        :param atomic_number: The atomic number of the element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_element(self, symbol_or_name: str) -> Atom:
        """
        Set the element of the atom.
        
        :param symbol_or_name: The atomic symbol or name of the element to set.
        
        .. note::
          The symbol or name is case-insensitive. Symbol is tried first, and if it
          fails, name is tried.
        """
    @typing.overload
    def set_element(self, element: Element) -> Atom:
        """
        Set the element of the atom.
        
        :param element: The element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_isotope(self, mass_number: int) -> Atom:
        """
        Set the isotope of the atom.
        
        :param mass_number: The mass number of the isotope to set.
        """
    @typing.overload
    def set_isotope(self, isotope: Isotope) -> Atom:
        """
        Set the isotope of the atom.
        
        :param isotope: The isotope to set.
        """
    def set_pos(self, pos: typing.Any, conf: int = 0) -> None:
        """
        Set the position of the atom.
        
        :param pos: The 3D vector to set the position to. Must be convertible to a numpy
          array of shape (3,).
        :param conf: The index of the conformation to set the position to. Defaults to
          0.
        """
    def update(self, *, hyb: Hyb | None = None, implicit_hydrogens: int | None = None, formal_charge: int | None = None, partial_charge: float | None = None, atomic_number: int | None = None, element: Element = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, chirality: Chirality | None = None, name: str | None = None) -> Atom:
        """
        Update the atom data. If any of the arguments are not given, the corresponding
        property is not updated.
        
        .. note::
          ``atomic_number`` and ``element`` are mutually exclusive. If both are given,
          an exception is raised.
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        """
    @typing.overload
    def update_from(self, atom: Atom) -> Atom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: ProxySubAtom) -> Atom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: SubAtom) -> Atom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, data: AtomData) -> Atom:
        """
        Update the atom data.
        
        :param data: The atom data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the atom is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def atomic_number(self) -> int:
        """
        :type: int
        
        The atomic number of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @property
    def atomic_weight(self) -> float:
        """
        :type: float
        
        The atomic weight of the atom. Equivalent to ``data.element.atomic_weight``.
        """
    @property
    def chirality(self) -> Chirality:
        """
        :type: Chirality
        
        Explicit chirality of the atom. Note that this does *not* imply the atom is a
        stereocenter chemically and might not correspond to the geometry of the
        molecule. See :class:`Chirality` for formal definition.
        
        .. tip::
          Assigning :obj:`None` clears the explicit chirality.
        
        .. seealso::
          :class:`Chirality`, :meth:`update`
        """
    @chirality.setter
    def chirality(self, arg1: Chirality | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def element(self) -> Element:
        """
        :type: Element
        
        The element of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @element.setter
    def element(self, arg1: Element) -> None:
        ...
    @property
    def element_name(self) -> str:
        """
        :type: str
        
        The IUPAC element name of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def element_symbol(self) -> str:
        """
        :type: str
        
        The IUPAC element symbol of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def formal_charge(self) -> int:
        """
        :type: int
        
        The formal charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @formal_charge.setter
    def formal_charge(self, arg1: int) -> None:
        ...
    @property
    def hyb(self) -> Hyb:
        """
        :type: Hyb
        
        The hybridization of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @hyb.setter
    def hyb(self, arg1: Hyb) -> None:
        ...
    @property
    def id(self) -> int:
        """
        :type: int
        
        A unique identifier of the atom in the molecule. The identifier is guaranteed
        to be unique within the atoms of the molecule.
        
        This is a read-only property.
        
        .. note::
          Implementation detail: the identifier is the index of the atom.
        """
    @property
    def implicit_hydrogens(self) -> int:
        """
        :type: int
        
        The number of implicit hydrogens of the atom. Guaranteed to be non-negative.
        
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        
        .. seealso::
          :meth:`update`
        """
    @implicit_hydrogens.setter
    def implicit_hydrogens(self, arg1: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the atom. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def partial_charge(self) -> float:
        """
        :type: float
        
        The partial charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @partial_charge.setter
    def partial_charge(self, arg1: float) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the atom. The keys
        and values are both strings.
        
        .. note::
          The properties are shared with the underlying :class:`AtomData` object. If the
          properties are modified, the underlying object is also modified.
        
          As a result, the property map is also invalidated when any changes are made
          to the molecule. If the properties must be kept alive, copy the properties
          first with ``copy()`` method.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the atom is a ring atom.
        
        .. note::
          Beware updating this property when the atom is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
class AtomData:
    """
    
    Data of an atom in a molecule.
    Refer to the ``nuri::AtomData`` class in the |cppdocs| for more details.
    """
    def __copy__(self) -> AtomData:
        ...
    def __deepcopy__(self, memo: dict) -> AtomData:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, atomic_number: int) -> None:
        ...
    @typing.overload
    def __init__(self, element: Element) -> None:
        ...
    def copy(self) -> AtomData:
        """
        Return a deep copy of self.
        """
    def get_isotope(self, explicit: bool = False) -> Isotope:
        """
        Get the isotope of the atom.
        
        :param explicit: If True, returns the explicit isotope of the atom. Otherwise,
          returns the isotope of the atom. Defaults to False.
        
        :returns: The isotope of the atom. If the atom does not have an explicit
          isotope,
        
          * If ``explicit`` is False, the representative isotope of the element is
            returned.
          * If ``explicit`` is True, None is returned.
        """
    @typing.overload
    def set_element(self, atomic_number: int) -> AtomData:
        """
        Set the element of the atom.
        
        :param atomic_number: The atomic number of the element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_element(self, symbol_or_name: str) -> AtomData:
        """
        Set the element of the atom.
        
        :param symbol_or_name: The atomic symbol or name of the element to set.
        
        .. note::
          The symbol or name is case-insensitive. Symbol is tried first, and if it
          fails, name is tried.
        """
    @typing.overload
    def set_element(self, element: Element) -> AtomData:
        """
        Set the element of the atom.
        
        :param element: The element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_isotope(self, mass_number: int) -> AtomData:
        """
        Set the isotope of the atom.
        
        :param mass_number: The mass number of the isotope to set.
        """
    @typing.overload
    def set_isotope(self, isotope: Isotope) -> AtomData:
        """
        Set the isotope of the atom.
        
        :param isotope: The isotope to set.
        """
    def update(self, *, hyb: Hyb | None = None, implicit_hydrogens: int | None = None, formal_charge: int | None = None, partial_charge: float | None = None, atomic_number: int | None = None, element: Element = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, chirality: Chirality | None = None, name: str | None = None) -> AtomData:
        """
        Update the atom data. If any of the arguments are not given, the corresponding
        property is not updated.
        
        .. note::
          ``atomic_number`` and ``element`` are mutually exclusive. If both are given,
          an exception is raised.
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        """
    @typing.overload
    def update_from(self, atom: Atom) -> AtomData:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: ProxySubAtom) -> AtomData:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: SubAtom) -> AtomData:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, data: AtomData) -> AtomData:
        """
        Update the atom data.
        
        :param data: The atom data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the atom is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def atomic_number(self) -> int:
        """
        :type: int
        
        The atomic number of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @property
    def atomic_weight(self) -> float:
        """
        :type: float
        
        The atomic weight of the atom. Equivalent to ``data.element.atomic_weight``.
        """
    @property
    def chirality(self) -> Chirality:
        """
        :type: Chirality
        
        Explicit chirality of the atom. Note that this does *not* imply the atom is a
        stereocenter chemically and might not correspond to the geometry of the
        molecule. See :class:`Chirality` for formal definition.
        
        .. tip::
          Assigning :obj:`None` clears the explicit chirality.
        
        .. seealso::
          :class:`Chirality`, :meth:`update`
        """
    @chirality.setter
    def chirality(self, arg1: Chirality | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def element(self) -> Element:
        """
        :type: Element
        
        The element of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @element.setter
    def element(self, arg1: Element) -> None:
        ...
    @property
    def element_name(self) -> str:
        """
        :type: str
        
        The IUPAC element name of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def element_symbol(self) -> str:
        """
        :type: str
        
        The IUPAC element symbol of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def formal_charge(self) -> int:
        """
        :type: int
        
        The formal charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @formal_charge.setter
    def formal_charge(self, arg1: int) -> None:
        ...
    @property
    def hyb(self) -> Hyb:
        """
        :type: Hyb
        
        The hybridization of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @hyb.setter
    def hyb(self, arg1: Hyb) -> None:
        ...
    @property
    def implicit_hydrogens(self) -> int:
        """
        :type: int
        
        The number of implicit hydrogens of the atom. Guaranteed to be non-negative.
        
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        
        .. seealso::
          :meth:`update`
        """
    @implicit_hydrogens.setter
    def implicit_hydrogens(self, arg1: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the atom. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def partial_charge(self) -> float:
        """
        :type: float
        
        The partial charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @partial_charge.setter
    def partial_charge(self, arg1: float) -> None:
        ...
    @property
    def props(self) -> _PropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the atom. The keys
        and values are both strings.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the atom is a ring atom.
        
        .. note::
          Beware updating this property when the atom is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
class Bond:
    """
    
    A bond of a molecule.
    
    This is a proxy object to the :class:`BondData` of the bond in a molecule. The
    proxy object is invalidated when any changes are made to the molecule. If
    underlying data must be kept alive, copy the data first with :meth:`copy_data`
    method.
    
    We only document the differences from the original class. Refer to the
    :class:`BondData` class for common properties and methods.
    
    .. note:: Unlike the underlying data object, the bond cannot be created
      directly. Use the :meth:`Mutator.add_bond` method to add a bond to a molecule.
    """
    def approx_order(self) -> float:
        """
        The approximate bond order of the bond.
        """
    def copy_data(self) -> BondData:
        """
        Copy the underlying :class:`BondData` object.
        
        :returns: A copy of the underlying :class:`BondData` object.
        """
    def length(self, conf: int = 0) -> float:
        """
        Calculate the length of the bond.
        
        :param conf: The index of the conformation to calculate the length from.
          Defaults to 0.
        :returns: The length of the bond.
        """
    def rotatable(self) -> bool:
        """
        Whether the bond is rotatable.
        
        .. note::
          The result is calculated as the bond order is :data:`BondOrder.Single` or
          :data:`BondOrder.Other`, and the bond is not a conjugated or a ring bond.
        """
    def rotate(self, angle: float, rotate_src: bool = False, strict: bool = True, conf: int | None = None) -> None:
        """
        Rotate the bond by the given angle. The components connected only to the
        destination atom (excluding this bond) are rotated around the bond axis.
        Rotation is done in the direction of the right-hand rule, i.e., the rotation is
        counter-clockwise with respect to the src -> dst vector.
        
        :param angle: The angle to rotate the bond by, in *degrees*.
        :param rotate_src: If True, the source atom side is rotated instead.
        :param strict: If True, rotation will fail for multiple bonds and conjugated
          bonds. If False, the rotation will be attempted regardless.
        :param conf: The index of the conformation to rotate the bond in. If not given,
          all conformations are rotated.
        :raises ValueError: If the bond is not rotatable. If ``strict`` is False, it
          will be raised only if the bond is a member of a ring, as it will be
          impossible to rotate the bond without breaking the ring.
        """
    def sqlen(self, conf: int = 0) -> float:
        """
        Calculate the square of the length of the bond.
        
        :param conf: The index of the conformation to calculate the length from.
          Defaults to 0.
        :returns: The square of the length of the bond.
        """
    def update(self, *, order: BondOrder | None = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, config: BondConfig | None = None, name: str | None = None) -> Bond:
        """
        Update the bond data. If any of the arguments are not given, the corresponding
        property is not updated.
        """
    @typing.overload
    def update_from(self, bond: Bond) -> Bond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: ProxySubBond) -> Bond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: SubBond) -> Bond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, data: BondData) -> Bond:
        """
        Update the bond data.
        
        :param data: The bond data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the bond is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def config(self) -> BondConfig:
        """
        :type: BondConfig
        
        The explicit configuration of the bond. Note that this does *not* imply the bond
        is a torsionally restricted bond chemically.
        
        .. note::
          For bonds with more than 3 neighboring atoms, :attr:`BondConfig.Cis` or
          :attr:`BondConfig.Trans` configurations are not well defined terms. In such
          cases, this will return whether **the first neighbors are on the same side of
          the bond**. For example, in the following structure (assuming the neighbors
          are ordered in the same way as the atoms), the bond between atoms 0 and 1 is
          considered to be in a cis configuration (first neighbors are marked with angle
          brackets)::
        
            <2>     <4>
              \\     /
               0 = 1
              /     \\
             3       5
        
          On the other hand, when the neighbors are ordered in the opposite way, the
          bond between atoms 0 and 1 is considered to be in a trans configuration::
        
            <2>      5
              \\     /
               0 = 1
              /     \\
             3      <4>
        
        .. tip::
          Assigning :obj:`None` clears the explicit bond configuration.
        
        .. seealso::
          :meth:`update`
        """
    @config.setter
    def config(self, arg1: BondConfig | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def dst(self) -> Atom:
        """
        :type: Atom
        
        The destination atom of the bond.
        """
    @property
    def id(self) -> int:
        """
        :type: int
        
        A unique identifier of the bond in the molecule. The identifier is guaranteed
        to be unique within the bonds of the molecule.
        
        This is a read-only property.
        
        .. note::
          Implementation detail: the identifier is the index of the bond.
        """
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the bond. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def order(self) -> BondOrder:
        """
        :type: BondOrder
        
        The bond order of the bond.
        
        .. seealso::
          :meth:`update`
        """
    @order.setter
    def order(self, arg1: BondOrder) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the bond. The keys
        and values are both strings.
        
        .. note::
          The properties are shared with the underlying :class:`BondData` object. If the
          properties are modified, the underlying object is also modified.
        
          As a result, the property map is invalidated when any changes are made to the
          molecule. If the properties must be kept alive, copy the properties first with
          ``copy()`` method.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the bond is a ring bond.
        
        .. note::
          Beware updating this property when the bond is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
    @property
    def src(self) -> Atom:
        """
        :type: Atom
        
        The source atom of the bond.
        """
class BondConfig:
    """
    Members:
    
      Unknown
    
      Trans
    
      Cis
    """
    Cis: typing.ClassVar[BondConfig]  # value = <BondConfig.Cis: 1>
    Trans: typing.ClassVar[BondConfig]  # value = <BondConfig.Trans: 2>
    Unknown: typing.ClassVar[BondConfig]  # value = <BondConfig.Unknown: 0>
    __members__: typing.ClassVar[dict[str, BondConfig]]  # value = {'Unknown': <BondConfig.Unknown: 0>, 'Trans': <BondConfig.Trans: 2>, 'Cis': <BondConfig.Cis: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BondData:
    """
    
    Data of a bond in a molecule.
    Refer to the ``nuri::BondData`` class in the |cppdocs| for more details.
    """
    def __copy__(self) -> BondData:
        ...
    def __deepcopy__(self, memo: dict) -> BondData:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, order: BondOrder) -> None:
        """
        Create a bond data with the given bond order.
        
        :param BondOrder|int order: The bond order of the bond.
        """
    def approx_order(self) -> float:
        """
        The approximate bond order of the bond.
        """
    def copy(self) -> BondData:
        """
        Return a deep copy of self.
        """
    def rotatable(self) -> bool:
        """
        Whether the bond is rotatable.
        
        .. note::
          The result is calculated as the bond order is :data:`BondOrder.Single` or
          :data:`BondOrder.Other`, and the bond is not a conjugated or a ring bond.
        """
    def update(self, *, order: BondOrder | None = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, config: BondConfig | None = None, name: str | None = None) -> BondData:
        """
        Update the bond data. If any of the arguments are not given, the corresponding
        property is not updated.
        """
    @typing.overload
    def update_from(self, bond: Bond) -> BondData:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: ProxySubBond) -> BondData:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: SubBond) -> BondData:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, data: BondData) -> BondData:
        """
        Update the bond data.
        
        :param data: The bond data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the bond is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def config(self) -> BondConfig:
        """
        :type: BondConfig
        
        The explicit configuration of the bond. Note that this does *not* imply the bond
        is a torsionally restricted bond chemically.
        
        .. note::
          For bonds with more than 3 neighboring atoms, :attr:`BondConfig.Cis` or
          :attr:`BondConfig.Trans` configurations are not well defined terms. In such
          cases, this will return whether **the first neighbors are on the same side of
          the bond**. For example, in the following structure (assuming the neighbors
          are ordered in the same way as the atoms), the bond between atoms 0 and 1 is
          considered to be in a cis configuration (first neighbors are marked with angle
          brackets)::
        
            <2>     <4>
              \\     /
               0 = 1
              /     \\
             3       5
        
          On the other hand, when the neighbors are ordered in the opposite way, the
          bond between atoms 0 and 1 is considered to be in a trans configuration::
        
            <2>      5
              \\     /
               0 = 1
              /     \\
             3      <4>
        
        .. tip::
          Assigning :obj:`None` clears the explicit bond configuration.
        
        .. seealso::
          :meth:`update`
        """
    @config.setter
    def config(self, arg1: BondConfig | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the bond. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def order(self) -> BondOrder:
        """
        :type: BondOrder
        
        The bond order of the bond.
        
        .. seealso::
          :meth:`update`
        """
    @order.setter
    def order(self, arg1: BondOrder) -> None:
        ...
    @property
    def props(self) -> _PropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the bond. The keys
        and values are both strings.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the bond is a ring bond.
        
        .. note::
          Beware updating this property when the bond is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
class BondOrder:
    """
    Members:
    
      Other
    
      Single
    
      Double
    
      Triple
    
      Quadruple
    
      Aromatic
    """
    Aromatic: typing.ClassVar[BondOrder]  # value = <BondOrder.Aromatic: 5>
    Double: typing.ClassVar[BondOrder]  # value = <BondOrder.Double: 2>
    Other: typing.ClassVar[BondOrder]  # value = <BondOrder.Other: 0>
    Quadruple: typing.ClassVar[BondOrder]  # value = <BondOrder.Quadruple: 4>
    Single: typing.ClassVar[BondOrder]  # value = <BondOrder.Single: 1>
    Triple: typing.ClassVar[BondOrder]  # value = <BondOrder.Triple: 3>
    __members__: typing.ClassVar[dict[str, BondOrder]]  # value = {'Other': <BondOrder.Other: 0>, 'Single': <BondOrder.Single: 1>, 'Double': <BondOrder.Double: 2>, 'Triple': <BondOrder.Triple: 3>, 'Quadruple': <BondOrder.Quadruple: 4>, 'Aromatic': <BondOrder.Aromatic: 5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Chirality:
    """
    
    Chirality of an atom.
    
    When viewed from the first neighboring atom of a "chiral" atom, the chirality
    is determined by the spatial arrangement of the remaining neighbors. That is,
    when the remaining neighbors are arranged in a clockwise direction, the
    chirality is "clockwise" (:attr:`CW`), and when they are arranged in a
    counter-clockwise direction, the chirality is "counter-clockwise" (:attr:`CCW`).
    If the atom is not a stereocenter or the chirality is unspecified, the chirality
    is "unknown" (:attr:`Unknown`).
    
    If the atom has an implicit hydrogen, it will be always placed at the end of the
    neighbor list. This is to ensure that the chirality of the atom is not affected
    by adding back the implicit hydrogen (which will be placed at the end).
    
    .. note::
      It is worth noting that this chirality definition ("NuriKit Chirality") is not
      strictly equivalent to the chirality definition in SMILES ("SMILES
      Chirality"), although it appears to be similar and often resolves to the same
      chirality.
    
      One notable difference is that most SMILES parser implementations place the
      implicit hydrogen where it appears in the SMILES string. [#fn-non-conforming]_
      For example, consider the stereocenter in the following SMILES string::
    
        [C@@H](F)(Cl)Br
    
      The SMILES Chirality of the atom is "clockwise" because the implicit hydrogen
      is interpreted as the first neighbor. On the other hand, the NuriKit Chirality
      of the atom is "counter-clockwise" because the implicit hydrogen is
      interpreted as the last neighbor.
    
      This is not a problem in most cases, because when the stereocenter is not the
      first atom of a fragment, the SMILES Chirality and the NuriKit Chirality are
      consistent. For example, a slightly modified SMILES string of the above
      example will result in a "counter-clockwise" configuration in both
      definitions::
    
        F[C@H](Cl)Br
    
      Another neighbor ordering inconsistency might occur when ring closure is
      involved. This is because a ring-closing bond **addition** could only be done
      after the partner atom is added, but the SMILES Chirality is resolved in the
      order of the **appearance** of the bonds in the SMILES string. For example,
      consider the following SMILES string, in which the two stereocenters are both
      "clockwise" in terms of the SMILES Chirality (atoms are numbered for
      reference)::
    
        1 2  3  4 5     6 7
        C[C@@H]1C[C@@]1(F)C
    
      The NuriKit Chirality of atom 2 is "counter-clockwise" because the order of
      the neighbors is 1, 3, 5, 4 in the SMILES Chirality (atom 5 precedes atom 4
      because the ring-closing bond between atoms 2 and 5 *appears before* the bond
      between atoms 2 and 4), but 1, 3, 4, 5 in the NuriKit Chirality (atom 4
      precedes atom 5 because the ring-closing bond is *added after* the bond
      between atoms 2 and 4).
    
      On the other hand, the NuriKit Chirality of atom 5 is "clockwise" because the
      order of the neighbors is 4, 2, 6, 7 in both definitions. Unlike the other
      stereocenter, the partner of the ring-closing bond (atom 2) is already added,
      and the ring-closing bond can now be added where it appears in the SMILES
      string.
    
      .. rubric:: Footnotes
    
      .. [#fn-non-conforming] Note that this behavior of the implementations is not
         strictly conforming to the OpenSMILES specification, which states that the
         implicit hydrogen should be considered to be the **first atom in the
         clockwise or anticlockwise accounting**.
    
    
    Members:
    
      Unknown
    
      CW
    
      CCW
    """
    CCW: typing.ClassVar[Chirality]  # value = <Chirality.CCW: 2>
    CW: typing.ClassVar[Chirality]  # value = <Chirality.CW: 1>
    Unknown: typing.ClassVar[Chirality]  # value = <Chirality.Unknown: 0>
    __members__: typing.ClassVar[dict[str, Chirality]]  # value = {'Unknown': <Chirality.Unknown: 0>, 'CW': <Chirality.CW: 1>, 'CCW': <Chirality.CCW: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Element:
    """
    
        An element.
    
        All instances of this class are immutable and singleton. If you want to
        compare two instances, just use the ``is`` operator. You can also compare
        two elements using the comparison operators, which in turn compares their
        :attr:`atomic_number` (added for convenience).
    
        >>> from nuri import periodic_table
        >>> periodic_table["H"] < periodic_table["He"]
        True
    
        Refer to the ``nuri::Element`` class in the |cppdocs| for more details.
      
    """
    def __ge__(self, arg0: Element) -> bool:
        ...
    def __gt__(self, arg0: Element) -> bool:
        ...
    def __le__(self, arg0: Element) -> bool:
        ...
    def __lt__(self, arg0: Element) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def get_isotope(self, mass_number: int) -> Isotope:
        """
        Get an isotope of this element by mass number.
        
        :param mass_number: The mass number of the isotope.
        :raises ValueError: If no such isotope exists.
        """
    @property
    def atomic_number(self) -> int:
        """
        :type: int
        """
    @property
    def atomic_weight(self) -> float:
        """
        :type: float
        """
    @property
    def covalent_radius(self) -> float:
        """
        :type: float
        """
    @property
    def eneg(self) -> float:
        """
        :type: float
        """
    @property
    def group(self) -> int:
        """
        :type: int
        """
    @property
    def isotopes(self) -> _IsotopeList:
        """
        :type: collections.abc.Sequence[Isotope]
        """
    @property
    def major_isotope(self) -> Isotope:
        """
        :type: Isotope
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def period(self) -> int:
        """
        :type: int
        """
    @property
    def symbol(self) -> str:
        """
        :type: str
        """
    @property
    def vdw_radius(self) -> float:
        """
        :type: float
        """
class Hyb:
    """
    Members:
    
      Unbound
    
      Terminal
    
      SP
    
      SP2
    
      SP3
    
      SP3D
    
      SP3D2
    
      Other
    """
    Other: typing.ClassVar[Hyb]  # value = <Hyb.Other: 7>
    SP: typing.ClassVar[Hyb]  # value = <Hyb.SP: 2>
    SP2: typing.ClassVar[Hyb]  # value = <Hyb.SP2: 3>
    SP3: typing.ClassVar[Hyb]  # value = <Hyb.SP3: 4>
    SP3D: typing.ClassVar[Hyb]  # value = <Hyb.SP3D: 5>
    SP3D2: typing.ClassVar[Hyb]  # value = <Hyb.SP3D2: 6>
    Terminal: typing.ClassVar[Hyb]  # value = <Hyb.Terminal: 1>
    Unbound: typing.ClassVar[Hyb]  # value = <Hyb.Unbound: 0>
    __members__: typing.ClassVar[dict[str, Hyb]]  # value = {'Unbound': <Hyb.Unbound: 0>, 'Terminal': <Hyb.Terminal: 1>, 'SP': <Hyb.SP: 2>, 'SP2': <Hyb.SP2: 3>, 'SP3': <Hyb.SP3: 4>, 'SP3D': <Hyb.SP3D: 5>, 'SP3D2': <Hyb.SP3D2: 6>, 'Other': <Hyb.Other: 7>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Isotope:
    """
    
        An isotope of an element.
    
        All instances of this class are immutable and singleton. If you want to
        compare two instances, just use the ``is`` operator. You can also compare
        two elements using the comparison operators, which in turn compares their
        :attr:`mass_number` (added for convenience).
    
        Refer to the ``nuri::Element`` class in the |cppdocs| for more details.
      
    """
    def __ge__(self, arg0: Isotope) -> bool:
        ...
    def __gt__(self, arg0: Isotope) -> bool:
        ...
    def __le__(self, arg0: Isotope) -> bool:
        ...
    def __lt__(self, arg0: Isotope) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def abundance(self) -> float:
        """
        :type: float
        """
    @property
    def atomic_weight(self) -> float:
        """
        :type: float
        """
    @property
    def element(self) -> Element:
        """
                :type: Element
        
                The element of this isotope.
        """
    @property
    def mass_number(self) -> int:
        """
        :type: int
        """
class Molecule:
    """
    
    A molecule.
    Refer to the ``nuri::Molecule`` class in the |cppdocs| for more details.
    """
    @typing.overload
    def __contains__(self, idx: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: Atom) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: Bond) -> bool:
        ...
    def __copy__(self) -> Molecule:
        ...
    def __deepcopy__(self, memo: dict) -> Molecule:
        ...
    def __getitem__(self, idx: int) -> Atom:
        ...
    def __init__(self) -> None:
        """
        Create an empty molecule.
        """
    def __iter__(self) -> _AtomIterator:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def add_conf(self, coords: typing.Any) -> int:
        """
        Add a conformation to the molecule at the end.
        
        :param coords: The coordinates of the atoms in the conformation. Must be
          convertible to a numpy array of shape ``(num_atoms, 3)``.
        :returns: The index of the added conformation.
        """
    @typing.overload
    def add_conf(self, coords: typing.Any, conf: int) -> int:
        """
        Add a conformation to the molecule.
        
        :param coords: The coordinates of the atoms in the conformation. Must be
          convertible to a numpy array of shape ``(num_atoms, 3)``.
        :param conf: The index of the conformation to add the coordinates to. If
          negative, counts from back to front (i.e., the new conformer
          will be created at ``max(0, num_confs() + conf)``). Otherwise, the
          coordinates are added at ``min(conf, num_confs())``. This resembles
          the behavior of Python's :meth:`list.insert` method.
        :returns: The index of the added conformation.
        """
    @typing.overload
    def add_from(self, other: Molecule) -> None:
        """
        Add all atoms and bonds from another molecule to the molecule.
        
        :param other: The molecule to add from.
        """
    @typing.overload
    def add_from(self, other: Substructure) -> None:
        """
        Add all atoms and bonds from a substructure to the molecule.
        
        :param other: The substructure to add from.
        """
    @typing.overload
    def add_from(self, other: ProxySubstructure) -> None:
        """
        Add all atoms and bonds from a substructure to the molecule.
        
        :param other: The substructure to add from.
        """
    def assign_charges(self, method: str = 'gasteiger') -> None:
        """
        Assign partial charges to the molecule.
        
        :param method: The charge assignment method. See below for the possible charge
          assignment methods. Default to ``"gasteiger"``.
        :raises RuntimeError: If the charge assignment method fails.
        :raises ValueError: If the charge assignment method is not supported.
        
        Supported methods:
        
        * ``"gasteiger"``: Assigns Marsili-Gasteiger charges, as described in the
          original paper\\ :footcite:`algo:pcharge:gasteiger`.
        
          The Gasteiger algorithm requires initial "seed" charges to be assigned to
          atoms. In this implementation, the initial charges are assigned from the
          (localized) formal charges of the atoms, then a charge delocalization
          algorithm is applied to the terminal atoms of a conjugated system with the
          same Gasteiger type (e.g., oxygens of a carboxylate group will be assigned
          -0.5 charge each).
        
        .. footbibliography::
        """
    def atom(self, idx: int) -> Atom:
        """
        Get an atom of the molecule.
        
        :param idx: The index of the atom to get.
        :returns: The atom at the index.
        :rtype: Atom
        
        .. note::
          The returned atom is invalidated when a mutator context is exited. If the atom
          must be kept alive, copy the atom data first with :meth:`Atom.copy_data`
          method.
        """
    @typing.overload
    def bond(self, idx: int) -> Bond:
        """
        Get a bond of the molecule.
        
        :param idx: The index of the bond to get.
        :returns: The bond at the index.
        :rtype: Bond
        
        .. note::
          The returned bond is invalidated when a mutator context is exited. If the bond
          must be kept alive, copy the bond data first with :meth:`Bond.copy_data`
          method.
        """
    @typing.overload
    def bond(self, src: int, dst: int) -> Bond:
        """
        Get a bond of the molecule. ``src`` and ``dst`` are interchangeable.
        
        :param src: The index of the source atom of the bond.
        :param dst: The index of the destination atom of the bond.
        :returns: The bond from the source to the destination atom.
        :rtype: Bond
        :raises ValueError: If the bond does not exist.
        :raises IndexError: If the source or destination atom does not exist.
        
        .. seealso::
          :meth:`neighbor`
        .. note::
          The returned bond may not have ``bond.src.id == src`` and
          ``bond.dst.id == dst``, as the source and destination atoms of the bond may be
          swapped.
        .. note::
          The returned bond is invalidated when a mutator context is exited. If the bond
          must be kept alive, copy the bond data first with :meth:`Bond.copy_data`
          method.
        """
    @typing.overload
    def bond(self, src: Atom, dst: Atom) -> Bond:
        """
        Get a bond of the molecule. ``src`` and ``dst`` are interchangeable.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :returns: The bond from the source to the destination atom.
        :rtype: Bond
        :raises ValueError: If the bond does not exist, or any of the atoms does not
          belong to the molecule.
        
        .. seealso::
          :meth:`neighbor`
        .. note::
          The returned bond may not have ``bond.src.id == src.id`` and
          ``bond.dst.id == dst.id``, as the source and destination atoms of the bond
          may be swapped.
        .. note::
          The returned bond is invalidated when a mutator context is exited. If the bond
          must be kept alive, copy the bond data first with :meth:`Bond.copy_data`
          method.
        """
    def bonds(self) -> _BondsWrapper:
        """
        :rtype: collections.abc.Sequence[Bond]
        
        A wrapper object to access the bonds of the molecule. You can iterate the bonds
        of the molecule with this object.
        """
    def clear(self) -> None:
        """
        Effectively resets the molecule to an empty state.
        
        .. note::
          Invalidates all atom and bond objects.
        
        .. warning::
          Molecules with active mutator context cannot be cleared.
        .. seealso::
          :meth:`Mutator.clear`
        """
    def clear_atoms(self) -> None:
        """
        Clear all atoms and bonds of the molecule. Other metadata are left unmodified.
        
        .. note::
          Invalidates all atom and bond objects.
        .. warning::
          Molecules with active mutator context cannot clear atoms.
        .. seealso::
          :meth:`Mutator.clear_atoms`
        """
    def clear_bonds(self) -> None:
        """
        Clear all bonds of the molecule. Atoms and other metadata are left unmodified.
        
        .. note::
          Invalidates all atom and bond objects.
        .. warning::
          Molecules with active mutator context cannot clear bonds.
        .. seealso::
          :meth:`Mutator.clear_bonds`
        """
    def clear_confs(self) -> None:
        """
        Remove all conformations from the molecule.
        """
    def conceal_hydrogens(self) -> None:
        """
        Convert trivial explicit hydrogen atoms of the molecule to implicit hydrogens.
        
        Trivial explicit hydrogen atoms are the hydrogen atoms that are connected to
        only one heavy atom with a single bond and have no other neighbors (including
        implicit hydrogens).
        
        .. note::
          Invalidates all atom and bond objects.
        """
    def conformers(self) -> _ConformerIterator:
        """
        Get an iterable object of all conformations of the molecule. Each conformation
        is a 2D array of shape ``(num_atoms, 3)``. It is not available to update the
        coordinates from the returned conformers; you should manually assign to the
        conformers to update the coordinates.
        
        :rtype: collections.abc.Iterable[numpy.ndarray]
        
        .. seealso::
          :meth:`get_conf`, :meth:`set_conf`
        """
    def copy(self) -> Molecule:
        """
        Return a deep copy of self.
        """
    def del_conf(self, conf: int) -> None:
        """
        Remove a conformation from the molecule.
        
        :param conf: The index of the conformation to remove.
        """
    def get_conf(self, conf: int = 0) -> numpy.ndarray:
        """
        Get the coordinates of the atoms in a conformation.
        
        :param conf: The index of the conformation to get the coordinates from.
        :returns: The coordinates of the atoms in the conformation, as a 2D array of
          shape ``(num_atoms, 3)``.
        
        .. note::
          The returned array is a copy of the coordinates. To update the coordinates,
          use the :meth:`set_conf` method.
        """
    @typing.overload
    def has_bond(self, src: int, dst: int) -> bool:
        """
        Check if two atoms are connected by a bond.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :returns: Whether the source and destination atoms are connected by a bond.
        :raises IndexError: If the source or destination atom does not exist.
        """
    @typing.overload
    def has_bond(self, src: Atom, dst: Atom) -> bool:
        """
        Check if two atoms are connected by a bond.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :returns: Whether the source and destination atoms are connected by a bond.
        :raises ValueError: If any of the atoms does not belong to the molecule.
        """
    def mutator(self) -> Mutator:
        """
        Get a mutator for the molecule. Use this as a context manager to make changes to
        the molecule.
        
        .. note::
          The mutator will invalidate all atom and bond objects when the context is
          exited, whether or not the changes are made. If the objects must be kept
          alive, copy the data first with :meth:`Atom.copy_data` and
          :meth:`Bond.copy_data` methods.
        .. note::
          Successive calls to this method will raise an exception if the previous
          mutator is not finalized.
        """
    @typing.overload
    def neighbor(self, src: int, dst: int) -> Neighbor:
        """
        Get a neighbor of the molecule.
        
        :param src: The index of the source atom of the neighbor.
        :param dst: The index of the destination atom of the neighbor.
        :returns: The neighbor from the source to the destination atom.
        :rtype: Neighbor
        :raises ValueError: If the underlying bond does not exist.
        :raises IndexError: If the source or destination atom does not exist.
        
        .. seealso::
          :meth:`bond`
        .. note::
          Unlike :meth:`bond`, the returned neighbor is always guaranteed to have
          ``nei.src.id == src`` and ``nei.dst.id == dst``.
        .. note::
          The returned neighbor is invalidated when a mutator context is exited.
        """
    @typing.overload
    def neighbor(self, src: Atom, dst: Atom) -> Neighbor:
        """
        Get a neighbor of the molecule.
        
        :param src: The source atom of the neighbor.
        :param dst: The destination atom of the neighbor.
        :returns: The neighbor from the source to the destination atom.
        :rtype: Neighbor
        :raises ValueError: If the underlying bond does not exist, or any of the atoms
          does not belong to the molecule.
        
        .. seealso::
          :meth:`bond`
        .. note::
          Unlike :meth:`bond`, the returned neighbor is always guaranteed to have
          ``nei.src.id == src.id`` and ``nei.dst.id == dst.id``.
        .. note::
          The returned neighbor is invalidated when a mutator context is exited.
        """
    def num_atoms(self) -> int:
        """
        Get the number of atoms in the molecule. Equivalent to ``len(mol)``.
        """
    def num_bonds(self) -> int:
        """
        Get the number of bonds in the molecule. Equivalent to ``len(mol.bonds)``.
        """
    def num_confs(self) -> int:
        """
        Get the number of conformations of the molecule.
        """
    def num_fragments(self) -> int:
        """
        The number of connected components (fragments) in the molecule.
        
        .. warning::
           This might return incorrect value if the molecule is in a mutator context.
        """
    def num_sssr(self) -> int:
        """
        The number of smallest set of smallest rings (SSSR) in the molecule.
        
        .. warning::
           This might return incorrect value if the molecule is in a mutator context.
        """
    def reveal_hydrogens(self, update_confs: bool = True, optimize: bool = True) -> None:
        """
        Convert implicit hydrogen atoms of the molecule to explicit hydrogens.
        
        :param update_confs: If True, the conformations of the molecule will be
          updated to include the newly added hydrogens. When set to False, the
          coordinates of the added hydrogens will have garbage values. Default to True.
        :param optimize: If True, the conformations will be optimized after adding
          hydrogens. Default to True. This parameter is ignored if ``update_confs`` is
          False.
        :raises ValueError: If the hydrogens cannot be added. This can only happen if
          ``update_confs`` is True and the molecule has at least one conformation.
        
        .. note::
          Invalidates all atom and bond objects.
        """
    def sanitize(self, *, conjugation: bool = True, aromaticity: bool = True, hyb: bool = True, valence: bool = True) -> None:
        """
        Sanitize the molecule.
        
        :param conjugation: If True, sanitize conjugation.
        :param aromaticity: If True, sanitize aromaticity.
        :param hyb: If True, sanitize hybridization.
        :param valence: If True, sanitize valence.
        :raises ValueError: If the sanitization fails.
        
        .. note::
          The sanitization is done in the order of conjugation, aromaticity,
          hybridization, and valence. If any of the sanitization fails, the subsequent
          sanitization will not be attempted.
        
        .. note::
          The sanitization is done in place. The state of molecule will be mutated even
          if the sanitization fails.
        
        .. note::
          If any of the other three sanitization is requested, the conjugation will be
          automatically turned on.
        
        .. warning::
          This interface is experimental and may change in the future.
        """
    def set_conf(self, coords: typing.Any, conf: int = 0) -> None:
        """
        Set the coordinates of the atoms in a conformation.
        
        :param coords: The coordinates of the atoms in the conformation. Must be
          convertible to a numpy array of shape ``(num_atoms, 3)``.
        :param conf: The index of the conformation to set the coordinates to.
        """
    def sub(self, atoms: typing.Iterable[Atom | int] | None = None, bonds: typing.Iterable[Bond | int] | None = None, cat: SubstructureCategory = SubstructureCategory.Unknown) -> Substructure:
        """
        Create a substructure of the molecule.
        
        :param collections.abc.Iterable[Atom | int] atoms: The atoms to include in the
          substructure.
        :param collections.abc.Iterable[Bond | int] bonds: The bonds to include in the
          substructure.
        :param cat: The category of the substructure.
        
        This has three mode of operations:
        
        #. If both ``atoms`` and ``bonds`` are given, a substructure is created with
           the given atoms and bonds. The atoms connected by the bonds will also be
           added to the substructure, even if they are not in the ``atoms`` list.
        #. If only ``atoms`` are given, a substructure is created with the given atoms.
           All bonds between the atoms will also be added to the substructure.
        #. If only ``bonds`` are given, a substructure is created with the given bonds.
           The atoms connected by the bonds will also be added to the substructure.
        #. If neither ``atoms`` nor ``bonds`` are given, an empty substructure is
           created.
        
        .. tip::
          Pass empty list to ``bonds`` to create an atoms-only substructure.
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the molecule. The
        keys and values are both strings.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def subs(self) -> SubstructureContainer:
        """
        :type: SubstructureContainer
        
        A container of substructures of the molecule. You can iterate the substructures
        of the molecule with this object.
        """
class Mutator:
    """
    
    A mutator for a molecule. Use this as a context manager to make changes to a
    molecule:
    
    >>> from nuri.core import Molecule, AtomData
    >>> mol = Molecule()
    >>> print(mol.num_atoms())
    0
    >>> with mol.mutator() as mut:  # doctest: +IGNORE_RESULT
    ...     src = mut.add_atom(6)
    ...     dst = mut.add_atom(6)
    ...     mut.add_bond(src, dst)
    >>> print(mol.num_atoms())
    2
    >>> print(mol.num_bonds())
    1
    >>> print(mol.atom(0).atomic_number)
    6
    >>> print(mol.bond(0).order)
    BondOrder.Single
    
    .. note::
      The mutator is invalidated when the context is exited. It is an error to use
      the mutator after the context is exited.
    """
    def __enter__(self) -> Mutator:
        ...
    def __exit__(self, *args, **kwargs) -> None:
        ...
    @typing.overload
    def add_atom(self, data: AtomData = None) -> Atom:
        """
        Add an atom to the molecule.
        
        :param data: The data of the atom to add. If not given, the atom is added with
          default properties.
        :returns: The created atom.
        """
    @typing.overload
    def add_atom(self, atomic_number: int) -> Atom:
        """
        Add an atom to the molecule.
        
        :param atomic_number: The atomic number of the atom to add. Other properties of
          the atom are set to default.
        :returns: The created atom.
        """
    @typing.overload
    def add_bond(self, src: int, dst: int, order: BondOrder = BondOrder.Single) -> Bond:
        """
        Add a bond to the molecule.
        
        :param src: The index of the source atom.
        :param dst: The index of the destination atom.
        :param order: The order of the bond to add. Other properties of the bond are set
          to default. If not given, the bond is added with single bond order.
        :returns: The created bond.
        """
    @typing.overload
    def add_bond(self, src: Atom, dst: Atom, order: BondOrder = BondOrder.Single) -> Bond:
        """
        Add a bond to the molecule.
        
        :param src: The source atom.
        :param dst: The destination atom.
        :param order: The order of the bond to add. Other properties of the bond are set
          to default. If not given, the bond is added with single bond order.
        :returns: The created bond.
        """
    @typing.overload
    def add_bond(self, src: int, dst: int, data: BondData) -> Bond:
        """
        Add a bond to the molecule.
        
        :param src: The index of the source atom.
        :param dst: The index of the destination atom.
        :param data: The data of the bond to add.
        :returns: The created bond.
        """
    @typing.overload
    def add_bond(self, src: Atom, dst: Atom, data: BondData) -> Bond:
        """
        Add a bond to the molecule.
        
        :param src: The source atom.
        :param dst: The destination atom.
        :param data: The data of the bond to add.
        :returns: The created bond.
        """
    def clear(self) -> None:
        """
        Effectively resets the molecule to an empty state.
        
        .. note::
          Invalidates all atom and bond objects.
        """
    def clear_atoms(self) -> None:
        """
        Clear all atoms and bonds of the molecule. Other metadata are left unmodified.
        
        .. note::
          Invalidates all atom and bond objects.
        """
    def clear_bonds(self) -> None:
        """
        Clear all bonds of the molecule. Atoms and other metadata are left unmodified.
        
        .. note::
          Invalidates all atom and bond objects.
        """
    @typing.overload
    def mark_atom_erase(self, arg0: int) -> None:
        """
        Mark an atom to be erased from the molecule. The atom is not erased until the
        context manager is exited.
        
        :param idx: The index of the atom to erase.
        """
    @typing.overload
    def mark_atom_erase(self, arg0: Atom) -> None:
        """
        Mark an atom to be erased from the molecule. The atom is not erased until the
        context manager is exited.
        
        :param atom: The atom to erase.
        """
    @typing.overload
    def mark_bond_erase(self, src: int, dst: int) -> None:
        """
        Mark a bond to be erased from the molecule. The bond is not erased until the
        context manager is exited.
        
        :param src: The index of the source atom of the bond.
        :param dst: The index of the destination atom of the bond.
        :raises ValueError: If the bond does not exist.
        """
    @typing.overload
    def mark_bond_erase(self, src: Atom, dst: Atom) -> None:
        """
        Mark a bond to be erased from the molecule. The bond is not erased until the
        context manager is exited.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :raises ValueError: If the bond does not exist.
        """
    @typing.overload
    def mark_bond_erase(self, idx: int) -> None:
        """
        Mark a bond to be erased from the molecule. The bond is not erased until the
        context manager is exited.
        
        :param idx: The index of the bond to erase.
        """
    @typing.overload
    def mark_bond_erase(self, bond: Bond) -> None:
        """
        Mark a bond to be erased from the molecule. The bond is not erased until the
        context manager is exited.
        
        :param bond: The bond to erase.
        """
class Neighbor:
    """
    
    A neighbor of an atom in a molecule.
    """
    @property
    def bond(self) -> Bond:
        """
        :type: Bond
        
        The bond between the source and destination atoms.
        
        .. note::
          There is no guarantee that ``nei.src.id == bond.src.id`` and
          ``nei.dst.id == bond.dst.id``; the source and destination atoms of the bond
          may be swapped.
        """
    @property
    def dst(self) -> Atom:
        """
        :type: Atom
        
        The destination atom of the bond.
        """
    @property
    def src(self) -> Atom:
        """
        :type: Atom
        
        The source atom of the bond.
        """
class PeriodicTable:
    """
    
    The periodic table of elements.
    
    The periodic table is a singleton object. You can access the periodic table via
    the :data:`nuri.periodic_table` attribute, or the factory static method
    :meth:`PeriodicTable.get()`. Both of them refer to the same object. Note that
    :class:`PeriodicTable` object is *not* constructible from the Python side.
    
    You can access the periodic table as a dictionary-like object. The keys are
    atomic numbers, atomic symbols, and atomic names, tried in this order. The
    returned values are :class:`Element` objects. For example:
    
    >>> from nuri import periodic_table
    >>> periodic_table[1]
    <Element H>
    >>> periodic_table["H"]
    <Element H>
    >>> periodic_table["Hydrogen"]
    <Element H>
    
    The symbols and names are case insensitive. If no such element exists, a
    :exc:`KeyError` is raised.
    
    >>> periodic_table[1000]
    Traceback (most recent call last):
      ...
    KeyError: '1000'
    
    You can also test for the existence of an element using the ``in`` operator.
    
    >>> 1 in periodic_table
    True
    >>> "H" in periodic_table
    True
    >>> "Hydrogen" in periodic_table
    True
    >>> 1000 in periodic_table
    False
    
    The periodic table itself is an iterable object. You can iterate over the
    elements in the periodic table.
    
    >>> for elem in periodic_table:
    ...     print(elem)
    ...
    <Element Xx>
    <Element H>
    ...
    <Element Og>
    
    Refer to the ``nuri::PeriodicTable`` class in the |cppdocs| for details.
    """
    @staticmethod
    @typing.overload
    def __contains__(atomic_number: int) -> bool:
        ...
    @staticmethod
    @typing.overload
    def __contains__(atomic_symbol_or_name: str) -> bool:
        ...
    @staticmethod
    @typing.overload
    def __getitem__(atomic_number: int) -> Element:
        ...
    @staticmethod
    @typing.overload
    def __getitem__(atomic_symbol_or_name: str) -> Element:
        ...
    @staticmethod
    def __iter__() -> typing.Iterator[Element]:
        ...
    @staticmethod
    def __len__() -> int:
        ...
    @staticmethod
    def get() -> PeriodicTable:
        """
            Get the singleton :class:`PeriodicTable` object (same as
            :data:`nuri.periodic_table`).
        """
class ProxySubAtom:
    def __iter__(self) -> _ProxySubNeighborIterator:
        ...
    def as_parent(self) -> Atom:
        """
        Returns the parent atom of this atom.
        """
    def copy_data(self) -> AtomData:
        """
        Copy the underlying :class:`AtomData` object.
        
        :returns: A copy of the underlying :class:`AtomData` object.
        """
    def get_isotope(self, explicit: bool = False) -> Isotope:
        """
        Get the isotope of the atom.
        
        :param explicit: If True, returns the explicit isotope of the atom. Otherwise,
          returns the isotope of the atom. Defaults to False.
        
        :returns: The isotope of the atom. If the atom does not have an explicit
          isotope,
        
          * If ``explicit`` is False, the representative isotope of the element is
            returned.
          * If ``explicit`` is True, None is returned.
        """
    def get_pos(self, conf: int = 0) -> numpy.ndarray:
        """
        Get the position of the atom.
        
        :param conf: The index of the conformation to get the position from. Defaults to
          0.
        :returns: The position of the atom.
        
        .. note::
          The position could not be directly set from Python. Use the :meth:`set_pos`
          method to set the position.
        """
    @typing.overload
    def set_element(self, atomic_number: int) -> ProxySubAtom:
        """
        Set the element of the atom.
        
        :param atomic_number: The atomic number of the element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_element(self, symbol_or_name: str) -> ProxySubAtom:
        """
        Set the element of the atom.
        
        :param symbol_or_name: The atomic symbol or name of the element to set.
        
        .. note::
          The symbol or name is case-insensitive. Symbol is tried first, and if it
          fails, name is tried.
        """
    @typing.overload
    def set_element(self, element: Element) -> ProxySubAtom:
        """
        Set the element of the atom.
        
        :param element: The element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_isotope(self, mass_number: int) -> ProxySubAtom:
        """
        Set the isotope of the atom.
        
        :param mass_number: The mass number of the isotope to set.
        """
    @typing.overload
    def set_isotope(self, isotope: Isotope) -> ProxySubAtom:
        """
        Set the isotope of the atom.
        
        :param isotope: The isotope to set.
        """
    def set_pos(self, pos: typing.Any, conf: int = 0) -> None:
        """
        Set the position of the atom.
        
        :param pos: The 3D vector to set the position to. Must be convertible to a numpy
          array of shape (3,).
        :param conf: The index of the conformation to set the position to. Defaults to
          0.
        """
    def update(self, *, hyb: Hyb | None = None, implicit_hydrogens: int | None = None, formal_charge: int | None = None, partial_charge: float | None = None, atomic_number: int | None = None, element: Element = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, chirality: Chirality | None = None, name: str | None = None) -> ProxySubAtom:
        """
        Update the atom data. If any of the arguments are not given, the corresponding
        property is not updated.
        
        .. note::
          ``atomic_number`` and ``element`` are mutually exclusive. If both are given,
          an exception is raised.
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        """
    @typing.overload
    def update_from(self, atom: Atom) -> ProxySubAtom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: ProxySubAtom) -> ProxySubAtom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: SubAtom) -> ProxySubAtom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, data: AtomData) -> ProxySubAtom:
        """
        Update the atom data.
        
        :param data: The atom data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the atom is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def atomic_number(self) -> int:
        """
        :type: int
        
        The atomic number of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @property
    def atomic_weight(self) -> float:
        """
        :type: float
        
        The atomic weight of the atom. Equivalent to ``data.element.atomic_weight``.
        """
    @property
    def chirality(self) -> Chirality:
        """
        :type: Chirality
        
        Explicit chirality of the atom. Note that this does *not* imply the atom is a
        stereocenter chemically and might not correspond to the geometry of the
        molecule. See :class:`Chirality` for formal definition.
        
        .. tip::
          Assigning :obj:`None` clears the explicit chirality.
        
        .. seealso::
          :class:`Chirality`, :meth:`update`
        """
    @chirality.setter
    def chirality(self, arg1: Chirality | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def element(self) -> Element:
        """
        :type: Element
        
        The element of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @element.setter
    def element(self, arg1: Element) -> None:
        ...
    @property
    def element_name(self) -> str:
        """
        :type: str
        
        The IUPAC element name of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def element_symbol(self) -> str:
        """
        :type: str
        
        The IUPAC element symbol of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def formal_charge(self) -> int:
        """
        :type: int
        
        The formal charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @formal_charge.setter
    def formal_charge(self, arg1: int) -> None:
        ...
    @property
    def hyb(self) -> Hyb:
        """
        :type: Hyb
        
        The hybridization of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @hyb.setter
    def hyb(self, arg1: Hyb) -> None:
        ...
    @property
    def id(self) -> int:
        """
        :type: int
        
        A unique identifier of the atom in the substructure. The identifier is
        guaranteed to be unique within the atoms of the substructure.
        
        This is a read-only property.
        
        .. warning::
          This is not the same as the parent atom's identifier. Convert this to the
          parent atom using :meth:`as_parent` if you need the parent atom's identifier.
        .. note::
          Implementation detail: the identifier is the index of the atom in the
          substructure's atom list.
        """
    @property
    def implicit_hydrogens(self) -> int:
        """
        :type: int
        
        The number of implicit hydrogens of the atom. Guaranteed to be non-negative.
        
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        
        .. seealso::
          :meth:`update`
        """
    @implicit_hydrogens.setter
    def implicit_hydrogens(self, arg1: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the atom. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def partial_charge(self) -> float:
        """
        :type: float
        
        The partial charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @partial_charge.setter
    def partial_charge(self, arg1: float) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the atom. The keys
        and values are both strings.
        
        .. note::
          The properties are shared with the underlying :class:`AtomData` object. If the
          properties are modified, the underlying object is also modified.
        
          As a result, the property map is also invalidated when any changes are made
          to the molecule. If the properties must be kept alive, copy the properties
          first with ``copy()`` method.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the atom is a ring atom.
        
        .. note::
          Beware updating this property when the atom is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
class ProxySubBond:
    def approx_order(self) -> float:
        """
        The approximate bond order of the bond.
        """
    def as_parent(self) -> Bond:
        """
        Returns the parent bond of this bond.
        """
    def copy_data(self) -> BondData:
        """
        Copy the underlying :class:`BondData` object.
        
        :returns: A copy of the underlying :class:`BondData` object.
        """
    def length(self, conf: int = 0) -> float:
        """
        Calculate the length of the bond.
        
        :param conf: The index of the conformation to calculate the length from.
          Defaults to 0.
        :returns: The length of the bond.
        """
    def rotatable(self) -> bool:
        """
        Whether the bond is rotatable.
        
        .. note::
          The result is calculated as the bond order is :data:`BondOrder.Single` or
          :data:`BondOrder.Other`, and the bond is not a conjugated or a ring bond.
        """
    def sqlen(self, conf: int = 0) -> float:
        """
        Calculate the square of the length of the bond.
        
        :param conf: The index of the conformation to calculate the length from.
          Defaults to 0.
        :returns: The square of the length of the bond.
        """
    def update(self, *, order: BondOrder | None = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, config: BondConfig | None = None, name: str | None = None) -> ProxySubBond:
        """
        Update the bond data. If any of the arguments are not given, the corresponding
        property is not updated.
        """
    @typing.overload
    def update_from(self, bond: Bond) -> ProxySubBond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: ProxySubBond) -> ProxySubBond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: SubBond) -> ProxySubBond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, data: BondData) -> ProxySubBond:
        """
        Update the bond data.
        
        :param data: The bond data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the bond is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def config(self) -> BondConfig:
        """
        :type: BondConfig
        
        The explicit configuration of the bond. Note that this does *not* imply the bond
        is a torsionally restricted bond chemically.
        
        .. note::
          For bonds with more than 3 neighboring atoms, :attr:`BondConfig.Cis` or
          :attr:`BondConfig.Trans` configurations are not well defined terms. In such
          cases, this will return whether **the first neighbors are on the same side of
          the bond**. For example, in the following structure (assuming the neighbors
          are ordered in the same way as the atoms), the bond between atoms 0 and 1 is
          considered to be in a cis configuration (first neighbors are marked with angle
          brackets)::
        
            <2>     <4>
              \\     /
               0 = 1
              /     \\
             3       5
        
          On the other hand, when the neighbors are ordered in the opposite way, the
          bond between atoms 0 and 1 is considered to be in a trans configuration::
        
            <2>      5
              \\     /
               0 = 1
              /     \\
             3      <4>
        
        .. tip::
          Assigning :obj:`None` clears the explicit bond configuration.
        
        .. seealso::
          :meth:`update`
        """
    @config.setter
    def config(self, arg1: BondConfig | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def dst(self) -> ProxySubAtom:
        """
        :type: Atom
        
        The destination atom of the bond.
        """
    @property
    def id(self) -> int:
        """
        :type: int
        
        A unique identifier of the bond in the substructure. The identifier is
        guaranteed to be unique within the atoms of the substructure.
        
        This is a read-only property.
        
        .. warning::
          This is not the same as the parent bond's identifier. Convert this to the
          parent bond using :meth:`as_parent` if you need the parent bond's identifier.
        .. note::
          Implementation detail: the identifier is the index of the bond in the
          substructure's bond list.
        """
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the bond. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def order(self) -> BondOrder:
        """
        :type: BondOrder
        
        The bond order of the bond.
        
        .. seealso::
          :meth:`update`
        """
    @order.setter
    def order(self, arg1: BondOrder) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the bond. The keys
        and values are both strings.
        
        .. note::
          The properties are shared with the underlying :class:`BondData` object. If the
          properties are modified, the underlying object is also modified.
        
          As a result, the property map is invalidated when any changes are made to the
          molecule. If the properties must be kept alive, copy the properties first with
          ``copy()`` method.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the bond is a ring bond.
        
        .. note::
          Beware updating this property when the bond is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
    @property
    def src(self) -> ProxySubAtom:
        """
        :type: Atom
        
        The source atom of the bond.
        """
class ProxySubNeighbor:
    def as_parent(self) -> Neighbor:
        """
        Returns the parent version of this neighbor.
        """
    @property
    def bond(self) -> ProxySubBond:
        """
        Bond between the source and destination atoms.
        """
    @property
    def dst(self) -> ProxySubAtom:
        """
        Destination atom of the neighbor.
        """
    @property
    def src(self) -> ProxySubAtom:
        """
        Source atom of the neighbor.
        """
class ProxySubstructure:
    """
    
    This represents a substructure managed by a molecule. If a user wishes to
    create a short-lived substructure not managed by a molecule, use
    :meth:`Molecule.substructure` method instead.
    
    This will invalidate when the parent molecule is modified, or any substructures
    are removed from the parent molecule. If the substructure must be kept alive,
    convert the substructure first with :meth:`copy` method.
    
    .. seealso::
      :class:`Substructure`
    
    Here, we only provide the methods that are additional to the
    :class:`Substructure` class.
    """
    @typing.overload
    def __contains__(self, idx: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: ProxySubAtom) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: Atom) -> bool:
        ...
    @typing.overload
    def __getitem__(self, idx: int) -> ProxySubAtom:
        ...
    @typing.overload
    def __getitem__(self, atom: Atom) -> ProxySubAtom:
        ...
    def __iter__(self) -> _ProxySubAtomIterator:
        ...
    def __len__(self) -> int:
        ...
    def add_atoms(self, atoms: typing.Iterable[Atom | int], add_bonds: bool = True) -> None:
        """
        Add atoms to the substructure.
        
        :param collections.abc.Iterable[Atom | int] atoms: The atoms to add to the
          substructure. The atoms must belong to the same molecule as the substructure.
          All duplicate atoms are ignored.
        :param bool add_bonds: If True, the bonds between the added atoms are also added
          to the substructure. If False, the bonds are not added.
        :raises TypeError: If any atom is not an :class:`Atom` or :class:`int`.
        :raises ValueError: If any atom does not belong to the same molecule.
        :raises IndexError: If any atom index is out of range.
        
        .. note::
          Due to the implementation, it is much faster to add atoms in bulk than adding
          them one by one. Thus, we explicitly provide only the bulk addition method.
        """
    def add_bonds(self, bonds: typing.Iterable[Bond | int]) -> None:
        """
        Add bonds to the substructure. If any atom of the bond does not belong to the
        substructure, the atom is also added to the substructure.
        
        :param collections.abc.Iterable[Bond | int] bonds: The bonds to add to the
          substructure. The bonds must belong to the same molecule as the substructure.
          All duplicate bonds are ignored.
        :raises TypeError: If any bond is not a :class:`Bond` or :class:`int`.
        :raises ValueError: If any bond does not belong to the same molecule.
        :raises IndexError: If any bond index is out of range.
        
        .. note::
          Due to the implementation, it is much faster to add bonds in bulk than adding
          them one by one. Thus, we explicitly provide only the bulk addition method.
        """
    @typing.overload
    def atom(self, idx: int) -> ProxySubAtom:
        """
        Get a substructure atom by index.
        
        :param idx: The index of the atom.
        :return: The atom at the given index.
        :rtype: SubAtom
        
        .. note::
          The returned atom is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the atom must be kept alive, copy the atom
          data first.
        """
    @typing.overload
    def atom(self, atom: Atom) -> ProxySubAtom:
        """
        Get a substructure atom from a parent atom.
        
        :param atom: The parent atom to get the sub-atom of.
        :return: The sub-atom of the parent atom.
        :rtype: SubAtom
        
        .. note::
          The returned atom is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the atom must be kept alive, copy the atom
          data first.
        """
    @typing.overload
    def bond(self, idx: int) -> ProxySubBond:
        """
        Get a bond by index.
        
        :param idx: The index of the bond.
        :return: The bond at the given index.
        :rtype: SubBond
        """
    @typing.overload
    def bond(self, bond: Bond) -> ProxySubBond:
        """
        Get a substructure bond from a parent bond.
        
        :param bond: The parent bond to get the sub-bond of.
        :return: The sub-bond of the parent bond.
        :rtype: SubBond
        
        .. note::
          The returned bond is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the bond must be kept alive, copy the bond
          data first.
        """
    @typing.overload
    def bond(self, src: ProxySubAtom, dst: ProxySubAtom) -> ProxySubBond:
        """
        Get a bond of the substructure. ``src`` and ``dst`` are interchangeable.
        
        :param src: The source sub-atom of the bond.
        :param dst: The destination sub-atom of the bond.
        :returns: The bond from the source to the destination sub-atom.
        :rtype: SubBond
        :raises ValueError: If the bond does not exist, or any of the sub-atoms does not
          belong to the substructure.
        
        .. seealso::
          :meth:`neighbor`
        .. note::
          The returned bond may not have ``bond.src.id == src.id`` and
          ``bond.dst.id == dst.id``, as the source and destination atoms of the bond may
          be swapped.
        .. note::
          The returned bond is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the bond must be kept alive, copy the bond
          data first.
        """
    @typing.overload
    def bond(self, src: Atom, dst: Atom) -> ProxySubBond:
        """
        Get a bond of the substructure. ``src`` and ``dst`` are interchangeable.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :returns: The bond from the source to the destination atom.
        :rtype: SubBond
        :raises ValueError: If the bond does not exist, the source or destination
          atom does not belong to the substructure, or any of the atoms does not belong
          to the same molecule.
        
        .. seealso::
          :meth:`neighbor`
        .. note::
          The source and destination atoms of the bond may be swapped.
        .. note::
          The returned bond is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the bond must be kept alive, copy the bond
          data first.
        """
    def bonds(self) -> _ProxySubBonds:
        """
        :rtype: collections.abc.Sequence[SubBond]
        
        Get a collection of bonds in the substructure. Invalidated when the parent
        molecule is modified, or if the substructure is modified.
        """
    def clear(self) -> None:
        """
        Effectively reset the substructure to an empty state.
        """
    def clear_atoms(self) -> None:
        """
        Remove all atoms from the substructure. The bonds are also removed. Other
        metadata of the substructure is not affected.
        """
    def clear_bonds(self) -> None:
        """
        Remove all bonds from the substructure. The atoms and other metadata of the
        substructure is not affected.
        """
    def conceal_hydrogens(self) -> None:
        """
        Convert trivial explicit hydrogen atoms of the substructure to implicit
        hydrogens.
        
        Trivial explicit hydrogen atoms are the hydrogen atoms that are connected to
        only one heavy atom with a single bond and have no other neighbors (including
        implicit hydrogens).
        
        .. note::
          Invalidates all atom and bond objects.
        """
    def conformers(self) -> _ProxySubConformersIterator:
        """
        Get an iterable object of all conformations of the substructure. Each
        conformation is a 2D array of shape ``(num_atoms, 3)``. It is not available to
        update the coordinates from the returned conformers; you should manually assign
        to the conformers to update the coordinates.
        
        :rtype: collections.abc.Iterable[numpy.ndarray]
        
        .. seealso::
          :meth:`get_conf`, :meth:`set_conf`
        """
    def copy(self) -> Substructure:
        """
        Create a copy of the substructure. The returned substructure is not managed by
        the parent molecule.
        """
    @typing.overload
    def erase_atom(self, sub_atom: ProxySubAtom) -> None:
        """
        Remove an atom from the substructure. Any bonds connected to the atom are also
        removed.
        
        :param sub_atom: The sub-atom to remove.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_atom(self, atom: Atom) -> None:
        """
        Remove an atom from the substructure. Any bonds connected to the atom are also
        removed.
        
        :param atom: The parent atom to remove.
        :raises ValueError: If the atom is not in the substructure.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, sub_bond: ProxySubBond) -> None:
        """
        Remove a bond from the substructure.
        
        :param sub_bond: The sub-bond to remove.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, bond: Bond) -> None:
        """
        Remove a bond from the substructure.
        
        :param bond: The parent bond to remove.
        :raises ValueError: If the bond is not in the substructure.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, src: ProxySubAtom, dst: ProxySubAtom) -> None:
        """
        Remove a bond from the substructure. The source and destination atoms are
        interchangeable.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :raises ValueError: If the bond is not in the substructure.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, src: Atom, dst: Atom) -> None:
        """
        Remove a bond from the substructure. The source and destination atoms are
        interchangeable.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :raises ValueError: If the bond is not in the substructure or does not exist.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    def get_conf(self, conf: int = 0) -> numpy.ndarray:
        """
        Get the coordinates of the atoms in a conformation of the substructure.
        
        :param conf: The index of the conformation to get the coordinates from.
        :returns: The coordinates of the atoms in the substructure, as a 2D array of
          shape ``(num_atoms, 3)``.
        
        .. note::
          The returned array is a copy of the coordinates. To update the coordinates,
          use the :meth:`set_conf` method.
        """
    @typing.overload
    def has_bond(self, src: ProxySubAtom, dst: ProxySubAtom) -> bool:
        """
        Check if two atoms are connected by a bond.
        
        :param src: The source sub-atom of the bond.
        :param dst: The destination sub-atom of the bond.
        :returns: Whether the source and destination atoms are connected by a bond.
        :raises ValueError: If any of the sub-atoms does not belong to the substructure.
        """
    @typing.overload
    def has_bond(self, src: Atom, dst: Atom) -> bool:
        """
        Check if two atoms are connected by a bond.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :returns: Whether the source and destination atoms are connected by a bond.
        :raises ValueError: If any of the atoms does not belong to the molecule.
        """
    @typing.overload
    def neighbor(self, src: ProxySubAtom, dst: ProxySubAtom) -> ProxySubNeighbor:
        """
        Get a neighbor of the substructure.
        
        :param src: The source sub-atom of the neighbor.
        :param dst: The destination sub-atom of the neighbor.
        :returns: The neighbor from the source to the destination sub-atom.
        :rtype: SubNeighbor
        :raises ValueError: If the underlying bond does not exist, or any of the
          sub-atoms does not belong to the substructure.
        
        .. seealso::
          :meth:`bond`
        .. note::
          Unlike :meth:`bond`, the returned neighbor is always guaranteed to have
          ``nei.src.id == src.id`` and ``nei.dst.id == dst.id``.
        .. note::
          The returned neighbor is invalidated when the parent molecule is modified, or
          if the substructure is modified.
        """
    @typing.overload
    def neighbor(self, src: Atom, dst: Atom) -> ProxySubNeighbor:
        """
        Get a neighbor of the substructure.
        
        :param src: The source atom of the neighbor.
        :param dst: The destination atom of the neighbor.
        :returns: The neighbor from the source to the destination atom.
        :rtype: SubNeighbor
        :raises ValueError: If the underlying bond does not exist, the source or
          destination atom does not belong to the substructure, or any of the atoms does
          not belong to the same molecule.
        
        .. seealso::
          :meth:`bond`
        .. note::
          Unlike :meth:`bond`, the returned neighbor is always guaranteed to have
          the source and destination atoms in the same order as the arguments.
        .. note::
          The returned neighbor is invalidated when the parent molecule is modified, or
          if the substructure is modified.
        """
    def num_atoms(self) -> int:
        """
        The number of atoms in the substructure. Equivalent to ``len(sub)``.
        """
    def num_bonds(self) -> int:
        """
        The number of bonds in the substructure. Equivalent to ``len(sub.bonds)``.
        """
    def num_confs(self) -> int:
        """
        Get the number of conformations of the substructure.
        """
    def parent_atoms(self) -> list:
        """
        The parent atom indices of the substructure atoms. The indices are guaranteed to
        be unique and in ascending order.
        
        :rtype: list[int]
        
        .. note::
          The returned list is a copy of the internal list, so modifying the list does
          not affect the substructure.
        """
    def parent_bonds(self) -> list:
        """
        The parent bond indices of the substructure bonds. The indices are guaranteed to
        be unique and in ascending order.
        
        :rtype: list[int]
        
        .. note::
          The returned list is a copy of the internal list, so modifying the list does
          not affect the substructure.
        """
    def refresh_bonds(self) -> None:
        """
        Refresh the bonds of the substructure. All bonds between the atoms of the
        substructure are removed, and new bonds are added based on the parent molecule.
        """
    def set_conf(self, coords: typing.Any, conf: int = 0) -> None:
        """
        Set the coordinates of the atoms in a conformation of the substructure.
        
        :param coords: The coordinates of the atoms in the conformation. Must be
          convertible to a numpy array of shape ``(num_atoms, 3)``.
        :param conf: The index of the conformation to set the coordinates to.
        
        .. note::
          The coordinates of the atoms that are *not* in the substructure are not
          affected.
        """
    @property
    def category(self) -> SubstructureCategory:
        """
        :type: SubstructureCategory
        
        The category of the substructure. This is used to categorize the substructure.
        """
    @category.setter
    def category(self, arg1: SubstructureCategory) -> None:
        ...
    @property
    def id(self) -> int:
        """
        :type: int
        
        An integral identifier of the substructure. The identifier is mostly for use in
        the protein residue numbering system.
        
        .. warning::
          This is *not* guaranteed to be unique within the molecule.
        """
    @id.setter
    def id(self, arg1: int) -> None:
        ...
    @property
    def molecule(self) -> Molecule:
        """
        :type: Molecule
        
        The parent molecule of the substructure.
        """
    @property
    def name(self) -> str:
        """
        :type: str
        
        A name of the substructure. This is for user convenience and has no effect on
        the substructure's behavior.
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the substructure. The
        keys and values are both strings.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
class SubAtom:
    """
    
    Atom of a substructure.
    """
    def __iter__(self) -> _SubNeighborIterator:
        ...
    def as_parent(self) -> Atom:
        """
        Returns the parent atom of this atom.
        """
    def copy_data(self) -> AtomData:
        """
        Copy the underlying :class:`AtomData` object.
        
        :returns: A copy of the underlying :class:`AtomData` object.
        """
    def get_isotope(self, explicit: bool = False) -> Isotope:
        """
        Get the isotope of the atom.
        
        :param explicit: If True, returns the explicit isotope of the atom. Otherwise,
          returns the isotope of the atom. Defaults to False.
        
        :returns: The isotope of the atom. If the atom does not have an explicit
          isotope,
        
          * If ``explicit`` is False, the representative isotope of the element is
            returned.
          * If ``explicit`` is True, None is returned.
        """
    def get_pos(self, conf: int = 0) -> numpy.ndarray:
        """
        Get the position of the atom.
        
        :param conf: The index of the conformation to get the position from. Defaults to
          0.
        :returns: The position of the atom.
        
        .. note::
          The position could not be directly set from Python. Use the :meth:`set_pos`
          method to set the position.
        """
    @typing.overload
    def set_element(self, atomic_number: int) -> SubAtom:
        """
        Set the element of the atom.
        
        :param atomic_number: The atomic number of the element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_element(self, symbol_or_name: str) -> SubAtom:
        """
        Set the element of the atom.
        
        :param symbol_or_name: The atomic symbol or name of the element to set.
        
        .. note::
          The symbol or name is case-insensitive. Symbol is tried first, and if it
          fails, name is tried.
        """
    @typing.overload
    def set_element(self, element: Element) -> SubAtom:
        """
        Set the element of the atom.
        
        :param element: The element to set.
        
        .. seealso::
          :meth:`update`
        """
    @typing.overload
    def set_isotope(self, mass_number: int) -> SubAtom:
        """
        Set the isotope of the atom.
        
        :param mass_number: The mass number of the isotope to set.
        """
    @typing.overload
    def set_isotope(self, isotope: Isotope) -> SubAtom:
        """
        Set the isotope of the atom.
        
        :param isotope: The isotope to set.
        """
    def set_pos(self, pos: typing.Any, conf: int = 0) -> None:
        """
        Set the position of the atom.
        
        :param pos: The 3D vector to set the position to. Must be convertible to a numpy
          array of shape (3,).
        :param conf: The index of the conformation to set the position to. Defaults to
          0.
        """
    def update(self, *, hyb: Hyb | None = None, implicit_hydrogens: int | None = None, formal_charge: int | None = None, partial_charge: float | None = None, atomic_number: int | None = None, element: Element = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, chirality: Chirality | None = None, name: str | None = None) -> SubAtom:
        """
        Update the atom data. If any of the arguments are not given, the corresponding
        property is not updated.
        
        .. note::
          ``atomic_number`` and ``element`` are mutually exclusive. If both are given,
          an exception is raised.
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        """
    @typing.overload
    def update_from(self, atom: Atom) -> SubAtom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: ProxySubAtom) -> SubAtom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, atom: SubAtom) -> SubAtom:
        """
        Update the atom data.
        
        :param atom: The atom to copy the data from.
        """
    @typing.overload
    def update_from(self, data: AtomData) -> SubAtom:
        """
        Update the atom data.
        
        :param data: The atom data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the atom is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def atomic_number(self) -> int:
        """
        :type: int
        
        The atomic number of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @property
    def atomic_weight(self) -> float:
        """
        :type: float
        
        The atomic weight of the atom. Equivalent to ``data.element.atomic_weight``.
        """
    @property
    def chirality(self) -> Chirality:
        """
        :type: Chirality
        
        Explicit chirality of the atom. Note that this does *not* imply the atom is a
        stereocenter chemically and might not correspond to the geometry of the
        molecule. See :class:`Chirality` for formal definition.
        
        .. tip::
          Assigning :obj:`None` clears the explicit chirality.
        
        .. seealso::
          :class:`Chirality`, :meth:`update`
        """
    @chirality.setter
    def chirality(self, arg1: Chirality | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def element(self) -> Element:
        """
        :type: Element
        
        The element of the atom.
        
        .. seealso::
          :meth:`set_element`, :meth:`update`
        """
    @element.setter
    def element(self, arg1: Element) -> None:
        ...
    @property
    def element_name(self) -> str:
        """
        :type: str
        
        The IUPAC element name of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def element_symbol(self) -> str:
        """
        :type: str
        
        The IUPAC element symbol of the atom.
        
        .. seealso::
          :meth:`set_element`
        """
    @property
    def formal_charge(self) -> int:
        """
        :type: int
        
        The formal charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @formal_charge.setter
    def formal_charge(self, arg1: int) -> None:
        ...
    @property
    def hyb(self) -> Hyb:
        """
        :type: Hyb
        
        The hybridization of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @hyb.setter
    def hyb(self, arg1: Hyb) -> None:
        ...
    @property
    def id(self) -> int:
        """
        :type: int
        
        A unique identifier of the atom in the substructure. The identifier is
        guaranteed to be unique within the atoms of the substructure.
        
        This is a read-only property.
        
        .. warning::
          This is not the same as the parent atom's identifier. Convert this to the
          parent atom using :meth:`as_parent` if you need the parent atom's identifier.
        .. note::
          Implementation detail: the identifier is the index of the atom in the
          substructure's atom list.
        """
    @property
    def implicit_hydrogens(self) -> int:
        """
        :type: int
        
        The number of implicit hydrogens of the atom. Guaranteed to be non-negative.
        
        .. note::
          It is illegal to set the number of implicit hydrogens to a negative number.
        
        .. seealso::
          :meth:`update`
        """
    @implicit_hydrogens.setter
    def implicit_hydrogens(self, arg1: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the atom. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def partial_charge(self) -> float:
        """
        :type: float
        
        The partial charge of the atom.
        
        .. seealso::
          :meth:`update`
        """
    @partial_charge.setter
    def partial_charge(self, arg1: float) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the atom. The keys
        and values are both strings.
        
        .. note::
          The properties are shared with the underlying :class:`AtomData` object. If the
          properties are modified, the underlying object is also modified.
        
          As a result, the property map is also invalidated when any changes are made
          to the molecule. If the properties must be kept alive, copy the properties
          first with ``copy()`` method.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the atom is a ring atom.
        
        .. note::
          Beware updating this property when the atom is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
class SubBond:
    """
    
    Bond of a substructure.
    """
    def approx_order(self) -> float:
        """
        The approximate bond order of the bond.
        """
    def as_parent(self) -> Bond:
        """
        Returns the parent bond of this bond.
        """
    def copy_data(self) -> BondData:
        """
        Copy the underlying :class:`BondData` object.
        
        :returns: A copy of the underlying :class:`BondData` object.
        """
    def length(self, conf: int = 0) -> float:
        """
        Calculate the length of the bond.
        
        :param conf: The index of the conformation to calculate the length from.
          Defaults to 0.
        :returns: The length of the bond.
        """
    def rotatable(self) -> bool:
        """
        Whether the bond is rotatable.
        
        .. note::
          The result is calculated as the bond order is :data:`BondOrder.Single` or
          :data:`BondOrder.Other`, and the bond is not a conjugated or a ring bond.
        """
    def sqlen(self, conf: int = 0) -> float:
        """
        Calculate the square of the length of the bond.
        
        :param conf: The index of the conformation to calculate the length from.
          Defaults to 0.
        :returns: The square of the length of the bond.
        """
    def update(self, *, order: BondOrder | None = None, aromatic: bool | None = None, conjugated: bool | None = None, ring: bool | None = None, config: BondConfig | None = None, name: str | None = None) -> SubBond:
        """
        Update the bond data. If any of the arguments are not given, the corresponding
        property is not updated.
        """
    @typing.overload
    def update_from(self, bond: Bond) -> SubBond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: ProxySubBond) -> SubBond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, bond: SubBond) -> SubBond:
        """
        Update the bond data.
        
        :param bond: The bond to copy the data from.
        """
    @typing.overload
    def update_from(self, data: BondData) -> SubBond:
        """
        Update the bond data.
        
        :param data: The bond data to update from.
        """
    @property
    def aromatic(self) -> bool:
        """
        :type: bool
        
        Whether the bond is aromatic.
        
        .. seealso::
          :meth:`update`
        """
    @aromatic.setter
    def aromatic(self, arg1: bool) -> None:
        ...
    @property
    def config(self) -> BondConfig:
        """
        :type: BondConfig
        
        The explicit configuration of the bond. Note that this does *not* imply the bond
        is a torsionally restricted bond chemically.
        
        .. note::
          For bonds with more than 3 neighboring atoms, :attr:`BondConfig.Cis` or
          :attr:`BondConfig.Trans` configurations are not well defined terms. In such
          cases, this will return whether **the first neighbors are on the same side of
          the bond**. For example, in the following structure (assuming the neighbors
          are ordered in the same way as the atoms), the bond between atoms 0 and 1 is
          considered to be in a cis configuration (first neighbors are marked with angle
          brackets)::
        
            <2>     <4>
              \\     /
               0 = 1
              /     \\
             3       5
        
          On the other hand, when the neighbors are ordered in the opposite way, the
          bond between atoms 0 and 1 is considered to be in a trans configuration::
        
            <2>      5
              \\     /
               0 = 1
              /     \\
             3      <4>
        
        .. tip::
          Assigning :obj:`None` clears the explicit bond configuration.
        
        .. seealso::
          :meth:`update`
        """
    @config.setter
    def config(self, arg1: BondConfig | None) -> None:
        ...
    @property
    def conjugated(self) -> bool:
        """
        :type: bool
        
        Whether the atom is conjugated.
        
        .. seealso::
          :meth:`update`
        """
    @conjugated.setter
    def conjugated(self, arg1: bool) -> None:
        ...
    @property
    def dst(self) -> SubAtom:
        """
        :type: Atom
        
        The destination atom of the bond.
        """
    @property
    def id(self) -> int:
        """
        :type: int
        
        A unique identifier of the bond in the substructure. The identifier is
        guaranteed to be unique within the atoms of the substructure.
        
        This is a read-only property.
        
        .. warning::
          This is not the same as the parent bond's identifier. Convert this to the
          parent bond using :meth:`as_parent` if you need the parent bond's identifier.
        .. note::
          Implementation detail: the identifier is the index of the bond in the
          substructure's bond list.
        """
    @property
    def name(self) -> str:
        """
        :type: str
        
        The name of the bond. Returns an empty string if the name is not set.
        
        .. seealso::
          :meth:`update`
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def order(self) -> BondOrder:
        """
        :type: BondOrder
        
        The bond order of the bond.
        
        .. seealso::
          :meth:`update`
        """
    @order.setter
    def order(self, arg1: BondOrder) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the bond. The keys
        and values are both strings.
        
        .. note::
          The properties are shared with the underlying :class:`BondData` object. If the
          properties are modified, the underlying object is also modified.
        
          As a result, the property map is invalidated when any changes are made to the
          molecule. If the properties must be kept alive, copy the properties first with
          ``copy()`` method.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
    @property
    def ring(self) -> bool:
        """
        :type: bool
        
        Whether the bond is a ring bond.
        
        .. note::
          Beware updating this property when the bond is owned by a molecule. The
          molecule may not be aware of the change.
        
        .. seealso::
          :meth:`update`
        """
    @ring.setter
    def ring(self, arg1: bool) -> None:
        ...
    @property
    def src(self) -> SubAtom:
        """
        :type: Atom
        
        The source atom of the bond.
        """
class SubNeighbor:
    """
    
    Neighbor of a substructure.
    """
    def as_parent(self) -> Neighbor:
        """
        Returns the parent version of this neighbor.
        """
    @property
    def bond(self) -> SubBond:
        """
        Bond between the source and destination atoms.
        """
    @property
    def dst(self) -> SubAtom:
        """
        Destination atom of the neighbor.
        """
    @property
    def src(self) -> SubAtom:
        """
        Source atom of the neighbor.
        """
class Substructure:
    """
    
    A substructure of a molecule.
    
    This will invalidate when the parent molecule is modified.
    """
    @typing.overload
    def __contains__(self, idx: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: SubAtom) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: Atom) -> bool:
        ...
    @typing.overload
    def __getitem__(self, idx: int) -> SubAtom:
        ...
    @typing.overload
    def __getitem__(self, atom: Atom) -> SubAtom:
        ...
    def __iter__(self) -> _SubAtomIterator:
        ...
    def __len__(self) -> int:
        ...
    def add_atoms(self, atoms: typing.Iterable[Atom | int], add_bonds: bool = True) -> None:
        """
        Add atoms to the substructure.
        
        :param collections.abc.Iterable[Atom | int] atoms: The atoms to add to the
          substructure. The atoms must belong to the same molecule as the substructure.
          All duplicate atoms are ignored.
        :param bool add_bonds: If True, the bonds between the added atoms are also added
          to the substructure. If False, the bonds are not added.
        :raises TypeError: If any atom is not an :class:`Atom` or :class:`int`.
        :raises ValueError: If any atom does not belong to the same molecule.
        :raises IndexError: If any atom index is out of range.
        
        .. note::
          Due to the implementation, it is much faster to add atoms in bulk than adding
          them one by one. Thus, we explicitly provide only the bulk addition method.
        """
    def add_bonds(self, bonds: typing.Iterable[Bond | int]) -> None:
        """
        Add bonds to the substructure. If any atom of the bond does not belong to the
        substructure, the atom is also added to the substructure.
        
        :param collections.abc.Iterable[Bond | int] bonds: The bonds to add to the
          substructure. The bonds must belong to the same molecule as the substructure.
          All duplicate bonds are ignored.
        :raises TypeError: If any bond is not a :class:`Bond` or :class:`int`.
        :raises ValueError: If any bond does not belong to the same molecule.
        :raises IndexError: If any bond index is out of range.
        
        .. note::
          Due to the implementation, it is much faster to add bonds in bulk than adding
          them one by one. Thus, we explicitly provide only the bulk addition method.
        """
    @typing.overload
    def atom(self, idx: int) -> SubAtom:
        """
        Get a substructure atom by index.
        
        :param idx: The index of the atom.
        :return: The atom at the given index.
        :rtype: SubAtom
        
        .. note::
          The returned atom is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the atom must be kept alive, copy the atom
          data first.
        """
    @typing.overload
    def atom(self, atom: Atom) -> SubAtom:
        """
        Get a substructure atom from a parent atom.
        
        :param atom: The parent atom to get the sub-atom of.
        :return: The sub-atom of the parent atom.
        :rtype: SubAtom
        
        .. note::
          The returned atom is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the atom must be kept alive, copy the atom
          data first.
        """
    @typing.overload
    def bond(self, idx: int) -> SubBond:
        """
        Get a bond by index.
        
        :param idx: The index of the bond.
        :return: The bond at the given index.
        :rtype: SubBond
        """
    @typing.overload
    def bond(self, bond: Bond) -> SubBond:
        """
        Get a substructure bond from a parent bond.
        
        :param bond: The parent bond to get the sub-bond of.
        :return: The sub-bond of the parent bond.
        :rtype: SubBond
        
        .. note::
          The returned bond is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the bond must be kept alive, copy the bond
          data first.
        """
    @typing.overload
    def bond(self, src: SubAtom, dst: SubAtom) -> SubBond:
        """
        Get a bond of the substructure. ``src`` and ``dst`` are interchangeable.
        
        :param src: The source sub-atom of the bond.
        :param dst: The destination sub-atom of the bond.
        :returns: The bond from the source to the destination sub-atom.
        :rtype: SubBond
        :raises ValueError: If the bond does not exist, or any of the sub-atoms does not
          belong to the substructure.
        
        .. seealso::
          :meth:`neighbor`
        .. note::
          The returned bond may not have ``bond.src.id == src.id`` and
          ``bond.dst.id == dst.id``, as the source and destination atoms of the bond may
          be swapped.
        .. note::
          The returned bond is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the bond must be kept alive, copy the bond
          data first.
        """
    @typing.overload
    def bond(self, src: Atom, dst: Atom) -> SubBond:
        """
        Get a bond of the substructure. ``src`` and ``dst`` are interchangeable.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :returns: The bond from the source to the destination atom.
        :rtype: SubBond
        :raises ValueError: If the bond does not exist, the source or destination
          atom does not belong to the substructure, or any of the atoms does not belong
          to the same molecule.
        
        .. seealso::
          :meth:`neighbor`
        .. note::
          The source and destination atoms of the bond may be swapped.
        .. note::
          The returned bond is invalidated when the parent molecule is modified, or if
          the substructure is modified. If the bond must be kept alive, copy the bond
          data first.
        """
    def bonds(self) -> _SubBonds:
        """
        :rtype: collections.abc.Sequence[SubBond]
        
        Get a collection of bonds in the substructure. Invalidated when the parent
        molecule is modified, or if the substructure is modified.
        """
    def clear(self) -> None:
        """
        Effectively reset the substructure to an empty state.
        """
    def clear_atoms(self) -> None:
        """
        Remove all atoms from the substructure. The bonds are also removed. Other
        metadata of the substructure is not affected.
        """
    def clear_bonds(self) -> None:
        """
        Remove all bonds from the substructure. The atoms and other metadata of the
        substructure is not affected.
        """
    def conceal_hydrogens(self) -> None:
        """
        Convert trivial explicit hydrogen atoms of the substructure to implicit
        hydrogens.
        
        Trivial explicit hydrogen atoms are the hydrogen atoms that are connected to
        only one heavy atom with a single bond and have no other neighbors (including
        implicit hydrogens).
        
        .. note::
          Invalidates all atom and bond objects.
        """
    def conformers(self) -> _SubConformersIterator:
        """
        Get an iterable object of all conformations of the substructure. Each
        conformation is a 2D array of shape ``(num_atoms, 3)``. It is not available to
        update the coordinates from the returned conformers; you should manually assign
        to the conformers to update the coordinates.
        
        :rtype: collections.abc.Iterable[numpy.ndarray]
        
        .. seealso::
          :meth:`get_conf`, :meth:`set_conf`
        """
    @typing.overload
    def erase_atom(self, sub_atom: SubAtom) -> None:
        """
        Remove an atom from the substructure. Any bonds connected to the atom are also
        removed.
        
        :param sub_atom: The sub-atom to remove.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_atom(self, atom: Atom) -> None:
        """
        Remove an atom from the substructure. Any bonds connected to the atom are also
        removed.
        
        :param atom: The parent atom to remove.
        :raises ValueError: If the atom is not in the substructure.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, sub_bond: SubBond) -> None:
        """
        Remove a bond from the substructure.
        
        :param sub_bond: The sub-bond to remove.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, bond: Bond) -> None:
        """
        Remove a bond from the substructure.
        
        :param bond: The parent bond to remove.
        :raises ValueError: If the bond is not in the substructure.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, src: SubAtom, dst: SubAtom) -> None:
        """
        Remove a bond from the substructure. The source and destination atoms are
        interchangeable.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :raises ValueError: If the bond is not in the substructure.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    @typing.overload
    def erase_bond(self, src: Atom, dst: Atom) -> None:
        """
        Remove a bond from the substructure. The source and destination atoms are
        interchangeable.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :raises ValueError: If the bond is not in the substructure or does not exist.
        
        .. note::
          The parent molecule is not modified by this operation.
        """
    def get_conf(self, conf: int = 0) -> numpy.ndarray:
        """
        Get the coordinates of the atoms in a conformation of the substructure.
        
        :param conf: The index of the conformation to get the coordinates from.
        :returns: The coordinates of the atoms in the substructure, as a 2D array of
          shape ``(num_atoms, 3)``.
        
        .. note::
          The returned array is a copy of the coordinates. To update the coordinates,
          use the :meth:`set_conf` method.
        """
    @typing.overload
    def has_bond(self, src: SubAtom, dst: SubAtom) -> bool:
        """
        Check if two atoms are connected by a bond.
        
        :param src: The source sub-atom of the bond.
        :param dst: The destination sub-atom of the bond.
        :returns: Whether the source and destination atoms are connected by a bond.
        :raises ValueError: If any of the sub-atoms does not belong to the substructure.
        """
    @typing.overload
    def has_bond(self, src: Atom, dst: Atom) -> bool:
        """
        Check if two atoms are connected by a bond.
        
        :param src: The source atom of the bond.
        :param dst: The destination atom of the bond.
        :returns: Whether the source and destination atoms are connected by a bond.
        :raises ValueError: If any of the atoms does not belong to the molecule.
        """
    @typing.overload
    def neighbor(self, src: SubAtom, dst: SubAtom) -> SubNeighbor:
        """
        Get a neighbor of the substructure.
        
        :param src: The source sub-atom of the neighbor.
        :param dst: The destination sub-atom of the neighbor.
        :returns: The neighbor from the source to the destination sub-atom.
        :rtype: SubNeighbor
        :raises ValueError: If the underlying bond does not exist, or any of the
          sub-atoms does not belong to the substructure.
        
        .. seealso::
          :meth:`bond`
        .. note::
          Unlike :meth:`bond`, the returned neighbor is always guaranteed to have
          ``nei.src.id == src.id`` and ``nei.dst.id == dst.id``.
        .. note::
          The returned neighbor is invalidated when the parent molecule is modified, or
          if the substructure is modified.
        """
    @typing.overload
    def neighbor(self, src: Atom, dst: Atom) -> SubNeighbor:
        """
        Get a neighbor of the substructure.
        
        :param src: The source atom of the neighbor.
        :param dst: The destination atom of the neighbor.
        :returns: The neighbor from the source to the destination atom.
        :rtype: SubNeighbor
        :raises ValueError: If the underlying bond does not exist, the source or
          destination atom does not belong to the substructure, or any of the atoms does
          not belong to the same molecule.
        
        .. seealso::
          :meth:`bond`
        .. note::
          Unlike :meth:`bond`, the returned neighbor is always guaranteed to have
          the source and destination atoms in the same order as the arguments.
        .. note::
          The returned neighbor is invalidated when the parent molecule is modified, or
          if the substructure is modified.
        """
    def num_atoms(self) -> int:
        """
        The number of atoms in the substructure. Equivalent to ``len(sub)``.
        """
    def num_bonds(self) -> int:
        """
        The number of bonds in the substructure. Equivalent to ``len(sub.bonds)``.
        """
    def num_confs(self) -> int:
        """
        Get the number of conformations of the substructure.
        """
    def parent_atoms(self) -> list:
        """
        The parent atom indices of the substructure atoms. The indices are guaranteed to
        be unique and in ascending order.
        
        :rtype: list[int]
        
        .. note::
          The returned list is a copy of the internal list, so modifying the list does
          not affect the substructure.
        """
    def parent_bonds(self) -> list:
        """
        The parent bond indices of the substructure bonds. The indices are guaranteed to
        be unique and in ascending order.
        
        :rtype: list[int]
        
        .. note::
          The returned list is a copy of the internal list, so modifying the list does
          not affect the substructure.
        """
    def refresh_bonds(self) -> None:
        """
        Refresh the bonds of the substructure. All bonds between the atoms of the
        substructure are removed, and new bonds are added based on the parent molecule.
        """
    def set_conf(self, coords: typing.Any, conf: int = 0) -> None:
        """
        Set the coordinates of the atoms in a conformation of the substructure.
        
        :param coords: The coordinates of the atoms in the conformation. Must be
          convertible to a numpy array of shape ``(num_atoms, 3)``.
        :param conf: The index of the conformation to set the coordinates to.
        
        .. note::
          The coordinates of the atoms that are *not* in the substructure are not
          affected.
        """
    @property
    def category(self) -> SubstructureCategory:
        """
        :type: SubstructureCategory
        
        The category of the substructure. This is used to categorize the substructure.
        """
    @category.setter
    def category(self, arg1: SubstructureCategory) -> None:
        ...
    @property
    def id(self) -> int:
        """
        :type: int
        
        An integral identifier of the substructure. The identifier is mostly for use in
        the protein residue numbering system.
        
        .. warning::
          This is *not* guaranteed to be unique within the molecule.
        """
    @id.setter
    def id(self, arg1: int) -> None:
        ...
    @property
    def molecule(self) -> Molecule:
        """
        :type: Molecule
        
        The parent molecule of the substructure.
        """
    @property
    def name(self) -> str:
        """
        :type: str
        
        A name of the substructure. This is for user convenience and has no effect on
        the substructure's behavior.
        """
    @name.setter
    def name(self, arg1: str) -> None:
        ...
    @property
    def props(self) -> _ProxyPropertyMap:
        """
        :type: collections.abc.MutableMapping[str, str]
        
        A dictionary-like object to store additional properties of the substructure. The
        keys and values are both strings.
        """
    @props.setter
    def props(self, arg1: _PropertyMap) -> None:
        ...
class SubstructureCategory:
    """
    
    The category of a substructure.
    
    This is used to categorize the substructure. Mainly used for the proteins.
    
    
    Members:
    
      Unknown
    
      Residue
    
      Chain
    """
    Chain: typing.ClassVar[SubstructureCategory]  # value = <SubstructureCategory.Chain: 2>
    Residue: typing.ClassVar[SubstructureCategory]  # value = <SubstructureCategory.Residue: 1>
    Unknown: typing.ClassVar[SubstructureCategory]  # value = <SubstructureCategory.Unknown: 0>
    __members__: typing.ClassVar[dict[str, SubstructureCategory]]  # value = {'Unknown': <SubstructureCategory.Unknown: 0>, 'Residue': <SubstructureCategory.Residue: 1>, 'Chain': <SubstructureCategory.Chain: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SubstructureContainer:
    """
    
    A collection of substructures of a molecule.
    """
    def __contains__(self, idx: int) -> bool:
        ...
    def __delitem__(self, arg0: int) -> None:
        ...
    def __getitem__(self, idx: int) -> ProxySubstructure:
        ...
    def __iter__(self) -> _ProxySubstructureIterator:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Substructure) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: ProxySubstructure) -> None:
        ...
    @typing.overload
    def add(self, atoms: typing.Iterable[Atom | int] | None = None, bonds: typing.Iterable[Bond | int] | None = None, cat: SubstructureCategory = SubstructureCategory.Unknown) -> ProxySubstructure:
        """
        Add a substructure to the collection and return it.
        
        :param collections.abc.Iterable[Atom] atoms: The atoms to include in the
          substructure.
        :param collections.abc.Iterable[Bond] bonds: The bonds to include in the
          substructure.
        :param cat: The category of the substructure.
        :returns: The newly added substructure.
        
        This has three mode of operations:
        
        #. If both ``atoms`` and ``bonds`` are given, a substructure is created with
           the given atoms and bonds. The atoms connected by the bonds will also be
           added to the substructure, even if they are not in the ``atoms`` list.
        #. If only ``atoms`` are given, a substructure is created with the given atoms.
           All bonds between the atoms will also be added to the substructure.
        #. If only ``bonds`` are given, a substructure is created with the given bonds.
           The atoms connected by the bonds will also be added to the substructure.
        #. If neither ``atoms`` nor ``bonds`` are given, an empty substructure is
           created.
        
        .. tip::
          Pass empty list to ``bonds`` to create an atoms-only substructure.
        """
    @typing.overload
    def add(self, idx: int, atoms: typing.Iterable[Atom | int] | None = None, bonds: typing.Iterable[Bond | int] | None = None, cat: SubstructureCategory = SubstructureCategory.Unknown) -> ProxySubstructure:
        """
        Add a substructure to the collection at the given index and return it.
        Effectively invalidates all currently existing substructures.
        
        :param idx: The index of the new substructure. If negative, counts from back to
          front (i.e., the new substructure will be created at
          ``max(0, len(subs) + idx)``). Otherwise, the substructure is added at
          ``min(idx, len(subs))``. This resembles the behavior of Python's
          :meth:`list.insert` method.
        :param collections.abc.Iterable[Atom] atoms: The atoms to include in the
          substructure.
        :param collections.abc.Iterable[Bond] bonds: The bonds to include in the
          substructure.
        :param cat: The category of the substructure.
        :returns: The newly added substructure.
        
        This has three mode of operations:
        
        #. If both ``atoms`` and ``bonds`` are given, a substructure is created with
           the given atoms and bonds. The atoms connected by the bonds will also be
           added to the substructure, even if they are not in the ``atoms`` list.
        #. If only ``atoms`` are given, a substructure is created with the given atoms.
           All bonds between the atoms will also be added to the substructure.
        #. If only ``bonds`` are given, a substructure is created with the given bonds.
           The atoms connected by the bonds will also be added to the substructure.
        #. If neither ``atoms`` nor ``bonds`` are given, an empty substructure is
           created.
        
        .. tip::
          Pass empty list to ``bonds`` to create an atoms-only substructure.
        """
    @typing.overload
    def append(self, other: Substructure) -> None:
        """
        Add a substructure to the collection.
        
        :param Substructure other: The substructure to add.
        
        .. note::
          The given substructure is copied to the collection.
        """
    @typing.overload
    def append(self, other: ProxySubstructure) -> None:
        """
        Add a substructure to the collection.
        
        :param ProxySubstructure other: The substructure to add.
        
        .. note::
          The given substructure is copied to the collection.
        """
    def clear(self) -> None:
        """
        Remove all substructures from the collection. Effectively invalidates all
        currently existing substructures.
        """
    @typing.overload
    def insert(self, idx: int, other: Substructure) -> None:
        """
        Add a substructure to the collection at the given index. Effectively invalidates
        all currently existing substructures.
        
        :param idx: The index of the new substructure. If negative, counts from back to
          front (i.e., the new substructure will be created at
          ``max(0, len(subs) + idx)``). Otherwise, the substructure is added at
          ``min(idx, len(subs))``. This resembles the behavior of Python's
          :meth:`list.insert` method.
        :param Substructure other: The substructure to add.
        
        .. note::
          The given substructure is copied to the collection, so modifying the given
          substructure does not affect the collection.
        """
    @typing.overload
    def insert(self, idx: int, other: ProxySubstructure) -> None:
        """
        Add a substructure to the collection at the given index. Effectively invalidates
        all currently existing substructures.
        
        :param idx: The index of the new substructure. If negative, counts from back to
          front (i.e., the new substructure will be created at
          ``max(0, len(subs) + idx)``). Otherwise, the substructure is added at
          ``min(idx, len(subs))``. This resembles the behavior of Python's
          :meth:`list.insert` method.
        :param ProxySubstructure other: The substructure to add.
        
        .. note::
          The given substructure is copied to the collection, so modifying the given
          substructure does not affect the collection.
        """
    def pop(self, idx: int | None = None) -> Substructure:
        """
        Remove a substructure from the collection and return it.
        
        :param idx: The index of the substructure to remove. If not given, removes the
          last substructure.
        """
class _AtomIterator:
    def __iter__(self) -> _AtomIterator:
        ...
    def __next__(self) -> Atom:
        ...
class _BondIterator:
    def __iter__(self) -> _BondIterator:
        ...
    def __next__(self) -> Bond:
        ...
class _BondsWrapper:
    @typing.overload
    def __contains__(self, idx: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: Bond) -> bool:
        ...
    def __getitem__(self, idx: int) -> Bond:
        ...
    def __iter__(self) -> _BondIterator:
        ...
    def __len__(self) -> int:
        ...
class _ConformerIterator:
    def __iter__(self) -> _ConformerIterator:
        ...
    def __next__(self) -> numpy.ndarray:
        ...
class _IsotopeList:
    def __getitem__(self, index: int) -> Isotope:
        ...
    def __iter__(self) -> typing.Iterator[Isotope]:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
class _NeighborIterator:
    def __iter__(self) -> _NeighborIterator:
        ...
    def __next__(self) -> Neighbor:
        ...
class _PropertyMap:
    def __contains__(self, arg0: str) -> bool:
        ...
    def __copy__(self) -> _PropertyMap:
        ...
    def __deepcopy__(self, memo: dict) -> _PropertyMap:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> str:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: _ProxyPropertyMap) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: dict) -> None:
        ...
    def __iter__(self) -> _PropertyMapKeys:
        ...
    def __len__(self) -> int:
        ...
    def __setitem__(self, arg0: str, arg1: str) -> None:
        ...
    def clear(self) -> None:
        ...
    def copy(self) -> _PropertyMap:
        ...
    @typing.overload
    def get(self, arg0: str) -> str:
        ...
    @typing.overload
    def get(self, key: str, default: str) -> str:
        ...
    def items(self) -> _PropertyMapItems:
        ...
    def keys(self) -> _PropertyMapKeys:
        ...
    @typing.overload
    def pop(self, arg0: str) -> str:
        ...
    @typing.overload
    def pop(self, key: str, default: str) -> str:
        ...
    def popitem(self) -> tuple[str, str]:
        ...
    def setdefault(self, arg0: str, arg1: str) -> str:
        ...
    @typing.overload
    def update(self, arg0: dict) -> None:
        ...
    @typing.overload
    def update(self, **kwargs) -> None:
        ...
    @typing.overload
    def update(self, arg0: typing.Iterable[tuple[str, str]]) -> None:
        ...
    def values(self) -> _PropertyMapValues:
        ...
class _PropertyMapItems:
    def __iter__(self) -> _PropertyMapItems:
        ...
    def __next__(self) -> tuple[str, str]:
        ...
class _PropertyMapKeys:
    def __iter__(self) -> _PropertyMapKeys:
        ...
    def __next__(self) -> str:
        ...
class _PropertyMapValues:
    def __iter__(self) -> _PropertyMapValues:
        ...
    def __next__(self) -> str:
        ...
class _ProxyPropertyMap:
    def __contains__(self, arg0: str) -> bool:
        ...
    def __copy__(self) -> _PropertyMap:
        ...
    def __deepcopy__(self, memo: dict) -> _PropertyMap:
        ...
    def __delitem__(self, arg0: str) -> None:
        ...
    def __getitem__(self, arg0: str) -> str:
        ...
    def __iter__(self) -> _ProxyPropertyMapKeys:
        ...
    def __len__(self) -> int:
        ...
    def __setitem__(self, arg0: str, arg1: str) -> None:
        ...
    def clear(self) -> None:
        ...
    def copy(self) -> _PropertyMap:
        ...
    @typing.overload
    def get(self, arg0: str) -> str:
        ...
    @typing.overload
    def get(self, key: str, default: str) -> str:
        ...
    def items(self) -> _ProxyPropertyMapItems:
        ...
    def keys(self) -> _ProxyPropertyMapKeys:
        ...
    @typing.overload
    def pop(self, arg0: str) -> str:
        ...
    @typing.overload
    def pop(self, key: str, default: str) -> str:
        ...
    def popitem(self) -> tuple[str, str]:
        ...
    def setdefault(self, arg0: str, arg1: str) -> str:
        ...
    @typing.overload
    def update(self, arg0: dict) -> None:
        ...
    @typing.overload
    def update(self, **kwargs) -> None:
        ...
    @typing.overload
    def update(self, arg0: typing.Iterable[tuple[str, str]]) -> None:
        ...
    def values(self) -> _ProxyPropertyMapValues:
        ...
class _ProxyPropertyMapItems:
    def __iter__(self) -> _ProxyPropertyMapItems:
        ...
    def __next__(self) -> tuple[str, str]:
        ...
class _ProxyPropertyMapKeys:
    def __iter__(self) -> _ProxyPropertyMapKeys:
        ...
    def __next__(self) -> str:
        ...
class _ProxyPropertyMapValues:
    def __iter__(self) -> _ProxyPropertyMapValues:
        ...
    def __next__(self) -> str:
        ...
class _ProxySubAtomIterator:
    def __iter__(self) -> _ProxySubAtomIterator:
        ...
    def __next__(self) -> ProxySubAtom:
        ...
class _ProxySubBondIterator:
    def __iter__(self) -> _ProxySubBondIterator:
        ...
    def __next__(self) -> ProxySubBond:
        ...
class _ProxySubBonds:
    @typing.overload
    def __contains__(self, idx: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: ProxySubBond) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: Bond) -> bool:
        ...
    @typing.overload
    def __getitem__(self, idx: int) -> ProxySubBond:
        ...
    @typing.overload
    def __getitem__(self, bond: Bond) -> ProxySubBond:
        ...
    def __iter__(self) -> _ProxySubBondIterator:
        ...
    def __len__(self) -> int:
        ...
class _ProxySubConformersIterator:
    def __iter__(self) -> _ProxySubConformersIterator:
        ...
    def __next__(self) -> numpy.ndarray:
        ...
class _ProxySubNeighborIterator:
    def __iter__(self) -> _ProxySubNeighborIterator:
        ...
    def __next__(self) -> ProxySubNeighbor:
        ...
class _ProxySubstructureIterator:
    def __iter__(self) -> _ProxySubstructureIterator:
        ...
    def __next__(self) -> ProxySubstructure:
        ...
class _SubAtomIterator:
    def __iter__(self) -> _SubAtomIterator:
        ...
    def __next__(self) -> SubAtom:
        ...
class _SubBondIterator:
    def __iter__(self) -> _SubBondIterator:
        ...
    def __next__(self) -> SubBond:
        ...
class _SubBonds:
    """
    
    A collection of bonds in a substructure.
    
    This is a read-only collection of bonds in a substructure. The collection is
    invalidated when the parent molecule is modified, or if the substructure is
    modified.
    """
    @typing.overload
    def __contains__(self, idx: int) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: SubBond) -> bool:
        ...
    @typing.overload
    def __contains__(self, arg0: Bond) -> bool:
        ...
    @typing.overload
    def __getitem__(self, idx: int) -> SubBond:
        ...
    @typing.overload
    def __getitem__(self, bond: Bond) -> SubBond:
        ...
    def __iter__(self) -> _SubBondIterator:
        ...
    def __len__(self) -> int:
        ...
class _SubConformersIterator:
    def __iter__(self) -> _SubConformersIterator:
        ...
    def __next__(self) -> numpy.ndarray:
        ...
class _SubNeighborIterator:
    def __iter__(self) -> _SubNeighborIterator:
        ...
    def __next__(self) -> SubNeighbor:
        ...
def _py_array_cast_test_helper(obj: typing.Any, kind: str) -> numpy.ndarray:
    ...
def _random_test_helper(arg0: int) -> int:
    ...
def seed_thread(seed: int | None = None) -> None:
    """
    Set the seed of random number generator for the current thread.
    
    :param seed: The seed to set. If not specified, a random seed is chosen.
    """
periodic_table: PeriodicTable  # value = <nuri.core._core.PeriodicTable object>
