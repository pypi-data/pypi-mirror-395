"""
A modular, extensible framework for generating and manipulating
gravitational-wave (GW) waveforms.

Provides:
    - A unified interface for waveform generation across multiple
      backends (LALSimulation, PhenomX, and future models).
    - A minimal abstraction layer (`Waveform`, `DimensionlessWaveform`,
      etc.) for representing waveforms in a consistent format.
    - Tools for registry-based backend dispatching, enabling seamless
      extension through plugin-style waveform generators.
    - Utility functions for unit handling, metadata extraction, and
      waveform-domain conversions.

## Package layout

qcextender/
    generators/
        backends/
            lal_backend.py           - LALSimulation waveform backend
            phenomx_backend.py       - PhenomX/PyIMRPhenomT waveform backend
            __init__.py              - Registry API surface.
        registry.py                  - Backend registry + dispatch logic
        __init__.py                  - Public generator API surface

    basewaveform.py                  - Base waveform container class
    dimensionlesswaveform.py         - Waveform class operating in
                                       dimensionless geometric units
    waveform.py                      - SI-unit waveform class

    units.py                         - Utility helpers for unit scaling,
                                       conversions, and constants

    functions.py                     - Mathematical helper functions:
                                       spherical harmonics, amplitude &
                                       phase functions, etc.

    metadata.py                      - Metadata container and helpers for
                                       annotating waveform objects

    __init__.py                      - Package summary, user-facing namespace

## Feature breakdown

### Core classes

- `BaseWaveform`
  Abstract interface defining the minimal waveform API shared by all
  waveform objects.

- `Waveform`
  SI-unit waveform implementation. Includes storage for strain, time,
  and metadata, and basic convenience methods.

- `DimensionlessWaveform`
  Representation in geometric (G=c=1) units, enabling easy conversions
  and comparisons between models.

### Waveform generation

- Registry-based backend selection
  Backends register themselves with `@register_backend`, enabling
  plug-and-play addition of new waveform families.

- LALSimulation backend
  Supports TaylorT4, EccentricTD, IMRPhenomD, SEOBNRv4 (TD).

- PhenomX backend
  Supports IMRPhenomT / THM / TP / TPHM (TD).

- Unified generator interface
  All backends return `(hp, hc, time)` arrays in SI units unless
  explicitly documented otherwise.

### Mathematical helpers

- Spin-weighted spherical harmonics
- Amplitude and phase construction utilities
- Miscellaneous numerical helpers reused throughout the package

### Units and conversions

- Constants (solar mass, parsec, etc.)
- Conversion utilities between SI and geometric unit systems
- Helpers used during backend interaction and waveform preparation

### Metadata tools

- Metadata object attached to waveforms
- Helpers for validation, inspection, and formatting
- Supports both backend-derived and user-supplied metadata

### Extensibility and design

- Clean separation between interface and implementation
- Backends remain fully isolated and self-contained
- Users can add new backends without modifying package internals


## Backend Philosophy

`qcextender` separates *what* waveform is requested from *how* it is generated.

New backends can be added by:
    1. Implementing a function that returns `(hp, hc, time)` arrays.
    2. Decorating it with ``@register_backend("ApproximantName", ...)``.
    3. Ensuring all quantities are returned in SI units.

This design keeps the interface narrow, stable, and testable.

## Usage Example

```python
from qcextender.waveform import Waveform

wf = Waveform.from_model(
    approximant="IMRPhenomD",
    mass1=30, mass2=25,
    distance=400,
    delta_t=1/4096,
    f_lower=20,
)
```
"""
