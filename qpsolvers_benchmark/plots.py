#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Plots for analysis of test set results."""

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas

from .test_set import TestSet


def hist(
    metric: str,
    df: pandas.DataFrame,
    settings: str,
    test_set: TestSet,
    solvers: Optional[List[str]] = None,
    nb_bins: int = 10,
    alpha: float = 0.8,
    linewidth: float = 3.0,
) -> None:
    """Histogram comparing solvers on a given metric.

    Args:
        metric: Metric to compare solvers on.
        df: Test set results data frame.
        settings: Settings to compare solvers on.
        test_set: Test set.
        solvers: Names of solvers to compare (default: all).
        nb_bins: Number of bins in the histogram.
        alpha: Histogram transparency.
    """
    assert issubclass(df[metric].dtype.type, np.floating)
    nb_problems = test_set.count_problems()
    settings_df = df[df["settings"] == settings]
    metric_tol = test_set.tolerances[settings].from_metric(metric)
    hist_df = settings_df[settings_df["found"]]
    plot_solvers: List[str] = (
        solvers if solvers is not None else list(set(hist_df.solver))
    )
    for solver in plot_solvers:
        values = hist_df[hist_df["solver"] == solver][metric].values
        nb_solved = len(values)
        sorted_values = np.sort(values)
        y = np.arange(1, 1 + nb_solved)
        padded_values = np.hstack([sorted_values, [metric_tol]])
        padded_y = np.hstack([y, [nb_solved]])
        plt.step(padded_values, padded_y, linewidth=linewidth)
    plt.legend(plot_solvers)
    plt.title(
        f"Comparing {metric} on {test_set.title} with {settings} settings"
    )
    plt.xlabel(metric)
    plt.xscale("log")
    plt.axhline(y=nb_problems, color="r")
    plt.axvline(x=metric_tol, color="r")
    plt.ylabel("# problems solved")
    plt.grid(True)
    plt.show(block=True)
