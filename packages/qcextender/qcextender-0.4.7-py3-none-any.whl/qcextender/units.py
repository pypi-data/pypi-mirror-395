"""
Utility module for converting between geometric units and SI units.

All functions assume geometric units with G = c = 1 unless otherwise noted.
Conversions are provided for time, frequency, and strain. Each conversion
has a corresponding inverse, ensuring round-trip consistency.

Constants:
    MTSUN_SI (float): Solar mass in seconds [s].
    PC_SI (float): Parsec in meters [m].
    C_SI (float): Speed of light [m/s].

Example:
    >>> from qcextender import units
    >>> units.tM_to_tSI(100, 30)
    0.0147764728429238
"""

from typing import overload

import numpy as np
from numpy.typing import NDArray

MTSUN_SI: float = 4.925490947641267e-06
PC_SI: float = 3.085677581491367e16
C_SI: float = 299792458.0


@overload
def tM_to_tSI(time: float, total_mass: float) -> float: ...
@overload
def tM_to_tSI(
    time: NDArray[np.floating], total_mass: float
) -> NDArray[np.floating]: ...
def tM_to_tSI(time, total_mass):
    """
    Convert geometric time [M] into SI time [s].

    Inverse of `tSI_to_tM`.

    Args:
        time (NDArray[np.floating] | float): Geometric time [M].
        total_mass (float): Total mass of the system [solar masses].

    Returns:
        NDArray[np.floating] | float: Time [s].
    """
    return time * (MTSUN_SI * total_mass)


@overload
def tSI_to_tM(time: float, total_mass: float) -> float: ...
@overload
def tSI_to_tM(
    time: NDArray[np.floating], total_mass: float
) -> NDArray[np.floating]: ...
def tSI_to_tM(time, total_mass):
    """
    Convert SI time [s] into geometric time [M].

    Inverse of `tM_to_tSI`.

    Args:
        time (NDArray[np.floating] | float): Time [s].
        total_mass (float): Total mass of the system [solar masses].

    Returns:
        NDArray[np.floating] | float: Geometric time [M].
    """
    return time / (MTSUN_SI * total_mass)


@overload
def fM_to_fSI(frequency: float, total_mass: float) -> float: ...
@overload
def fM_to_fSI(
    frequency: NDArray[np.floating], total_mass: float
) -> NDArray[np.floating]: ...
def fM_to_fSI(frequency, total_mass):
    """
    Convert geometric frequency [1/M] into SI frequency [Hz].

    Inverse of `fSI_to_fM`.

    Args:
        frequency (NDArray[np.floating] | float): Geometric frequency [1/M].
        total_mass (float): Total mass of the system [solar masses].

    Returns:
        NDArray[np.floating] | float: Frequency [Hz].
    """
    return frequency / (MTSUN_SI * total_mass)


@overload
def fSI_to_fM(frequency: float, total_mass: float) -> float: ...
@overload
def fSI_to_fM(
    frequency: NDArray[np.floating], total_mass: float
) -> NDArray[np.floating]: ...
def fSI_to_fM(frequency, total_mass):
    """
    Convert SI frequency [Hz] into geometric frequency [1/M].

    Inverse of `fM_to_fSI`.

    Args:
        frequency (NDArray[np.floating] | float): Frequency [Hz].
        total_mass (float): Total mass of the system [solar masses].

    Returns:
        NDArray[np.floating] | float: Geometric frequency [1/M].
    """
    return frequency * (MTSUN_SI * total_mass)


def hM_to_hSI(
    strain: NDArray[np.floating], total_mass: float, distance: float
) -> NDArray[np.floating]:
    """
    Convert geometric strain [dimensionless] into SI displacement amplitude [m].

    Inverse of `hSI_to_hM`.

    Args:
        strain (NDArray[np.floating]): Strain in geometric units [dimensionless].
        total_mass (float): Total mass of the system [solar masses].
        distance (float): Luminosity distance to source [Mpc].

    Returns:
        NDArray[np.floating]: Displacement amplitude [m].
    """
    return strain * total_mass * MTSUN_SI * C_SI / (distance * 1e6 * PC_SI)


def hSI_to_hM(
    strain: NDArray[np.floating], total_mass: float, distance: float
) -> NDArray[np.floating]:
    """
    Convert SI displacement amplitude [m] into geometric strain [dimensionless].

    Inverse of `hM_to_hSI`.

    Args:
        strain (NDArray[np.floating]): Displacement amplitude [m].
        total_mass (float): Total mass of the system [solar masses].
        distance (float): Luminosity distance to source [Mpc].

    Returns:
        NDArray[np.floating]: Strain in geometric units [dimensionless].
    """
    return strain / (total_mass * MTSUN_SI * C_SI / (distance * 1e6 * PC_SI))
