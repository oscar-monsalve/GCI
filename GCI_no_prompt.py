from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np


f = 1/2  # Physical grid dimension. f=1/2 for 2D, or f=1/3 for 3D

# Define the grid cell counts
n1 = 18000  # Fine grid
n2 = 8000  # Medium grid
n3 = 4500  # Coarse grid

# Define the representative grid size h
h1 = (1 / n1) ** f
h2 = (1 / n2) ** f
h3 = (1 / n3) ** f

print("The grid size representative values are: ")
print(f"h1: {h1:.4f}")
print(f"h2: {h2:.4f}")
print(f"h3: {h3:.4f}")
print()

# Define the grid refinement factor r
r21 = h2/h1
r32 = h3/h2

print("The grid refiment factors are: ")
print(f"r21: {r21:.4f}")
print(f"r32: {r32:.4f}\n")

# Define the grid solution values
phi1 = 6.063  # Solution for the fine grid
phi2 = 5.972  # Solution for the medium grid
phi3 = 5.863  # Solution for the coarse grid

ep21 = phi2-phi1
ep32 = phi3-phi2

# Define the apparent order p by fixed-point iteration
s = 1*np.sign(ep32/ep21)


def fixedp(g, x0: int, tol=1e-6, max_iter=100) -> [float, int]:
    x = x0
    for i in range(max_iter):
        x_next = g(x)
        if abs(x_next-x) < tol:
            return x_next, i
        x = x_next
    raise ValueError(f"Failed to converge after {max_iter} iterations")


def g(x: float) -> float:
    return (1/(np.log(r21)))*(np.abs(np.log(ep32/ep21)+np.log(((r21**x)-s)/((r32**x)-s))))


x0 = 1
x, num_iterations = fixedp(g, x0)

print(f"The apparent order is p: {x:.4f}. Converged after {num_iterations} iterations\n")

# Define the extrapolated values
phi21_ext = (((r21**x)*phi1)-phi2)/((r21**x)-1)
phi32_ext = (((r32**x)*phi2)-phi3)/((r32**x)-1)

print("The extrapolated grid solution values are: ")
print(f"phi21_ext: {phi21_ext:.4f}")
print(f"phi32_ext: {phi32_ext:.4f}\n")

# Define the approximate relative errors
e21_a = (np.abs((phi1-phi2)/phi1))*100
e32_a = (np.abs((phi2-phi3)/phi2))*100

print("The approximate relative errors are: ")
print(f"e21_a: {e21_a:.4f} %")
print(f"e32_a: {e32_a:.4f} %\n")

# Define the extrapolated relative errors
e21_ext = (np.abs((phi21_ext-phi1)/phi21_ext))*100
e32_ext = (np.abs((phi32_ext-phi2)/phi32_ext))*100

print("The extrapolated relative errors are: ")
print(f"e21_ext: {e21_ext:.4f} %")
print(f"e32_ext: {e32_ext:.4f} %\n")

# Define the GCI values for the fine and medium grids
GCI21_fine = ((1.25*e21_a)/((r21**x)-1))
GCI32_medium = ((1.25*e32_a)/((r32**x)-1))

print("The Grid Convergence Index (GCI) values are: ")
print(f"GCI21_fine: {GCI21_fine:.4f} %")
print(f"GCI32_medium: {GCI32_medium:.4f} %\n")

# define the approximate constancy GCI
GCI = (GCI32_medium)/((r21**x) * GCI21_fine)

print(f"The approximate constancy GCI is: {GCI:.4f}\n")
print("Note: If GCI is approximately equal to 1, the grid solution is within the asymptotic range of convergence. Thus, no further grid refinement is neccesary.")

# Output table summarizing the GCI results using the package "prettytable".
table = PrettyTable()
table.field_names = ["Parameters", "Results for grid solution phi"]

table.add_row(["N1", n1])
table.add_row(["N2", n2])
table.add_row(["N3", n3])
table.add_row(["r21", format(r21, ".4f")])
table.add_row(["r32", format(r32, ".4f")])
table.add_row(["phi1", format(phi1, ".4f")])
table.add_row(["phi2", format(phi2, ".4f")])
table.add_row(["phi1", format(phi3, ".4f")])
table.add_row(["p", format(x, ".4f")])
table.add_row(["phi_ext", format(phi21_ext, ".4f")])
table.add_row(["e_21_a (%)", format(e21_a, ".4f")])
table.add_row(["e_32_a (%)", format(e21_a, ".4f")])
table.add_row(["e_21_ext (%)", format(e21_ext, ".4f")])
table.add_row(["e_32_ext (%)", format(e32_ext, ".4f")])
table.add_row(["GCI_21_fine (%)", format(GCI21_fine, ".4f")])
table.add_row(["GCI_32_medium (%)", format(GCI32_medium, ".4f")])
table.add_row(["GCI", format(GCI, ".4f")])
print()
print("The following table summarizes the GCI results")
print(table)

# Plotting the grid size h vs. the solution grid value phi

hi = [h1, h2, h3]
y = [phi1, phi2, phi3]
phi_ext_x = [0, h1]
phi_ext_y = [phi21_ext, phi1]

plt.plot(hi, y, 'o-k', label=r"Grid solution $\phi_i$")
plt.plot(0, phi21_ext, '*r', markersize=9, label="Richardson extrapolation")
plt.plot(phi_ext_x, phi_ext_y, 'r--')

plt.title(r"$h_i$ vs. $\phi_i$", fontsize=16)
plt.xlabel(fr"$h_i=\left(  1/N_i \right)^{{{f:.2f}}}$", fontsize=16)
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
