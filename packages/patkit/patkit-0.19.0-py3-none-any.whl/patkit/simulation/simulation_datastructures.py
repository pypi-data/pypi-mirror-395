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
Datastructures used in simulation.

Currently, mainly classes to support simulating behaviour of splines.
"""

from dataclasses import dataclass
from typing import Annotated, Callable

import numpy as np
from pydantic import BaseModel

from patkit.constants import ComparisonMember, SplineMetricEnum, \
    SplineShapesEnum

MetricFunction = Annotated[
    Callable[[np.ndarray], np.ndarray],
    "Metrics need to accept one np.ndarray as argument and "
    "return a np.ndarray. This is only an alias for 'Metric'"
]


class ComparisonSoundPair(BaseModel, frozen=True):
    """
    Defines a comparison between two contours.

    First should be compared to second.
    """
    first: str
    second: str

    def __repr__(self) -> str:
        return (f"Comparison: from first {self.first} "
                f"to second {self.second}.")


class Comparison(ComparisonSoundPair):
    """
    Defines a comparison between two contours, and which of them is perturbed.

    First should be compared to second with the contour named in perturbed
    being the one that gets perturbed.
    """
    # first: str
    # second: str
    perturbed: ComparisonMember

    @property
    def perturbed_name(self) -> str:
        """
        Name of the perturbed contour.

        Returns
        -------
        str
            The name as a string.
        """
        if self.perturbed == ComparisonMember.FIRST:
            return self.first
        return self.second

    def __repr__(self) -> str:
        return (f"Comparison: from first {self.first} "
                f"to second {self.second}, perturbed is {self.perturbed}")


@dataclass
class ShapeMetricSimulationResult:
    """
    Baseline and results from simulations of shape metrics.

    Parameters
    ----------
    metric : SplineShapesEnum
        Metric used in deriving the results.
    baselines : dict[str, float]
        Baseline for each metric and contour.
    results : dict[str, dict[str, np.ndarray]]
        Results for each metric/contour/perturbation
    """
    metric: SplineShapesEnum
    baselines: dict[str, float]
    results: dict[str, dict[str, np.ndarray]]


@dataclass
class DistanceMetricSimulationResult:
    """
    Baseline and results from simulations of shape metrics.

    Parameters
    ----------
    metric : SplineMetricEnum
        Metric used in deriving the results. While SplineMetricEnum includes
        also spline shape metrics, passing one here will result in a ValueError
        being raised or unpredictable behavior.
    baselines : dict[str, float]
        Baseline for each metric and contour.
    results : dict[Comparison, dict[str, np.ndarray]]
        Results for each metric/contour/perturbation
    """
    metric: SplineMetricEnum
    baselines: dict[Comparison, float]
    results: dict[Comparison, dict[str, np.ndarray]]

    def __post_init__(self):
        if isinstance(self.metric, SplineShapesEnum):
            raise ValueError(
                f"DistanceMetricSimulationResult does not accept "
                f"SplineShapesEnum as metric type. Found {self.metric}."
            )
