r"""
Sensitivity curves
==================

This package provides functions to compute sensitivity curves from noise and
signal covariance matrices.

Computing sensitivity
---------------------

.. autofunction:: compute_sensitivity_from_covariances

"""

import numpy as np


def compute_sensitivity_from_covariances(
    noise_cov: np.ndarray, signal_cov: np.ndarray
) -> np.ndarray:
    r"""Compute sensitivity curve from noise and signal covariance matrices.

    The multivariate sensitivity is defined as a function of the response mixing
    matrix :math:`\mathbf{R}` and the noise covariance matrix
    :math:`\mathbf{C}_\text{noise}`,

    .. math::

        S(t, f) = \frac{1}{ \text{Tr}[\mathbf{R}(t, f)
        \mathbf{C}_\text{noise}^{-1}(t, f)] }.

    This definition is valid for any set of :math:`N` observables for which
    :math:`\mathbf{C}_\text{noise}` is full rank.

    In practice, the response mixing matrix is deduced from the signal
    covariance matrix :math:`\mathbf{C}_\text{signal}` computed from a
    normalized diagonal strain covariance matrix
    :math:`(\mathbf{C}_\text{strain})_{ij} = \frac{1}{2} \delta_{ij}`. This
    corresponds to a stochastic unit-power unpolarized gravitational wave.

    For a sky-averaged sensitivity curve, the signal covariance matrix can be
    computed from :func:`segwo.response.compute_isotropic_signal_cov`.

    .. admonition:: Normalization

        The normalization used in the definition of the sensitivity is
        conventional. The convention adopted here follows the LISA Conventions
        :cite:`Babak:2021mhe`.

    To compute single-channel sensitivity curves, one can trim the
    covariance matrices to the single channel of interest. For example, if
    the signal covariance matrix is of shape ``(..., N, N)`` and the noise
    covariance matrix is of shape ``(..., M, M)``, one can compute the
    sensitivity for the first channel of the signal covariance matrix and
    the first channel of the noise covariance matrix as follows:

    .. code-block:: python

        sensitivity = compute_sensitivity_from_covariances(
            noise_cov[..., 0:1, 0:1], signal_cov[..., 0:1, 0:1]
        )

    .. admonition:: Combined sensitivity from single-channel sensitivities

        In general, the combined sensitivity cannot be easily deduced from the
        single-channel sensitivities due to correlations between the
        observables. For noise-orthogonal observables (i.e., if the noise
        covariance matrix is diagonal), the combined sensitivity can be computed
        as

        .. math::
            S_\text{combined}^{-1} = \sum_{i=1}^N S_i^{-1}.

    Args:
        noise_cov: Noise covariance matrix, of shape ``(..., N, N)``.
        signal_cov: Signal covariance matrix, of shape ``(..., N, N)``.

    Returns:
        Sensitivity curve, as an array of shape ``(...)``. Those axes are
        usually reserved for time and frequency.

        Units are those of ``response_cov`` divided by those of ``noise_cov``
        and power spectral density [1/Hz].

    Raises:
        ValueError: If the noise covariance matrix is singular.
    """
    if noise_cov.ndim < 2:
        raise ValueError("Noise covariance must have at least two dimensions.")
    if noise_cov.shape[-1] != noise_cov.shape[-2]:
        raise ValueError("Noise covariance must be square.")
    if signal_cov.ndim < 2:
        raise ValueError("Response covariance must have at least two dimensions.")
    if signal_cov.shape[-1] != signal_cov.shape[-2]:
        raise ValueError("Response covariance must be square.")

    if noise_cov.shape[1] == 1:
        inv_noise_cov = 1 / noise_cov
    else:
        try:
            inv_noise_cov = np.linalg.inv(noise_cov)  # (..., N, N)
        except np.linalg.LinAlgError as e:
            raise ValueError("Noise covariance is singular.") from e

    snr_psd = np.einsum("...ij, ...ji -> ...", signal_cov, inv_noise_cov)  # (...)
    np.allclose(snr_psd.imag / np.abs(snr_psd), 0)  # imaginary part should be small

    normalized_snr_psd = snr_psd.real
    return 1 / normalized_snr_psd
