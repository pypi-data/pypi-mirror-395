[![PDBFixer CI Workflow](https://github.com/abhishektiwari/pdbfixer-wheel/actions/workflows/CI.yml/badge.svg)](https://github.com/abhishektiwari/pdbfixer-wheel/actions/workflows/CI.yml)
![PyPI - Version](https://img.shields.io/pypi/v/pdbfixer-wheel)
![Python Wheels](https://img.shields.io/pypi/wheel/pdbfixer-wheel)
![Python Versions](https://img.shields.io/pypi/pyversions/pdbfixer-wheel?logo=python&logoColor=white)
![GitHub last commit](https://img.shields.io/github/last-commit/abhishektiwari/pdbfixer-wheel)
![PyPI - Status](https://img.shields.io/pypi/status/pdbfixer-wheel)

PDBFixer Wheel
==============
This is clone of [PDBFixer](https://github.com/openmm/pdbfixer) package released as [wheel](https://pypi.org/project/pdbfixer-wheel) on to PyPI.

Install PDBFixeruse via PyPI using `pdbfixer-wheel`

```
pip install pdbfixer-wheel
```

PDBFixer
========

PDBFixer is an easy to use application for fixing problems in Protein Data Bank files in preparation for simulating them.  It can automatically fix the following problems:

- Add missing heavy atoms.
- Add missing hydrogen atoms.
- Build missing loops.
- Convert non-standard residues to their standard equivalents.
- Select a single position for atoms with multiple alternate positions listed.
- Delete unwanted chains from the model.
- Delete unwanted heterogens.
- Build a water box for explicit solvent simulations.

See our [manual](https://htmlpreview.github.io/?https://github.com/abhishektiwari/pdbfixer-wheel/blob/master/Manual.html)

## Installation

PDBFixer can be installed with conda or mamba.

```
conda install -c conda-forge pdbfixer
```

Alternatively you can install from source, as described in the manual.

Or install PDBFixeruse via PyPI using `pdbfixer-wheel`

```
pip install pdbfixer-wheel
```
