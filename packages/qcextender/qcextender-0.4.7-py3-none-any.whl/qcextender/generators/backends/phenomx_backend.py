"""
Waveform generation interface using the PhenomX (IMRPhenomT family) models.

Provides a clean interface for generating time-domain gravitational wave
polarizations using the IMRPhenomT, IMRPhenomTP, and IMRPhenomTHM models via
``phenomxpy`` and ``lalsimulation.gwsignal``.

All quantities are returned in **SI units**. Masses are provided in solar
masses, distances in megaparsecs, and spins as dimensionless vectors.

This module is registered automatically into the central approximant registry
via the ``@register_backend`` decorator. Importing this module is sufficient to
enable dispatch through :func:`qcextender.generators.generate_polarizations`.

Example:
    >>> from qcextender.generators import backends     # triggers registration
    >>> from qcextender.generators.registry import generate_polarizations
    >>> hp, hc, time = generate_polarizations(
    ...     "IMRPhenomTPHM",
    ...     mass1=35, mass2=28,
    ...     distance=500,
    ...     delta_t=1/4096,
    ...     f_lower=20, f_ref=20,
    ...     inclination=0.3, coa_phase=1.1
    ... )
    >>> hp.shape, hc.shape
    ((N,), (N,))
"""

import numpy as np
from numpy.typing import NDArray

from qcextender.generators.registry import register_backend

try:
    from phenomxpy.phenomte import PhenomTE

    imported = True
except ImportError:
    imported = False

if imported:
    PC_SI: float = 3.085677581491367e16
    MSUN_SI: float = 1.9884098706980507e30

    DEFAULTS = {
        "spin1": [0.0, 0.0, 0.0],
        "spin2": [0.0, 0.0, 0.0],
        "inclination": 0.0,
        "coa_phase": 0.0,
        "long_asc_nodes": 0.0,
        "eccentricity": 0.0,
        "mean_per_ano": 0.0,
        "f_ref": 20.0,
        "condition": 0,
    }

    @register_backend("IMRPhenomTE")
    def generate_phenomx_polarizations(
        approximant: str, **kwargs
    ) -> tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
        """
        Generate gravitational-wave polarizations using the PhenomX
        (IMRPhenomT-family) waveform models.

        Args:
            approximant (str): Name of the PhenomX approximant (e.g.
                ``"IMRPhenomT"``, ``"IMRPhenomTPHM"``).
            mass1 (float): Primary mass in solar masses.
            mass2 (float): Secondary mass in solar masses.
            distance (float): Luminosity distance in megaparsecs.
            delta_t (float): Sampling interval in seconds.
            f_lower (float): Starting GW frequency (22-mode) in Hz.
            spin1 (list[float] | np.ndarray, optional): Dimensionless spin
                vector ``[S1x, S1y, S1z]``. Defaults to ``[0.0, 0.0, 0.0]``.
            spin2 (list[float] | np.ndarray, optional): Dimensionless spin
                vector ``[S2x, S2y, S2z]``. Defaults to ``[0.0, 0.0, 0.0]``.
            inclination (float, optional): Inclination angle in radians.
            coa_phase (float, optional): Coalescence phase in radians.
            long_asc_nodes (float, optional): Longitude of the ascending node
                in radians.
            eccentricity (float, optional): Orbital eccentricity.
            mean_per_ano (float, optional): Mean anomaly at reference epoch.
            f_ref (float, optional): Reference frequency in Hz.
            condition (int, optional): Conditioning flag for the PhenomX model.
            **kwargs: Additional model-specific keyword arguments.

        Raises:
            ValueError: If a required argument is missing (``mass1``, ``mass2``,
                ``distance``, ``delta_t``, ``f_lower``).

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

        q = kwargs["mass1"] / kwargs["mass2"]
        if q < 1:
            q = 1 / q

        params = {
            "mode": [2, 2],
            "total_mass": kwargs["mass1"] + kwargs["mass2"],
            "mass_ratio": q,
            "spin1x": kwargs["spin1"][0],
            "spin1y": kwargs["spin1"][1],
            "spin1z": kwargs["spin1"][2],
            "spin2x": kwargs["spin2"][0],
            "spin2y": kwargs["spin2"][1],
            "spin2z": kwargs["spin2"][2],
            "distance": kwargs["distance"],
            "inclination": kwargs["inclination"],
            "phiRef": kwargs["coa_phase"],
            "longAscNodes": kwargs["long_asc_nodes"],
            "eccentricity": kwargs["eccentricity"],
            "meanPerAno": kwargs["mean_per_ano"],
            "deltaT": kwargs["delta_t"],
            "f22_start": kwargs["f_lower"],
            "f22_ref": kwargs["f_ref"],
            "condition": kwargs["condition"],
        }

        hp, hc = PhenomTE(**params).compute_polarizations(**params)  # type: ignore
        time = np.linspace(0, kwargs["delta_t"] * len(hc), len(hc))

        return hp, hc, time
