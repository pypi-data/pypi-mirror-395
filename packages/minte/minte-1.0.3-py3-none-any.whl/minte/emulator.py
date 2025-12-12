"""
Neural network emulator for malaria scenario predictions.

This module provides functions for:
- Loading trained LSTM/GRU models
- Running batch predictions for multiple scenarios
- Feature preparation with schema-aware processing

Based on model_helpers_optimized.py from the original R package.
"""

from __future__ import annotations

import json
import logging
import pickle
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Literal

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler

from .cache import get_cached_model, set_cached_model, is_cached

logger = logging.getLogger(__name__)


# ---------------------------
# Target transforms (from model_helpers_optimized.py)
# ---------------------------

def _clip01(x: np.ndarray, eps: float) -> np.ndarray:
    """Clip values to (eps, 1-eps) range."""
    return np.clip(x, eps, 1.0 - eps)


def transform_targets_np(y: np.ndarray, predictor: str, eps: float = 1e-5) -> np.ndarray:
    """Transform targets for model training/inference."""
    if predictor == "prevalence":
        y = _clip01(y, eps)
        return np.log(y / (1.0 - y))  # logit
    else:
        return np.log1p(np.maximum(y, 0.0))


def inverse_transform_np(y: np.ndarray, predictor: str) -> np.ndarray:
    """Inverse transform model outputs to original scale."""
    if predictor == "prevalence":
        return 1.0 / (1.0 + np.exp(-y))  # sigmoid
    else:
        return np.expm1(y)


# ---------------------------
# Schema dataclass
# ---------------------------

@dataclass
class ModelSchema:
    """Schema describing the expected input features for a model."""

    expected_in: int
    cyc: bool = True  # Use cyclical time encoding
    add_year_idx: bool = False  # Add year index feature
    include_lag: bool = False  # Include lagged target
    events_n: int = 0  # Number of event features (0 or 9)
    extra2: int = 0  # Extra post-intervention features (0 or 2)
    has_jump: bool = False  # Has jump connection for events
    use_film: bool = False  # Has FiLM layers


@dataclass
class EmulatorModels:
    """Container for loaded emulator models and configuration."""

    lstm_model: nn.Module
    lstm_schema: ModelSchema
    static_scaler: StandardScaler
    static_covars: list[str]
    after9_covars: list[str]
    intervention_day: int
    use_cyclical_time: bool
    predictor: str
    device: torch.device
    training_args: dict
    models_dir: Path
    eps_prevalence: float = 1e-5
    event_jitter_days: int = 7


# Standard static covariates used by the models
STATIC_COVARS = [
    "eir",
    "dn0_use",
    "dn0_future",
    "Q0",
    "phi_bednets",
    "seasonal",
    "routine",
    "itn_use",
    "irs_use",
    "itn_future",
    "irs_future",
    "lsm",
]

# Covariates that only apply after year 9 (intervention day)
AFTER9_COVARS = ["dn0_future", "itn_future", "irs_future", "lsm", "routine"]


# ---------------------------
# Schema-aware LSTM Model (from model_helpers_optimized.py)
# ---------------------------

