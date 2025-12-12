"""
Module for loading, storing, and converting dimensionless gravitational waveforms.

This module provides the `DimensionlessWaveform` class, which wraps waveforms
from numerical relativity simulations (e.g., the SXS catalog). It stores
dimensionless time-domain data with associated metadata and allows conversion
to dimensional waveforms in SI units.

Conversions are handled using utility functions from `qcextender.units`, and
metadata is managed using the `Metadata` class. Dimensionless waveforms can be
converted to `Waveform` objects for direct use in physical analyses and model
comparisons.

Example:
    >>> from qcextender.dimensionlesswaveform import DimensionlessWaveform
    >>> dwf = DimensionlessWaveform.from_sim("SXS:BBH:1155")
    >>> wf = dwf.to_Waveform(f_lower=20, total_mass=60, distance=400)
"""

from typing import Self

import numpy as np
import sxs
from numpy.typing import NDArray

from qcextender.basewaveform import BaseWaveform
from qcextender.functions import amp, frequency_window, phase
from qcextender.metadata import Metadata
from qcextender.units import hM_to_hSI, tM_to_tSI
from qcextender.waveform import Waveform


class DimensionlessWaveform(BaseWaveform):
    """
    Represents a dimensionless gravitational waveform from an NR simulation.

    The waveform contains multiple spherical harmonic modes and associated simulation metadata. It can be converted into a dimensional
    `Waveform` object using the `to_Waveform` method.

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
        Initialize a dimensionless waveform object, by passing class attributes to the `BaseWaveform` parent.

        Args:
            strain (NDArray[np.floating]): Stacked array of complex strain modes.
            time (NDArray[np.floating]): Time array (dimensionless units), need to have the same length as strain arrays.
            metadata (Metadata): Simulation metadata describing the waveform.
        """
        super().__init__(strain, time, metadata)

    @classmethod
    def from_sim(cls, sim_id: str, modes: list[tuple[int, int]] = [(2, 2)]) -> Self:
        """
        Loads a dimensionless waveform from an SXS simulation.

        Args:
            sim_id (str): Simulation identifier in the SXS catalog (e.g., "SXS:BBH:1155").
            modes (list[tuple[int, int]]): List of (l, m) modes to include. Defaults to [(2, 2)].

        Raises:
            ValueError: If a requested mode is not available in the simulation.

        Returns:
            DimensionlessWaveform: Waveform object containing the requested modes.
        """
        sim = sxs.load(sim_id, extrapolation="Outer")
        meta = sim.metadata
        meta["modes"] = modes

        q = meta["initial_mass_ratio"]
        if q < 1:
            q = 1 / q

        reference_time = meta.reference_time
        reference_index = sim.h.index_closest_to(reference_time)

        dt = np.min(np.diff(sim.h.t))
        sim = sim.h.interpolate(np.arange(sim.h.t[reference_index], sim.h.t[-1], dt))

        meta.update(
            library="SXS",
            simulation_id=sim_id,
            q=q,
            modes=list(modes),
            delta_t=dt,
            dimensionless=True,
        )

        # Does not properly support multiple modes as of yet
        single_mode_strain = []
        for ell, m in modes:
            try:
                mode = np.array(sim[:, sim.index(ell, m)])

                # Make sure there is no phase difference at the merger (t=0)
                phases, amps = phase(mode), amp(mode)
                phases -= phases[np.argmax(amps)]
                single_mode_strain.append(amps * np.exp(1j * phases))
            except IndexError:
                raise ValueError(f"Mode (l={ell}, m={m}) not found in this simulation.")

        time = cls._align(np.array(sim[:, sim.index(2, 2)]), sim.t)
        multi_mode_strain = np.vstack(single_mode_strain)
        metadata = cls._kwargs_to_metadata(meta)
        return cls(multi_mode_strain, time, metadata)

    def to_Waveform(
        self,
        f_lower: float,
        total_mass: float,
        distance: float,
        inclination: float = 0,
        coa_phase: float = 0,
    ) -> Waveform:
        """
        Convert the dimensionless waveform to a dimensional `Waveform`.

        The conversion scales time and strain using physical parameters such
        as total mass and distance. The resulting waveform is cropped to the longest
        continuous segment where the orbital frequency exceeds `f_lower`.

        Args:
            f_lower (float): Lower frequency bound of the signal [Hz].
            total_mass (float): Total mass of the binary [solar masses].
            distance (float): Luminosity distance to the source [megaparsecs].
            inclination (float, optional): Inclination angle of the system [radians]. Defaults to 0.
            coa_phase (float, optional): Coalescence phase [radians]. Defaults to 0.

        Raises:
            ValueError: If no part of the waveform remains above `f_lower`.

        Returns:
            Waveform: Dimensional waveform object with physical units.
        """
        time = tM_to_tSI(self.time, total_mass)
        metadata = self.metadata.copy()
        newmetadata = metadata.to_dimensional(
            f_lower, total_mass, distance, inclination, coa_phase
        )

        single_mode_strains = []
        for mode in self.metadata.modes:
            singlemode = hM_to_hSI(self[mode], total_mass, distance)

            strain, time = frequency_window(singlemode, time, f_lower)

            phases, amps = phase(strain), amp(strain)
            phases -= phases[np.argmax(amps)]
            single_mode_strains.append(amps * np.exp(1j * phases))

        strain = np.vstack(single_mode_strains)
        return Waveform(strain, time, newmetadata)
