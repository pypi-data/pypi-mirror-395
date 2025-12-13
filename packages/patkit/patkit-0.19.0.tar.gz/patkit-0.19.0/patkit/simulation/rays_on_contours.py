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
Plot metric rays on contours for different perturbations.
"""

import numpy as np

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

from patkit.constants import ComparisonMember
from patkit.plot_and_publish.plot_utilities import get_colors_in_sequence
from .simulation_datastructures import (
    Comparison,
    ComparisonSoundPair,
    DistanceMetricSimulationResult,
    ShapeMetricSimulationResult,
)
from .simulation_plots import (
    contour_ray_plot,
    dual_contour_ray_plot,
)
from patkit.configuration.configuration_models import RayPlotParams


def distance_metric_rays_on_contours(
    contours: dict[str, np.ndarray],
    distance_metric_result: DistanceMetricSimulationResult,
    ray_plot_params: RayPlotParams,
    number_of_perturbations: int,
    columns: list[ComparisonSoundPair],
    nrows: int = 2,
    contour_rows: int = 2,
) -> None:
    """
    Plot a distance metric values on contours.

    Parameters
    ----------
    contours : dict[str, np.ndarray]
        Contours by name to plot the metrics on.
    distance_metric_result : DistanceMetricSimulationResult
        Results and baselines from distance metric simulation.
    ray_plot_params : RayPlotParams
        Plotting parameters for the ray plot.
    number_of_perturbations : int
        How many perturbation values there are.
    columns : list[ComparisonSoundPair]
        Order of contours to go through. 
    nrows : int
        number of subplot rows in the plot, by default 1
    contour_rows : int
        number of contour rows in the subplots, by default 2
    """
    metrics = distance_metric_result.results
    metric_name = str(distance_metric_result.metric).upper()
    baselines = distance_metric_result.baselines

    plt.style.use('tableau-colorblind10')
    colors = None
    if ray_plot_params.color_threshold is not None:
        colors = get_colors_in_sequence(2)

    gridspec_keywords = {
        'wspace': 0.0,
        'hspace': 0.0,
    }

    ncols = len(columns)
    _, axes = plt.subplots(nrows=nrows,
                           ncols=ncols,
                           figsize=ray_plot_params.figure_size,
                           sharey=True,
                           sharex=True,
                           gridspec_kw=gridspec_keywords)

    for ax in axes.flatten():
        ax.set_aspect('equal')
        ax.set_yticks([])
        ax.set_xticks([])
        font_properties = fm.FontProperties(size=9)
        scale_bar = AnchoredSizeBar(
            ax.transData,
            size=.1*ray_plot_params.scale, label=f'0.1 {metric_name}',
            loc='upper left',
            pad=.5,
            color=plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
            frameon=False,
            size_vertical=1,
            label_top=True,
            fontproperties=font_properties)
        ax.add_artist(scale_bar)

    for i, sound_pair in enumerate(columns):
        axes[0, i].set_title(f"[{sound_pair.first}] to [{sound_pair.second}]")

        if sound_pair.first == sound_pair.second:
            axes[1, i].set_xlabel(f"{metric_name} = 0")
        else:
            reference = baselines[Comparison(
                first=sound_pair.first, second=sound_pair.second,
                perturbed=ComparisonMember.FIRST)]
            axes[1, i].set_xlabel(f"{metric_name} = {reference:.2f}")

    axes[0, 0].set_ylabel("Baseline to perturbed")
    axes[1, 0].set_ylabel("Perturbed to baseline")

    comparisons = []
    for sound_pair in columns:
        comparisons.append(
            Comparison(first=sound_pair.first,
                       second=sound_pair.second,
                       perturbed=ComparisonMember.SECOND))
        comparisons.append(
            Comparison(first=sound_pair.first,
                       second=sound_pair.second,
                       perturbed=ComparisonMember.FIRST))

    for j, comparison in enumerate(comparisons):
        row = j % nrows
        column = j//nrows
        metric_dict = metrics[comparison]
        baseline = baselines[comparison]
        for i, perturbation in enumerate(metric_dict):
            p_row = i // (number_of_perturbations//contour_rows)
            p_column = i % (number_of_perturbations//contour_rows)
            origin_offset = np.array([0+125*p_row, 0+100*p_column])
            axes[row, column].text(
                origin_offset[1]-10, origin_offset[0]-15,
                f"{perturbation} mm",
                horizontalalignment='center',)
            if comparison.first == comparison.second:
                contour_ray_plot(
                    axes=axes[row, column],
                    contour=contours[comparison.first],
                    metric_values=metric_dict[perturbation],
                    metric_reference_value=baseline,
                    scale=ray_plot_params.scale,
                    origin_offset=origin_offset,
                    color_threshold=ray_plot_params.color_threshold,
                    colors=colors,
                )
            else:
                if comparison.perturbed == ComparisonMember.SECOND:
                    dual_contour_ray_plot(
                        axes=axes[row, column],
                        unperturbed_contour=contours[comparison.first],
                        perturbed_contour=contours[comparison.second],
                        metric_values=metric_dict[perturbation],
                        metric_reference_value=baseline,
                        scale=ray_plot_params.scale,
                        origin_offset=origin_offset,
                        relative=False,
                        color_threshold=ray_plot_params.color_threshold,
                        colors=colors,
                    )
                else:
                    dual_contour_ray_plot(
                        axes=axes[row, column],
                        unperturbed_contour=contours[comparison.second],
                        perturbed_contour=contours[comparison.first],
                        metric_values=metric_dict[perturbation],
                        metric_reference_value=baseline,
                        scale=ray_plot_params.scale,
                        origin_offset=origin_offset,
                        relative=False,
                        color_threshold=ray_plot_params.color_threshold,
                        colors=colors,
                    )


def shape_metric_rays_on_contours(
    contours: dict[str, np.ndarray],
    shape_metric_result: ShapeMetricSimulationResult,
    ray_plot_params: RayPlotParams,
    number_of_perturbations: int,
    nrows: int = 1,
    contour_rows: int = 2,
) -> None:
    """
    Plot shape metric values on contours.

    Parameters
    ----------
    contours : dict[str, np.ndarray]
        Contours by name to plot the metrics on.
    shape_metric_result : ShapeMetricSimulationResult
        Results and baselines from shape metric simulation.
    ray_plot_params : RayPlotParams
        Plotting parameters for the ray plot.
    number_of_perturbations : int
        How many perturbation values there are.
    nrows : int
        number of subplot rows in the plot, by default 1
    contour_rows : int
        number of contour rows in the subplots, by default 2
    """
    metrics = shape_metric_result.results
    metric_name = shape_metric_result.metric.short_name()
    baselines = shape_metric_result.baselines

    plt.style.use('tableau-colorblind10')
    colors = None
    if ray_plot_params.color_threshold is not None:
        colors = get_colors_in_sequence(2)

    gridspec_keywords = {
        'wspace': 0.0,
        'hspace': 0.0,
    }

    contour_names = metrics.keys()
    ncols = len(contour_names)
    _, axes = plt.subplots(nrows=nrows,
                           ncols=ncols,
                           figsize=ray_plot_params.figure_size,
                           sharey=True,
                           sharex=True,
                           gridspec_kw=gridspec_keywords)

    for ax in axes.flatten():
        ax.set_aspect('equal')
        ax.set_yticks([])
        ax.set_xticks([])
        font_properties = fm.FontProperties(size=9)
        scale_bar = AnchoredSizeBar(
            ax.transData,
            size=ray_plot_params.scale*np.log10(2), label='log10(2)',
            loc='upper left',
            pad=.5,
            color=plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
            frameon=False,
            size_vertical=1,
            label_top=True,
            fontproperties=font_properties)
        ax.add_artist(scale_bar)

    for j, contour_name in enumerate(metrics):
        reference = baselines[contour_name]
        axes[j].set_title(f"[{contour_name}]")
        axes[j].set_xlabel(
            f"{metric_name}/Baseline {metric_name} = {reference:.2f}")
        metric_dict = metrics[contour_name]
        baseline = baselines[contour_name]
        for i, perturbation in enumerate(metric_dict):
            p_row = i // (number_of_perturbations//contour_rows)
            p_column = i % (number_of_perturbations//contour_rows)
            origin_offset = np.array([0+125*p_row, 0+100*p_column])
            axes[j].text(
                origin_offset[1]-10, origin_offset[0]+25,
                f"{perturbation} mm",
                horizontalalignment='center',)
            contour_ray_plot(
                axes=axes[j],
                contour=contours[contour_name],
                metric_values=metric_dict[perturbation],
                metric_reference_value=baseline,
                scale=ray_plot_params.scale,
                origin_offset=origin_offset,
                relative=True,
                color_threshold=ray_plot_params.color_threshold,
                colors=colors,)
