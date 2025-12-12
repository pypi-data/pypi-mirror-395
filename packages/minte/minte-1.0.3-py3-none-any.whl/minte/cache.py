"""
Model caching utilities for MINTe.

Provides in-memory caching of loaded models to improve performance
across multiple scenario runs.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Global cache dictionary
_minter_cache: dict[str, Any] = {}


def get_cached_model(model_type: str) -> Any | None:
    """
    Retrieve a cached model by type.

    Parameters
    ----------
    model_type : str
        Type of model to retrieve. Options:
        - "eir_models": XGBoost EIR prediction models
        - "nn_prevalence": Neural network prevalence models
        - "nn_cases": Neural network cases models

    Returns
    -------
    Any or None
        The cached model object, or None if not cached.
    """
    return _minter_cache.get(model_type)


def set_cached_model(model_type: str, model: Any) -> None:
    """
    Store a model in the cache.

    Parameters
    ----------
    model_type : str
        Type identifier for the model.
    model : Any
        The model object to cache.
    """
    _minter_cache[model_type] = model
    logger.debug(f"Cached model: {model_type}")


def clear_cache(model_type: str | None = None) -> None:
    """
    Clear cached models.

    Parameters
    ----------
    model_type : str, optional
        Specific model type to clear. If None, clears all cached models.
    """
    global _minter_cache

    if model_type is None:
        _minter_cache.clear()
        logger.info("Cleared all cached models")
    elif model_type in _minter_cache:
        del _minter_cache[model_type]
        logger.info(f"Cleared cached model: {model_type}")


def is_cached(model_type: str) -> bool:
    """Check if a model type is cached."""
    return model_type in _minter_cache


def preload_all_models(
    models_base_dir: str | None = None,
    device: str | None = None,
    verbose: bool = True,
    force: bool = False,
) -> bool:
    """
    Pre-load all models into cache for faster execution.

    Parameters
    ----------
    models_base_dir : str, optional
        Base directory containing model files.
    device : str, optional
        Device to load models on ("cpu" or "cuda").
    verbose : bool, default True
        Print loading messages.
    force : bool, default False
        Force reload even if already cached.

    Returns
    -------
    bool
        True if all models loaded successfully.
    """
    from .emulator import load_emulator_models

    # Check if already loaded
    if not force:
        all_loaded = (
            is_cached("nn_prevalence")
            and is_cached("nn_cases")
        )
        if all_loaded:
            if verbose:
                logger.info("All models already loaded in cache")
            return True

    if verbose:
        logger.info("Pre-loading all models into cache...")

    # Load neural network models for both predictors
    for predictor in ["prevalence", "cases"]:
        cache_key = f"nn_{predictor}"
        if force or not is_cached(cache_key):
            if verbose:
                logger.info(f"  - Loading {predictor} neural network models...")
            try:
                models = load_emulator_models(
                    models_base_dir=models_base_dir,
                    predictor=predictor,
                    device=device,
                    verbose=False,
                )
                set_cached_model(cache_key, models)
            except Exception as e:
                logger.warning(f"Failed to load {predictor} models: {e}")
        elif verbose:
            logger.info(f"  - {predictor} neural network models already cached")

    if verbose:
        logger.info("All models pre-loaded successfully")

    return True


def get_cache_info() -> dict[str, bool]:
    """
    Get information about what's currently cached.

    Returns
    -------
    dict[str, bool]
        Dictionary mapping model types to whether they are cached.
    """
    return {
        "eir_models": is_cached("eir_models"),
        "nn_prevalence": is_cached("nn_prevalence"),
        "nn_cases": is_cached("nn_cases"),
    }
