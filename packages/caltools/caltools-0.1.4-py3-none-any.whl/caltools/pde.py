import sympy as sp
import numpy as np

# Export symbols if user wants them
x, y, u, p, q = sp.symbols("x y u p q")


# ---------------------------------------------------------------------
# 1) Classification of first-order PDE
# ---------------------------------------------------------------------
def clsfy_pde(E):
    """
    Classify a first-order PDE E(x, y, u, p, q) = 0
    based on its dependence on p = u_x and q = u_y.

    Returns one of:
      "Linear"
      "Quasilinear"
      "Fully nonlinear (polynomial in p, q)"
      "Fully nonlinear (non-polynomial in p, q)"
      "No derivatives present"
    """

    # No p or q anywhere
    if not (E.has(p) or E.has(q)):
        return "No derivatives present"

    # Try polynomial classification in p, q
    try:
        poly = sp.Poly(E, p, q)
    except sp.PolynomialError:
        # e.g. sin(p), exp(p*q), etc.
        return "Fully nonlinear (non-polynomial in p, q)"

    deg = poly.total_degree()

    # Technically SymPy may treat something like (p-p) as degree 0
    if deg <= 0:
        return "No derivatives present"

    if deg == 1:
        # E is at most linear in p,q, check coefficients for u-dependence
        a_p = sp.diff(E, p)  # coefficient of p
        a_q = sp.diff(E, q)  # coefficient of q

        # If coefficients depend on u -> quasilinear
        if a_p.has(u) or a_q.has(u):
            return "Quasilinear"
        else:
            return "Linear"

    # Degree >= 2
    return "Fully nonlinear (polynomial in p, q)"


import sympy as sp

# make sure these are defined once at module level
x, y, u = sp.symbols("x y u")


def pde_fo(a, b, c, print_steps=True):
    """
    Symbolic Method of Characteristics for a first-order PDE

        a(x, y, u) * u_x + b(x, y, u) * u_y = c(x, y, u)

    Parameters
    ----------
    a, b, c : sympy expressions in (x, y, u)
        PDE coefficients.
    print_steps : bool
        If True, print intermediate symbolic information.

    Returns
    -------
    dict
        {
          "first_integral": I(x, y) or None,
          "general_solution": Eq(u, F(I)) (formal),
          "details": {...}
        }
    """

    # Characteristic functions
    Y = sp.Function("Y")
    U = sp.Function("U")

    # --------------------------------------------------------------
    # 1) Characteristic ODE: dy/dx = b/a
    # --------------------------------------------------------------
    # Substitute y -> Y(x) in b and a.  We keep u as a symbol; SymPy
    # will treat it as a parameter (constant) for this ODE.
    rhs_y = (b / a).subs({y: Y(x)})

    ode_y = sp.Eq(sp.diff(Y(x), x), rhs_y)

    def safe_dsolve(eq):
        try:
            return sp.dsolve(eq)
        except (NotImplementedError, ValueError):
            return None

    sol_y = safe_dsolve(ode_y)

    # --------------------------------------------------------------
    # 2) First integral I(x, y) from the characteristic equation
    # --------------------------------------------------------------
    I_xy = None
    if isinstance(sol_y, sp.Equality):
        # Typical dsolve output:  F(x, Y(x)) = C1
        # Move everything to left and then substitute Y(x) -> y.
        lhs, rhs = sol_y.lhs, sol_y.rhs
        I_expr = sp.simplify(lhs - rhs)      # this is constant on chars
        I_xy = sp.simplify(I_expr.subs({Y(x): y}))

    # --------------------------------------------------------------
    # 3) Second characteristic ODE: du/dx = c/a
    # --------------------------------------------------------------
    # Substitute y -> Y(x), u -> U(x)
    rhs_u = (c / a).subs({y: Y(x), u: U(x)})
    ode_u = sp.Eq(sp.diff(U(x), x), rhs_u)
    sol_u = safe_dsolve(ode_u)

    # --------------------------------------------------------------
    # 4) Formal general solution u = F(I(x,y))
    # --------------------------------------------------------------
    F = sp.Function("F")
    if I_xy is not None:
        general_solution = sp.Eq(u, F(I_xy))
    else:
        # if we couldn't compute I explicitly, keep it symbolic
        I_symbolic = sp.Function("I")(x, y)
        general_solution = sp.Eq(u, F(I_symbolic))

    # Build details dict
    details = {
        "pde": sp.Eq(a * sp.Symbol("u_x") + b * sp.Symbol("u_y"), c),
        "characteristic_odes": {
            "dy/dx": ode_y,
            "du/dx": ode_u,
        },
        "char_curves": {
            "y(x)": sol_y,
            "u(x)": sol_u,
        },
        "first_integral": I_xy,
        "u_along_characteristics": sol_u,
        "general_solution": general_solution,
    }

    if print_steps:
        print("=== PDE ===")
        print(details["pde"])

        print("\n=== Characteristic ODEs ===")
        print("dy/dx =", ode_y)
        print("du/dx =", ode_u)

        print("\n=== Characteristic curves from dsolve (may be None) ===")
        print("y(x):", sol_y)
        print("u(x):", sol_u)

        print("\n=== First integral I(x,y) (if found) ===")
        print(I_xy)

        print("\n=== Formal general solution ===")
        print(general_solution)

    return {
        "first_integral": I_xy,
        "general_solution": general_solution,
        "details": details,
    }


