"""
Backend implementations for waveform generation.

This package contains the individual backend modules that wrap external
waveform-generation libraries. Each backend registers one or more approximants
into the central registry when imported.

Included backends:
    - LAL-based TaylorF2 and IMR models.
    - PhenomX (IMRPhenomT, TP, THM, and P/PHM variants).
    - Additional or experimental models as separate modules.

Usage:
    Importing this package triggers registration of all available backends:
        >>> from qcextender.generators import backends
        >>> from qcextender.generators.registry import generate_polarizations
        >>> hp, hc, t = generate_polarizations("IMRPhenomTPHM", mass1=30, ...)

Structure:
    Each backend module:
        - Provides one or more functions to compute hp/hc/time or h(f).
        - Uses consistent SI units and standardized keyword arguments.
        - Registers itself via ``@register_backend``.

The purpose of this package is to keep backend logic isolated while presenting a
uniform interface to the rest of ``qcextender``.
"""

from qcextender.generators.backends import lal_backend, phenomx_backend  # noqa
