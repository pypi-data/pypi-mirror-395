"""
Core mathematical functions for gravitational waveform analysis.

Provides basic utilities to extract amplitude, phase, and instantaneous
frequency from complex gravitational-wave strains. These functions are
lightweight wrappers around NumPy operations and are intended for use
throughout the `qcextender` package.

Example:
    >>> from qcextender import functions as fn
    >>> strain = np.exp(1j * np.linspace(0, 4*np.pi, 1000))
    >>> fn.amp(strain)[0], fn.phase(strain)[-1]
    (1.0, 12.566370614359172)
"""

from math import factorial

import numpy as np
from numpy.typing import NDArray
from scipy.special import binom


def amp(strain: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Compute the amplitude of a complex strain signal.

    Args:
        strain (NDArray[np.floating]): Complex gravitational-wave strain.

    Returns:
        NDArray[np.floating]: Amplitude |h(t)|.
    """
    return np.abs(strain)


def phase(strain: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Compute the accumulated phase of a complex strain signal.

    Args:
        strain (NDArray[np.floating]): Complex gravitational-wave strain.

    Returns:
        NDArray[np.floating]: Accumulated phase φ(t) [rad].
    """
    return np.unwrap(np.angle(strain))


def omega(
    strain: NDArray[np.floating], time: NDArray[np.floating]
) -> NDArray[np.floating]:
    """
    Compute the instantaneous angular frequency of a strain signal.

    Calculated as the time derivative of the unwrapped phase.

    Args:
        strain (NDArray[np.floating]): Complex gravitational-wave strain.
        time (NDArray[np.floating]): Time array corresponding to the strain samples [s].

    Returns:
        NDArray[np.floating]: Instantaneous angular frequency ω(t) [rad/s].
    """
    return np.gradient(-phase(strain), time)


def spherical_harmonics(
    ell: int,
    m: int,
    iota: float,
    phi: float,
    s: int = -2,
) -> complex:
    """
    Calculates the spin-weighted spherical harmonics. Code adapted from the Spheroidal package.

    Args:
        l (int): Degree of the spherical harmonics.
        m (int): Integer order of the spherical harmonics.
        iota (float): The inclination angle in radians.
        phi (float): The phase of coalescence in radians.
        s (int, optional): Int or half-integer spin-weight.
            Current implementation is limited to integers. Defaults to -2.

    Returns:
        complex: The spin-weighted spherical harmonics of mode (l, m)
    """
    prefactor = (-1.0) ** (ell + m - s + 0j)
    prefactor *= np.sqrt(
        factorial(ell + m)
        * factorial(ell - m)
        * (2 * ell + 1)
        / (4 * np.pi * factorial(ell + s) * factorial(ell - s))
    )

    alternating_sum = 0
    for r in range(int(max(m - s, 0)), int(min(ell - s, ell + m) + 1)):
        alternating_sum += (
            (-1) ** r
            * binom(ell - s, r)
            * binom(ell + s, r + s - m)
            * np.sin(iota / 2) ** (2 * ell - 2 * r - s + m)
            * np.cos(iota / 2) ** (2 * r + s - m)
        )

    return prefactor * np.exp(1j * m * phi) * alternating_sum


def frequency_window(
    strain: NDArray[np.floating], time: NDArray[np.floating], f_lower: float
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Extracts the longest continuous segment of the waveform where the instantaneous
    frequency exceeds a given lower bound.

    This function identifies the region of the strain signal where the angular frequency
    is greater than ``2π * f_lower``, under the assumption that the true waveform remains
    above this threshold longer than any noise component. It then reconstructs the complex
    strain using the amplitude and unwrapped phase corresponding to that region.

    Args:
        strain (NDArray[np.floating]): Complex strain time series.
        time (NDArray[np.floating]): Time array corresponding to the strain samples.
        f_lower (float): Lower frequency cutoff [Hz]. Portions of the signal below
            this threshold are discarded.

    Raises:
        ValueError: If no portion of the waveform remains above ``f_lower`` for
            the given parameters.

    Returns:
        tuple[NDArray[np.floating], NDArray[np.floating]]:
            filtered_strain : NDArray[np.floating]
                Complex strain restricted to the longest contiguous segment where frequency > f_lower.
            filtered_time : NDArray[np.floating]
                Time array corresponding to the filtered strain segment.
    """
    omegas = omega(strain, time)
    amps = amp(strain)
    phases = phase(strain)

    # Takes longest stretch where wave is above f_lower, assumes wave above f_lower is longer than noise above f_lower
    indices = np.where(omegas > 2 * np.pi * f_lower)[0]
    if len(indices) == 0:
        mask = np.array([], dtype=int)
    else:
        breaks = np.where(np.diff(indices) != 1)[0] + 1
        segments = np.split(indices, breaks)

        mask = max(segments, key=len)

    if mask.size == 0:
        raise ValueError(
            "None of the wave remains above f_lower with the chosen parameters."
        )

    return amps[mask] * np.exp(1j * phases[mask]), time[mask]
