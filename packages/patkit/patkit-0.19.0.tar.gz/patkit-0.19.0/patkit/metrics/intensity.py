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
Modality for Intensity and its parameter class.
"""

import logging

import numpy as np

from patkit.data_structures import (
    FileInformation, Modality, ModalityData,
    ModalityMetaData, Recording
)
from patkit.utility_functions import product_dict

_logger = logging.getLogger('patkit.intensity')


class IntensityParameters(ModalityMetaData):
    """
    Parameters used in calculating the Intensity.

    Intensity memory will not be regularly released after it has been
    calculated regardless of when this happens since it is not a very
    memory-intensive metric, but can take significant computation to do.

    Parameters
    ----------
    parent_name: str
        Name of the Modality this instance of PD was calculated on.
    preload : bool
        Should the Intensity be calculated on initialisation or only on demand.
    release_data_memory : bool
        Whether to assign None to `parent.data` after deriving this Modality
        from the data. Currently, has no effect as deriving PD at runtime is
        not yet supported.
    """
    parent_name: str
    preload: bool = False
    release_data_memory: bool = False


class Intensity(Modality):
    """
    Represent Intensity as a Modality. 
    """

    @classmethod
    def generate_name(cls, params: IntensityParameters) -> str:
        """
        Generate an Intensity name to be used as its unique identifier.

        This static method **defines** what the names are. This implementation
        pattern (Intensity.name calls this and anywhere that needs to guess
        what a name would be calls this) is how all derived Modalities should
        work.

        Parameters
        ----------
        params : IntensityParameters
            The parameters of the Intensity instance. Note that this
            IntensityParameters instance does not need to be attached to a
            Intensity instance.

        Returns
        -------
        str
            Name of the Intensity instance.
        """
        name_string = cls.__name__

        if params.parent_name:
            name_string = name_string + " on " + params.parent_name

        return name_string

    @staticmethod
    def get_names_and_meta(
            modality: Modality | str,
            release_data_memory: bool = True
    ) -> dict[str: IntensityParameters]:
        """
        Generate Intensity modality names and metadata.

        This method will generate the full cartesian product of the possible
        combinations. If only some of them are needed, make more than one call
        or weed the results afterwards.

        Parameters
        ----------
        modality : Modality
            parent modality that Intensity would be derived from
        release_data_memory: bool
            Should parent Modality's data be assigned to None after
            calculations are complete, by default True.

        Returns
        -------
        dict[str: PdParameters]
            Dictionary where the names of the PD Modalities index the
            PdParameter objects.
        """
        if isinstance(modality, str):
            parent_name = modality
        else:
            parent_name = modality.__name__

        param_dict = {
            'parent_name': [parent_name],
            'release_data_memory': [release_data_memory]}

        pd_params = [IntensityParameters(**item)
                     for item in product_dict(**param_dict)]

        return {
            Intensity.generate_name(params): params for params in pd_params
        }

    def __init__(
            self,
            container: Recording,
            metadata: IntensityParameters,
            file_info: FileInformation,
            parsed_data: ModalityData | None = None,
            time_offset: float | None = None
    ) -> None:
        """
        Build an Intensity Modality       

        Parameters
        ----------
        owner : Recording
            the containing Recording.
        metadata : IntensityParameters
            Parameters used in calculating this instance of Intensity.
        file_info : FileInformation
            Save paths for numerical and meta data.
        parsed_data : ModalityData | None
            ModalityData object, by default None. Contains Intensity values,
            sampling rate, and either timevector and/or `time_offset`.
            Providing a timevector overrides any time_offset value given, but
            in absence of a timevector the `time_offset` will be applied on
            reading the data from file.
        time_offset : ModalityData | None
            If not specified or 0, `time_offset` will be copied from
            `parsed_data`, by default None
        """
        # This allows the caller to be lazy.
        if not time_offset:
            if parsed_data is not None:
                time_offset = parsed_data.timevector[0]

        super().__init__(
            container=container,
            metadata=metadata,
            file_info=file_info,
            parsed_data=parsed_data,
            time_offset=time_offset)

    def _derive_data(self) -> tuple[np.ndarray, np.ndarray, float]:
        """
        Calculate Intensity on the data Modality parent.       
        """
        raise NotImplementedError(
            "Currently Intensity Modalities have to be "
            "calculated at instantiation time.")

    def get_meta(self) -> dict:
        return self.metadata.model_dump()

    @property
    def name(self) -> str:
        """
        Identity, metric, and parent data class.

        The name will be of the form
        'PD [metric name] on [data modality class name]'.

        This overrides the default behaviour of Modality.name.
        """
        return Intensity.generate_name(self.metadata)
