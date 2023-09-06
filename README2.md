
# VRPSolverEasy

VRPSolverEasy is a Python package which provides a **simple interface for** [VRPSolver](https://vrpsolver.math.u-bordeaux.fr/), a state-of-the-art Branch-Cut-and-Price exact solver for vehicle routing problems (VRPs). The simplified interface is accessible for **users without operations research background**, meaning you do not need to know how to model your problem as an Integer Programming problem. As a price to pay for the simplicity, this interface is restricted to some standard VRP variants, which involve the following features and their combinations:

- capacitated vehicles
- customer time windows
- heterogeneous fleet
- multiple depots
- open routes
- optional customers with penalties
- parallel links to model transition time/cost trade-off
- incompatibilities between vehicles and customers
- customers with alternative locations and/or time windows

## Overview

To our knowledge, VRPSolver is the most efficient **exact** solver available for VRPs. Its particularity is to focus on finding and improving a **lower bound** on the optimal solution value of your instance. It is less efficient in finding feasible solutions but still can be better than available heuristic solvers for non-classic VRP variants.

## License

The VRPSolverEasy package itself is open-source and free to use. It includes compiled libraries of [BaPCod](https://bapcod.math.u-bordeaux.fr/), its VRPSolver extension, and COIN-OR CLP solver. These libraries are also free to use.

## Academic Version

For better performance, it is possible to use VRPSolverEasy together with CPLEX MIP solver. This combination called *academic version* requires an access to the source code of BaPCod available with an [academic-use-only license](https://bapcod.math.u-bordeaux.fr/#licence).

## Accompanying Paper

The paper presents the motivation to create VRPSolverEasy, the interface of the package, the solution approach, the computational results, and possible future extensions. The paper is available as a preprint:

> N. Errami, E. Queiroga, R. Sadykov, E. Uchoa. "VRPSolverEasy: a Python library for the exact solution of a rich vehicle routing problem", [Technical report HAL-04057985](https://hal.inria.fr/hal-04057985/document), 2023.

Please cite it if you use VRPSolverEasy in your research.

## Installation

![Python Logo](https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg)

VRPSolverEasy requires a version of python >= 3.6

> ⚠️ Before starting the installation, update your version of pip:
> ```bash
> python -m pip install --upgrade pip
> ```

Installation instructions for Mac computers with Apple ARM processors,
as well as for the academic version, are given in the documentation.

### Installation Methods

1. Install with `pip`:

   ```bash
   python -m pip install VRPSolverEasy
   ```

2. Or follow these steps:

   - Download the package and extract it
   - Move to the directory and run:
     ```bash
     python pip install .
     ```

## Example

Here's a simple example to show how to use VRPSolverEasy:

```python
# Your Python code here...
```

## Documentation

For more details, check the [official documentation](https://vrpsolvereasy.readthedocs.io/en/latest/).

You can also build the documentation locally:

```bash
cd docs
python -m pip install -r requirements.txt
cd ..
make html
```

The HTML pages will be in the folder `build/html`.