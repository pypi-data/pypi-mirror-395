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
PATKIT command line commands.
"""

from pathlib import Path

import click

from patkit.initialise import initialise_config, initialise_patkit
from patkit.qt_annotator import run_annotator
from patkit.interpreter import run_interpreter
from patkit.simulation import run_simulations
from patkit.simulation.simulate import setup_contours_comparisons_soundpairs


@click.command(name="open")
@click.argument(
    "path",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=True, path_type=Path
    ),
)
def open_in_annotator(
        path: Path
) -> None:
    """
    Open the PATH in the annotator GUI.

    \b
    PATH to the data - maybe be a file or a directory.
    """
    config, logger = initialise_config(
        path=path, require_gui=True, require_data=True)
    session = initialise_patkit(config=config, logger=logger)
    run_annotator(session=session, config=config)


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, file_okay=True), )
def interact(
        path: Path
):
    """
    Open the PATH in interactive commandline mode.

    \b
    PATH to the data - maybe be a file or a directory.
    """
    config, logger = initialise_config(path=path, require_data=True)
    configuration, session = initialise_patkit(
        config=config,
        logger=logger
    )
    run_interpreter(session=session, configuration=configuration)


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, file_okay=True), )
def publish(path: Path):
    """
    Publish plots from the data in PATH.

    \b
    PATH to the data - maybe be a file or a directory.

    NOT IMPLEMENTED YET.
    """
    config, logger = initialise_config(path=path, require_publish=True)
    session = initialise_patkit(
        config=config, logger=logger
    )
    print(
        f"Loaded {session} but rest of publish is scheduled for "
        f"implementation in a later version."
    )


@click.command()
@click.argument(
    "path",
    type=click.Path(dir_okay=True, file_okay=True, path_type=Path),
)
def simulate(path: Path):
    """
    Run a simulation experiment.

    \b
    PATH to a `.yaml` file which contains the parameters for running the
    simulation.
    """
    # TODO 0.20: simulate command will not work if given the actual config file
    # instead of containing dir
    config, _ = initialise_config(path=path, require_simulation=True)
    contours, comparisons, sound_pairs = setup_contours_comparisons_soundpairs(
        sim_configuration=config.simulation_config)
    run_simulations(
        sim_configuration=config.simulation_config,
        contours=contours,
        comparisons=comparisons,
        sound_pairs=sound_pairs
    )
