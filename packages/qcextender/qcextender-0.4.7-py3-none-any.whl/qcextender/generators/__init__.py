"""
High-level waveform-generation utilities and the central backend registry.

The ``generators`` package exposes the user-facing API for waveform generation.
It defines functions for computing gravitational-wave polarizations and
frequency-domain strains, and manages the backend registry that dispatches to
the appropriate approximant implementation.

Key entry points:
    - :func:`generate_polarizations`: Time-domain (hp, hc, t).
    - :func:`available_waveforms`: A list of the available approximants.

Internal components:
    - :mod:`registry`: Backend registration and lookup.
    - :mod:`backends`: Modules that register approximant implementations.

Design:
    - Backends declare support via the ``@register_backend`` decorator.
    - The registry handles method dispatch and checks for required arguments.
    - Generators normalize inputs to SI conventions before calling a backend.

Importing ``qcextender.generators`` is sufficient to activate all
available backends.
"""

from qcextender.generators import backends  # noqa
from qcextender.generators.registry import generate_polarizations, available_waveforms  # noqa
