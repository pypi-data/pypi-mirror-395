# PyCarmat

A Python toolkit for S-Parameters measurements and material characterization.

## Installation

> **Note:** Use `pip3` instead of `pip` if your system defaults to Python 2.  
> On some Linux distributions, you may need to add `--break-system-packages`.


Install directly from GitLab:

```bash
pip install git+https://gitlab.imt-atlantique.fr/material-sensing-and-simulation/pycarmat.git
```

Install directly from PIP (if and when available):

```bash
pip install pycarmat
```
### Development Mode

```bash
git clone https://gitlab.imt-atlantique.fr/material-sensing-and-simulation/pycarmat.git
cd pycarmat
pip install -e .
```

## Usage

Launch PyCarmat using `python -m pycarmat` (or `python3` on Linux):

```bash
# Main GUI
python -m pycarmat

# Specific applications
python -m pycarmat meas      # Measurement interface
python -m pycarmat epsilon   # Material characterization with thickness validation
python -m pycarmat optim     # Enhanced characterization for multilayer samples
```

> **Note:** The QOSM application (quasi-optical bench simulation and forward model) is available as a button within the main GUI.

## Support

Visit the [GitLab repository](https://gitlab.imt-atlantique.fr/material-sensing-and-simulation/pycarmat) for issues, questions, or contributions.