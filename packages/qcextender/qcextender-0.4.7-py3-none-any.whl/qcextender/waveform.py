"""
Waveform module for quasicircular and extended gravitational-wave models.

This module defines the :class:`Waveform` class, the primary interface for
loading, generating, manipulating, and comparing gravitational waveforms
in the time domain.

The class extends :class:`BaseWaveform` and supports:
    - Generation of multi-modal waveforms from several models.
    - Recombination of spin-weighted spherical-harmonic modes.
    - Match calculations between two waveforms using PyCBC.
    - Conversion to frequency domain.
    - Eccentricity extensions.

Example:
    >>> wf = Waveform.from_model("IMRPhenomD", mass1=30, mass2=25, ...)
    >>> wf2 = Waveform.from_model("SEOBNRv4", mass1=30, mass2=25, ...)
    >>> wf.match(wf2)
"""

from collections.abc import Callable
from typing import Any, Self

import numpy as np
from numpy.typing import NDArray
from pycbc.filter.matchedfilter import match as cbcmatch
from pycbc.psd import aLIGOZeroDetHighPower  # type: ignore
from pycbc.types import FrequencySeries
from pycbc.types import timeseries as ts

from qcextender.basewaveform import BaseWaveform
from qcextender.functions import amp, frequency_window, phase, spherical_harmonics
from qcextender.generators import generate_polarizations
from qcextender.metadata import Metadata


