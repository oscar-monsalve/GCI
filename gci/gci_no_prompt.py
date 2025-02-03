# Inputs description:
# 'dimension': Physical dimension of the grid to analyze. Enter "2d", "2D" or "3d", "3D".
# 'n1':        Fine grid cell count
# 'n2':        Medium grid cell count
# 'n3':        Coarse grid cell count
# 'phi1':      CFD solution for the fine gri
# 'phi2':      CFD solution for the medium grid
# 'phi3':      CFD solution for the coarse grid

from numpy import log
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import model

# --------------------------------------Inputs--------------------------------------
# dimension: str = "3d"
# n1:        int = 29284657
# n2:        int = 3673834
# n3:        int = 46071
# phi1:    float = 2198.56
# phi2:    float = 2152.32
# phi3:    float = 2112.79

# ASME's GCI test data:
dimension: str = "2d"
n1:        int = 18000
n2:        int = 8000
n3:        int = 4500
phi1:    float = 6.063
phi2:    float = 5.972
phi3:    float = 5.863
# --------------------------------------Inputs--------------------------------------


def main() -> None:
    f = model.physical_dimension_no_prompt(dimension)
    h1, h2, h3 = model.representative_grid_size(n1, n2, n3, f)
    r21, r32 = model.refinement_factor(h1, h2, h3)
    ep21, ep32, s = model.sign_calculation(phi1, phi2, phi3)

    def fixed_point_iter(apparent_order_function, init_value: int, tol=1e-6, max_iter=100) -> [float, int]:
        """
        Performs a fixed-point iteration and returns its result and the iteration step if within specified tolerance and number of iterations.

        Args:
        aparent_order: function of interest to iterate over it. In this case is the aparent order function.
        init_value: starting point of the iteration process. For the aparent order function, "init_value" could be 1.
        tol, max_iter: stop criteria of the iteration process.
        """
        x = init_value
        for i in range(max_iter):
            x_next = apparent_order_function(x)
            if abs(x_next-x) < tol:
                return x_next, i
            x = x_next
        raise ValueError(f"Failed to converge after {max_iter} iterations")

    def apparent_order_function(init_value: int) -> float:
        """
        Returns the aparent order p.

        Args:
        init_value: iteration variable obtained from the fixed-point iteration.
        """
        return (1/(log(r21)))*(abs(log(ep32/ep21)+log(((r21**init_value)-s)/((r32**init_value)-s))))

    init_value = 1  # Initial value for used in the fixed-point iteration process
    aparent_order, num_iterations = fixed_point_iter(apparent_order_function, init_value)
    phi21_ext, phi32_ext = model.extrapolated_values(phi1, phi2, phi3, r21, r32, aparent_order)  # Extrapolated CFD solutions
    e21_a, e32_a = model.approximate_relative_errors(phi1, phi2, phi3)  # Approximate relative errors
    e21_ext, e32_ext = model.extrapolated_relative_errors(phi1, phi2, phi21_ext, phi32_ext)  # Define the extrapolated relative errors
    gci21_fine, gci32_medium = model.gci(r21, r32, e21_a, e32_a, aparent_order)  # Convergence index results for the fine and medium grids
    # GCI = (gci32_medium)/((r21**aparent_order) * gci21_fine)  # define the approximate constancy GCI

    # Output table summarizing the GCI results using the package "prettytable".
    table = PrettyTable()
    table.field_names = ["Parameters", "Results", "Description"]
    table.add_row(["N1",                n1,                     "Fine grid cell count"])
    table.add_row(["N2",                n2,                     "Medium grid cell count"])
    table.add_row(["N3",                n3,                     "Coarse grid cell count"])
    table.add_row(["r21",               f"{r21:.4f}",           "Medium-to-fine refinement factor"])
    table.add_row(["r32",               f"{r32:.4f}",           "Coarse-to-medium refinement factor"])
    table.add_row(["phi1",              f"{phi1:.4f}",          "Fine grid numerical solution"])
    table.add_row(["phi2",              f"{phi2:.4f}",          "Medium grid numerical solution"])
    table.add_row(["phi1",              f"{phi3:.4f}",          "Coarse grid numerical solution"])
    table.add_row(["p",                 f"{aparent_order:.4f}", "Aparent oder"])
    table.add_row(["phi_ext",           f"{phi21_ext:.4f}",     "Extrapolated solution"])
    table.add_row(["e_21_a (%)",        f"{e21_a:.4f}",         "Medium-to-fine approximate relative error"])
    table.add_row(["e_32_a (%)",        f"{e21_a:.4f}",         "Coarse-to-medium approximate relative error"])
    table.add_row(["e_21_ext (%)",      f"{e21_ext:.4f}",       "Medium-to-fine extrapolated relative error"])
    table.add_row(["e_32_ext (%)",      f"{e32_ext:.4f}",       "Coarse-to-medium extrapolated relative error"])
    table.add_row(["GCI_21_fine (%)",   f"{gci21_fine:.4f}",    "Fine grid convergence index result"])
    table.add_row(["GCI_32_medium (%)", f"{gci32_medium:.4f}",  "Medium grid convergence index result"])
    # table.add_row(["GCI", format(GCI, ".4f")])
    print()
    print("Grid Convergence Index (GCI) results:")
    print(table)

    # Define the variable f to a string to print on the plot result
    if f == 1/2:
        f_print = "1/2"
    if f == 1/3:
        f_print = "1/3"

    # Plotting the grid size h vs. the solution grid value phi
    hi = [h1, h2, h3]
    y = [phi1, phi2, phi3]
    phi_ext_x = [0, h1]
    phi_ext_y = [phi21_ext, phi1]

    plt.plot(hi, y, 'o-k', label=r"Grid solution $\phi_i$")
    plt.plot(0, phi21_ext, '*r', markersize=9, label="Richardson extrapolation")
    plt.plot(phi_ext_x, phi_ext_y, 'r--')

    plt.title(r"$h_i$ vs. $\phi_i$", fontsize=16)
    plt.xlabel(fr"$h_i=\left(  1/N_i \right)^{{{f_print}}}$", fontsize=16)
    plt.ylabel(r"$\phi_i$", fontsize=16)
    plt.legend(fontsize=12)

    plt.xlim(-0.002, None)

    plt.annotate(
        r'$N_1$',
        xy=(h1, phi1),
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=14,
    )

    plt.annotate(
        r'$N_2$',
        xy=(h2, phi2),
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=14,
    )

    plt.annotate(
        r'$N_3$',
        xy=(h3, phi3),
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=14,
    )

    plt.annotate(
        r'$\phi_{ext}^{21}$',
        xy=(0, phi21_ext),
        horizontalalignment='right',
        verticalalignment='top',
        fontsize=14,
    )

    plt.show()
    pass


if __name__ == "__main__":
    main()
