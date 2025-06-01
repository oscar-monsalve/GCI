# --------------------------------------Grid Convergence Index (GCI)--------------------------------------
# ----Input description----
# 'dimension': Physical dimension of the grid to analyze. Enter "1", "2", or "3".
# 'n1':        Fine grid cell count
# 'n2':        Medium grid cell count
# 'n3':        Coarse grid cell count
# 'phi1':      CFD solution for the fine gri
# 'phi2':      CFD solution for the medium grid
# 'phi3':      CFD solution for the coarse grid

# ----Input data examples from ASME's article (https://doi.org/10.1115/1.2960953)----
# 2d grid monotonic convergence:
# dimension: str = "2"
# n1:        int = 18000
# n2:        int = 8000
# n3:        int = 4500
# phi1:    float = 6.063
# phi2:    float = 5.972
# phi3:    float = 5.863

# 2d p-value<1 monotonic convergence:
# dimension: str = "2"
# n1:        int = 18000
# n2:        int = 4500
# n3:        int = 980
# phi1:    float = 10.7880
# phi2:    float = 10.7250
# phi3:    float = 10.6050

# 2d grid oscillatory convergence:
# dimension: str = "2"
# n1:        int = 18000
# n2:        int = 4500
# n3:        int = 980
# phi1:    float = 6.0042
# phi2:    float = 5.9624
# phi3:    float = 6.0909

# ----Input 3d grid data examples from master thesis (https://repositorio.itm.edu.co/handle/20.500.12622/6477)----
# 3d grid monotonic convergence:
# dimension: str = "3"
# n1:        int = 2583006
# n2:        int = 678911
# n3:        int = 93188
# phi1:    float = 1.05100
# phi2:    float = 1.03460
# phi3:    float = 0.88580
# --------------------------------------Grid Convergence Index (GCI)--------------------------------------

import matplotlib.pyplot as plt
from prettytable import PrettyTable
import model

# --------------------------------------Inputs--------------------------------------
dimension: str = "3"
n1:        int = 2583006
n2:        int = 678911
n3:        int = 93188
phi1:    float = 1.05100
phi2:    float = 1.03460
phi3:    float = 0.88580
# --------------------------------------Inputs--------------------------------------
# --------------------------------------Inputs--------------------------------------


