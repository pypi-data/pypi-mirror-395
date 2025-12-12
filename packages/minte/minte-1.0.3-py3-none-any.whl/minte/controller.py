"""
Main controller for running MINT malaria intervention scenarios.

This module provides the primary interface for:
- Running multiple scenarios with various intervention parameters
- Predicting EIR (Entomological Inoculation Rate)
- Running neural network predictions for prevalence and cases
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
import pandas as pd
from estimint import load_xgb_model, run_xgb_model

from .cache import get_cached_model, preload_all_models, is_cached
from .emulator import run_malaria_emulator
from .parser import calculate_overall_dn0

logger = logging.getLogger(__name__)


def _to_list(x: Any) -> list | None:
    """Convert scalar or array-like to list, preserving None."""
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return [x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    return list(x)


@dataclass
class MinterConfig:
    """Configuration for MINT scenario runs."""

    eir_models: list[str] = field(default_factory=lambda: ["xgboost"])
    prevalence_models: list[str] = field(default_factory=lambda: ["LSTM"])
    cases_models: list[str] = field(default_factory=lambda: ["LSTM"])
    predictor: list[str] = field(default_factory=lambda: ["prevalence", "cases"])
    year_start: int = 2
    year_end: int = 5
    benchmark: bool = True
    preload_models: bool = True
    use_cache: bool = True


@dataclass
class MinterResults:
    """Results from a MINT scenario run.
    
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


# Valid net type names
ALLOWED_NET_TYPES = ["py_only", "py_pbo", "py_pyrrole", "py_ppf"]


# Cache for the XGBoost model so we only load it once
_XGB_MODEL = None

def predict_eir_xgboost(
    runtime: pd.DataFrame,
    pretrained: Any = None,
) -> float:
    """
    Predict EIR using the estiMINT XGBoost model.

    Parameters
    ----------
    runtime : pd.DataFrame
        DataFrame with runtime parameters. Must contain:
        dn0_use, Q0, phi_bednets, seasonal, itn_use, irs_use, prev_y9
    pretrained : Any, optional
        Pre-loaded XGBoost model (if you want to pass one in).

    Returns
    -------
    float
        Predicted EIR value for the first row.
    """
    global _XGB_MODEL

    # Decide which model to use
    if pretrained is not None:
        mdl = pretrained
    else:
        if _XGB_MODEL is None:
            _XGB_MODEL = load_xgb_model()  # estimint handles the path internally
        mdl = _XGB_MODEL

    # Make sure column names match what estiMINT expects
    if "prev_y9" not in runtime.columns:
        if "prevalence" in runtime.columns:
            runtime = runtime.rename(columns={"prevalence": "prev_y9"})
        else:
            raise KeyError(
                "runtime must contain either a 'prev_y9' or 'prevalence' column."
            )

    feature_cols = [
        "dn0_use",
        "Q0",
        "phi_bednets",
        "seasonal",
        "itn_use",
        "irs_use",
        "prev_y9",
    ]
    new_data = runtime[feature_cols]

    eir = run_xgb_model(new_data, mdl)
    return float(eir[0])


