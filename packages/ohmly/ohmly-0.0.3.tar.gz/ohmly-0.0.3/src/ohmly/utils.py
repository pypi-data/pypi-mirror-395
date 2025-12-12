"""
Module `utils`

Provides utility functions for numerical calculations related to catenary
and mechanical analysis.

Functions:
    find_root: Finds a root of a real-valued function using the Newton-Raphson
        method with a recursive implementation.

Type Aliases:
    MathFunction: A callable representing a function from float to float.

Notes:
    - `find_root` stops iterating when the successive approximations differ
      by less than 1e-8 or when the maximum number of iterations is reached.
    - Care should be taken that the derivative provided to `find_root` is
      non-zero near the root to avoid division by zero.
"""


from collections.abc import Callable

type MathFunction = Callable[[float], float]

def find_root(func: MathFunction, fprime: MathFunction, x0: float, max_iter: int = 1000):
    """Find a root of a function using Newton-Raphson iteration.

    Args:
        func: The function for which to find a root.
        fprime: The derivative of `func`.
        x0: Initial guess for the root.
        max_iter: Maximum number of iterations (default is 1000).

    Returns:
        float: Approximated root of `func` where `func(root) ≈ 0`.

    Notes:
        Uses recursion to iterate. Convergence is assumed when successive
        approximations differ by less than 1e-8. If `max_iter` is exhausted,
        returns the last approximation.
    """

    if max_iter <= 0:
        return x0

    y = func(x0)
    y_prime = fprime(x0)
    x_new = x0 - y / y_prime

    if abs(x_new - x0) < 1e-8: return x_new
    return find_root(func, fprime, x_new, max_iter - 1)

