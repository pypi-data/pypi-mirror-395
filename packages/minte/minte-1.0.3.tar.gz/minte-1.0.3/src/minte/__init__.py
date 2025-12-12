"""
MINTe - Malaria Intervention Emulator

A neural network-based malaria scenario prediction package for evaluating
intervention strategies including ITNs, IRS, and LSM.
"""

__version__ = "0.1.0"

from .controller import run_minter_scenarios, MinterConfig, MinterResults
from .emulator import (
    run_malaria_emulator,
    load_emulator_models,
    generate_scenario_predictions,
    create_scenarios,
    predict_full_sequence,
    batch_predict_scenarios,
    inverse_transform_np,
    transform_targets_np,
    SchemaAwareLSTM,
)
from .parser import (
    calculate_overall_dn0,
    available_net_types,
    define_bednet_types,
    resistance_to_dn0,
)
from .web_controller import run_mintweb_controller, MintwebResults, format_for_json
from .plotting import create_scenario_plots, plot_emulator_results
from .cache import preload_all_models, get_cached_model, clear_cache

__all__ = [
    # Controller
    "run_minter_scenarios",
    "MinterConfig",
    "MinterResults",
    # Emulator
    "run_malaria_emulator",
    "load_emulator_models",
    "generate_scenario_predictions",
    "create_scenarios",
    "predict_full_sequence",
    "batch_predict_scenarios",
    "inverse_transform_np",
    "transform_targets_np",
    "SchemaAwareLSTM",
    # Parser
    "calculate_overall_dn0",
    "available_net_types",
    "define_bednet_types",
    "resistance_to_dn0",
    # Web controller
    "run_mintweb_controller",
    "MintwebResults",
    "format_for_json",
    # Plotting
    "create_scenario_plots",
    "plot_emulator_results",
    # Cache
    "preload_all_models",
    "get_cached_model",
    "clear_cache",
]