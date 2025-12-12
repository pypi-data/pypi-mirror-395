"""
Backend registry and dispatch system for waveform generation.

This module implements a lightweight plugin architecture for waveform
approximants. Backends (e.g., LAL, PhenomX, SEOBNR) register themselves via the
``@register_backend`` decorator, which associates one or more approximant names
with a backend function.

Users interact with the system through :func:`generate_polarizations`, which
dispatches to the correct backend based on the selected approximant. Backends
must return the plus polarization, cross polarization, and corresponding time
array.

The registry is intentionally simple: importing a backend module is enough to
trigger registration, enabling automatic discovery of all available waveform
generators.

Example:
    >>> from qcextender.generators import backends     # triggers registration
    >>> from qcextender.generators.registry import generate_polarizations
    >>> hp, hc, time = generate_polarizations("IMRPhenomD", mass1=30, mass2=30)
    >>> time.shape, hp.shape, hc.shape
    ((16384,), (16384,), (16384,))
"""

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

_APPROXIMANT_REGISTRY: dict[str, Callable] = {}


def register_backend(*approximants: str):
    """
    Register one or more waveform backends for given approximant names.

    This decorator allows backend functions to be associated with a set of
    approximant identifiers. When ``generate_polarizations`` is called with one
    of these names, the corresponding backend function is dispatched.

    Args:
        *approximants (str):
            One or more approximant names to associate with the decorated backend.

    Raises:
        ValueError:
            If any approximant is already registered by another backend.
    """

    def decorator(func: Callable):
        for approx in approximants:
            if approx in _APPROXIMANT_REGISTRY:
                raise ValueError(
                    f"Approximant '{approx}' already registered "
                    f"by {_APPROXIMANT_REGISTRY[approx].__module__}"
                )
            _APPROXIMANT_REGISTRY[approx] = func
        return func

    return decorator


def generate_polarizations(
    approximant: str, **kwargs
) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """
    Generate the polarizations according to `approximant` waveform model.

    Args:
        approximant (str): Waveform model to generate with.

    Raises:
        ValueError:
            Unavailable approximant, prints available approximants.

    Returns:
        tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
            - hp (NDArray[np.floating]): Plus polarization strain.
            - hc (NDArray[np.floating]): Cross polarization strain.
            - time (NDArray[np.floating]): Time samples corresponding to the waveform.
    """
    if approximant not in _APPROXIMANT_REGISTRY:
        available = ", ".join(sorted(_APPROXIMANT_REGISTRY.keys()))
        raise ValueError(
            f"Approximant '{approximant}' is not supported.\nAvailable: {available}"
        )

    backend_fn = _APPROXIMANT_REGISTRY[approximant]
    return backend_fn(approximant=approximant, **kwargs)


def available_waveforms() -> list[str]:
    """
    Returns the available waveform models.

    Returns:
        list[str]: The available waveform models.
    """
    return list(_APPROXIMANT_REGISTRY.keys())
