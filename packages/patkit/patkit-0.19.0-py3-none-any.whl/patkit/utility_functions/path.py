#
# Copyright (c) 2019-2025
# Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
#
# This file is part of the Phonetic Analysis ToolKIT
# (see https://github.com/giuthas/patkit/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.md. They can also be found in
# citations.bib in BibTeX format.
#
"""
Path helper functions.
"""

from pathlib import Path


def path_from_name(filename: str | Path | None) -> Path:
    """
    Ensure the output is a Path instance.

    Parameters
    ----------
    filename : str | Path | None
        The filename can be either string, Path or None. None is interpreted as
        current directory.
    Returns
    -------
    Path
        Output is always a Path instance. If None is passed as filename the
        return value will be `Path('.')`.
    """
    if filename is None:
        return Path(".")
    if not isinstance(filename, Path):
        return Path(filename)
    return filename


def stem_path(path: Path) -> Path:
    """
    Return the path without suffixes.

    Parameters
    ----------
    path : Path
        A filepath.

    Returns
    -------
    Path
        The filepath with suffixes removed.
    """
    name = path.name
    path = path.parent
    name = name.split('.')[0]
    return path/name
