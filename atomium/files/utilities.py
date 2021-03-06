"""This module contains various utility functions for dealing with files."""

from requests import get
from .pdbstring2pdbdict import pdb_string_to_pdb_dict
from .pdbdict2pdb import pdb_dict_to_pdb
from .xyzstring2xyzdict import xyz_string_to_xyz_dict
from .xyzdict2xyz import xyz_dict_to_xyz

def string_from_file(path):
    """Opens a file from the given path and returns the contents as a string.

    :param str path: The path to the file.
    :rtype: ``str``"""

    with open(path) as f:
        return f.read()


def fetch_string(code, pdbe=False):
    """Gets a the filestring of a PDB from the RCSB web services.

    :param str code: The PDB code to fetch.
    :param bool pdbe: If ``True``, the PDB will instead be fetched from PDBe.
    :raises TypeError: if the code is not a string.
    :raises ValueError: if the code is not four caracters long.
    :rtype: ``str``"""

    if not isinstance(code, str):
        raise TypeError("PDB code {} is not string".format(code))
    if len(code) != 4:
        raise ValueError("PDB code {} is not of length 4".format(code))
    url = "https://files.rcsb.org/view/{}.pdb"
    if pdbe:
        url = "https://www.ebi.ac.uk/pdbe/entry-files/pdb{}.ent"
    response = get(url.format(code.lower()))
    if response.status_code == 200:
        return response.text


def string_to_lines(s, width=None):
    """Takes a filestring and turns it into a ``list`` of ``str`` lines. You can
    pad these out to a fixed number of characters if you want.

    :param str s: The filestring.
    :param int width: if given, the lines will be padded out with spaces to\
    this width.
    :rtype: ``list``"""

    lines = [line.replace("\r", "") for line in s.split("\n") if line]
    if width:
        lines = [line.ljust(width) for line in lines]
    return lines


def pdb_data_from_file(path):
    """Opens a .pdb file at the specified path and creates a
    data dictionary from it.

    :param str path: The path to open.
    :rtype: ``dict``"""

    filestring = string_from_file(path)
    return pdb_string_to_pdb_dict(filestring)


def fetch_data(code, **kwargs):
    """Gets a PDB data dictionary from the RCSB web services.

    :param str code: The PDB code to fetch.
    :param bool pdbe: If ``True``, the PDB will instead be fetched from PDBe.
    :rtype: ``dict``"""

    filestring = fetch_string(code, **kwargs)
    if filestring is not None:
        return pdb_string_to_pdb_dict(filestring)


def pdb_from_file(path):
    """Opens a .pdb file at the specified path and creates a :py:class:`.Pdb`
    from it.

    :param str path: The path to open.
    :rtype: ``Pdb``"""

    pdb_dict = pdb_data_from_file(path)
    return pdb_dict_to_pdb(pdb_dict)


def fetch(code, **kwargs):
    """Gets a :py:class:`.Pdb` from the RCSB web services.

    :param str code: The PDB code to fetch.
    :param bool pdbe: If ``True``, the PDB will instead be fetched from PDBe.
    :rtype: ``PdbFile``"""

    pdb_dict = fetch_data(code, **kwargs)
    if pdb_dict is not None:
        return pdb_dict_to_pdb(pdb_dict)


def xyz_data_from_file(path):
    """Opens a .xyz file at the specified path and creates a
    data dictionary from it.

    :param str path: The path to open.
    :rtype: ``dict``"""

    filestring = string_from_file(path)
    return xyz_string_to_xyz_dict(filestring)


def xyz_from_file(path):
    """Opens a .xyz file at the specified path and creates a :py:class:`.Pdb`
    from it.

    :param str path: The path to open.
    :rtype: ``Pdb``"""

    xyz_dict = xyz_data_from_file(path)
    return xyz_dict_to_xyz(xyz_dict)


def lines_to_string(lines):
    """Creates a single string from a list of record strings.

    :param list lines: The list of lines to join.
    :rtype: ``str``"""

    return "\n".join(lines)


def string_to_file(string, path):
    """Saves a string to a given path as a file.

    :param str string: The string to save.
    :param str path: The file to save it in."""

    with open(path, "w") as f:
        f.write(string)
