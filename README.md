[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# VRPSolverEasy

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[VRPSolverEasy: a Python library for the exact
solution of a rich vehicle routing problem](https://doi.org/10.1287/ijoc.2023.0103) by N. Errami, E. Queiroga, R. Sadykov, and E. Uchoa. 

**Important: This code is being developed on an on-going basis at 
https://github.com/inria-UFF/VRPSolverEasy. Please go there if you would like to
get a more recent version or would like support**

## Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2023.0103

https://doi.org/10.1287/ijoc.2023.0103.cd

Below is the BibTex for citing this snapshot of the respoitory.

```
@article{VrpSolverEasyIjoc2023,
  author =        {N. Errami and E. Queiroga and R. Sadykov and E. Uchoa},
  publisher =     {INFORMS Journal on Computing},
  title =         {{VRPSolverEasy: a Python library for the exact solution of a rich vehicle routing problem}},
  year =          {2023},
  doi =           {10.1287/ijoc.2023.0103.cd},
  url =           {https://github.com/INFORMSJoC/2023.0103},
}  
```

## Description

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

To our knowledge, VRPSolver is the most efficient **exact** solver available for VRPs. Its particularity is to focus on finding and improving a **lower bound** on the optimal solution value of your instance. It is less efficient in finding feasible solutions but still can be better than available heuristic solvers for non-classic VRP variants.

## Installation

VRPSolverEasy requires a version of python >= 3.6

> ⚠️ Before starting the installation, update your version of pip:
> ```bash
> python -m pip install --upgrade pip
> ```

### Installation Method

- Download the repository and extract it
- Move to the directory ``src`` and run:
    ```bash
    python -m pip install .
    ```

## Example

A simple example that shows how to use the VRPSolverEasy package:

```python
import VRPSolverEasy as vrpse
import math

def compute_euclidean_distance(x_i, x_j, y_i, y_j):
  """compute the euclidean distance between 2 points from graph"""
    return round(math.sqrt((x_i - x_j)**2 +
                            (y_i - y_j)**2), 3)

# Data
cost_per_distance = 10
begin_time = 0
end_time = 5000
nb_point = 7

# Map with names and coordinates
coordinates = {"Wisconsin, USA": (44.50, -89.50),  # depot
              "West Virginia, USA": (39.000000, -80.500000),
              "Vermont, USA": (44.000000, -72.699997),
              "Texas, the USA": (31.000000, -100.000000),
              "South Dakota, the US": (44.500000, -100.000000),
              "Rhode Island, the US": (41.742325, -71.742332),
              "Oregon, the US": (44.000000, -120.500000)
              }

# Demands of points
demands = [0, 500, 300, 600, 658, 741, 436]

# Initialisation
model = vrpse.Model()

# Add vehicle type
model.add_vehicle_type(
    id=1,
    start_point_id=0,
    end_point_id=0,
    name="VEH1",
    capacity=1100,
    max_number=6,
    var_cost_dist=cost_per_distance,
    tw_end=5000)

# Add depot
model.add_depot(id=0, name="D1", tw_begin=0, tw_end=5000)

coordinates_keys = list(coordinates.keys())
# Add customers
for i in range(1, nb_point):
    model.add_customer(
        id=i,
        name=coordinates_keys[i],
        demand=demands[i],
        tw_begin=begin_time,
        tw_end=end_time)

# Add links
coordinates_values = list(coordinates.values())
for i in range(0, 7):
    for j in range(i + 1, 7):
        dist = compute_euclidean_distance(coordinates_values[i][0],
                                          coordinates_values[j][0],
                                          coordinates_values[i][1],
                                          coordinates_values[j][1])
        model.add_link(
            start_point_id=i,
            end_point_id=j,
            distance=dist,
            time=dist)

# solve model
model.solve()
model.export()

if model.solution.is_defined():
    print(model.solution)
```

## Replicating Experiments

### File Naming Conventions

Scripts in the `scripts` folder follow a naming convention:

- **Problem**: `CVRP`, `CVRPTW`, or `HFVRP`
- **Solver**: `CLP` or `CPLEX`.
- **Upper Bound Source**: `hgs`, `no`, `yes`.
  - `hgs`: Via Hybrid Genetic Search (HGS).
  - `no`: No heuristic upper bound.
  - `yes`: Via OR-Tools.
- **CPLEX Settings**: Specifies whether the CPLEX built-in heuristic is enabled or disabled.
  - `yes_no`: Upper bound from OR-Tools, CPLEX built-in heuristic disabled.
  - `yes_yes`: Upper bound from OR-Tools, CPLEX built-in heuristic enabled.

### Demos options
The demos `CVRP.py`, `CVRPTW.py`, and `HFVRP.py` are called with the following options:

- `-i`: Instance path.
- `-s`: Solver (`CLP` or `CPLEX`).
  - To use `CPLEX`, you'll need to install the academic version of VRPSolverEasy (see the documentation).
- `-u`: Upper bound, whether obtained from OR-Tools or HGS.
- `-e`: Time limit in seconds.
- `-b`: Disables the CPLEX built-in heuristic (set to `yes` to disable, `no` to enable).

### Running Experiments

1. Navigate to `scripts`.
2. Run desired script: `sh script_name.sh`.
3. Output will be written to the `results` folder. The results obtained for the paper are already available there.


### Ongoing Development

This code is being developed on an on-going basis at the author's
[Github site](https://github.com/inria-UFF/VRPSolverEasy).

## Support

For support in using this software, submit an
[issue](https://github.com/inria-UFF/VRPSolverEasy/issues/new).
