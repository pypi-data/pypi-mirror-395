# MINTe - Malaria Intervention Emulator

A Python package for neural network-based malaria scenario predictions, enabling rapid evaluation of intervention strategies including ITNs (Insecticide-Treated Nets), IRS (Indoor Residual Spraying), and LSM (Larval Source Management).

## Features

- **Fast Scenario Predictions**: Run thousands of malaria intervention scenarios in seconds using pre-trained LSTM models
- **Multiple Predictors**: Predict both prevalence and clinical cases
- **Flexible Net Types**: Support for various ITN types (pyrethroid-only, PBO, pyrrole, PPF)
- **Model Caching**: Efficient caching of loaded models for faster subsequent runs
- **Visualization**: Built-in plotting utilities for results visualization
- **Web Interface Support**: Lightweight controller for web application integration

## Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager. Install it first:

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then create a new project and install MINTe:

```bash
# Create a new project directory
mkdir my-malaria-project
cd my-malaria-project

# Initialize a new Python project with uv
uv init

# Add MINTe as a dependency (from local path)
uv add /path/to/minte

# Or from PyPI:
uv add minte
```

### Development Installation

For development, clone the repository and install in editable mode:

```bash
# Clone the repository
git clone https://github.com/CosmoNaught/minte.git
cd minte

# Create virtual environment and install with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Using pip

```bash
pip install minte

# Or for development:
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
import numpy as np
from minte import run_minter_scenarios

# Define a single scenario
results = run_minter_scenarios(
    res_use=[0.3],           # Current resistance level
    py_only=[0.4],           # Pyrethroid-only net coverage
    py_pbo=[0.3],            # PBO net coverage
    py_pyrrole=[0.2],        # Pyrrole net coverage
    py_ppf=[0.1],            # PPF net coverage
    prev=[0.25],             # Current prevalence
    Q0=[0.92],               # Indoor biting proportion
    phi=[0.85],              # Bednet usage proportion
    season=[1],              # Seasonality indicator
    routine=[0.1],           # Routine treatment coverage
    irs=[0.0],               # Current IRS coverage
    irs_future=[0.3],        # Future IRS coverage
    lsm=[0.0],               # LSM coverage
    predictor=["prevalence", "cases"],
)

# Access results
print(results.prevalence.head())
print(results.cases.head())
```

### Running Multiple Scenarios

```python
import numpy as np
from minte import run_minter_scenarios

# Define multiple scenarios
n_scenarios = 100
results = run_minter_scenarios(
    res_use=np.random.uniform(0.1, 0.8, n_scenarios),
    py_only=np.random.uniform(0, 0.5, n_scenarios),
    py_pbo=np.random.uniform(0, 0.3, n_scenarios),
    py_pyrrole=np.random.uniform(0, 0.2, n_scenarios),
    py_ppf=np.random.uniform(0, 0.1, n_scenarios),
    prev=np.random.uniform(0.1, 0.5, n_scenarios),
    Q0=np.full(n_scenarios, 0.92),
    phi=np.full(n_scenarios, 0.85),
    season=np.ones(n_scenarios),
    routine=np.full(n_scenarios, 0.1),
    irs=np.zeros(n_scenarios),
    irs_future=np.random.uniform(0, 0.5, n_scenarios),
    lsm=np.zeros(n_scenarios),
    scenario_tag=[f"Scenario_{i}" for i in range(n_scenarios)],
    benchmark=True,
)
```

### Using the Emulator Directly

```python
import pandas as pd
from minte import run_malaria_emulator, create_scenarios

# Create scenarios DataFrame
scenarios = create_scenarios(
    eir=[50, 100, 150],
    dn0_use=[0.5, 0.4, 0.3],
    dn0_future=[0.6, 0.5, 0.4],
    Q0=[0.92, 0.92, 0.92],
    phi_bednets=[0.85, 0.85, 0.85],
    seasonal=[1, 1, 1],
    routine=[0.1, 0.1, 0.1],
    itn_use=[0.6, 0.5, 0.4],
    irs_use=[0.0, 0.0, 0.0],
    itn_future=[0.7, 0.6, 0.5],
    irs_future=[0.3, 0.3, 0.3],
    lsm=[0.0, 0.0, 0.0],
)

