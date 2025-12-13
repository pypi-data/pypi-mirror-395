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
Calculate and add Intensity to a Recording.
"""

import logging

import numpy as np

from patkit.data_structures import (
    FileInformation, Modality, ModalityData, Recording
)
from patkit.modalities import RawUltrasound
from .intensity import Intensity, IntensityParameters

_logger = logging.getLogger('patkit.intensity')


def calculate_intensity_metric(
    parent_modality: Modality
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculate overall intensity on the Modality as a function of time.

    Currently works on video Modalities, but not audio.

    Parameters
    ----------
    parent_modality : Modality
        Modality containing grayscale data.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Overall intensity as a function of time and the timevector.
    """
    data = parent_modality.data
    data = data.reshape(data.shape[0], -1)
    return np.sum(data, axis=1), parent_modality.timevector


def create_intensities(
        parent_modality: Modality,
        to_be_computed: dict[str, IntensityParameters]
) -> list[Intensity]:
    """
    Create Intensity Modalities for each of the entries in `to_be_computed`.

    Parameters
    ----------
    parent_modality : Modality
        The Modality the Intensities will be computed on. 
    to_be_computed : dict[str, IntensityParameters]
        The parameters for the Intensities to be created.

    Returns
    -------
    list[Intensity]
        The created Intensity Modalities.

    Raises
    ------
    NotImplementedError
        If run on anything but RawUltrasound at the moment.
    """

    if not isinstance(parent_modality, RawUltrasound):
        raise NotImplementedError(
            "Calculating intensity for anything else than RawUltrasound is "
            "not yet implemented."
        )

    sampling_rate = parent_modality.sampling_rate

    intensities = []
    for item in to_be_computed:
        intensity_data, timevector = calculate_intensity_metric(
            parent_modality=parent_modality)
        modality_data = ModalityData(
            data=intensity_data,
            sampling_rate=sampling_rate,
            timevector=timevector
        )

        if parent_modality.patkit_path:
            file_info = FileInformation(
                patkit_path=parent_modality.patkit_path)
        else:
            file_info = FileInformation()
        new_intensity = Intensity(
                container=parent_modality.container,
                metadata=to_be_computed[item],
                file_info=file_info,
                parsed_data=modality_data,
        )
        intensities.append(new_intensity)
    return intensities


def add_intensity(
    recording: Recording,
    modality: Modality,
    preload: bool = True,
    release_data_memory: bool = False,
) -> None:
    """
    Calculate Intensity and add it to the Recording.

    Parameters
    ----------
    recording : Recording
        The Recording the new Intensity will be added to.
    modality : Modality
        The Modality the new Intensity will be calculated on.
    preload : bool, optional
        Should the Intensity be calculated on creation (preloaded) or only on
        access, by default True
    release_data_memory : bool, optional
        Should the data attribute of the Modality be set to None after use, by
        default True

    Raises
    ------
    NotImplementedError
        Running with preload set to False has not yet been implemented.
    """
    if not preload:
        message = ("Looks like somebody is trying to leave Intensity to be "
                   "calculated on the fly. This is not yet supported.")
        raise NotImplementedError(message)

    if recording.excluded:
        _logger.info(
            "Recording %s excluded from processing.", recording.basename)
    elif not modality.__name__ in recording:
        _logger.info("Data modality '%s' not found in recording: %s.",
                     modality.__name__, recording.basename)
    else:
        all_requested = Intensity.get_names_and_meta(
            modality, release_data_memory)
        missing_keys = set(all_requested).difference(
            recording.keys())
        to_be_computed = dict((key, value) for key,
                              value in all_requested.items()
                              if key in missing_keys)

        data_modality = recording[modality.__name__]

        if to_be_computed:
            intensities = create_intensities(data_modality, to_be_computed)

            for intensity in intensities:
                recording.add_modality(intensity)
                _logger.info("Added '%s' to recording: %s.",
                             intensity.name, recording.basename)
        else:
            _logger.info(
                "Nothing to compute in Intensity for Recording: %s.",
                recording.basename)
