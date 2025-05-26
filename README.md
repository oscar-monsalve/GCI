# Grid Convergence Index (GCI)

This code applies the Grid Convergence Index (GCI) method to quantify the grid error for Computational Fluid Dynamics (CFD) applications.

The program asks the user the following:

1. The dimensions of the problem/grid, i.e., 2D or 3D.
2. The grid's number of cells for the fine, medium and coarse grids.
3. The CFD solution for the fine, medium and coarse grids.

- The file "gci/gci_no_prompt.py" is intended for users who prefer to change the input parameters directly in the source code.
- The file "gci/gci_prompt.py" is inteded for users who prefer to be prompted for the input parameters when the code is executed,
  or possibly to create an executable with the ladder file.

Note: this code is at its first implementation iteration, meaning it can be improved.

**Dependencies:**

- prettytable
- matplotlib
- numpy
- pytest (optional for testing).


# TODO

- [x] Add warnings for refinement ratio (r>1.3).
- [x] Add calculations for 1D geometries.
- [ ] Add convergence condition (monotonic convergence, oscillatory conv, etc). If divergent print warning.
- [ ] Add asymptotic range (calculate only if r21 = r32).
- [ ] Add latex, word, markdown tables for reporting results.
- [ ] Calculate results for more than one CFD solution at a time.
- [ ] Add calculations for variable length, area or volume for the simulation domain.
- [ ] Add calculation for local GCI to report error bars on a result along a plane/profile/surface (Last part of Celik, et al.)
