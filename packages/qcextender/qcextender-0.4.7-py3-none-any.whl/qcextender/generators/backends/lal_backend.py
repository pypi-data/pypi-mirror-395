"""
Waveform generation interface using LALSimulation.

Provides a minimal, extendable interface for generating
gravitational waveforms in the time domain.

All quantities are returned in SI units. Masses are provided in solar
masses, distances in megaparsecs, and spins as dimensionless vectors.

This module is registered automatically into the central approximant registry
via the ``@register_backend`` decorator. Importing this module is sufficient to
enable dispatch through :func:`qcextender.generators.generate_polarizations`.

Constants:
    PC_SI (float): Parsec in meters.
    MSUN_SI (float): Solar mass in kilograms.

Example:
    >>> from qcextender.generators import backends     # triggers registration
    >>> from qcextender.generators.registry import generate_polarizations
    >>> hp, hc, time = generate_polarizations(
    ...     "IMRPhenomD",
    ...     mass1=35, mass2=28,
    ...     distance=500,
    ...     delta_t=1/4096,
    ...     f_lower=20, f_ref=20,
    ...     inclination=0.3, coa_phase=1.1
    ... )
    >>> hp.shape, hc.shape
    ((N,), (N,))
"""

import lal
import lalsimulation as ls
import numpy as np

from qcextender.generators.registry import register_backend

PC_SI: float = 3.085677581491367e16
MSUN_SI: float = 1.9884098706980507e30


APPROXIMANT_OPTIONS = {
    "TaylorT4": {"lambda1", "lambda2", "tide0", "amplitudeO", "phaseO"},
    "EccentricTD": {"amplitude0", "phaseO"},
    "IMRPhenomD": {"extraParams", "NRTidal_version"},
    "SEOBNRv4": {"nk_max", "NRTidal_version"},
}

DEFAULTS = {
    "spin1": [0.0, 0.0, 0.0],
    "spin2": [0.0, 0.0, 0.0],
    "inclination": 0.0,
    "coa_phase": 0.0,
    "long_asc_nodes": 0.0,
    "eccentricity": 0.0,
    "mean_per_ano": 0.0,
    "f_ref": 20.0,
}


@register_backend("TaylorT4", "EccentricTD", "IMRPhenomD", "SEOBNRv4")
def generate_lal_polarizations(
    approximant: str, **kwargs
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate gravitational wave polarizations using LALSimulation for any supported approximant.

    Args:
        approximant (str): Name of the LALSimulation approximant (e.g. "IMRPhenomD", "TaylorT4", "EccentricTD").
        mass1 (float): Primary mass in solar masses.
        mass2 (float): Secondary mass in solar masses.
        distance (float): Luminosity distance to the source in megaparsecs.
        delta_t (float): Sampling interval in seconds.
        f_lower (float): Lower frequency cutoff in Hz.
        spin1 (list[float] | np.ndarray, optional): Dimensionless spin vector (S1x, S1y, S1z). Defaults to [0.0, 0.0, 0.0].
        spin2 (list[float] | np.ndarray, optional): Dimensionless spin vector (S2x, S2y, S2z). Defaults to [0.0, 0.0, 0.0].
        inclination (float, optional): Inclination angle in radians. Defaults to 0.0.
        coa_phase (float, optional): Coalescence phase in radians. Defaults to 0.0.
        long_asc_nodes (float, optional): Longitude of ascending node in radians. Defaults to 0.0.
        eccentricity (float, optional): Orbital eccentricity. Defaults to 0.0.
        mean_per_ano (float, optional): Mean anomaly at reference epoch. Defaults to 0.0.
        f_ref (float, optional): Reference frequency in Hz. Defaults to 0.0.
        **kwargs: Additional model-specific keyword arguments (e.g. `lambda1`, `lambda2`, `phaseO`, `amplitudeO`).

    Raises:
        ValueError: If any required argument (mass1, mass2, distance, delta_t, f_lower, approximant) is missing.
        ValueError: If the provided approximant name is not recognized by LALSimulation.

    Returns:
        tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
            - hp (NDArray[np.floating]): Plus polarization strain.
            - hc (NDArray[np.floating]): Cross polarization strain.
            - time (NDArray[np.floating]): Time samples corresponding to the waveform.
    """

    required = ["mass1", "mass2", "distance", "delta_t", "f_lower"]
    for key in required:
        if key not in kwargs:
            raise ValueError(f"Missing required argument: '{key}'")

    for key, val in DEFAULTS.items():
        kwargs.setdefault(key, val)

    if not hasattr(ls, approximant):
        raise ValueError(f"Unknown approximant '{approximant}'")

    approx_enum = getattr(ls, approximant)

    params = lal.CreateDict()  # type: ignore
    recognized = APPROXIMANT_OPTIONS.get(approximant, set())

    for key, val in kwargs.items():
        if key in recognized:
            if isinstance(val, (float, int)):
                lal.DictInsertREAL8Value(params, key, float(val))  # type: ignore
            elif isinstance(val, bool):
                lal.DictInsertBOOLEANValue(params, key, val)  # type: ignore
            elif isinstance(val, int):
                lal.DictInsertINT4Value(params, key, val)  # type: ignore

    hp, hc = ls.SimInspiralTD(  # type: ignore
        kwargs["mass1"] * MSUN_SI,
        kwargs["mass2"] * MSUN_SI,
        *kwargs["spin1"],
        *kwargs["spin2"],
        kwargs["distance"] * 1e6 * PC_SI,
        kwargs["inclination"],
        kwargs["coa_phase"],
        kwargs["long_asc_nodes"],
        kwargs["eccentricity"],
        kwargs["mean_per_ano"],
        kwargs["delta_t"],
        kwargs["f_lower"],
        kwargs["f_ref"],
        params,
        approx_enum,
    )

    time = np.arange(hp.data.length) * hp.deltaT
    return hp.data.data, hc.data.data, time
