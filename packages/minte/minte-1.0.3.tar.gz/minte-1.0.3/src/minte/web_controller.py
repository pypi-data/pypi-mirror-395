"""
Lightweight web controller for MINT scenarios.

This module provides a simplified interface for the MINT web application,
wrapping the main controller with default parameters and output processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from .controller import run_minter_scenarios


def _to_list(x: Any) -> list:
    """Convert scalar or array-like to list."""
    if x is None:
        return None
    if isinstance(x, (int, float, str)):
        return [x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    return list(x)


@dataclass
class MintwebResults:
    """Results from a MINT web controller run.
    
    Provides attribute access to match R API: results$prevalence, results$cases, etc.
    """
    prevalence: pd.DataFrame | None = None
    cases: pd.DataFrame | None = None
    scenario_meta: pd.DataFrame | None = None
    eir_valid: bool = True
    benchmarks: dict | None = None
    
    def __getitem__(self, key: str) -> Any:
        """Allow dict-style access for backwards compatibility."""
        return getattr(self, key)
    
    def keys(self) -> list[str]:
        """Return available keys."""
        return ["prevalence", "cases", "scenario_meta", "eir_valid", "benchmarks"]


def run_mintweb_controller(
    res_use,
    py_only,
    py_pbo,
    py_pyrrole,
    py_ppf,
    prev,
    Q0,
    phi,
    season,
    routine,
    irs,
    irs_future,
    lsm,
    res_future=None,
    net_type_future=None,
    itn_future=None,
    scenario_tag=None,
    clean_output: bool = True,
    tabulate: bool = True,
) -> MintwebResults:
    """
    Run MINT scenarios with web-friendly defaults and output processing.

    This is a simplified wrapper around run_minter_scenarios that:
    - Uses default technical parameters
    - Optionally cleans and tabulates output for web display
    - Accepts both scalars and arrays (like the R version)
    - It is intened as the primary access point for MINTweb back end. Or a quick smoke-test

    Parameters
    ----------
    res_use : float or array-like
        Current resistance levels.
    py_only : float or array-like
        Pyrethroid-only net proportions.
    py_pbo : float or array-like
        Pyrethroid-PBO net proportions.
    py_pyrrole : float or array-like
        Pyrethroid-pyrrole net proportions.
    py_ppf : float or array-like
        Pyrethroid-PPF net proportions.
    prev : float or array-like
        Malaria prevalence levels.
    Q0 : float or array-like
        Q0 values.
    phi : float or array-like
        Phi bednet values.
    season : float or array-like
        Seasonality indicators.
    routine : float or array-like
        Routine treatment indicators.
    irs : float or array-like
        Current IRS coverage.
    irs_future : float or array-like
        Future IRS coverage.
    lsm : float or array-like
        LSM coverage.
    res_future : float or array-like, optional
        Future resistance levels.
    net_type_future : str or list[str], optional
        Future net type choices.
    itn_future : float or array-like, optional
        Future ITN coverage (0-1).
    scenario_tag : str or list[str], optional
        Scenario identifiers.
    clean_output : bool, default True
        Remove helper columns and filter timesteps.
    tabulate : bool, default True
        Aggregate cases into 4 time periods per scenario.

    Returns
    -------
    MintwebResults
        Object with attributes:
        - prevalence: DataFrame with prevalence predictions
        - cases: DataFrame with cases predictions
        - scenario_meta: DataFrame with scenario metadata
        - eir_valid: bool indicating if EIR values are valid
    """
    # Convert scalars to lists (R-style flexibility)
    res_use = _to_list(res_use)
    py_only = _to_list(py_only)
    py_pbo = _to_list(py_pbo)
    py_pyrrole = _to_list(py_pyrrole)
    py_ppf = _to_list(py_ppf)
    prev = _to_list(prev)
    Q0 = _to_list(Q0)
    phi = _to_list(phi)
    season = _to_list(season)
    routine = _to_list(routine)
    irs = _to_list(irs)
    irs_future = _to_list(irs_future)
    lsm = _to_list(lsm)
    res_future = _to_list(res_future)
    itn_future = _to_list(itn_future)
    
    # Handle string scenario_tag and net_type_future
    if isinstance(scenario_tag, str):
        scenario_tag = [scenario_tag]
    if isinstance(net_type_future, str):
        net_type_future = [net_type_future]
    
    # Run main MINT scenarios with default parameters
    results = run_minter_scenarios(
        res_use=res_use,
        res_future=res_future,
        py_only=py_only,
        py_pbo=py_pbo,
        py_pyrrole=py_pyrrole,
        py_ppf=py_ppf,
        net_type_future=net_type_future,
        itn_future=itn_future,
        prev=prev,
        Q0=Q0,
        phi=phi,
        season=season,
        routine=routine,
        irs=irs,
        irs_future=irs_future,
        lsm=lsm,
        # Default technical parameters
        eir_models=["xgboost"],
        prevalence_models=["LSTM"],
        predictor=["prevalence", "cases"],
        year_start=2,
        year_end=5,
        scenario_tag=scenario_tag,
        benchmark=False,
        preload_models=True,
        use_cache=True,
    )

    # Create output object
    output = MintwebResults(
        prevalence=results.prevalence,
        cases=results.cases,
        scenario_meta=results.scenario_meta,
        eir_valid=results.eir_valid,
        benchmarks=results.benchmarks,
    )

    # Clean output if requested
    if clean_output:
        output = _clean_mintweb_output(output, tabulate=tabulate)

    return output


def _clean_mintweb_output(output: MintwebResults, tabulate: bool = True) -> MintwebResults:
    """
    Clean and process output for web display.

    Parameters
    ----------
    output : MintwebResults
        Raw output from run_minter_scenarios.
    tabulate : bool
        Whether to aggregate cases into time periods.

    Returns
    -------
    MintwebResults
        Cleaned output.
    """
    columns_to_remove = ["index", "timestep", "model_type"]

    # Process prevalence data
    if output.prevalence is not None:
        df = output.prevalence.copy()

        # Filter to timesteps > 52 per scenario (skip first year)
        # Fixed: Use explicit loop to avoid FutureWarning
        filtered_dfs = []
        for scenario in df["scenario"].unique():
            scenario_df = df[df["scenario"] == scenario].iloc[52:]
            filtered_dfs.append(scenario_df)
        
        if filtered_dfs:
            df = pd.concat(filtered_dfs, ignore_index=True)
        else:
            df = pd.DataFrame()

        # Remove helper columns
        cols_to_keep = [c for c in df.columns if c not in columns_to_remove]
        output.prevalence = df[cols_to_keep]

    # Process cases data
    if output.cases is not None:
        df = output.cases.copy()

        # Remove helper columns
        cols_to_keep = [c for c in df.columns if c not in columns_to_remove]
        df = df[cols_to_keep]

        if tabulate:
            # Aggregate cases into 4 time periods per scenario
            # Period 1: timesteps 53-78 (weeks 1-26 of year 2-6)
            # Period 2: timesteps 79-104
            # Period 3: timesteps 105-130
            # Period 4: timesteps 131-156
            tabulated = []

            for scenario in df["scenario"].unique():
                scenario_df = df[df["scenario"] == scenario]

                # Get cases values for timesteps 53-156
                if "cases" in scenario_df.columns:
                    cases_values = scenario_df["cases"].values

                    # Take the relevant portion (indices 52-155, which are timesteps 53-156)
                    if len(cases_values) >= 156:
                        relevant_cases = cases_values[52:156]  # 104 values
                    else:
                        # Handle shorter sequences
                        relevant_cases = cases_values

                    # Sum into 4 periods of 26 timesteps each
                    if len(relevant_cases) >= 104:
                        periods = np.array_split(relevant_cases, 4)
                        period_sums = [float(np.sum(p)) for p in periods]
                    else:
                        # Just sum all if not enough data
                        period_sums = [float(np.sum(relevant_cases))]

                    for period_sum in period_sums:
                        tabulated.append({
                            "cases_per_1000": max(0, period_sum),
                            "scenario": scenario,
                        })

            output.cases = pd.DataFrame(tabulated)

            # Ensure non-negative values
            if "cases_per_1000" in output.cases.columns:
                output.cases["cases_per_1000"] = output.cases["cases_per_1000"].clip(lower=0)
        else:
            # Just ensure non-negative
            if "cases" in df.columns:
                df["cases"] = df["cases"].clip(lower=0)
            output.cases = df

    return output


def format_for_json(output: MintwebResults) -> dict[str, Any]:
    """
    Format output for JSON serialization.

    Converts DataFrames to list-of-dicts format suitable for JSON APIs.

    Parameters
    ----------
    output : MintwebResults
        Output from run_mintweb_controller.

    Returns
    -------
    dict
        JSON-serializable dictionary.
    """
    json_output = {}

    for key in output.keys():
        value = getattr(output, key)
        if isinstance(value, pd.DataFrame):
            json_output[key] = value.to_dict(orient="records")
        elif isinstance(value, np.ndarray):
            json_output[key] = value.tolist()
        elif isinstance(value, (np.bool_, np.integer, np.floating)):
            json_output[key] = value.item()
        else:
            json_output[key] = value

    return json_output