class Waveform(BaseWaveform):
    """
    Class representing multi-modal time-domain gravitational waveforms.

    The :class:`Waveform` class extends :class:`BaseWaveform` and provides utilities
    for generation, manipulation, and comparison of gravitational waveforms. Each
    waveform may consist of multiple spin-weighted spherical-harmonic modes.

    Attributes:
        strain (NDArray[np.floating]): Stacked complex strain data for each mode.
        time (NDArray[np.floating]): Time array corresponding to the waveform.
        metadata (Metadata): Object storing waveform parameters and provenance.
    """

    def __init__(
        self,
        strain: NDArray[np.floating],
        time: NDArray[np.floating],
        metadata: Metadata,
    ) -> None:
        """
        Initializes a waveform object with given strain, time, and metadata.

        Args:
            strain (NDArray[np.floating]): Stacked array of mode strains, one per (l, m) mode.
            time (NDArray[np.floating]): Time array of uniform spacing.
            metadata (Metadata): Metadata containing waveform parameters.
        """
        super().__init__(strain, time, metadata)

    @classmethod
    def from_model(
        cls, approximant: str, modes: list[tuple[int, int]] = [(2, 2)], **kwargs
    ) -> Self:
        """
        Generates a time-domain waveform from a given approximant.

        Uses LALSimulation models (via :func:`lal_mode`) to generate specified
        modes and combines them into a multi-modal waveform.

        Args:
            approximant (str): LALSimulation waveform approximant name (e.g. "IMRPhenomD").
            modes (list[tuple[int, int]], optional): List of (l, m) mode indices to include.
                Currently fixed to ``[(2, 2)]``.
            **kwargs: Additional parameters required by the model, such as ``mass1``, ``mass2``,
                ``spin1``, ``spin2``, ``distance``, ``coa_phase``,``delta_t``, ``f_lower``,
                and ``f_ref``.

        Raises:
            ValueError: If a requested approximant is not made available.

        Returns:
            Waveform: The generated waveform object containing the stacked strain data.
        """
        total_mass = kwargs["mass1"] + kwargs["mass2"]

        q = kwargs["mass1"] / kwargs["mass2"]
        if q < 1:
            q = 1 / q

        kwargs.update(
            library="lalsimulation",
            q=q,
            approximant=approximant,
            modes=[(2, 2)],
            total_mass=total_mass,
        )
        metadata = cls._kwargs_to_metadata(kwargs)

        strain = []

        hp, hc, time = generate_polarizations(**kwargs)
        mode, time = frequency_window(
            (hp - 1j * hc)  # type: ignore
            / spherical_harmonics(2, 2, metadata["inclination"], metadata["coa_phase"]),
            time,
            metadata["f_lower"],
        )

        # Make sure there is no phase difference at the merger (t=0)
        phases, amps = phase(mode), amp(mode)
        phases -= phases[np.argmax(amps)]
        strain.append(amps * np.exp(1j * phases))

        multi_mode_strain = np.vstack(strain)
        time = cls._align(strain[0], time)

        return cls(
            multi_mode_strain,
            time,
            metadata,
        )

    def match(
        self,
        waveform: Self,
        f_lower: float | None = None,
        f_max: float | None = None,
        psd: str = "aLIGOZeroDetHighPower",
    ) -> float:
        """
        Computes the normalized overlap (match) between two waveforms.

        The match quantifies similarity between two real-valued time-domain waveforms,
        taking into account their noise-weighted inner product under a given power
        spectral density (PSD).

        Args:
            waveform (Waveform): Second waveform to compare with ``self``.
            f_lower (float | None, optional): Low-frequency cutoff for the match [Hz].
                Defaults to ``None``, which uses the higher of both waveforms' ``f_lower``.
            f_max (float | None, optional): High-frequency cutoff for the match [Hz].
                Defaults to ``None``.
            psd (str, optional): PSD name. Currently only PyCBC PSD names are supported.
                Defaults to ``"aLIGOZeroDetHighPower"``.

        Returns:
            float: The computed match value between 0 and 1.
        """
        delta_t = max(self.metadata.delta_t, waveform.metadata.delta_t)
        wf1_time = np.arange(self.time[0], self.time[-1], delta_t)
        wf2_time = np.arange(waveform.time[0], waveform.time[-1], delta_t)

        wf1_strain = self.recombine_strain(wf1_time)
        wf2_strain = waveform.recombine_strain(wf2_time)

        wf1 = ts.TimeSeries(wf1_strain.real, delta_t=delta_t)
        wf2 = ts.TimeSeries(wf2_strain.real, delta_t=delta_t)

        if f_lower is None:
            f_lower = max(self.metadata.f_lower, waveform.metadata.f_lower)  # type: ignore

        flen = 1 << (max(len(wf1), len(wf2)) - 1).bit_length()
        delta_f = 1.0 / (flen * delta_t)

        psd = aLIGOZeroDetHighPower(flen, delta_f, f_lower)
        wf1.resize(flen)
        wf2.resize(flen)

        return cbcmatch(
            wf1, wf2, psd=psd, low_frequency_cutoff=f_lower, high_frequency_cutoff=f_max
        )[0]

    def freq(self) -> FrequencySeries:
        """
        Converts the waveform to the frequency domain.

        Returns:
            FrequencySeries: PyCBC's built-in frequency-domain representation
                (complex frequency series).
        """
        delta_t = self.metadata.delta_t
        wf = ts.TimeSeries(self.recombine_strain().real, delta_t=delta_t)

        wfreq = wf.to_frequencyseries()
        return wfreq

    def add_eccentricity(
        self,
        func: Callable[
            [Self, tuple[int, int]],
            tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]],
        ],
        kwargs: dict[str, Any],
        eccentricity: float,
        modes: list[tuple[int, int]] = [(2, 2)],
    ) -> Self:
        """
        Applies an eccentricity correction to the waveform.

        The correction function is user-supplied and returns time, phase, and amplitude.
        The waveform strain is reconstructed from these components.

        Args:
            func (Callable[[Self, tuple[int, int]],
                tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]):
                    Function that takes the waveform and mode, returning ``(time, phase, amplitude)``.
            kwargs (dict[str, Any]): Keyword arguments to be passed on to the supplied function.
            eccentricity (float): Eccentricity value to assign to the new waveform.
            modes (list[tuple[int, int]], optional): Modes to modify. Defaults to ``[(2, 2)]``.

        Returns:
            Waveform: New waveform instance with updated eccentricity and modes.
        """
        strain = []
        for mode in modes:
            time, phase, amplitude = func(self, mode, **kwargs)
            strain.append(amplitude * np.exp(1j * phase))

        metadata = self.metadata.copy()
        metadata.modes = modes
        metadata.eccentricity = eccentricity
        return type(self)(np.vstack(strain), time, metadata)  # type:ignore
