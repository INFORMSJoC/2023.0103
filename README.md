[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# VRPSolverEasy

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[This is a Template](https://doi.org/10.1287/ijoc.2019.0000) by T. Ralphs. 
The snapshot is based on 
[this SHA](https://github.com/tkralphs/JoCTemplate/commit/f7f30c63adbcb0811e5a133e1def696b74f3ba15) 
in the development repository. 

**Important: This code is being developed on an on-going basis at 
https://github.com/tkralphs/JoCTemplate. Please go there if you would like to
get a more recent version or would like support**

## Cite

To cite the contents of this repository, please cite both the paper and this repo, using their respective DOIs.

https://doi.org/10.1287/ijoc.2019.0000

https://doi.org/10.1287/ijoc.2019.0000.cd

Below is the BibTex for citing this snapshot of the respoitory.

```
@article{CacheTest,
  author =        {T. Ralphs},
  publisher =     {INFORMS Journal on Computing},
  title =         {{CacheTest}},
  year =          {2020},
  doi =           {10.1287/ijoc.2019.0000.cd},
  url =           {https://github.com/INFORMSJoC/2019.0000},
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

## Results

Figure 1 in the paper shows the results of the multiplication test with different
values of K using `gcc` 7.5 on an Ubuntu Linux box.

![Figure 1](results/mult-test.png)

Figure 2 in the paper shows the results of the sum test with different
values of K using `gcc` 7.5 on an Ubuntu Linux box.

![Figure 1](results/sum-test.png)

## Replicating

To replicate the results in [Figure 1](results/mult-test), do either

```
make mult-test
```
or
```
python test.py mult
```
To replicate the results in [Figure 2](results/sum-test), do either

```
make sum-test
```
or
```
python test.py sum
```

## Ongoing Development

This code is being developed on an on-going basis at the author's
[Github site](https://github.com/tkralphs/JoCTemplate).

## Support

For support in using this software, submit an
[issue](https://github.com/tkralphs/JoCTemplate/issues/new).
