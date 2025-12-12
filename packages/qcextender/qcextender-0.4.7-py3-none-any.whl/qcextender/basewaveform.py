"""
Base waveform module for the qcextender package.

Defines the `BaseWaveform` class, which implements common data structures and
operations for all waveform objects. It provides utilities for:
- Mode access and recombination.
- Time alignment.
- Metadata normalization.
- Amplitude, phase, and frequency (omega) computation.

This class is subclassed by `Waveform` and `DimensionlessWaveform` to provide
specific domain behavior (e.g., dimensional vs. dimensionless representations).
"""

from collections.abc import Iterable
from dataclasses import fields

import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import make_interp_spline

from qcextender.functions import amp, omega, phase, spherical_harmonics
from qcextender.metadata import Metadata


class BaseWaveform:
    """
    Base for all Waveform objects, containing all core attributes and methods.

    This class handles generic waveform functionality such as time alignment, strain
    recombination, and metadata normalization. It is not meant to be instantiated
    directly but serves as the foundation for higher-level classes like `Waveform`
    and `DimensionlessWaveform`.

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
        Creates class attributes for the arguments.

        Args:
            strain (NDArray[np.floating]): Stacked array of multi-modal wave strains.
            time (NDArray[np.floating]): Time array, should be the same length as component strain arrays.
            metadata (Metadata): Metadata belonging to the generated or requested waveform.
        """
        self.strain = strain
        self.time = time
        self.metadata = metadata

    def __getitem__(self, mode: tuple[int, int]) -> NDArray[np.floating]:
        """
        Returns the single-mode wave strain corresponding to (l, m).

        Args:
            mode (tuple[int, int]): Spherical harmonics decomposed strain mode.

        Raises:
            ValueError: If this waveform object does not contain the requested mode.

        Returns:
            NDArray[np.floating]: The complex strain for the requested mode.
        """
        modes = self.metadata["modes"]
        try:
            index = modes.index((mode[0], abs(mode[1])))
        except ValueError:
            raise ValueError(f"Mode {mode} not found in this waveform.")

        # For negative m, return the conjugate mode with parity correction
        if mode[1] < 0:
            return (-1) ** mode[0] * np.conj(self.strain[index])
        return self.strain[index]

    @staticmethod
    def _align(
        strain: NDArray[np.floating], time: NDArray[np.floating]
    ) -> NDArray[np.floating]:
        """
        Aligns waveform such that the dominant order peak is at t=0.

        Args:
            strain (NDArray[np.floating]): Waveform strain data.
            time (NDArray[np.floating]): Time array prior to realigning.

        Returns:
            NDArray[np.floating]: New time array aligned to the maximum amplitude.
        """
        time -= time[np.argmax(np.abs(strain))]
        return time

    @staticmethod
    def _kwargs_to_metadata(kwargs: dict[str, str | float | bool | None]) -> Metadata:
        """
        Converts simulation metadata or kwargs into a uniform Metadata object.

        Args:
            kwargs (dict[str, str | float | bool | None]): Keyword arguments used
            to generate waveform or SXS metadata.

        Returns:
            Metadata: Unified object encoding all important metadata fields.
        """
        meta_fields = {f.name for f in fields(Metadata)}

        # Known SXS keys mapped to Metadata object keys
        aliases = {
            "reference_dimensionless_spin1": "spin1",
            "reference_dimensionless_spin2": "spin2",
            "reference_eccentricity": "eccentricity",
        }

        fixed_kwargs = {}
        for k, v in kwargs.items():
            k = aliases.get(k, k)
            if k in meta_fields:
                if k in ("spin1", "spin2") and v is not None:
                    assert isinstance(v, Iterable)
                    fixed_kwargs[k] = tuple(v)  # normalize to tuple
                else:
                    fixed_kwargs[k] = v

        return Metadata(**fixed_kwargs)

    def recombine_strain(
        self, time: NDArray[np.floating] | None = None
    ) -> NDArray[np.floating]:
        """
        Recombines individual (l, m) strain modes into a total observed strain.

        Args:
            time (NDArray[np.floating] | None, optional): Optional new time array
                for resampling via spline interpolation. If None, uses the waveform's
                native time array.

        Returns:
            NDArray[np.floating]: Complex strain representing the full waveform at
                the given inclination and phase.
        """
        strain = 0
        for mode in self.metadata.modes:
            if time is not None:
                single_mode = make_interp_spline(self.time, self[mode])(time)
                single_minus_mode = make_interp_spline(
                    self.time, self[mode[0], -mode[1]]
                )(time)
            else:
                single_mode = self[mode]
                single_minus_mode = self[mode[0], -mode[1]]

            strain += single_mode * spherical_harmonics(
                mode[0], mode[1], self.metadata.inclination, self.metadata.coa_phase
            ) + single_minus_mode * spherical_harmonics(
                mode[0],
                -mode[1],
                self.metadata.inclination,
                self.metadata.coa_phase,
            )

        return strain  # type: ignore

    def amp(self, mode: tuple[int, int] = (2, 2)) -> NDArray[np.floating]:
        """
        Returns the amplitude of the specified mode.

        Args:
            mode (tuple[int, int], optional): Mode for which the amplitude is
            requested. Defaults to (2, 2).

        Returns:
            NDArray[np.floating]: The amplitude of the mode.
        """
        return amp(self[mode])

    def phase(self, mode: tuple[int, int] = (2, 2)) -> NDArray[np.floating]:
        """
        Returns the phase of the specified mode.

        Args:
            mode (tuple[int, int], optional): Mode for which the phase is
            requested. Defaults to (2, 2).

        Returns:
            NDArray[np.floating]: The phase of the mode.
        """
        return phase(self[mode])

    def omega(self, mode: tuple[int, int] = (2, 2)) -> NDArray[np.floating]:
        """
        Returns the angular frequency (omega) of the specified mode.

        Args:
            mode (tuple[int, int], optional): Mode for which the omega is requested.
            Defaults to (2, 2).

        Returns:
            NDArray[np.floating]: The instantaneous angular frequency of the mode.
        """
        return omega(self[mode], self.time)
