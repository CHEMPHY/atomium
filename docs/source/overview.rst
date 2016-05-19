Overview
--------

Creating Pdb objects
~~~~~~~~~~~~~~~~~~~~

There are two main ways to create a Pdb object from a PDB file. The first is
from a local PDB file:

    >>> import molecupy
    >>> pdb = molecupy.get_pdb_from_file("path/to/file.pdb")

This is the quickest way, though it is not always convenient to store PDB files
locally. The second way is to fetch the PDB file over the internet:

    >>> import molecupy
    >>> pdb = molecup.get_pdb_remotely("1LOL")

This takes longer, but it means you can access any published PDB file without
needing to manually download them first.

However the text of the PDB file is obtained, the process of parsing it is
always the same:

    1. First a :py:class:`.PdbFile` object is created, which is a
    representation of the file itself. This is essentially a list of records,
    with methods for getting records of a certain name.

    2. This is used to make a :py:class:`.PdbDataFile` object. This is the
    object which extracts the data from the file, and is essentially an
    unstructured list of values.

    3. This is used to make a :py:class:`.Pdb` object, by using the values in
    the data file to create a user-friendly handle to the information.


Accessing Pdb properties
~~~~~~~~~~~~~~~~~~~~~~~~

Aside from structural information, PDB files also contain many other pieces of
information about the file, such as its title, experimental techniques used to
create it, publication information etc.

    >>> pdb.pdb_code
    '1LOL'
    >>> pdb.deposition_date
    datetime.date(2002, 5, 6)
    >>> pdb.authors
    ['N.WU', 'E.F.PAI']

molecuPy is a reasonably forgiving parser. If records are missing from the PDB
file - even records which the PDB specification insists *must* be present - the
file will still parse, and any missing properties will just be set to ``None``
or an empty list, whichever is appropriate.


Pdb Models
~~~~~~~~~~

The heart of a Pdb is its model. A :py:class:`.PdbModel` represents the
structure contained in that PDB file, and is the environment in which all other
molecules and structures are based.

All Pdb objects have a list of models, which in most cases will contain a single
model. Structures created from NMR will often have multiple models - each
containing the same structures but with slightly different coordinates. For ease
of use, all Pdb objects also have a ``model`` attribute, which points to the
first model in the list.

    >>> pdb.models
    [<Model (3431 atoms)>]
    >>> pdb.model
    <Model (3431 atoms)>

The PdbModel class is an atomic structure (i.e. it inherits from
:py:class:`.AtomicStructure`) which means you can get certain atomic properties
directly from the model, such as mass, empirical formula, and the atoms
themselves:

    >>> pdb.model.get_mass()
    20630.8656
    >>> pdb.model.get_empirical_formula()
    Counter({'C': 2039, 'O': 803, 'N': 565, 'S': 22, 'P': 2})
    >>> len(pdb.model.atoms)
    3431
    >>> pdb.model.get_atoms_by_element("P")
    {<Atom 3200 (P)>, <Atom 3230 (P)>}
    >>> pdb.get_atom_by_id(23)
    <Atom 23 (N)>


The chains and small molecules of the model exist as sets, and can be queried
by ID or name:

    >>> pdb.model.chains
    {<Chain B (214 residues)>, <Chain A (204 residues)>}
    >>> len(pdb.model.small_molecules) # Includes solvent molecules
    184
    >>> pdb.model.get_chain_by_id("B")
    <Chain B (214 residues)>
    >>> pdb.model.get_small_molecules_by_name("XMP")
    {<SmallMolecule (XMP)>, <SmallMolecule (XMP)>}


.. note::

   PDB files are not always perfect representations of the real molecular
   structures they are created from. Sometimes there are missing atoms, and
   sometimes there are missing residues. Future versions of molecuPy will flag
   these and maybe even fill them in, but for now simply bear in mind that there
   may be missing atoms and disconnected chains.


Pdb Chains
~~~~~~~~~~

A :py:class:`.PdbChain` object is an ordered sequence of Residue objects, and
they are the macromolecular structures which constitute the bulk of the model.

    >>> pdb.model.get_chain_by_id("A")
    <Chain A (204 residues)>
    >>> pdb.model.get_chain_by_id("A").chain_id
    'A'
    >>> pdb.model.get_chain_by_id("A").residues[0]
    <Residue (VAL)>

Chains inherit from :py:class:`.ResiduicStructure` and
:py:class:`.ResiduicSequence` and so have methods for retrieving residues:

    >>> pdb.model.get_chain_by_id("A").get_residue_by_id(23)
    <Residue (ASN)>
    >>> pdb.model.get_chain_by_id("A").get_residue_by_name("ASP")
    <Residue (ASP)>
    >>> pdb.model.get_chain_by_id("A").get_residues_by_name("ASN")
    {<Residue (ASN)>, <Residue (ASN)>, <Residue (ASN)>, <Residue (ASN)>, <Residu
    e (ASN)>, <Residue (ASN)>}

Like pretty much everything else in molecuPy, chains are ultimately atomic
structures, and have the usual atomic structure methods for getting mass,
retrieving atoms etc.

The :py:class:`.PdbResidue` objects themselves are also atomic structures, and behave very
similar to small molecules.


Pdb Small Molecules
~~~~~~~~~~~~~~~~~~~

Many PDB files also contain non-macromolecular objects, such as ligands, and
solvent molecules. In molecuPy, these are represented as
:py:class:`.PdbSmallMolecule` objects.

There's not a great deal to be said about small molecules. They are atomic
structures, so you can get their mass, get atoms by name/ID etc.

    >>> pdb.model.get_small_molecule_by_name("BU2")
    <SmallMolecule (BU2)>
    >>> pdb.model.get_small_molecule_by_name("XMP").atoms
    {<Atom 3240 (C)>, <Atom 3241 (N)>, <Atom 3242 (N)>, <Atom 3243 (C)>, <Atom 3
    244 (O)>, <Atom 3245 (C)>, <Atom 3246 (O)>, <Atom 3247 (C)>, <Atom 3248 (N)>
    , <Atom 3249 (C)>, <Atom 3250 (C)>, <Atom 3251 (O)>, <Atom 3252 (C)>, <Atom
    3253 (O)>, <Atom 3230 (P)>, <Atom 3231 (O)>, <Atom 3232 (O)>, <Atom 3233 (O)
    >, <Atom 3234 (O)>, <Atom 3235 (C)>, <Atom 3236 (C)>, <Atom 3237 (O)>, <Atom
     3238 (C)>, <Atom 3239 (N)>}
    >>> pdb.model.get_small_molecule_by_name("XMP").get_atom_by_id(3252)
    <Atom 3252 (C)>


Pdb Atoms
~~~~~~~~~

Pdb structures - like everything else in the universe really - are ultimately
collections of Atom - :py:class:`.PdbAtom` - objects. They possess a few key
properties from which much of everything else is created:

    >>> pdb.model.get_atom_by_id(28)
    <Atom 28 (C)>
    >>> pdb.model.get_atom_by_id(28).atom_id
    28
    >>> pdb.model.get_atom_by_id(28).atom_name
    'CB'
    >>> pdb.model.get_atom_by_id(28).element
    'C'
    >>> pdb.model.get_atom_by_id(28).get_mass()
    12.0107

The distance between any two atoms can be calculated easily:

    >>> atom1 = pdb.model.get_atom_by_id(23)
    >>> atom2 = pdb.model.get_atom_by_id(28)
    >>> atom1.distance_to(atom2)
    7.931296047935668