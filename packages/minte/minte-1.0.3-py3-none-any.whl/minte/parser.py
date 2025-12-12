"""
Bednet parameter parsing and dn0 calculation utilities.

This module provides functions for:
- Loading ITN (insecticide-treated net) parameter files
- Creating spline fits for resistance-to-dn0 conversion
- Calculating weighted average dn0 across net types
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import NamedTuple

import numpy as np
from scipy.interpolate import UnivariateSpline

logger = logging.getLogger(__name__)

# Canonical name mapping for net types
CANONICAL_NET_TYPES = {
    "py_only": "pyrethroid_only",
    "pyrethroid_only": "pyrethroid_only",
    "py_pbo": "pyrethroid_pbo",
    "pyrethroid_pbo": "pyrethroid_pbo",
    "py_pyrrole": "pyrethroid_pyrrole",
    "pyrethroid_pyrrole": "pyrethroid_pyrrole",
    "py_ppf": "pyrethroid_ppf",
    "pyrethroid_ppf": "pyrethroid_ppf",
}


class DN0Result(NamedTuple):
    """Result of dn0 calculation."""

    dn0: float
    itn_use: float


def get_default_itn_params_path() -> Path:
    """Get the default path to ITN parameters file."""
    # Try package data directory
    package_dir = Path(__file__).parent
    candidates = [
        package_dir / "data" / "itn_dn0.csv",
        package_dir / "extdata" / "itn_dn0.csv",
        package_dir / "itn_dn0.csv",
    ]
    for path in candidates:
        if path.exists():
            return path

    raise FileNotFoundError(
        "ITN parameter file not found. Please provide itn_params_path explicitly."
    )


def load_itn_params(itn_params_path: str | Path | None = None) -> dict:
    """
    Load ITN parameters from file.

    Parameters
    ----------
    itn_params_path : str or Path, optional
        Path to the ITN parameters file (CSV or pickle format).

    Returns
    -------
    dict
        Dictionary with 'net_type', 'resistance', and 'dn0' arrays.
    """
    import pandas as pd

    if itn_params_path is None:
        itn_params_path = get_default_itn_params_path()

    path = Path(itn_params_path)

    if not path.exists():
        raise FileNotFoundError(f"ITN parameter file not found: {path}")

    if path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix in (".pkl", ".pickle"):
        df = pd.read_pickle(path)
    elif path.suffix == ".rds":
        # For RDS files, we need to convert or provide CSV alternative
        raise ValueError(
            "RDS files are not directly supported. Please convert to CSV or pickle format."
        )
    else:
        # Try reading as CSV
        df = pd.read_csv(path)

    return {
        "net_type": df["net_type"].values,
        "resistance": df["resistance"].values,
        "dn0": df["dn0"].values,
    }


def available_net_types(itn_params_path: str | Path | None = None) -> list[str]:
    """
    Return the list of net types available in the ITN parameter file.

    Parameters
    ----------
    itn_params_path : str or Path, optional
        Path to the ITN parameters file.

    Returns
    -------
    list[str]
        List of unique net type names.
    """
    params = load_itn_params(itn_params_path)
    return list(np.unique(params["net_type"]))


def define_bednet_types(
    net_types: list[str],
    itn_params_path: str | Path | None = None,
    strict: bool = False,
) -> dict[str, UnivariateSpline]:
    """
    Create spline fits for resistance-to-dn0 conversion for each net type.

    Parameters
    ----------
    net_types : list[str]
        List of net type names to process.
    itn_params_path : str or Path, optional
        Path to the ITN parameters file.
    strict : bool, default False
        If True, raise error for missing net types. If False, warn and skip.

    Returns
    -------
    dict[str, UnivariateSpline]
        Dictionary mapping net type names to fitted spline objects.
    """
    params = load_itn_params(itn_params_path)
    have_types = set(np.unique(params["net_type"]))

    missing = set(net_types) - have_types
    if missing:
        msg = f"No data for net type(s): {', '.join(missing)}"
        if strict:
            raise ValueError(msg)
        logger.warning(f"{msg}. They will be ignored.")
        net_types = [nt for nt in net_types if nt not in missing]

    splines = {}
    for net_type in net_types:
        mask = params["net_type"] == net_type
        resistance = params["resistance"][mask]
        dn0 = params["dn0"][mask]

        # Sort by resistance for proper spline fitting
        sort_idx = np.argsort(resistance)
        resistance = resistance[sort_idx]
        dn0 = dn0[sort_idx]

        # Create spline fit (smoothing spline)
        splines[net_type] = UnivariateSpline(resistance, dn0, s=0)

    return splines


def resistance_to_dn0(spline_fit: UnivariateSpline, resistance_level: float) -> float:
    """
    Convert resistance level to dn0 using a fitted spline.

    Parameters
    ----------
    spline_fit : UnivariateSpline
        Fitted spline object for a net type.
    resistance_level : float
        Resistance level to predict dn0 for.

    Returns
    -------
    float
        Predicted dn0 value.
    """
    return float(spline_fit(resistance_level))


def resistance_to_overall_dn0(
    splines: dict[str, UnivariateSpline],
    usage_values: dict[str, float],
    resistance_level: float,
) -> float:
    """
    Calculate weighted average dn0 across net types.

    Parameters
    ----------
    splines : dict[str, UnivariateSpline]
        Dictionary of spline fits for each net type.
    usage_values : dict[str, float]
        Usage proportions for each net type.
    resistance_level : float
        Resistance level to calculate dn0 for.

    Returns
    -------
    float
        Weighted average dn0 value.
    """
    net_types = list(splines.keys())

    # Validate usage values
    missing = set(usage_values.keys()) - set(net_types)
    if missing:
        raise ValueError(f"usage_values contains net types not in splines: {missing}")

    # Handle zero-weight mix
    total_weight = sum(usage_values.get(nt, 0) for nt in net_types)
    if total_weight == 0:
        return 0.0

    # Calculate weighted average
    dn0_values = []
    weights = []
    for net_type in net_types:
        weight = usage_values.get(net_type, 0)
        if weight > 0:
            dn0 = resistance_to_dn0(splines[net_type], resistance_level)
            dn0_values.append(dn0)
            weights.append(weight)

    return float(np.average(dn0_values, weights=weights))


def calculate_overall_dn0(
    resistance_level: float,
    itn_params_path: str | Path | None = None,
    strict: bool = False,
    **usage_values: float,
) -> DN0Result:
    """
    Calculate overall dn0 in a single call.

    Supply the net-type usage mix as keyword arguments and get:
    - dn0: the weighted-average dn0 at the requested resistance level
    - itn_use: the total usage proportion of pyrethroid-based ITNs

    Parameters
    ----------
    resistance_level : float
        Resistance level (0-1 scale).
    itn_params_path : str or Path, optional
        Path to the ITN parameters file.
    strict : bool, default False
        If True, raise error for missing net types.
    **usage_values : float
        Named usage proportions for each net type.
        Examples: py_only=0.4, py_pbo=0.3, py_pyrrole=0.2, py_ppf=0.1

    Returns
    -------
    DN0Result
        Named tuple with 'dn0' and 'itn_use' fields.

    Examples
    --------
    >>> result = calculate_overall_dn0(
    ...     resistance_level=0.5,
    ...     py_only=0.4,
    ...     py_pbo=0.3,
    ...     py_pyrrole=0.2,
    ...     py_ppf=0.1,
    ... )
    >>> print(f"dn0: {result.dn0:.3f}, itn_use: {result.itn_use:.3f}")
    """
    if not usage_values:
        raise ValueError("You must supply at least one `<net_type>=<value>` pair")

    # Normalize names to canonical form
    canonical_usage = {}
    for name, value in usage_values.items():
        lower_name = name.lower()
        if lower_name not in CANONICAL_NET_TYPES:
            raise ValueError(f"Unknown net type: {name}")
        canonical_name = CANONICAL_NET_TYPES[lower_name]
        canonical_usage[canonical_name] = value

    # Create splines for the requested net types
    splines = define_bednet_types(
        list(canonical_usage.keys()),
        itn_params_path=itn_params_path,
        strict=strict,
    )

    # Calculate weighted dn0
    dn0_val = resistance_to_overall_dn0(splines, canonical_usage, resistance_level)

    # Calculate total ITN use (all pyrethroid-based nets)
    itn_use_val = sum(
        v for k, v in canonical_usage.items() if k.startswith("pyrethroid")
    )

    return DN0Result(dn0=dn0_val, itn_use=itn_use_val)