# ---------------------------------------------------------------------
# 3) Nonlinear elliptic PDE via Jacobi iteration
# ---------------------------------------------------------------------
def pde_nl(
    N,
    g0=1.0,   # u(0,y)
    g1=0.0,   # u(1,y)
    h0=0.0,   # u(x,0)
    h1=1.0,   # u(x,1)
    max_iter=10_000,
    tol=1e-6,
    verbose=False,
    initial_guess=0.0,
):
    """
    Solve the nonlinear PDE:

        u_xx + u_yy + u**2 = 0   on  (0,1)x(0,1)

    using Jacobi's method on a uniform grid of size (N+1)x(N+1).

    Boundary conditions (user-specified):
        u(0,y) = g0(y)
        u(1,y) = g1(y)
        u(x,0) = h0(x)
        u(x,1) = h1(x)

    Parameters
    ----------
    N : int
        Number of intervals (grid points = N+1).
    g0, g1, h0, h1 : float or callable
        Boundary values or boundary functions (vectorized over numpy arrays).
    max_iter : int
    tol : float
    verbose : bool
    initial_guess : float

    Returns
    -------
    u : ndarray (N+1, N+1)
        Numerical approximation (rows ~ y, cols ~ x).
    info : dict
        { "iterations", "converged", "max_diff", "h" }
    """

    if N < 2:
        raise ValueError("N must be at least 2.")

    h = 1.0 / N
    h2 = h * h

    # Grid: j -> y (rows), i -> x (cols)
    u_grid = np.full((N + 1, N + 1), float(initial_guess), dtype=float)
    u_new = u_grid.copy()

    x_arr = np.linspace(0.0, 1.0, N + 1)
    y_arr = np.linspace(0.0, 1.0, N + 1)

    def eval_bc(val, arr):
        if callable(val):
            return np.array(val(arr), dtype=float)
        else:
            return np.full_like(arr, float(val), dtype=float)

    # ---------------------------------------------------------
    # Apply boundary conditions (same layout as "hand-written"):
    #   left  column  (x=0) -> u(0,y) = g0
    #   right column  (x=1) -> u(1,y) = g1
    #   bottom row    (y=0) -> u(x,0) = h0
    #   top    row    (y=1) -> u(x,1) = h1
    # ---------------------------------------------------------
    u_grid[:, 0] = eval_bc(g0, y_arr)   # x=0
    u_grid[:, N] = eval_bc(g1, y_arr)   # x=1
    u_grid[0, :] = eval_bc(h0, x_arr)   # y=0
    u_grid[N, :] = eval_bc(h1, x_arr)   # y=1

    # Jacobi iterations (vectorised, like your 51x51 code)
    for it in range(1, max_iter + 1):
        # interior update: 1..N-1 in both directions
        u_center = u_grid[1:-1, 1:-1]
        neighbors = (
            u_grid[2:, 1:-1] +     # down   (y+1)
            u_grid[:-2, 1:-1] +    # up     (y-1)
            u_grid[1:-1, 2:] +     # right  (x+1)
            u_grid[1:-1, :-2]      # left   (x-1)
        )

        u_new[1:-1, 1:-1] = 0.25 * (neighbors + h2 * u_center**2)

        # Reapply boundary conditions (to keep them exact)
        u_new[:, 0] = eval_bc(g0, y_arr)
        u_new[:, N] = eval_bc(g1, y_arr)
        u_new[0, :] = eval_bc(h0, x_arr)
        u_new[N, :] = eval_bc(h1, x_arr)

        # Convergence check
        diff = float(np.max(np.abs(u_new - u_grid)))

        if verbose and (it == 1 or it % 100 == 0):
            print(f"Iter {it}, max diff = {diff:e}")

        if diff < tol:
            if verbose:
                print(f"Converged in {it} iterations.")
            return u_new.copy(), {
                "iterations": it,
                "converged": True,
                "max_diff": diff,
                "h": h,
            }

        # Jacobi swap
        u_grid, u_new = u_new, u_grid

    if verbose:
        print(f"Reached max_iter={max_iter} with max diff = {diff:e}")

    return u_grid.copy(), {
        "iterations": max_iter,
        "converged": False,
        "max_diff": diff,
        "h": h,
    }


