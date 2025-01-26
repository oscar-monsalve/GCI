from numpy import sign
from numpy import log
from numpy import abs


def physical_dimension(dimension: str) -> float:
    """Returns f"""
    pass


def representative_grid_size(n1: float, n2: float, n3: float, f: float) -> [float, float, float]:
    """Returns three represetative grid sizes (h1, h2, h3)"""
    pass


def grid_refinement_factor(h1: float, h2: float, h3: float) -> [float, float]:
    """Returns two grid refinement factors (r21, r32)"""
    pass


def fixed_point_iteration(aparent_order, init_number: int, tol=1e-6, max_iter=100) -> [float, int]:
    x = init_number
    for i in range(max_iter):
        x_next = aparent_order(x)
        if abs(x_next-x) < tol:
            return x_next, i
        x = x_next
    raise ValueError(f"Failed to converge after {max_iter} iterations")


def aparent_order(phi1: float, phi2: float, phi3: float, r21: float, r32: float, iter: float) -> float:
    """
    Returns the aparent order p.

    Args:
    iter: iteration variable obtained from the fixed-point iteration.
    """
    ep21 = phi2-phi1
    ep32 = phi3-phi2
    s = 1*sign(ep32/ep21)
    return (1/(log(r21)))*(abs(log(ep32/ep21)+log(((r21**iter)-s)/((r32**iter)-s))))


def extrapolated_values(phi1: float, phi2: float, phi3: float, r21: float, r32: float, aparent_order: float) -> [float, float]:
    phi21_ext = (((r21**aparent_order)*phi1)-phi2)/((r21**aparent_order)-1)
    phi32_ext = (((r32**aparent_order)*phi2)-phi3)/((r32**aparent_order)-1)
    return phi21_ext, phi32_ext


def approximate_relative_errors(phi1: float, phi2: float, phi3: float) -> [float, float]:
    """
    Returns the approximate relative errors.
    """
    e21_a = (abs((phi1-phi2)/phi1))*100
    e32_a = (abs((phi2-phi3)/phi2))*100
    return e21_a, e32_a


def extrapolated_relative_errors(phi1: float, phi2: float, phi21_ext: float, phi32_ext: float) -> [float, float]:
    e21_ext = (((phi21_ext-phi1)/phi21_ext)) * 100
    e32_ext = (((phi32_ext-phi2)/phi32_ext)) * 100
    return e21_ext, e32_ext


def gci(r21: float, r32: float, e21_a: float, e32_a: float, aparent_order: float) -> [float, float]:
    """
    Returns the fine (GCI21_fine) and medium (GCI32_medium) GCI results.

    Args:
    e21_a, e32_a: approximate relative errors.
    """
    gci21_fine = ((1.25*e21_a)/((r21**aparent_order)-1))
    gci32_medium = ((1.25*e32_a)/((r32**aparent_order)-1))
    return gci21_fine, gci32_medium