# Run emulator
results = run_malaria_emulator(
    scenarios=scenarios,
    predictor="prevalence",
    benchmark=True,
)
```

### Visualization

```python
from minte import create_scenario_plots

# Create plots from results
plots = create_scenario_plots(
    results.prevalence,
    output_dir="plots/",
    plot_type="both",
)
```

### Web Controller

For web applications, use the simplified controller:

```python
from minte import run_mintweb_controller

results = run_mintweb_controller(
    res_use=[0.3],
    py_only=[0.4],
    py_pbo=[0.3],
    py_pyrrole=[0.2],
    py_ppf=[0.1],
    prev=[0.25],
    Q0=[0.92],
    phi=[0.85],
    season=[1],
    routine=[0.1],
    irs=[0.0],
    irs_future=[0.3],
    lsm=[0.0],
    clean_output=True,
    tabulate=True,
)
```

## Model Files

The package requires trained model files to run predictions. These should be placed in the `src/minte/models/` directory (or specify a custom path) with the following structure:

```
models/
├── prevalence/
│   ├── lstm_best.pt          # PyTorch LSTM checkpoint
│   ├── gru_best.pt           # (optional) GRU checkpoint  
│   ├── static_scaler.pkl     # sklearn StandardScaler
│   └── args.json             # Training arguments
└── cases/
    ├── lstm_best.pt
    ├── gru_best.pt           # (optional)
    ├── static_scaler.pkl
    └── args.json
```

### Converting from R Package Files

If you have the original R package files, you'll need to:

1. **Model files (`.pt`, `.pkl`)**: These are already Python-compatible and can be copied directly.

2. **RDS data files** (e.g., `itn_dn0.rds`): Convert to CSV using one of these methods:

**Method 1: Using the included script (requires rpy2)**
```bash
pip install rpy2
python scripts/convert_rds.py path/to/itn_dn0.rds src/minte/data/itn_dn0.csv
```

**Method 2: Using R directly**
```r
# In R console:
data <- readRDS("path/to/itn_dn0.rds")
write.csv(data, "src/minte/data/itn_dn0.csv", row.names = FALSE)
```

### Expected Data File Locations

```
src/minte/
├── data/
│   └── itn_dn0.csv           # ITN parameters (resistance vs dn0)
└── models/
    ├── prevalence/
    │   └── ...
    └── cases/
        └── ...
```

## Configuration

### Model Caching

Models are cached by default for faster subsequent runs:

```python
from minte import preload_all_models, clear_cache, get_cache_info

# Preload all models
preload_all_models(verbose=True)

# Check what's cached
print(get_cache_info())

# Clear cache if needed
clear_cache()
```

### Device Selection

By default, the package uses CUDA if available:

```python
from minte import load_emulator_models

# Force CPU
models = load_emulator_models(device="cpu")

# Force CUDA
models = load_emulator_models(device="cuda")
```

## API Reference

### Main Functions

- `run_minter_scenarios()`: Main entry point for running intervention scenarios
- `run_malaria_emulator()`: Direct emulator interface for scenario predictions
- `run_mintweb_controller()`: Simplified web interface controller
- `create_scenario_plots()`: Create visualizations from results

### Utility Functions

- `calculate_overall_dn0()`: Calculate net effectiveness from resistance and coverage
- `preload_all_models()`: Pre-load models into cache
- `create_scenarios()`: Helper to create scenarios DataFrame

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black src/
uv run ruff check src/
```

### Type Checking

```bash
uv run mypy src/
```

## License

MIT License - see LICENSE file for details.

## Citation

If you use MINTe in your research, please cite:

```bibtex
@software{minte,
  title = {MINTe: Malaria Intervention Emulator},
  author = {Cosmo Santoni},
  year = {2025},
  url = {https://github.com/CosmoNaught/MINTe-python}
}
```