# caltools/char_tools.py

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def char_sys(system, ics, s_start=0.0, s_end=5.0,
                      n_points=200, plot=True):
    """
    Solve a characteristic ODE system

        dx/ds = ...
        dy/ds = ...
        du/ds = ...

    Parameters
    ----------
    system : callable
        Function f(z, s) returning [dx/ds, dy/ds, du/ds],
        where z = [x, y, u].
    ics : list of tuples
        Initial conditions [(x0, y0, u0), ...].
    s_start, s_end : float
        Parameter range for s.
    n_points : int
        Number of points in the s-grid.
    plot : bool
        If True, plot characteristic curves in the xy-plane.

    Returns
    -------
    s : ndarray (n_points,)
        Parameter values.
    sols : list of ndarrays
        Each entry has shape (n_points, 3) with columns [x, y, u].
    """
    s = np.linspace(s_start, s_end, n_points)
    sols = []

    if plot:
        plt.figure()

    for ic in ics:
        sol = odeint(system, ic, s)
        sols.append(sol)

        if plot:
            x, y, u = sol.T
            plt.plot(x, y, label=f"(x0,y0,u0)={ic}")

    if plot:
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Characteristic curves in the xy-plane")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return s, sols

# src/caltools/ebb_eqn.py

def ebb_eqn(L, N, q0, EI,
            w0=0.0, wL=0.0,
            wpp0=0.0, wppL=0.0):
    """
    Build the finite-difference linear system for the Euler–Bernoulli beam

        EI * d^4 w / dx^4 = q0

    on a uniform grid x_i = i*h, i = 0,...,N with h = L/N.

    Boundary conditions (user-provided):
        w(0)   = w0
        w(L)   = wL
        w''(0) = wpp0
        w''(L) = wppL

    For example, a simply supported beam with uniform load:
        w0 = 0, wL = 0, wpp0 = 0, wppL = 0.

    Parameters
    ----------
    L : float
        Length of the beam.
    N : int
        Number of intervals (so N+1 grid points). Must be >= 4.
    q0 : float
        Uniform distributed load q(x) = q0.
    EI : float
        Flexural rigidity (E * I).
    w0 : float, optional
        Boundary value w(0).
    wL : float, optional
        Boundary value w(L).
    wpp0 : float, optional
        Second derivative at x = 0, w''(0).
    wppL : float, optional
        Second derivative at x = L, w''(L).

    Returns
    -------
    x : list[float]
        Grid points x_0,...,x_N.
    A : list[list[float]]
        Coefficient matrix for the linear system A w = b.
    b : list[float]
        Right-hand side vector.

    Notes
    -----
    This function only builds the system. To solve it, convert A and b to
    NumPy arrays and use numpy.linalg.solve, then plot with matplotlib.

    Example
    -------
    A simple usage example (simply supported beam with uniform load) is
    provided in the module's main block::

        if __name__ == "__main__":
            import numpy as np
            import matplotlib.pyplot as plt
            from caltools.ebb_eqn import ebb_eqn

            L = 1.0
            N = 20
            q0 = 1.0
            EI = 1.0

            x, A_list, b_list = ebb_eqn(L, N, q0, EI,
                                        w0=0.0, wL=0.0,
                                        wpp0=0.0, wppL=0.0)

            A = np.array(A_list, dtype=float)
            b = np.array(b_list, dtype=float)
            w = np.linalg.solve(A, b)

            plt.plot(x, w, marker="o")
            plt.xlabel("x")
            plt.ylabel("w(x)")
            plt.title("Euler–Bernoulli beam (simply supported, uniform load)")
            plt.grid(True)
            plt.show()
    """

    if N < 4:
        raise ValueError("N must be at least 4 for 4th-order finite differences.")

    # grid spacing and points
    h = L / N
    x = [i * h for i in range(N + 1)]

    # initialize matrix and rhs
    A = [[0.0 for _ in range(N + 1)] for _ in range(N + 1)]
    b = [0.0 for _ in range(N + 1)]

    # --- Boundary condition 1: w(0) = w0 ---
    A[0][0] = 1.0
    b[0] = w0

    # --- Boundary condition 2: w''(0) = wpp0 ---
    # (w_0 - 2 w_1 + w_2) / h^2 = wpp0
    A[1][0] = 1.0
    A[1][1] = -2.0
    A[1][2] = 1.0
    b[1] = wpp0 * (h ** 2)

    # --- Interior points: 4th derivative ---
    # EI * w''''(x_i) = q0
    # → w_{i-2} - 4 w_{i-1} + 6 w_i - 4 w_{i+1} + w_{i+2} = (q0/EI) h^4
    rhs_val = (q0 / EI) * (h ** 4)

    for i in range(2, N - 1):  # i = 2,...,N-2
        A[i][i - 2] = 1.0
        A[i][i - 1] = -4.0
        A[i][i]     = 6.0
        A[i][i + 1] = -4.0
        A[i][i + 2] = 1.0
        b[i] = rhs_val

    # --- Boundary condition 3: w''(L) = wppL ---
    # (w_N - 2 w_{N-1} + w_{N-2}) / h^2 = wppL
    A[N - 1][N]     = 1.0
    A[N - 1][N - 1] = -2.0
    A[N - 1][N - 2] = 1.0
    b[N - 1] = wppL * (h ** 2)

    # --- Boundary condition 4: w(L) = wL ---
    A[N][N] = 1.0
    b[N] = wL

    return x, A, b


if __name__ == "__main__":
    # Example usage and plot
    import numpy as np
    import matplotlib.pyplot as plt

    # beam parameters
    L = 1.0
    N = 20
    q0 = 1.0
    EI = 1.0

    # simply supported: w(0)=w(L)=0, w''(0)=w''(L)=0
    x, A_list, b_list = ebb_eqn(L, N, q0, EI,
                                w0=0.0, wL=0.0,
                                wpp0=0.0, wppL=0.0)

    A = np.array(A_list, dtype=float)
    b = np.array(b_list, dtype=float)

    w = np.linalg.solve(A, b)

    plt.plot(x, w, marker="o")
    plt.xlabel("x")
    plt.ylabel("w(x)")
    plt.title("Euler–Bernoulli beam (simply supported, uniform load)")
    plt.grid(True)
    plt.show()
