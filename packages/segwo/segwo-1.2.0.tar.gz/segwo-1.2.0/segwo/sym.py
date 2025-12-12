"""
Symbolic expressions
====================

This module offers functions to manipulate symbolic expressions of
covariance and mixing matrices. It mirrors the functionality of the
:mod:`segwo.cov` module, but operates on symbolic expressions instead of
numerical arrays. This allows to compute analytic expressions for the noise
transfer functions under certain assumptions.

Symbols
-------

.. autodata:: f

.. autodata:: d

.. autofunction:: delay_exp

Building covariance matrices
----------------------------

.. autofunction:: construct_covariance_from_psds

.. autofunction:: concatenate_covariances

Building mixing matrices
------------------------

.. autofunction:: construct_mixing_from_pytdi

.. autofunction:: compose_mixings

.. autofunction:: concatenate_mixings

Projecting measurements
-----------------------

.. autofunction:: project_covariance

"""

import pytdi
import sympy as sp

f = sp.symbols("f", real=True, positive=True)
"""Frequency symbol [Hz]."""

d = {
    link: sp.symbols(f"d_{{{link}}}", real=True, positive=True)
    for link in [12, 23, 31, 13, 32, 21]
}
"""Dictionary of light travel times (delays) for each link [s]."""


def delay_exp(links: int | list[int]) -> sp.Expr:
    r"""Compute the delay as a complex exponential.

    Assuming that delays are constnts, they can be written in the frequency
    domain as a complex exponential,

    .. math::

        e^{-i 2 \pi f d_{ij}}.

    This function makes use of :data:`f` and :data:`d`.

    Parameters
    ----------
    links : int or list of int
        The links to compute the delay for. If a single link is given, it is
        assumed to be a single link. Otherwise, it is assumed to be a list of
        links and the delays are simply added together.

    Returns
    -------
    sympy.Expr
        The delay as a complex exponential.
    """
    if isinstance(links, int):
        links = [links]

    return sp.prod(sp.exp(-2j * sp.pi * f * d[link]) for link in links)


def construct_covariance_from_psds(psds: list[sp.Expr]) -> sp.Matrix:
    """Construct covariance matrix from a list of power spectral densities.

    We assume that the covariance matrix is diagonal (i.e. no correlations).

    Parameters
    ----------
    psds : list of N sympy.Expr
        List of power spectral densities. The order of the PSDs in this list
        determines the order of the rows and columns in the covariance matrix.

    Returns
    -------
    sympy.Matrix
        Covariance matrix, of shape ``N x N``.
    """
    return sp.diag(*psds)


def concatenate_covariances(covariances: list[sp.Matrix]) -> sp.Matrix:
    r"""Concatenate a sequence of covariance matrices into a single matrix.

    See :func:`segwo.cov.concatenate_covariances` for a description of the
    function.

    Parameters
    ----------
    covariances : list of N sympy.Matrix
        Covariance matrices of shapes ``N[i] x N[i]``, where ``N[i]`` is the
        number of observables in the i-th covariance matrix.

    Returns
    -------
    sympy.Matrix
        Concatenated covariance matrix, of shape ``N x N``, where ``N`` is the
        total number of observables across all covariance matrices.

        Units of each covariance matrix remain the same.
    """
    # Check we have at least one covariance matrix
    if not covariances:
        return sp.Matrix([])
    assert len(covariances) > 0

    block_matrix = sp.BlockDiagMatrix(*covariances)
    matrix = sp.Matrix(block_matrix)

    return matrix


def _pytdi_delay_exp(delays: list[str]) -> sp.Expr:
    """Transform a list of delay strings from PyTDI to sympy expressions.

    PyTDI uses a different syntax for delays, so we need to convert them to
    sympy expressions. This function is used internally in the
    :func:`construct_mixing_from_pytdi` function.

    PyTDI uses a list of strings, such as "A_12" or "D_31" to represent delays
    and advancements. Because we assume that delays are constant, we can
    simply replace these strings with the corresponding sympy symbols and
    advancements are replaced with the corresponding negative delays.

    Parameters
    ----------
    delays : list of str
        List of strings representing delays and advancements. The strings can
        be in the form "A_ij" or "D_ij", where "ij" is the link number.

    Returns
    -------
    sympy.Expr
        The delay as a complex exponential.
    """
    # Convert the list of strings to a list of sympy symbols
    delays = [
        d[int(link[2:])] if link.startswith("D_") else -d[int(f"{link[-1]}{link[-2]}")]
        for link in delays
    ]

    # Compute the product of the delays
    return sp.prod(sp.exp(-2j * sp.pi * f * delay) for delay in delays)


