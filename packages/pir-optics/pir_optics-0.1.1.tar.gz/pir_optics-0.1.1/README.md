# Purpose

Introduce the concept of **Pixel Impulse Response (PIR)** as a means to predict the expected irradiance distribution for DLP (UV image projection) 3D printing systems.

# Theory & Implementation

See [`src/pir_optics/docs/PIR_theory_summary.md`](src/pir_optics/docs/PIR_theory_summary.md).

# Usage

TBD.

## Run marimo notebook hosted at molab.marimo.io

[Run marimo notebook online](https://molab.marimo.io/notebooks/nb_qvexx3YHiiRo9dVniMLuou/app)

## Test package installation success

Using uv in an arbitrary directory:

```bash
# Create test environment, activate, install package
uv venv test-env
  Using CPython 3.14.0
  Creating virtual environment at: test-env
source test-env/bin/activate
uv pip install pir_optics

# Test that package installation worked
python -m pir_optics.pixel_irradiance

# Clean up
deactivate
rm -rf test-env/
```