class SchemaAwareLSTM(nn.Module):
    """
    LSTM model with schema-aware features.
    
    Supports FiLM conditioning, jump connections for events, and 
    flexible input schemas.
    
    CRITICAL: Uses batch_first=False, so input shape is [T, B, F]
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        dropout_prob: float,
        num_layers: int = 1,
        predictor: str = "prevalence",
        use_film: bool = False,
        has_jump: bool = False,
        events_n: int = 0,
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.predictor = predictor
        self.use_film = use_film
        self.has_jump = has_jump
        self.events_n = events_n

        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers=num_layers,
            dropout=dropout_prob if num_layers > 1 else 0.0,
            batch_first=False,  # CRITICAL: sequence-first [T, B, F]
        )
        self.fc = nn.Linear(hidden_size, output_size)
        self.ln = nn.LayerNorm(hidden_size)
        self.dropout = nn.Dropout(dropout_prob)
        self.activation = nn.Identity()  # No activation in forward pass

        self.film = None
        if self.use_film:
            self.film = nn.Sequential(
                nn.Linear(input_size, 128),
                nn.ReLU(),
                nn.Linear(128, hidden_size * 2),
            )

        self.jump_head = None
        if self.has_jump and events_n == 9:
            self.jump_head = nn.Linear(9, 1, bias=False)

    def _film_gb(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute FiLM gamma and beta from context."""
        ctx = x.mean(dim=0)  # [B, F]
        gamma, beta = torch.chunk(self.film(ctx), 2, dim=-1)
        return gamma.unsqueeze(0), beta.unsqueeze(0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        
        Parameters
        ----------
        x : torch.Tensor
            Input tensor of shape [T, B, F] (sequence-first!)
            
        Returns
        -------
        torch.Tensor
            Output tensor of shape [T, B, 1]
        """
        out, _ = self.lstm(x)

        if self.use_film and self.film is not None:
            gamma, beta = self._film_gb(x)
            out = out * (1 + gamma) + beta

        out = self.ln(out)
        out = self.dropout(out)
        base = self.fc(out)

        if self.has_jump and self.jump_head is not None and self.events_n == 9:
            pulses_block = x[..., -9:]  # Last 9 features are event pulses
            base = base + self.jump_head(pulses_block)

        return self.activation(base)


# Alias for backwards compatibility
LSTMModel = SchemaAwareLSTM


def get_device(device: str | None = None) -> torch.device:
    """Get the appropriate torch device."""
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    return torch.device(device)


# ---------------------------
# Schema inference from checkpoint (from model_helpers_optimized.py)
# ---------------------------

def safe_load_state(path: str | Path, device: torch.device) -> Dict[str, Any]:
    """Load checkpoint safely handling different formats."""
    try:
        ckpt = torch.load(path, map_location=device, weights_only=True)
    except TypeError:
        ckpt = torch.load(path, map_location=device)

    if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
        state = ckpt["model_state_dict"]
    else:
        state = ckpt

    if not isinstance(state, dict):
        raise RuntimeError("Unsupported checkpoint format.")

    return state


def infer_schema_from_state(
    state: Dict[str, Any], 
    static_n: int, 
    use_cyclical_time: bool
) -> ModelSchema:
    """
    Infer the feature schema from checkpoint state dict.
    
    Uses a scoring system to find the best matching feature combination.
    
    Parameters
    ----------
    state : dict
        Model state dictionary.
    static_n : int
        Number of static covariates.
    use_cyclical_time : bool
        Whether cyclical time encoding is expected.
        
    Returns
    -------
    ModelSchema
        Inferred schema with all feature flags.
    """
    # Infer input size from weight matrix
    if "lstm.weight_ih_l0" in state:
        expected_in = int(state["lstm.weight_ih_l0"].shape[1])
    else:
        keys = [k for k in state if k.endswith("weight_ih_l0")]
        if not keys:
            raise RuntimeError("Cannot infer input size: no *weight_ih_l0 in checkpoint.")
        expected_in = int(state[keys[0]].shape[1])

    has_jump = any(k.startswith("jump_head") for k in state.keys())
    use_film = any(k.startswith("film.") for k in state.keys())

    # Try different feature combinations with scoring
    candidates = []
    for cyc in (True, False):
        time_dim = 2 if cyc else 1
        for add_year_idx in (1, 0):
            for include_lag in (1, 0):
                for events_n in (9, 0):
                    for extra2 in (2, 0):
                        total = time_dim + add_year_idx + static_n + include_lag + events_n + extra2
                        if total == expected_in:
                            # Score this combination
                            score = 0
                            if cyc == use_cyclical_time:
                                score += 4
                            if events_n == 9 and has_jump:
                                score += 4
                            if extra2 == 2:
                                score += 5
                            if include_lag == 1:
                                score -= 1  # Lag is less common

                            candidates.append((
                                score,
                                ModelSchema(
                                    expected_in=expected_in,
                                    cyc=cyc,
                                    add_year_idx=bool(add_year_idx),
                                    include_lag=bool(include_lag),
                                    events_n=events_n,
                                    extra2=extra2,
                                    has_jump=has_jump,
                                    use_film=use_film,
                                ),
                            ))

    if not candidates:
        raise RuntimeError(
            f"Could not map checkpoint input size {expected_in} to any feature combination."
        )

    # Sort by score descending and return best match
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def load_model_from_checkpoint(
    checkpoint_path: str | Path,
    static_n: int,
    predictor: str,
    device: torch.device,
    use_cyclical_time: bool = True,
) -> tuple[nn.Module, ModelSchema]:
    """
    Load SchemaAwareLSTM from checkpoint with automatic schema inference.

    Parameters
    ----------
    checkpoint_path : str or Path
        Path to the model checkpoint file.
    static_n : int
        Number of static covariates.
    predictor : str
        Type of predictor ("prevalence" or "cases").
    device : torch.device
        Device to load model on.
    use_cyclical_time : bool
        Whether cyclical time encoding is expected.

    Returns
    -------
    tuple[nn.Module, ModelSchema]
        Loaded model and inferred schema.
    """
    state = safe_load_state(checkpoint_path, device)
    schema = infer_schema_from_state(state, static_n, use_cyclical_time)

    # Infer architecture from state dict
    if "lstm.weight_ih_l0" in state:
        hidden = state["lstm.weight_ih_l0"].shape[0] // 4
        layers = sum(1 for k in state if k.startswith("lstm.weight_ih_l"))
    else:
        wih0 = [k for k in state if k.endswith("weight_ih_l0")]
        hidden = state[wih0[0]].shape[0] // 4
        layers = len({k.split(".")[1] for k in state if k.startswith("lstm.weight_ih_l")})

    model = SchemaAwareLSTM(
        input_size=schema.expected_in,
        hidden_size=hidden,
        output_size=1,
        dropout_prob=0.0,  # No dropout at inference
        num_layers=layers,
        predictor=predictor,
        use_film=schema.use_film,
        has_jump=schema.has_jump,
        events_n=schema.events_n,
    )

    model.load_state_dict(state, strict=True)
    model.to(device).eval()

    logger.info(f"Loaded LSTM: {layers} layers, hidden {hidden}")
    logger.info(f"Schema: {schema}")

    return model, schema


def load_emulator_models(
    models_base_dir: str | Path | None = None,
    predictor: Literal["prevalence", "cases"] = "prevalence",
    device: str | None = None,
    verbose: bool = True,
    force_reload: bool = False,
) -> EmulatorModels:
    """
    Load emulator models with caching support.

    Parameters
    ----------
    models_base_dir : str or Path, optional
        Base directory containing model files.
    predictor : str
        Type of predictor ("prevalence" or "cases").
    device : str, optional
        Device to load models on ("cpu" or "cuda").
    verbose : bool
        Print loading messages.
    force_reload : bool
        Force reload even if cached.

    Returns
    -------
    EmulatorModels
        Container with loaded models and configuration.
    """
    cache_key = f"nn_{predictor}"

    # Check cache
    if not force_reload and is_cached(cache_key):
        if verbose:
            logger.info(f"Using cached {predictor} models")
        return get_cached_model(cache_key)

    # Determine device
    device_obj = get_device(device)
    if verbose:
        logger.info(f"Loading {predictor} models on device: {device_obj}")

    # Find model directory
    if models_base_dir is None:
        package_dir = Path(__file__).parent
        candidates = [
            package_dir / "models",
            package_dir / "data" / "models",
            Path("models"),
        ]
        for path in candidates:
            if path.exists():
                models_base_dir = path
                break

        if models_base_dir is None:
            raise FileNotFoundError("Models directory not found")

    models_base_dir = Path(models_base_dir)
    predictor_models_dir = models_base_dir / predictor

    # Load training args
    args_path = predictor_models_dir / "args.json"
    if not args_path.exists():
        raise FileNotFoundError(f"Could not find args.json in {predictor_models_dir}")

    with open(args_path) as f:
        training_args = json.load(f)

    if verbose:
        logger.info(f"Loaded training parameters from {args_path}")

    # Load scaler
    scaler_path = predictor_models_dir / "static_scaler.pkl"
    with open(scaler_path, "rb") as f:
        static_scaler = pickle.load(f)

    # Model configuration
    use_cyclical_time = training_args.get("use_cyclical_time", True)
    eps_prevalence = training_args.get("eps_prevalence", 1e-5)
    event_jitter_days = training_args.get("event_jitter_days", 7)

    # Load LSTM model
    lstm_path = predictor_models_dir / "lstm_best.pt"
    if verbose:
        logger.info(f"Loading LSTM model from {lstm_path}")

    lstm_model, lstm_schema = load_model_from_checkpoint(
        lstm_path,
        static_n=len(STATIC_COVARS),
        predictor=predictor,
        device=device_obj,
        use_cyclical_time=use_cyclical_time,
    )

    if verbose:
        logger.info(f"LSTM model loaded successfully")
        logger.info(f"Expected input features: {lstm_schema.expected_in}")
        logger.info(
            f"Schema: cyc={lstm_schema.cyc}, year_idx={lstm_schema.add_year_idx}, "
            f"lag={lstm_schema.include_lag}, events={lstm_schema.events_n}, extra2={lstm_schema.extra2}"
        )

    # Create models container
    models = EmulatorModels(
        lstm_model=lstm_model,
        lstm_schema=lstm_schema,
        static_scaler=static_scaler,
        static_covars=STATIC_COVARS,
        after9_covars=AFTER9_COVARS,
        intervention_day=9 * 365,
        use_cyclical_time=use_cyclical_time,
        predictor=predictor,
        device=device_obj,
        training_args=training_args,
        models_dir=predictor_models_dir,
        eps_prevalence=eps_prevalence,
        event_jitter_days=event_jitter_days,
    )

    # Cache the models
    set_cached_model(cache_key, models)

    if verbose:
        logger.info(f"{predictor} models loaded and cached")

    return models


def create_event_pulses(abs_t: np.ndarray, events: list[float], jitter_days: float) -> np.ndarray:
    """Create Gaussian pulse features for intervention events."""
    if len(events) == 0:
        return np.zeros(len(abs_t))

    sig = jitter_days
    result = np.zeros(len(abs_t))

    for i, t in enumerate(abs_t):
        result[i] = sum(np.exp(-0.5 * ((t - e) / sig) ** 2) for e in events)

    return result


def create_time_since(abs_t: np.ndarray, events: list[float]) -> np.ndarray:
    """Create time-since-event features."""
    if len(events) == 0:
        return np.zeros(len(abs_t))

    events = np.array(sorted(events))
    result = np.zeros(len(abs_t))

    for i, t in enumerate(abs_t):
        idx = np.searchsorted(events, t, side="right") - 1
        if idx < 0:
            result[i] = 0
        else:
            result[i] = max(0, (t - events[idx]) / 365)

    return result


def prepare_input_features_schema(
    df: pd.DataFrame,
    models: EmulatorModels,
    window_size: int = 14,
) -> np.ndarray:
    """
    Prepare input features with full schema support.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with timesteps and covariate values.
    models : EmulatorModels
        Loaded models container.
    window_size : int
        Window size in days.

    Returns
    -------
    np.ndarray
        Prepared input features array of shape (T, n_features).
    """
    T_len = len(df)
    abs_t = df["abs_timesteps"].values
    rel_t = df["timesteps"].values
    schema = models.lstm_schema

    # Base static features
    row0 = df.iloc[0]
    base_static = np.array([row0[cov] for cov in models.static_covars], dtype=np.float32)
    raw_matrix = np.tile(base_static, (T_len, 1))

    # Gate future-only covariates before intervention
    post_mask = abs_t >= models.intervention_day
    for cov in models.after9_covars:
        j = models.static_covars.index(cov)
        raw_matrix[~post_mask, j] = 0.0

    # Scale static features
    scaled = models.static_scaler.transform(raw_matrix)

    # Build feature columns based on schema
    cols = []

    # Time encoding
    if schema.cyc:
        day_of_year = abs_t % 365
        sin_t = np.sin(2 * np.pi * day_of_year / 365)
        cos_t = np.cos(2 * np.pi * day_of_year / 365)
        cols.append(np.column_stack([sin_t, cos_t]))
    else:
        t_min, t_max = rel_t.min(), rel_t.max()
        t_norm = (rel_t - t_min) / (t_max - t_min) if t_max > t_min else rel_t
        cols.append(t_norm.reshape(-1, 1))

    # Year index
    if schema.add_year_idx:
        cols.append((abs_t / 365).reshape(-1, 1))

    # Static covariates
    cols.append(scaled)

    # Extra post-intervention features
    if schema.extra2 == 2:
        post9 = (abs_t >= models.intervention_day).astype(np.float32)
        t_since9_years = np.maximum(0, abs_t - models.intervention_day) / 365
        cols.append(np.column_stack([post9, t_since9_years]))

    # Lagged target (if needed)
    if schema.include_lag:
        target_col = "prevalence" if models.predictor == "prevalence" else "cases"
        y = df[target_col].values

        # Transform target
        if models.predictor == "prevalence":
            y_clip = np.clip(y, models.eps_prevalence, 1 - models.eps_prevalence)
            y_tf = np.log(y_clip / (1 - y_clip))
        else:
            y_tf = np.log1p(np.maximum(y, 0))

        y_lag = np.concatenate([[y_tf[0]], y_tf[:-1]])
        cols.append(y_lag.reshape(-1, 1))

    # Event features
    if schema.events_n == 9:
        itn_future = float(row0["itn_future"])

        # ITN events
        if itn_future > 0:
            itn_events = [0, 1095, 2190, 3285]
        else:
            itn_events = [0]

        # IRS events
        irs_all = list(range(0, 4381, 365))
        irs_future = float(row0["irs_future"])
        if irs_future > 0:
            irs_events = irs_all
        else:
            irs_events = [e for e in irs_all if e < models.intervention_day]

        # LSM events
        lsm = float(row0["lsm"])
        lsm_events = [3285] if lsm > 0 else []

        # Create pulse and time-since features
        p_itn = create_event_pulses(abs_t, itn_events, models.event_jitter_days)
        p_irs = create_event_pulses(abs_t, irs_events, models.event_jitter_days)
        p_lsm = create_event_pulses(abs_t, lsm_events, models.event_jitter_days)

        is_post_itn = (abs_t >= models.intervention_day).astype(np.float32) if itn_future > 0 else np.zeros(T_len)
        is_post_irs = (abs_t >= (irs_events[0] if irs_events else 1e9)).astype(np.float32)
        is_post_lsm = (abs_t >= 3285).astype(np.float32) if lsm_events else np.zeros(T_len)

        tau_itn = create_time_since(abs_t, itn_events)
        tau_irs = create_time_since(abs_t, irs_events)
        tau_lsm = create_time_since(abs_t, lsm_events)

        event_matrix = np.column_stack([
            p_itn, p_irs, p_lsm,
            is_post_itn, is_post_irs, is_post_lsm,
            tau_itn, tau_irs, tau_lsm,
        ])
        cols.append(event_matrix)

    # Combine all features
    X = np.hstack(cols)

    # Verify dimensions
    if X.shape[1] != schema.expected_in:
        raise ValueError(
            f"Feature width {X.shape[1]} != checkpoint expected {schema.expected_in}"
        )

    return X.astype(np.float32)


def batch_predict_scenarios(
    model: nn.Module,
    X: np.ndarray,
    device: torch.device,
    predictor: str,
    batch_size: int = 32,
    use_amp: bool = False,
) -> np.ndarray:
    """
    Run batch predictions with the LSTM model.
    
    IMPORTANT: The SchemaAwareLSTM expects input in [T, B, F] format (sequence-first),
    so we need to transpose from the [B, T, F] input format.

    Parameters
    ----------
    model : nn.Module
        Loaded LSTM model.
    X : np.ndarray
        Input features of shape (n_scenarios, n_timesteps, n_features) = [B, T, F].
    device : torch.device
        Device to run inference on.
    predictor : str
        Type of predictor ("prevalence" or "cases").
    batch_size : int
        Batch size for inference.
    use_amp : bool
        Use automatic mixed precision.

    Returns
    -------
    np.ndarray
        Predictions of shape (n_scenarios, n_timesteps).
    """
    model.eval()
    n_scenarios = X.shape[0]
    all_predictions = []

    with torch.no_grad():
        for i in range(0, n_scenarios, batch_size):
            batch_end = min(i + batch_size, n_scenarios)
            batch_data = X[i:batch_end]  # [B, T, F]
            
            # CRITICAL: Transpose to [T, B, F] for sequence-first LSTM
            batch_data = np.transpose(batch_data, (1, 0, 2))  # [T, B, F]
            
            x_batch = torch.tensor(batch_data, dtype=torch.float32).to(device)

            if use_amp and device.type == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.float16):
                    batch_pred = model(x_batch)
            else:
                batch_pred = model(x_batch)

            # Output is [T, B, 1], need to convert to [B, T]
            batch_pred = batch_pred.squeeze(-1).permute(1, 0).cpu().numpy()  # [B, T]
            all_predictions.append(batch_pred)

    predictions = np.concatenate(all_predictions, axis=0)
    
    # Apply inverse transform
    return inverse_transform_np(predictions, predictor)


def predict_full_sequence(
    model: nn.Module,
    full_ts: np.ndarray,
    device: torch.device,
    predictor: str,
    use_amp: bool = False,
) -> np.ndarray:
    """
    Predict on a single sequence.
    
    Parameters
    ----------
    full_ts : np.ndarray
        Input array of shape [T, F].
    device : torch.device
        Device to run inference on.
    predictor : str
        Type of predictor.
    use_amp : bool
        Use automatic mixed precision.
        
    Returns
    -------
    np.ndarray
        Predictions of shape [T] (inverse transformed).
    """
    model.eval()
    with torch.no_grad():
        # Add batch dimension: [T, F] -> [T, 1, F]
        x_torch = torch.tensor(full_ts, dtype=torch.float32).unsqueeze(1).to(device)
        
        if device.type == "cuda" and use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.float16):
                pred = model(x_torch).squeeze(-1).squeeze(-1).cpu().numpy()
        else:
            pred = model(x_torch).squeeze(-1).squeeze(-1).cpu().numpy()
            
    return inverse_transform_np(pred, predictor)


def generate_scenario_predictions_batched(
    scenarios: pd.DataFrame,
    models: EmulatorModels,
    model_types: list[str] = ["LSTM"],
    time_steps: int = 2190,
    window_size: int = 14,
    benchmark: bool = False,
    use_amp: bool = False,
) -> list[dict]:
    """
    Generate predictions for multiple scenarios with batching.

    Parameters
    ----------
    scenarios : pd.DataFrame
        DataFrame with scenario parameters.
    models : EmulatorModels
        Loaded models container.
    model_types : list[str]
        List of model types to use (currently only "LSTM").
    time_steps : int
        Number of time steps in days.
    window_size : int
        Window size in days.
    benchmark : bool
        Track timing information.
    use_amp : bool
        Use automatic mixed precision.

    Returns
    -------
    list[dict]
        List of prediction dictionaries for each scenario.
    """
    bench = {} if benchmark else None
    if benchmark:
        t_start = time.time()

    n_scenarios = len(scenarios)
    n_timesteps = time_steps // window_size

    # Pre-allocate array for all scenarios
    X_all = np.zeros((n_scenarios, n_timesteps, models.lstm_schema.expected_in), dtype=np.float32)

    # Process each scenario
    for i in range(n_scenarios):
        # Create time series
        last_6_years_day = 6 * 365
        abs_t = last_6_years_day + np.arange(n_timesteps) * window_size
        rel_t = np.arange(1, n_timesteps + 1)

        # Build dataframe for this scenario
        df = pd.DataFrame({
            "abs_timesteps": abs_t,
            "timesteps": rel_t,
        })

        # Add static covariates
        for cov in models.static_covars:
            df[cov] = scenarios.iloc[i][cov]

        # Add dummy target for feature prep
        if models.predictor == "prevalence":
            df["prevalence"] = 0.1
        else:
            df["cases"] = 1.0

        # Prepare features
        X_i = prepare_input_features_schema(df, models, window_size)
        X_all[i] = X_i

    if benchmark:
        bench["data_prep"] = time.time() - t_start
        t_start = time.time()

    # Batch predict
    predictions_lstm = batch_predict_scenarios(
        models.lstm_model,
        X_all,
        models.device,
        models.predictor,
        use_amp=use_amp,
    )

    if benchmark:
        bench["python_inference"] = time.time() - t_start

    # Convert to list format
    predictions = []
    for i in range(n_scenarios):
        scenario_preds = {
            "scenario_index": i,
            "timesteps": list(range(1, n_timesteps + 1)),
            "parameters": scenarios.iloc[i].to_dict(),
            "lstm": predictions_lstm[i].tolist(),
        }
        predictions.append(scenario_preds)

    if benchmark:
        # Attach benchmark info
        for p in predictions:
            p["_benchmark"] = bench

    return predictions


def run_malaria_emulator(
    scenarios: pd.DataFrame,
    predictor: Literal["prevalence", "cases"] = "prevalence",
    models_base_dir: str | Path | None = None,
    window_size: int = 14,
    device: str | None = None,
    model_types: list[str] = ["LSTM"],
    time_steps: int = 2190,
    use_cache: bool = True,
    benchmark: bool = False,
    precision: Literal["fp32", "amp"] = "fp32",
) -> pd.DataFrame:
    """
    Run the malaria emulator on a set of scenarios.

    Parameters
    ----------
    scenarios : pd.DataFrame
        DataFrame with scenario parameters.
    predictor : str
        Type of predictor ("prevalence" or "cases").
    models_base_dir : str or Path, optional
        Base directory containing model files.
    window_size : int
        Window size for rolling average in days.
    device : str, optional
        Device to use ("cpu" or "cuda").
    model_types : list[str]
        List of model types to use.
    time_steps : int
        Number of time steps in days.
    use_cache : bool
        Use cached models.
    benchmark : bool
        Track timing information.
    precision : str
        Precision control ("fp32" or "amp").

    Returns
    -------
    pd.DataFrame
        DataFrame with predictions containing columns:
        - index: scenario index
        - timestep: time step number
        - prevalence/cases: predicted value
        - model_type: model type used
    """
    bench = {} if benchmark else None
    if benchmark:
        t_total = time.time()
        t_start = time.time()

    # Validate inputs
    if not isinstance(scenarios, pd.DataFrame):
        raise ValueError("Scenarios must be a DataFrame")
    if len(scenarios) == 0:
        raise ValueError("Scenarios DataFrame is empty")
    if predictor not in ["prevalence", "cases"]:
        raise ValueError("Predictor must be 'prevalence' or 'cases'")

    valid_models = ["LSTM"]
    if not all(m in valid_models for m in model_types):
        raise ValueError(f"Invalid model types. Must be: {', '.join(valid_models)}")

    use_amp = precision == "amp"

    # Load models
    if use_cache:
        cache_key = f"nn_{predictor}"
        models = get_cached_model(cache_key)
        if models is None:
            logger.info(f"Loading and caching {predictor} emulator models...")
            models = load_emulator_models(
                models_base_dir,
                predictor,
                device,
                verbose=False,
            )
        else:
            logger.info(f"Using cached {predictor} models")
    else:
        logger.info("Loading emulator models (cache disabled)...")
        models = load_emulator_models(
            models_base_dir,
            predictor,
            device,
            verbose=False,
            force_reload=True,
        )

    if benchmark:
        bench["model_loading"] = time.time() - t_start

    # Check required columns
    missing_cols = set(models.static_covars) - set(scenarios.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns in scenarios: {missing_cols}")

    logger.info(f"Processing {len(scenarios)} scenarios")
    logger.info(f"Using model types: {', '.join(model_types)}")
    logger.info(f"Generating predictions for {time_steps / 365:.1f} years")

    # Run batched prediction
    if benchmark:
        t_start = time.time()

    predictions = generate_scenario_predictions_batched(
        scenarios=scenarios,
        models=models,
        model_types=model_types,
        time_steps=time_steps,
        window_size=window_size,
        benchmark=benchmark,
        use_amp=use_amp,
    )

    if benchmark:
        bench["neural_network"] = time.time() - t_start
        if predictions and "_benchmark" in predictions[0]:
            bench["nn_details"] = predictions[0]["_benchmark"]

    # Convert to DataFrame
    if benchmark:
        t_start = time.time()

    results_list = []
    for i, pred in enumerate(predictions):
        if "lstm" in pred:
            lstm_df = pd.DataFrame({
                "index": i,
                "timestep": pred["timesteps"],
                predictor: pred["lstm"],
                "model_type": "LSTM",
            })
            results_list.append(lstm_df)

    results = pd.concat(results_list, ignore_index=True)

    if benchmark:
        bench["data_conversion"] = time.time() - t_start
        bench["total"] = time.time() - t_total

        logger.info("\n--- Emulator Performance ---")
        logger.info(f"  Model loading: {bench['model_loading']:.3f} seconds")
        logger.info(f"  Neural network: {bench['neural_network']:.3f} seconds")
        if "nn_details" in bench:
            logger.info(f"    - Data prep: {bench['nn_details']['data_prep']:.3f} seconds")
            logger.info(f"    - Python inference: {bench['nn_details']['python_inference']:.3f} seconds")
        logger.info(f"  Data conversion: {bench['data_conversion']:.3f} seconds")
        logger.info(f"  Total: {bench['total']:.3f} seconds")

    logger.info(f"\nSummary:")
    logger.info(f"  - Mode: Scenario")
    logger.info(f"  - Predictor type: {predictor}")
    logger.info(f"  - Number of scenarios: {len(scenarios)}")
    logger.info(f"  - Model types: {', '.join(model_types)}")
    logger.info(f"  - Time period: {time_steps / 365:.1f} years")
    logger.info(f"  - Total predictions: {len(results)} rows")

    return results


def create_scenarios(**kwargs) -> pd.DataFrame:
    """
    Create a scenarios DataFrame from parameter vectors.

    All parameters must have the same length.

    Parameters
    ----------
    **kwargs
        Named parameter vectors.

    Returns
    -------
    pd.DataFrame
        DataFrame with one row per scenario.

    Examples
    --------
    >>> scenarios = create_scenarios(
    ...     eir=[10, 20],
    ...     dn0_use=[0.5, 0.6],
    ...     # ... other parameters
    ... )
    """
    lengths = [len(v) for v in kwargs.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All scenario parameters must have the same length")

    return pd.DataFrame(kwargs)


def generate_scenario_predictions(
    scenarios: pd.DataFrame,
    models: EmulatorModels,
    model_types: list[str] = ["LSTM"],
    time_steps: int = 2190,
) -> list[dict]:
    """
    Generate predictions for scenarios (convenience wrapper).

    Parameters
    ----------
    scenarios : pd.DataFrame
        DataFrame with scenario parameters.
    models : EmulatorModels
        Loaded models container.
    model_types : list[str]
        List of model types to use.
    time_steps : int
        Number of time steps in days.

    Returns
    -------
    list[dict]
        List of prediction dictionaries.
    """
    return generate_scenario_predictions_batched(
        scenarios=scenarios,
        models=models,
        model_types=model_types,
        time_steps=time_steps,
    )