def main() -> None:
    f = model.physical_dimension_no_prompt(dimension)
    h1, h2, h3 = model.representative_grid_size(n1, n2, n3, f)
    r21, r32 = model.refinement_factor(h1, h2, h3)
    ep21, ep32, s = model.epsilon_and_sign_calculation(phi1, phi2, phi3)

    def apparent_order_wrapper(x):
        """
        Since the "fixed_point_iter" function expects a function with a single argument, this wrapper function is
        defined to pass the additional parameters required.

        Args:
        x: iteration value needed in "apparent_order_function" within the "fixed_point_iter" function.
        """
        return model.apparent_order_function(x, r21, r32, ep21, ep32, s)

    init_value = 1  # Initial value for used in the fixed-point iteration process
    aparent_order, num_iterations = model.fixed_point_iter(apparent_order_wrapper, init_value)
    phi21_ext, phi32_ext = model.extrapolated_values(phi1, phi2, phi3, r21, r32, aparent_order)  # Extrapolated CFD solutions
    e21_a, e32_a = model.approximate_relative_errors(phi1, phi2, phi3)  # Approximate relative errors
    e21_ext, e32_ext = model.extrapolated_relative_errors(phi1, phi2, phi21_ext, phi32_ext)  # Define the extrapolated relative errors
    gci21_fine, gci32_medium = model.gci(r21, r32, e21_a, e32_a, aparent_order)  # Convergence index results for the fine and medium grids
    asympt_range = model.asymptotic_range(gci21_fine, gci32_medium, r21, aparent_order)

    # Output table summarizing the GCI results using the package "prettytable".
    table = PrettyTable()
    table.field_names = ["Parameters", "Results", "Description"]
    table.add_row(["N1",                    n1,                     "Fine grid cell count"])
    table.add_row(["N2",                    n2,                     "Medium grid cell count"])
    table.add_row(["N3",                    n3,                     "Coarse grid cell count"])
    table.add_row(["r21",                   f"{r21:.4f}",           "Medium-to-fine refinement factor"])
    table.add_row(["r32",                   f"{r32:.4f}",           "Coarse-to-medium refinement factor"])
    table.add_row(["phi1",                  f"{phi1:.4f}",          "Fine grid numerical solution"])
    table.add_row(["phi2",                  f"{phi2:.4f}",          "Medium grid numerical solution"])
    table.add_row(["phi1",                  f"{phi3:.4f}",          "Coarse grid numerical solution"])
    table.add_row(["p",                     f"{aparent_order:.4f}", "Aparent oder"])
    table.add_row(["phi_ext",               f"{phi21_ext:.4f}",     "Extrapolated solution"])
    table.add_row(["e_21_a (%)",            f"{e21_a:.4f}",         "Medium-to-fine approximate relative error"])
    table.add_row(["e_32_a (%)",            f"{e21_a:.4f}",         "Coarse-to-medium approximate relative error"])
    table.add_row(["e_21_ext (%)",          f"{e21_ext:.4f}",       "Medium-to-fine extrapolated relative error"])
    table.add_row(["e_32_ext (%)",          f"{e32_ext:.4f}",       "Coarse-to-medium extrapolated relative error"])
    table.add_row(["GCI_21_fine (%)",       f"{gci21_fine:.4f}",    "Fine grid convergence index result"])
    table.add_row(["GCI_32_medium (%)",     f"{gci32_medium:.4f}",  "Medium grid convergence index result"])
    table.add_row(["Asymptotic_range (AR)", f"{asympt_range: .4f}", "A value near 1 indicates mesh convergence and minimal gain from further refinement."])
    # table.add_row(["Notes", "", ""])
    print()

    # Check GCI conditions
    model.check_refinement_factor(r21, r32)
    model.check_convergence_condition(ep21, ep32)

    print()
    print("Grid Convergence Index (GCI) results:")
    print(table)

    # Assign the variable f to a string to print on the plot result
    if f == 1:
        f_print = ""
    if f == 1/2:
        f_print = "1/2"
    if f == 1/3:
        f_print = "1/3"

    # Plotting the grid size h vs. the solution grid value phi
    h1, h2, h3 = h1*1000, h2*1000, h3*1000
    hi = [h1, h2, h3]
    y = [phi1, phi2, phi3]
    phi_ext_x = [0, h1]
    phi_ext_y = [phi21_ext, phi1]

    plt.plot(hi, y, 'o-k', label=r"Grid solution $\phi_i$")
    plt.plot(0, phi21_ext, '*r', markersize=9, label="Richardson extrapolation")
    plt.plot(phi_ext_x, phi_ext_y, 'r--')

    plt.xlabel(fr"$h_i=\left(  1/N_i \right)^{{{f_print}}}\; (\times 10^{{-3}})$", fontsize=16)
    plt.ylabel(r"$\phi_i$", fontsize=16)
    plt.legend(fontsize=10, loc='lower left')
    plt.xticks(range(-2, int(h3)+4, 2), fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlim(-2, int(h3)+2)

    plt.annotate(
        fr'$GCI_{{medium}}^{{32}}={{{gci32_medium:.3f}}}\;\%$',
        xy=(0.015, 0.2),
        xycoords='axes fraction',
        fontsize=14,
    )

    plt.annotate(
        fr'$GCI_{{fine}}^{{21}}={{{gci21_fine:.3f}}}\;\%$',
        xy=(0.015, 0.3),
        xycoords='axes fraction',
        fontsize=14,
    )

    plt.annotate(
        r'$N_1$',
        xy=(1.1*h1, phi1),
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=14,
    )

    plt.annotate(
        r'$N_2$',
        xy=(h2 + 0.1*h1, phi2),
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=14,
    )

    plt.annotate(
        r'$N_3$',
        xy=(h3 + 0.1*h1, phi3),
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


if __name__ == "__main__":
    main()