def construct_mixing_from_pytdi(
    tdi_combinations: list[pytdi.TDICombination],
    measurements: list[str],
) -> sp.Matrix:
    """Construct the mixing matrix from the TDI combinations.

    See :func:`segwo.cov.construct_mixing_from_pytdi` for a description of the
    function.

    Parameters
    ----------
    tdi_combinations : list of N pytdi.TDICombination
        List of TDI combinations. The order of the combinations in this list
        determines the order of the rows in the mixing matrix.
    measurements : list of M str
        List of measurement names. The order of the measurements in this list
        determines the order of the columns in the mixing matrix.

    Returns
    -------
    sympy.Matrix
        Mixing matrix, of shape ``N x M``.
    """
    # Start with an empty matrix
    mixing = sp.zeros(len(tdi_combinations), len(measurements))

    # For each combination, compute the corresponding row of the mixing matrix
    for i, combination in enumerate(tdi_combinations):
        # Fill element i,j of mixing matrix if measurement is in combination
        for j, measurement in enumerate(measurements):
            if measurement in combination.components:
                # Couplings are a list of tuples (coeff, list of delays)
                couplings = combination.components[measurement]
                mixing[i, j] = sum(
                    coeff * _pytdi_delay_exp(delays) for coeff, delays in couplings
                )

    return mixing


def compose_mixings(mixings: list[sp.Matrix]) -> sp.Matrix:
    r"""Compose a sequence of mixing matrices into a single mixing matrix.

    See :func:`segwo.cov.compose_mixings` for a description of the function.

    Parameters
    ----------
    mixings : list of N sympy.Matrix
        Mixing matrices of compatible successive shapes. The i-th mixing matrice
        should have shape ``M[i+1] x M[i])``.

    Returns
    -------
    sympy.Matrix
        Composed mixing matrix, of shape ``M[N] x M[0]``.

        Units are the product of the units of the input mixing matrices.

    Raises
    ------
    ValueError
        If the mixing matrices are not compatible, or if there are no mixing
        matrices.
    """
    # Check we have at least one mixing matrix
    if not mixings:
        raise ValueError("mixings must be a non-empty list.")

    return sp.prod(mixings[::-1])


def concatenate_mixings(mixings: list[sp.Matrix]) -> sp.Matrix:
    r"""Concatenate a sequence of mixing matrices into a single mixing matrix.

    See :func:`segwo.cov.concatenate_mixings` for a description of the function.

    Parameters
    ----------
    mixings : list of N sympy.Matrix
        Mixing matrices of shapes ``N[i] x N[i]``, where ``N[i]`` is the number
        of observables in the i-th mixing matrix.

    Returns
    -------
    sympy.Matrix
        Concatenated mixing matrix, of shape ``N x N``, where ``N`` is the
        total number of observables across all mixing matrices.

        Units of each mixing matrix remain the same.
    """
    # Check we have at least one mixing matrix
    if not mixings:
        return sp.Matrix([])
    assert len(mixings) > 0

    block_matrix = sp.BlockDiagMatrix(*mixings)
    matrix = sp.Matrix(block_matrix)

    return matrix


def project_covariance(
    cov: sp.Matrix, mixing: sp.Matrix | list[sp.Matrix]
) -> sp.Matrix:
    """Transform covariance to a new set of observables using mixing matrices.

    See :func:`segwo.cov.project_covariance` for a description of the function.

    Parameters
    ----------
    cov : sympy.Matrix
        Covariance matrix of shape ``N x N``.
    mixing : sympy.Matrix or list of sympy.Matrix
        Mixing matrix or list of mixing matrices. If a list is provided, the
        mixing matrices are composed before applying the transformation.

        The shape of the composed matrix must be compatible with the covariance
        matrix, i.e., it should be of shape ``M x N``, where ``M`` is the number
        of observables in the new set of observables.

    Returns
    -------
    sympy.Matrix
        Transformed covariance matrix of shape ``M x M``, where ``M`` is the
        number of observables in the new set of observables.

        Units are the product of the units of the input covariance and mixing
        matrices.
    """
    # Check we have at least one mixing matrix
    if not isinstance(mixing, sp.Matrix):
        mixing = compose_mixings(mixing)

    return mixing * cov * mixing.H
