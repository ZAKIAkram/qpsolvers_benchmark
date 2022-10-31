#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
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

"""
Report written from test set results.
"""

import datetime

import pandas

from .results import Results
from .solver_settings import SolverSettings
from .spdlog import logging
from .utils import get_cpu_info, get_solver_versions


class Report:
    def __init__(self, results: Results, solver_settings: SolverSettings):
        self.cpu_info = get_cpu_info()
        self.date = str(datetime.datetime.now(datetime.timezone.utc))
        self.results = results
        self.solver_settings = solver_settings

    def get_solvers_table(self):
        versions = get_solver_versions()
        versions_df = pandas.DataFrame(
            {
                "solver": list(versions.keys()),
                "version": list(versions.values()),
            },
        )
        versions_df = versions_df.set_index("solver")
        versions_df = versions_df.sort_index()
        versions_table = versions_df.to_markdown(index=True)
        return versions_table

    def get_success_rate_table(self):
        success_rate_df = self.results.build_success_rate_df()
        success_rate_table = success_rate_df.to_markdown(index=True)
        success_rate_table = success_rate_table.replace(" 100    ", " **100**")
        return success_rate_table

    def get_geometric_mean_table(self):
        geometric_mean_df = self.results.build_geometric_mean_df(
            time_limits={
                key: settings.time_limit
                for key, settings in self.solver_settings.items()
            }
        )
        geometric_mean_table = geometric_mean_df.to_markdown(
            index=True, floatfmt=".1f"
        )
        return geometric_mean_table

    def write(self, path: str) -> None:

        with open(path, "w") as fh:
            fh.write(
                f"""# Maros and Meszaros Convex Quadratic Programming Test Set

- Date: {self.date}
- CPU: {self.cpu_info}

## Solvers

{self.get_solvers_table()}

## Success rate

Precentage of problems each solver is able to solve:

{self.get_success_rate_table()}

Rows are solvers and columns are solver settings.

## Computation time

We compare solver computation times using the shifted geometric mean.

**Intuition:** a solver with a shifted geometric mean of Y is Y times slower
than the best solver over the test set.

### Details

There is a different ranking of solver runtimes for each problem in the test
set. To aggregate those rankings into a single metric over the whole test set,
we use the shifted geometric mean, which is a standard in [benchmarks for
optimization software](http://plato.asu.edu/bench.html).

The shifted geometric mean is a slowdown factor compared to the best solver
over the whole test set. It has the advantage of being compromised by neither
large outliers (as opposed to the arithmetic mean) nor by small outliers (in
contrast to the geometric geometric mean). The best solvers have a shifted
geometric mean close to one:

### Results

{self.get_geometric_mean_table()}

Rows are solvers and columns are solver settings.

## Precision

### Cost errors

### Constraint errors

"""
            )

        logging.info(f"Wrote report to {path}")