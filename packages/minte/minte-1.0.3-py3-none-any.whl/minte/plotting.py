"""
Plotting utilities for MINT emulator results.

This module provides functions for creating visualizations of
malaria scenario predictions from the emulator.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Color palette for model types
MODEL_COLORS = {
    "GRU": "#E41A1C",
    "LSTM": "#377EB8",
    "LSTM+estiMINT": "#4DAF4A",
    "Actual": "black",
}


def create_scenario_plots(
    results: pd.DataFrame,
    output_dir: str | Path | None = None,
    plot_type: Literal["individual", "combined", "both"] = "both",
    predictor: Literal["prevalence", "cases"] | None = None,
    window_size: int = 14,
    plot_tight: bool = False,
    figsize_combined: tuple[float, float] = (12, 8),
    figsize_individual: tuple[float, float] = (10, 6),
    dpi: int = 300,
) -> dict[str, plt.Figure]:
    """
    Create plots from emulator results.

    Can create either individual plots per scenario or a combined plot
    with all scenarios.

    Parameters
    ----------
    results : pd.DataFrame
        DataFrame with columns: index, timestep, prevalence/cases, model_type, scenario.
    output_dir : str or Path, optional
        Directory to save plots.
    plot_type : str
        Type of plots to create: "individual", "combined", or "both".
    predictor : str, optional
        Predictor type ("prevalence" or "cases"). Auto-detected if None.
    window_size : int
        Days per timestep.
    plot_tight : bool
        Use tight y-axis scaling.
    figsize_combined : tuple
        Figure size for combined plot.
    figsize_individual : tuple
        Figure size for individual plots.
    dpi : int
        DPI for saved figures.

    Returns
    -------
    dict[str, plt.Figure]
        Dictionary mapping plot names to Figure objects.
    """
    # Auto-detect predictor
    if predictor is None:
        if "prevalence" in results.columns:
            predictor = "prevalence"
        elif "cases" in results.columns:
            predictor = "cases"
        else:
            raise ValueError(
                "Cannot determine predictor type. Please specify 'prevalence' or 'cases'."
            )

    # Create output directory if needed
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Calculate timestep range for years 2-6
    start_timestep = int(np.ceil(730 / window_size))  # ~52
    end_timestep = int(np.floor(2190 / window_size))  # ~156

    # Filter to years 2-6 and prepare data
    plot_data = results[
        (results["timestep"] >= start_timestep) & (results["timestep"] <= end_timestep)
    ].copy()

    # Convert timesteps to years (shifted so year 2 becomes 0)
    plot_data["years_raw"] = (plot_data["timestep"] * window_size) / 365
    plot_data["years"] = plot_data["years_raw"] - 2

    # Ensure scenario column exists
    if "scenario" not in plot_data.columns:
        plot_data["scenario"] = plot_data["index"].apply(lambda x: f"Scenario_{x}")

    plots = {}

    # Create combined plot
    if plot_type in ["combined", "both"]:
        fig = _create_combined_scenario_plot(
            plot_data,
            predictor,
            plot_tight,
            figsize_combined,
        )
        plots["combined"] = fig

        if output_dir is not None:
            filename = f"{predictor}_all_scenarios_combined.png"
            filepath = output_dir / filename
            fig.savefig(filepath, dpi=dpi, bbox_inches="tight")
            logger.info(f"Saved combined plot to {filename}")

    # Create individual plots
    if plot_type in ["individual", "both"]:
        unique_scenarios = plot_data["scenario"].unique()

        for scenario in unique_scenarios:
            scenario_data = plot_data[plot_data["scenario"] == scenario]

            fig = _create_individual_scenario_plot(
                scenario_data,
                scenario,
                predictor,
                plot_tight,
                figsize_individual,
            )
            plots[scenario] = fig

            if output_dir is not None:
                # Clean scenario name for filename
                clean_name = "".join(
                    c if c.isalnum() or c in "-_" else "_" for c in scenario
                )
                filename = f"{predictor}_scenario_{clean_name}.png"
                filepath = output_dir / filename
                fig.savefig(filepath, dpi=dpi, bbox_inches="tight")
                logger.info(f"Saved {scenario} plot to {filename}")

    return plots


def _create_combined_scenario_plot(
    plot_data: pd.DataFrame,
    predictor: str,
    plot_tight: bool,
    figsize: tuple[float, float],
) -> plt.Figure:
    """Create a combined plot with all scenarios."""
    fig, ax = plt.subplots(figsize=figsize)

    # Get unique scenarios and create color map
    scenarios = plot_data["scenario"].unique()
    n_scenarios = len(scenarios)
    colors = plt.cm.tab10(np.linspace(0, 1, min(n_scenarios, 10)))

    # Plot each scenario
    for i, scenario in enumerate(scenarios):
        scenario_data = plot_data[plot_data["scenario"] == scenario]
        color = colors[i % len(colors)]

        # Plot each model type
        for model_type in scenario_data["model_type"].unique():
            model_data = scenario_data[scenario_data["model_type"] == model_type]
            linestyle = "-" if model_type == "LSTM" else "--"

            ax.plot(
                model_data["years"],
                model_data[predictor],
                color=color,
                linestyle=linestyle,
                linewidth=1.2,
                alpha=0.8,
                label=f"{scenario} ({model_type})" if i < 6 else None,
            )

    # Styling
    y_label = "Prevalence" if predictor == "prevalence" else "Cases per 1000"

    ax.set_xlabel("Years", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_title(f"All Scenarios - {y_label} Predictions", fontsize=14, fontweight="bold")

    ax.set_xlim(0, 4)
    ax.set_xticks(range(5))

    # Add intervention line
    ax.axvline(x=1, linestyle=":", color="gray", alpha=0.5)

    # Y-axis limits
    if not plot_tight:
        if predictor == "prevalence":
            ax.set_ylim(0, 1)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0%}"))
        else:
            y_max = plot_data[predictor].max() * 1.1
            ax.set_ylim(0, y_max)
    elif predictor == "prevalence":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0%}"))

    # Legend
    if n_scenarios <= 6:
        ax.legend(loc="upper right", fontsize=9)
    else:
        ax.legend(loc="upper right", fontsize=8, ncol=2)

    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    return fig


def _create_individual_scenario_plot(
    scenario_data: pd.DataFrame,
    scenario_name: str,
    predictor: str,
    plot_tight: bool,
    figsize: tuple[float, float],
) -> plt.Figure:
    """Create a plot for a single scenario."""
    fig, ax = plt.subplots(figsize=figsize)

    # Plot each model type
    for model_type in scenario_data["model_type"].unique():
        model_data = scenario_data[scenario_data["model_type"] == model_type]
        color = MODEL_COLORS.get(model_type, "#333333")

        ax.plot(
            model_data["years"],
            model_data[predictor],
            color=color,
            linewidth=1.5,
            label=model_type,
        )

    # Styling
    y_label = "Prevalence" if predictor == "prevalence" else "Cases per 1000"

    ax.set_xlabel("Years", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_title(
        f"{scenario_name} - {y_label} Prediction",
        fontsize=14,
        fontweight="bold",
    )

    ax.set_xlim(0, 4)
    ax.set_xticks(range(5))

    # Add intervention line
    ax.axvline(x=1, linestyle=":", color="gray", alpha=0.5)

    # Y-axis limits
    if not plot_tight:
        if predictor == "prevalence":
            ax.set_ylim(0, 1)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0%}"))
        else:
            y_max = scenario_data[predictor].max() * 1.1
            ax.set_ylim(0, y_max)
    elif predictor == "prevalence":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0%}"))

    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    return fig


def plot_emulator_results(
    csv_file: str | Path,
    output_dir: str | Path | None = None,
    plot_type: Literal["individual", "combined", "both"] = "both",
) -> dict[str, plt.Figure]:
    """
    Quick plot function for loading results from CSV and creating plots.

    Parameters
    ----------
    csv_file : str or Path
        Path to CSV file with emulator results.
    output_dir : str or Path, optional
        Directory to save plots.
    plot_type : str
        Type of plots to create.

    Returns
    -------
    dict[str, plt.Figure]
        Dictionary of created figures.
    """
    results = pd.read_csv(csv_file)

    plots = create_scenario_plots(
        results=results,
        output_dir=output_dir,
        plot_type=plot_type,
    )

    return plots


def plot_comparison(
    results_list: list[pd.DataFrame],
    labels: list[str],
    predictor: Literal["prevalence", "cases"] = "prevalence",
    scenario: str | None = None,
    figsize: tuple[float, float] = (12, 6),
    output_path: str | Path | None = None,
) -> plt.Figure:
    """
    Plot comparison of multiple result sets.

    Useful for comparing different model configurations or scenarios.

    Parameters
    ----------
    results_list : list[pd.DataFrame]
        List of result DataFrames to compare.
    labels : list[str]
        Labels for each result set.
    predictor : str
        Predictor type to plot.
    scenario : str, optional
        Specific scenario to plot. If None, uses first scenario.
    figsize : tuple
        Figure size.
    output_path : str or Path, optional
        Path to save figure.

    Returns
    -------
    plt.Figure
        Comparison figure.
    """
    fig, ax = plt.subplots(figsize=figsize)

    colors = plt.cm.tab10(np.linspace(0, 1, len(results_list)))

    for i, (results, label) in enumerate(zip(results_list, labels)):
        # Filter to specific scenario
        if scenario is not None and "scenario" in results.columns:
            plot_data = results[results["scenario"] == scenario]
        elif "scenario" in results.columns:
            plot_data = results[results["scenario"] == results["scenario"].iloc[0]]
        else:
            plot_data = results

        # Calculate years
        if "timestep" in plot_data.columns:
            years = (plot_data["timestep"] * 14) / 365 - 2
        else:
            years = np.arange(len(plot_data))

        ax.plot(
            years,
            plot_data[predictor],
            color=colors[i],
            linewidth=1.5,
            label=label,
        )

    y_label = "Prevalence" if predictor == "prevalence" else "Cases per 1000"

    ax.set_xlabel("Years", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_title(f"Model Comparison - {y_label}", fontsize=14, fontweight="bold")

    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    if predictor == "prevalence":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.0%}"))

    fig.tight_layout()

    if output_path is not None:
        fig.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig
