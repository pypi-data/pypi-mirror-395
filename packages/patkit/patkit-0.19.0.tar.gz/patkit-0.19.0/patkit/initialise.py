#!/usr/bin/env python3
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
Initialisation routines for PATKIT.
"""

import sys
from logging import Logger
from pathlib import Path

from patkit.annotations import add_peaks
from patkit.configuration import (
    ConfigPaths,
    Configuration,
)
from patkit.constants import (
    PatkitConfigFile,
    PatkitSuffix,
    SourceSuffix,
)
from patkit.data_loader import load_data
from patkit.data_processor import (
    process_modalities, process_statistics_in_recordings)
from patkit.data_structures import Session
from patkit.metrics import (
    add_aggregate_images,
    add_distance_matrices,
    add_intensity,
    add_pd,
    add_spline_metric,
    downsample_metrics_in_session,
)
from patkit.modalities import (
    RawUltrasound, Splines
)
from patkit.get_modality_types import get_modality_types
from patkit.utility_functions import (
    log_elapsed_time, set_logging_level
)


def get_config_dir(path: Path) -> Path:
    """
    Get configuration directory from a Path which is a file.

    As a side effect will exit the program if the file type can not be handled.

    Parameters
    ----------
    path : Path
        Path to a file.

    Returns
    -------
    Path
        Path of the configuration directory.
    """
    match path.suffix:
        case SourceSuffix.TEXTGRID:
            print("Direct TextGrid loading planned for "
                    "implementation in 0.18.")
            sys.exit()
        case SourceSuffix.WAV:
            print("Direct wav loading planned for "
                    "implementation in 0.18.")
            sys.exit()
        case SourceSuffix.AAA_ULTRA:
            print("Direct AAA ultrasound data loading planned for "
                    "implementation by 1.0.")
            sys.exit()
        case PatkitSuffix.CONFIG if path.name == PatkitConfigFile.MANIFEST:
            print("Loading based on a manifest file planned for "
                    "implementation in 0.18.")
            sys.exit()
        case PatkitSuffix.CONFIG if path.name == PatkitConfigFile.SESSION:
            path = path.parent
        case PatkitSuffix.CONFIG if path.name == PatkitConfigFile.SIMULATION:
            path = path.parent
        case PatkitSuffix.META:
            print("Loading based of a single saved trial planned for "
                    "a later release. For now loading the whole directory.")
            path = path.parent
        case _:
            message = (
                f"Unrecognised file type {path.suffix}.\n"
                f"Don't know how to load data from {path}."
            )
            print(message)
            sys.exit()
    return path


def initialise_config(
    path: Path,
    require_data: bool = False,
    require_gui: bool = False,
    require_publish: bool = False,
    require_simulation: bool = False,
    logging_level: int | None = None,
) -> tuple[Configuration, Logger]:
    """
    Initialise PATKIT configuration and set logging level.

    Configuration file's existence will be checked according to the flag
    arguments.

    Parameters
    ----------
    path : Path
        Path to the configuration directory or a file that PATKIT can handle.
    require_data : bool, optional
        Do we need data configuration, by default False. This can come in the
        form of either a `patkit_data.yaml` file or a manifest or a session
        `.meta`. The PATKIT will try to back track the latter two to the
        `patkit_data.yaml`. 
    require_gui : bool, optional
        If the annotator GUI is going to be opened, we should have
        `patkit_gui.yaml`, by default False
    require_publish : bool, optional
        If we are running a publish script, `patkit_publish.yaml`, by default
        False
    require_simulation : bool, optional
        If this is a simulation run, we need `patkit_simulation.yaml`, by
        default False
    logging_level : int | None, optional
        Logging level, by default None

    Returns
    -------
    [Configuration, Logger]
        Configuration for PATKIT and the logger for use with other functions in
        `initialise.py`.
    """
    logger = set_logging_level(logging_level)

    # TODO 0.20 check if this deals correctly with symlinks
    path = path.resolve()
    if not path.exists():
        message = (
            f"Path does not exist: {path}."
        )
        logger.error(message)
        sys.exit()
    elif path.is_file():
        path = get_config_dir(path)
    elif not path.is_dir():
        message = (
            f"Unknown path type: {path}."
        )
        logger.error(message)
        sys.exit()

    config_paths = ConfigPaths(path)
    fail = False

    if require_data and config_paths.data_config is None:
        print(
            f"Data configuration file not found in {path}. "
            f"Correct file name is {PatkitConfigFile.DATA}."
        )
        fail = True
    if require_gui and config_paths.gui_config is None:
        print(
            f"GUI configuration file not found in {path}. "
            f"Correct file name is {PatkitConfigFile.GUI}."
        )
        fail = True
    if require_publish and config_paths.publish_config is None:
        print(
            f"Publish configuration file not found in {path}. "
            f"Correct file name is {PatkitConfigFile.PUBLISH}."
        )
        fail = True

    if require_simulation and config_paths.simulation_config is None:
        print(
            f"Simulation configuration file not found in {path}. "
            f"Correct file name is {PatkitConfigFile.SIMULATION}."
        )
        fail = True

    if fail:
        sys.exit()

    config = Configuration(config_paths)
    return config, logger


def initialise_patkit(
    config: Configuration,
    logger: Logger,
) -> Session:
    """
    Initialise the basic structures for running patkit.

    This sets up the argument parser, reads the basic configuration, and loads
    the recorded and saved data into a Session. To initialise derived data run
    `add_derived_data`.

    Parameters
    ----------
    path : Path
        Path to load data from.
    config_file : Path | str | None
        Path to load configuration from, by default None.
    exclusion_file : Path | str | None
        Path to exclusion list, by default None.
    logging_level : int | None
        Logging level, by default None.

    Returns
    -------
    Session
        Data in a Session.
    """
    session = None
    if config.data_config:
        logger.info("Loading data.")
        session = load_data(config)
        log_elapsed_time(logger)

        # TODO 0.20: resolve this
        # exclusion_list = None
        # if exclusion_file is not None:
        #     exclusion_file = path_from_name(exclusion_file)
        #     exclusion_list = load_exclusion_list(exclusion_file)
        # apply_exclusion_list(session, exclusion_list=exclusion_list)
        # log_elapsed_time(logger)

        add_derived_data(session=session, config=config, logger=logger)
        log_elapsed_time(logger)

    return session


def add_derived_data(
    session: Session,
    config: Configuration,
    logger: Logger,
) -> None:
    """
    Add derived data to the Session according to the Configuration.

    NOTE: This function will not delete existing data unless it is being
    replaced (and the corresponding `replace` parameter is `True`). This means
    that already existing derived data is retained.

    Added data types include Modalities, Statistics and Annotations.

    Parameters
    ----------
    session : Session
        The Session to add derived data to.
    config : Configuration
        The configuration parameters to use in deriving the new derived data.
    logger : Logger
        The logger is passed as an argument since the initialise module is the
        one responsible for setting it up.

    Returns
    -------
    None
    """
    data_run_config = config.data_config

    # TODO 0.21: Automate most of this for arbitrary Modalities.
    modality_operation_dict = {}
    if data_run_config.intensity_arguments:
        intensity_arguments = data_run_config.intensity_arguments
        modality_types = get_modality_types(intensity_arguments.modalities)
        modality_operation_dict["Intensity"] = (
            add_intensity,
            modality_types,
            intensity_arguments.model_dump(exclude=['modalities']),
        )

    if data_run_config.pd_arguments:
        pd_arguments = data_run_config.pd_arguments
        modality_operation_dict["PD"] = (
            add_pd,
            [RawUltrasound],
            pd_arguments.model_dump(),
        )

    if data_run_config.aggregate_image_arguments:
        aggregate_image_arguments = data_run_config.aggregate_image_arguments
        modality_operation_dict["AggregateImage"] = (
            add_aggregate_images,
            [RawUltrasound],
            aggregate_image_arguments.model_dump(),
        )

    if data_run_config.spline_metric_arguments:
        spline_metric_args = data_run_config.spline_metric_arguments
        modality_operation_dict["SplineMetric"] = (
            add_spline_metric,
            [Splines],
            spline_metric_args.model_dump(),
        )

    process_modalities(
        recordings=session, processing_functions=modality_operation_dict)

    statistic_operation_dict = {}
    if data_run_config.distance_matrix_arguments:
        distance_matrix_arguments = data_run_config.distance_matrix_arguments
        statistic_operation_dict["DistanceMatrix"] = (
            add_distance_matrices,
            ["AggregateImage mean on RawUltrasound"],
            distance_matrix_arguments.model_dump(),
        )

    process_statistics_in_recordings(
        session=session, processing_functions=statistic_operation_dict
    )

    if data_run_config.downsample:
        downsample_metrics_in_session(
            recording_session=session, data_run_config=data_run_config
        )

    if data_run_config.peaks:
        modality_pattern = data_run_config.peaks.modality_pattern
        for recording in session:
            if recording.excluded:
                logger.info(
                    "Recording excluded from peak finding: %s",
                    recording.name)
                continue
            for modality_name in recording:
                if modality_pattern.search(modality_name):
                    add_peaks(
                        recording[modality_name],
                        config.data_config.peaks,
                    )