def run_minter_scenarios(
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
    itn_future: list[float] | np.ndarray | None = None,
    eir_models: list[str] = ["xgboost"],
    prevalence_models: list[str] = ["LSTM"],
    cases_models: list[str] = ["LSTM"],
    predictor: list[str] = ["prevalence", "cases"],
    year_start: int = 2,
    year_end: int = 5,
    scenario_tag: list[str] | None = None,
    benchmark: bool = True,
    preload_models: bool = True,
    use_cache: bool = True,
    itn_params_path: str | None = None,
) -> MinterResults:
    """
    Run MINT scenarios for malaria intervention analysis.

    Runs vectorized scenario builds, predicts EIR, and batches neural-network
    inference for prevalence and/or cases.

    Parameters
    ----------
    res_use : array-like
        Current resistance levels.
    py_only : array-like
        Pyrethroid-only net proportions.
    py_pbo : array-like
        Pyrethroid-PBO net proportions.
    py_pyrrole : array-like
        Pyrethroid-pyrrole net proportions.
    py_ppf : array-like
        Pyrethroid-PPF net proportions.
    prev : array-like
        Malaria prevalence levels.
    Q0 : array-like
        Q0 values (proportion of human blood meals taken indoors).
    phi : array-like
        Phi bednet values.
    season : array-like
        Seasonality indicators.
    routine : array-like
        Routine treatment indicators.
    irs : array-like
        Current IRS coverage.
    irs_future : array-like
        Future IRS coverage.
    lsm : array-like
        LSM (larval source management) coverage.
    res_future : array-like, optional
        Future resistance levels after next campaign.
    net_type_future : list[str], optional
        Future net choices per scenario.
    itn_future : array-like, optional
        Future ITN coverage per scenario (0-1).
    eir_models : list[str]
        Models to use for EIR prediction.
    prevalence_models : list[str]
        Models for prevalence prediction.
    cases_models : list[str]
        Models for cases prediction.
    predictor : list[str]
        Predictors to run ("prevalence", "cases", or both).
    year_start, year_end : int
        Year range for predictions.
    scenario_tag : list[str], optional
        Scenario identifiers.
    benchmark : bool
        Record timing information.
    preload_models : bool
        Preload all models at start.
    use_cache : bool
        Use cached models.
    itn_params_path : str, optional
        Path to ITN parameters file.

    Returns
    -------
    MinterResults
        Results containing prevalence and cases predictions.
    """
    # Initialize timing
    if benchmark:
        t_total_start = time.time()
        bench_times: dict[str, Any] = {}

    # Convert scalars to arrays (R-style flexibility)
    res_use = np.atleast_1d(np.asarray(res_use))
    py_only = np.atleast_1d(np.asarray(py_only))
    py_pbo = np.atleast_1d(np.asarray(py_pbo))
    py_pyrrole = np.atleast_1d(np.asarray(py_pyrrole))
    py_ppf = np.atleast_1d(np.asarray(py_ppf))
    prev = np.atleast_1d(np.asarray(prev))
    Q0 = np.atleast_1d(np.asarray(Q0))
    phi = np.atleast_1d(np.asarray(phi))
    season = np.atleast_1d(np.asarray(season))
    routine = np.atleast_1d(np.asarray(routine))
    irs = np.atleast_1d(np.asarray(irs))
    irs_future = np.atleast_1d(np.asarray(irs_future))
    lsm = np.atleast_1d(np.asarray(lsm))

    # Preload models if requested
    if preload_models and use_cache:
        if benchmark:
            t_start = time.time()

        models_loaded = is_cached("nn_prevalence") or is_cached("nn_cases")
        if not models_loaded:
            logger.info("Pre-loading all models into cache...")
            preload_all_models(verbose=False)

        if benchmark:
            bench_times["preload_models"] = time.time() - t_start

    # Validate inputs
    n_scenarios = len(res_use)

    if not all(len(arr) == n_scenarios for arr in [py_only, py_pbo, py_pyrrole, py_ppf]):
        raise ValueError(
            f"All net combination vectors must have the same length as res_use ({n_scenarios})"
        )

    if res_future is not None and len(res_future) > 0 and len(res_future) != n_scenarios:
        raise ValueError(f"If provided, res_future must have length {n_scenarios}")

    # Handle net_type_future and itn_future
    if net_type_future is None and itn_future is None:
        net_type_future = [None] * n_scenarios
        itn_future = np.full(n_scenarios, np.nan)
    else:
        if net_type_future is None:
            net_type_future = [None] * n_scenarios
        if itn_future is None:
            itn_future = np.full(n_scenarios, np.nan)
        else:
            itn_future = np.asarray(itn_future)

        if len(net_type_future) != n_scenarios or len(itn_future) != n_scenarios:
            raise ValueError(
                f"net_type_future and itn_future must each have length {n_scenarios}"
            )

        # Set net_type_future to None where itn_future is 0
        for i in range(n_scenarios):
            if not np.isnan(itn_future[i]) and itn_future[i] == 0:
                net_type_future[i] = None

        # Validate net types
        bad_type_idx = [
            i
            for i, nt in enumerate(net_type_future)
            if nt is not None and nt not in ALLOWED_NET_TYPES
        ]
        if bad_type_idx:
            raise ValueError(
                f"Unknown net_type_future at positions: {bad_type_idx}. "
                f"Allowed: {ALLOWED_NET_TYPES}"
            )

        # Validate itn_future values
        bad_itn_idx = [
            i
            for i in range(n_scenarios)
            if not np.isnan(itn_future[i]) and (itn_future[i] < 0 or itn_future[i] > 1)
        ]
        if bad_itn_idx:
            raise ValueError(
                f"itn_future must be between 0 and 1. Bad positions: {bad_itn_idx}"
            )

    if res_future is None or len(res_future) == 0:
        res_future = res_use.copy()
    else:
        res_future = np.asarray(res_future)

    # Validate settings vectors
    n_settings = len(prev)
    if not all(
        len(arr) == n_settings
        for arr in [Q0, phi, season, routine, irs, irs_future, lsm]
    ):
        raise ValueError(
            f"All malaria environment vectors must have the same length as prev ({n_settings})"
        )

    # Validate predictor
    valid_predictors = ["prevalence", "cases"]
    predictor = [p for p in predictor if p in valid_predictors]
    if not predictor:
        raise ValueError("predictor must contain 'prevalence' and/or 'cases'")

    # Generate scenario IDs
    if scenario_tag is None:
        scenario_ids = [f"Scenario{i + 1}" for i in range(n_scenarios)]
    else:
        # Handle single string scenario_tag
        if isinstance(scenario_tag, str):
            scenario_tag = [scenario_tag]
        if len(scenario_tag) != n_scenarios:
            raise ValueError(f"scenario_tag must have length {n_scenarios}")
        scenario_ids = list(scenario_tag)
    
    # Handle single string net_type_future
    if isinstance(net_type_future, str):
        net_type_future = [net_type_future]

    # Build all scenarios
    if benchmark:
        t_start = time.time()

    all_scenarios = []
    eir_values = np.zeros(n_scenarios)

    for i in range(n_scenarios):
        # Calculate net effectiveness for current nets
        try:
            net_now = calculate_overall_dn0(
                resistance_level=res_use[i],
                py_only=py_only[i],
                py_pbo=py_pbo[i],
                py_pyrrole=py_pyrrole[i],
                py_ppf=py_ppf[i],
                itn_params_path=itn_params_path,
            )
        except Exception:
            # If no ITN params available, use simple calculation
            total_itn = py_only[i] + py_pbo[i] + py_pyrrole[i] + py_ppf[i]
            net_now = type("obj", (object,), {"dn0": 0.5 * (1 - res_use[i]), "itn_use": total_itn})()

        # Handle zero ITN use
        if all(v == 0 for v in [py_only[i], py_pbo[i], py_pyrrole[i], py_ppf[i]]):
            net_now = type("obj", (object,), {"dn0": 0, "itn_use": 0})()

        # Calculate net effectiveness for future nets
        if not np.isnan(itn_future[i]) and itn_future[i] == 0:
            net_next = type("obj", (object,), {"dn0": 0, "itn_use": 0})()
        elif net_type_future[i] is None or np.isnan(itn_future[i]):
            try:
                net_next = calculate_overall_dn0(
                    resistance_level=res_future[i],
                    py_only=py_only[i],
                    py_pbo=py_pbo[i],
                    py_pyrrole=py_pyrrole[i],
                    py_ppf=py_ppf[i],
                    itn_params_path=itn_params_path,
                )
            except Exception:
                total_itn = py_only[i] + py_pbo[i] + py_pyrrole[i] + py_ppf[i]
                net_next = type("obj", (object,), {"dn0": 0.5 * (1 - res_future[i]), "itn_use": total_itn})()
        else:
            # Specific future net type
            future_props = {"py_only": 0, "py_pbo": 0, "py_pyrrole": 0, "py_ppf": 0}
            future_props[net_type_future[i]] = itn_future[i]
            try:
                net_next = calculate_overall_dn0(
                    resistance_level=res_future[i],
                    itn_params_path=itn_params_path,
                    **future_props,
                )
            except Exception:
                net_next = type("obj", (object,), {"dn0": 0.5 * (1 - res_future[i]), "itn_use": itn_future[i]})()

        # Predict EIR
        runtime = pd.DataFrame(
            {
                "prevalence": [prev[i]],
                "dn0_use": [net_now.dn0],
                "Q0": [Q0[i]],
                "phi_bednets": [phi[i]],
                "seasonal": [season[i]],
                "itn_use": [net_now.itn_use],
                "irs_use": [irs[i]],
            }
        )

        eir = predict_eir_xgboost(runtime)
        eir_values[i] = eir

        # Calculate effective LSM
        lsm_eff = lsm[i]
        if py_ppf[i] > 0:
            lsm_eff = min(py_ppf[i] * 0.248 + lsm_eff, 1)

        # Store scenario
        all_scenarios.append(
            {
                "eir": eir,
                "dn0_use": net_now.dn0,
                "dn0_future": net_next.dn0,
                "Q0": Q0[i],
                "phi_bednets": phi[i],
                "seasonal": season[i],
                "routine": routine[i],
                "itn_use": net_now.itn_use,
                "irs_use": irs[i],
                "itn_future": net_next.itn_use,
                "irs_future": irs_future[i],
                "lsm": lsm_eff,
                "scenario_id": scenario_ids[i],
            }
        )

    if benchmark:
        bench_times["run_eir_models"] = time.time() - t_start

    # Compute EIR validity
    eir_valid = (eir_values >= 0.68) & (eir_values <= 350.0)

    scenario_meta = pd.DataFrame(
        {"scenario_tag": scenario_ids, "eir_valid": eir_valid}
    )

    # Create scenarios DataFrame
    scenarios_df = pd.DataFrame(all_scenarios)
    scenarios_df = scenarios_df.rename(columns={"scenario_id": "scenario_tag"})

    # Run predictions
    results = MinterResults(scenario_meta=scenario_meta, eir_valid=any(eir_valid))

    if "prevalence" in predictor:
        if benchmark:
            t_start = time.time()

        prevalence_results = run_malaria_emulator(
            scenarios=scenarios_df,
            predictor="prevalence",
            model_types=prevalence_models,
            use_cache=use_cache,
            benchmark=benchmark,
        )

        # Add scenario info
        rows_per_scn = len(prevalence_results) // n_scenarios
        prevalence_results["scenario"] = np.repeat(scenario_ids, rows_per_scn)
        prevalence_results["scenario_tag"] = prevalence_results["scenario"]
        prevalence_results["eir_valid"] = np.repeat(eir_valid, rows_per_scn)

        results.prevalence = prevalence_results

        if benchmark:
            bench_times["run_neural_network_prevalence"] = time.time() - t_start

    if "cases" in predictor:
        if benchmark:
            t_start = time.time()

        cases_results = run_malaria_emulator(
            scenarios=scenarios_df,
            predictor="cases",
            model_types=cases_models,
            use_cache=use_cache,
            benchmark=benchmark,
        )

        # Add scenario info
        rows_per_scn = len(cases_results) // n_scenarios
        cases_results["scenario"] = np.repeat(scenario_ids, rows_per_scn)
        cases_results["scenario_tag"] = cases_results["scenario"]
        cases_results["eir_valid"] = np.repeat(eir_valid, rows_per_scn)

        results.cases = cases_results

        if benchmark:
            bench_times["run_neural_network_cases"] = time.time() - t_start

    # Finalize benchmarks
    if benchmark:
        bench_times["total"] = time.time() - t_total_start
        bench_times["total_scenarios"] = n_scenarios
        results.benchmarks = bench_times

        # Print summary
        print("\n=== Benchmark Results ===")
        if "preload_models" in bench_times:
            print(f"Pre-load models to cache: {bench_times['preload_models']:.3f} seconds")
        print(f"Run EIR predictions ({n_scenarios} scenarios): {bench_times['run_eir_models']:.3f} seconds")

        if "run_neural_network_prevalence" in bench_times:
            print(
                f"Run Prevalence NN ({n_scenarios} scenarios): "
                f"{bench_times['run_neural_network_prevalence']:.3f} seconds"
            )

        if "run_neural_network_cases" in bench_times:
            print(
                f"Run Cases NN ({n_scenarios} scenarios): "
                f"{bench_times['run_neural_network_cases']:.3f} seconds"
            )

        print(f"\nTotal time: {bench_times['total']:.3f} seconds")
        print("=" * 30)

    return results
