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
Test case results.
"""

import os.path

import pandas

from .problem import Problem


class Results:

    """
    Test case results.
    """

    def __init__(self, csv_path: str):
        """
        Initialize results.

        Args:
            csv_path: Persistent CSV file to load previous results from.
        """
        df = pandas.DataFrame(
            [],
            columns=[
                "problem",
                "solver",
                "duration_us",
                "found",
                "cost_error",
                "primal_error",
            ],
        )
        if os.path.exists(csv_path):
            df = pandas.concat([df, pandas.read_csv(csv_path)])
        self.df = df
        self.csv_path = csv_path
        self.__found_df = None
        self.__found_summary_df = None

    def write(self) -> None:
        """
        Write results to their CSV file for persistence.
        """
        self.df.to_csv(self.csv_path, index=False)

    def update(
        self, problem: Problem, solver: str, solution, duration_us: float
    ) -> None:
        """
        Update entry for a given (problem, solver) pair.

        Args:
            problem: Problem solved.
            solver: Solver name.
            solution: Solution found by the solver.
            duration_us: Duration the solver took, in microseconds.
        """
        self.df = self.df.drop(
            self.df.index[
                (self.df["problem"] == problem.name)
                & (self.df["solver"] == solver)
            ]
        )
        self.df = pandas.concat(
            [
                self.df,
                pandas.DataFrame(
                    {
                        "problem": [problem.name],
                        "solver": [solver],
                        "duration_us": [duration_us],
                        "found": [solution is not None],
                        "cost_error": [problem.cost_error(solution)],
                        "primal_error": [problem.primal_error(solution)],
                    }
                ),
            ],
            ignore_index=True,
        )

    def build_found_df(self) -> pandas.DataFrame:
        """
        Build the (solver, problem) found table.

        Returns:
            Found table data frame.
        """
        problems = set(self.df["problem"].to_list())
        solvers = set(self.df["solver"].to_list())
        found = {
            solver: {problem: None for problem in problems}
            for solver in solvers
        }
        for row in self.df.to_dict(orient="records"):
            found[row["solver"]][row["problem"]] = row["found"]
        self.__found_df = pandas.DataFrame.from_dict(found)
        return self.__found_df

    def build_found_summary_df(self) -> pandas.DataFrame:
        found_df = self.__found_df
        solvers = list(found_df)
        # problems = found_df.index.tolist()
        self.__found_summary_df = pandas.DataFrame(
            {
                "Success rate (%)": {
                    solver: 100.0 * found_df[solver].astype(float).mean()
                    for solver in solvers
                }
            }
        )
        return self.__found_summary_df