# Grid Convergence Index (GCI)

This code applies the Grid Convergence Index (GCI) method to quantify the grid error for Computational Fluid Dynamics (CFD) applications.

The program asks the user the following:

1. The dimensions of the problem/grid, i.e., 1D, 2D or 3D.
2. The grid's number of cells for the fine, medium and coarse grids.
3. The CFD solution for the fine, medium and coarse grids.

Main program scripts description:

- The file "gci/gci_no_prompt.py" is intended for users who prefer to change the input parameters directly in the source code.
- The file "gci/gci_prompt.py" is inteded for users who prefer to be prompted for the input parameters when the code is executed,
  or possibly to create an executable with the ladder file.

Note: this code is at its first implementation iteration, meaning it can be improved.

## Clone repository

Using git, copy and paste the following command in the terminal:

```shell
git clone https://github.com/oscar-monsalve/GCI.git
cd GCI
```

Dependencies:

- prettytable
- matplotlib
- pytest (optional for testing).

To install dependencies, run the following terminal command:

```shell
pip install -r requirements.txt
```

Run the main program scripts. If the Operating System is Windows, run with `python`. Otherwise, for Linux systems in general:

```shell
python3 gci/no_prompt.py
```

or

```shell
python3 gci/gci_prompt.py
```


# TODO

- [x] Add warnings for refinement ratio (r>1.3).
- [x] Add calculations for 1D geometries.
- [x] Add convergence condition (monotonic convergence, oscillatory conv, etc). If divergent print warning.
- [x] Add asymptotic range (calculate only if r21 = r32).
- [x] Add GCI results within the plot
- [x] Add python libs requirements in a .txt file.
- [x] Calculate desired number of cell for a dersired GCI value.
- [ ] Add calculation for local GCI to report error bars on a result along a plane/profile/surface (Last part of Celik, et al.)
- [ ] Add latex, word, markdown tables for reporting results.
- [ ] Calculate results for more than one CFD solution at a time.
- [ ] Add calculations for variable length, area or volume for the simulation domain.
