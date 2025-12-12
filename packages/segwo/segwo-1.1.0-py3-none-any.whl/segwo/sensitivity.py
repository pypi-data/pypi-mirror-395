r"""
Sensitivity curves
==================

This module provides functions to compute optimal (i.e., multi-channel)
sensitivity curves from noise and signal covariance matrices.

Optimal sensitivity curves
--------------------------

Two methods are available; :func:`compute_sensitivity_from_eigenvalues` is based
on the diagonalization of the noise covariance matrix, while
:func:`compute_sensitivity_from_inverse` is based on the inversion of the noise
covariance matrix.

In our experience, the first method is more numerically stable and should be
preferred.

Note that in both cases, the noice covariance matrix must be full rank (i.e.,
no singular values). If the noise covariance matrix is not full rank, one can
regularize it by adding a small value to the diagonal.

.. autofunction:: compute_sensitivity_from_eigenvalues

.. autofunction:: compute_sensitivity_from_inverse

Response mixing matrix
----------------------

Note that in practice, the response mixing matrix :math:`\mathbf{R}` is deduced
from the signal covariance matrix :math:`\mathbf{C}_\text{signal}` computed from
a normalized diagonal strain covariance matrix
:math:`(\mathbf{C}_\text{strain})_{ij} = \frac{1}{2} \delta_{ij}`. This
corresponds to a stochastic unit-power unpolarized gravitational wave.

For a sky-averaged sensitivity curve, the signal covariance matrix can be
computed from :func:`segwo.response.compute_isotropic_signal_cov`.

Single-channel sensitivity curves
---------------------------------

Use :func:`compute_single_channel_sensitivities` to compute the sensitivity
curves for each channel separately. This function ignores potential correlations
between the channels (only the diagonal elements of the noise covariance matrix
are provided).

In general, the combined sensitivity cannot be easily deduced from the
single-channel sensitivities due to correlations between the observables.
For noise-orthogonal observables (i.e., if the noise covariance matrix is
diagonal), the combined sensitivity can be computed as

.. math::
    S_\text{combined}^{-1} = \sum_{i=1}^N S_i^{-1}.

.. autofunction:: compute_single_channel_sensitivities


Noise orthogonalization
-----------------------

One can find noise-orthogonal observables by diagonalizing the noise covariance
matrix :math:`\mathbf{C}_\text{noise}`.

.. autofunction:: diagonalize_noise_covariance

Normalization
-------------

The normalization used in the definition of the sensitivity is conventional. The
convention adopted here follows the LISA Conventions :cite:`Babak:2021mhe`.

"""

from typing import Sequence

import numpy as np


def _check_noise_covariance_shape(noise_cov: np.ndarray) -> None:
    """Check the shape of the noise covariance matrix.

    Args:
        noise_cov: Noise covariance matrix, of shape ``(..., N, N)``.

    Raises:
        ValueError: If the noise covariance matrix is not square or has less than
            two dimensions.
    """
    if noise_cov.ndim < 2:
        raise ValueError("Noise covariance must have at least two dimensions.")
    if noise_cov.shape[-1] != noise_cov.shape[-2]:
        raise ValueError("Noise covariance must be square.")


def _check_signal_covariance_shape(signal_cov: np.ndarray) -> None:
    """Check the shape of the signal covariance matrix.

    Args:
        signal_cov: Signal covariance matrix, of shape ``(..., N, N)``.

    Raises:
        ValueError: If the signal covariance matrix is not square or has less than
            two dimensions.
    """
    if signal_cov.ndim < 2:
        raise ValueError("Signal covariance must have at least two dimensions.")
    if signal_cov.shape[-1] != signal_cov.shape[-2]:
        raise ValueError("Signal covariance must be square.")


def diagonalize_noise_covariance(
    noise_cov: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Diagonalize the noise covariance matrix.

    This function computes the eigenvectors and eigenvalues (or rather, its
    Hermitian transpose) of the noise covariance matrix.

    The eigenvalues represent the noise power spectral densities (PSDs)
    associated with the eigenvectors, and the eigenvector matrix conjugate
    transpose is the mixing matrix that transforms the original observables into
    noise-orthogonal observables.

    The following example illustrates how to use this function to find the
    noise-orthogonal observables and project the signal covariance onto them.

    .. code-block:: python

        # Diagonalize the noise covariance matrix noise_psds, mixing =
        diagonalize_noise_covariance(noise_cov)

        # Now project the signal covariance onto the eigenvectors
        projected_signal_cov = segwo.cov.project_covariance(signal_cov, mixing)

    Args:
        noise_cov: Noise covariance matrix, of shape ``(..., N, N)``.

    Returns:
        A tuple ``(noise_psds, mixing)`` containing:

        - The eigenvalues of the noise covariance matrix, i.e., the noise PSDs
          associated with the eigenvectors, of shape ``(..., N)``.
        - The transpose conjugate eigenvectors of the noise covariance matrix,
          i.e., the mixing matrix that transforms the original observables into
          noise-orthogonal observables, of shape ``(..., N, N)``.
    """
    # Check the shape of the noise covariance matrix
    _check_noise_covariance_shape(noise_cov)

    # Diagonalize the noise covariance matrix
    eigvals, eigvecs = np.linalg.eigh(noise_cov)  # (..., N), (..., N, N)
    if np.any(eigvals <= 0):
        raise ValueError("Noise covariance is singular or non Hermitian.")

    # The mixing matrix we want to return is the Hermitian transpose of eigvecs
    # taken over the two last axes (the observables)
    mixing = np.conj(np.swapaxes(eigvecs, -1, -2))

    return eigvals, mixing


def compute_sensitivity_from_eigenvalues(
    noise_cov: np.ndarray, signal_cov: np.ndarray
) -> np.ndarray:
    r"""Compute sensitivity curve by diagonalizing the noise covariance.

    This function first diagonalizes the noise covariance matrix to find
    noise-orthogonal observables :math:`\mathbf{V}(t, f)`, associated with
    eigenvalues :math:`\mathbf{D}_\text{noise}(t, f)` (the noise PSDs
    associated with the eigenvectors).

    It then projects the response mixing matrix :math:`\mathbf{R}(t, f)` onto
    the eigenvectors of the noise covariance matrix as

    .. math::

        \mathbf{R}'(t, f) = \mathbf{V}^\dagger(t, f) \mathbf{R}(t, f)
        \mathbf{V}(t, f),

    and compute the single-channel sensitivities associated with each
    eigenvector as

    .. math::

        S_i(t, f) = \frac{\left[\mathbf{D}_\text{noise}(t, f)\right]_i}
        {\left[\mathbf{R}'(t, f)\right]_{ii}}.

    Now that we have noise-orthogonal observables, the combined sensitivity as
    then simply given by

    .. math::
        S_\text{combined}^{-1}(t, f) = \sum_{i=1}^N S_i^{-1}(t, f).

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

    See Also:
        :func:`compute_sensitivity_from_inverse` for an alternative method of
        computing the sensitivity curve based on the inversion of the noise
        covariance matrix (often more numerically unstable).

        :func:`diagonalize_noise_covariance` for a function that diagonalizes
        the noise covariance matrix.
    """
    # Check the shapes of the covariance matrices
    _check_noise_covariance_shape(noise_cov)
    _check_signal_covariance_shape(signal_cov)

    # Diagonalize the noise covariance matrix
    psds, mixing = diagonalize_noise_covariance(noise_cov)  # (..., N), (..., N, N)

    # Project the signal covariance matrix onto the eigenvectors
    # (we directly take the diagonal elements of the projected covariance)
    projected_signal_cov = np.einsum(
        "...ik, ...kl, ...il -> ...i", mixing, signal_cov, mixing.conj()
    )  # (..., N)

    # Imaginary part should be small
    if not np.allclose(projected_signal_cov.imag, 0):
        raise ValueError(
            "Projected signal covariance has non-negligible imaginary part."
        )

    # Combine the single-channel sensitivities
    return 1 / np.sum(projected_signal_cov.real / psds, axis=-1)  # (...,)


def compute_sensitivity_from_inverse(
    noise_cov: np.ndarray, signal_cov: np.ndarray, *, rtol: float = 1e-12
) -> np.ndarray:
    r"""Compute sensitivity curve by inverting the noise covariance.

    The multivariate sensitivity is defined as a function of the response mixing
    matrix :math:`\mathbf{R}` and the noise covariance matrix
    :math:`\mathbf{C}_\text{noise}`,

    .. math::

        S(t, f) = \frac{1}{ \text{Tr}[\mathbf{R}(t, f)
        \mathbf{C}_\text{noise}^{-1}(t, f)] }.

    Args:
        noise_cov: Noise covariance matrix, of shape ``(..., N, N)``.
        signal_cov: Signal covariance matrix, of shape ``(..., N, N)``.
        rtol: Relative tolerance when making sure that the SNR of each channel
            has a vanishing imaginary part. This parameter might have to be
            adjusted for badly-conditioned noise covariance matrices whose
            inverse is numerically instable.

    Returns:
        Sensitivity curve, as an array of shape ``(...)``. Those axes are
        usually reserved for time and frequency.

        Units are those of ``response_cov`` divided by those of ``noise_cov``
        and power spectral density [1/Hz].

    Raises:
        ValueError: If the noise covariance matrix is singular.

    See Also:
        :func:`compute_sensitivity_from_eigenvalues` for an alternative method
        of computing the sensitivity curve based on the diagonalization of the
        noise covariance matrix (often more numerically stable).
    """
    # Check the shapes of the covariance matrices
    _check_noise_covariance_shape(noise_cov)
    _check_signal_covariance_shape(signal_cov)

    # Compute the inverse of the noise covariance matrix
    # If noise_cov is a single channel, we can use the reciprocal directly
    if noise_cov.shape[1] == 1:
        if np.any(np.isclose(noise_cov, 0)):
            raise ValueError("Noise covariance is singular.")
        inv_noise_cov = 1 / noise_cov
    else:
        try:
            inv_noise_cov = np.linalg.inv(noise_cov)  # (..., N, N)
        except np.linalg.LinAlgError as e:
            raise ValueError("Noise covariance is singular.") from e

    snr_psd = np.einsum("...ij, ...ji -> ...", signal_cov, inv_noise_cov)  # (...)

    # Imaginary part should be small
    tolerance = rtol * np.max(abs(snr_psd))
    if not np.allclose(snr_psd.imag, 0, atol=tolerance):
        raise ValueError("Sensitivity curve has non-negligible imaginary part.")

    return 1 / snr_psd.real


def compute_single_channel_sensitivities(
    noise_psds: np.ndarray,
    signal_cov: np.ndarray,
    *,
    channels: Sequence[int] | None = None,
) -> np.ndarray:
    r"""Compute single-channel sensitivities.

    This function computes the sensitivity for each channel specified in
    ``channels``, given their noise power spectral densities
    :math:`S_{\text{noise},i}` and the response mixing matrix
    :math:`\mathbf{R}`,

    .. math::

        S_i(t, f) = \frac{S_{\text{noise},i}(t, f)}{\left[\mathbf{R}(t,
        f)\right]_{ii}}.

    Note that the combined sensitivity cannot be easily deduced from the
    single-channel sensitivities due to correlations between the observables.

    The noise PSDs can be obtained as the diagonal elements of the noise
    covariance matrix, i.e.,

    .. code-block:: python

        noise_psds = np.diagonal(noise_cov, axis1=-2, axis2=-1)
        sensitivities = compute_single_channel_sensitivities(noise_psds, signal_cov)

    Args:
        noise_psds: Noise power spectral densities, of shape ``(..., N)``.
        signal_cov: Signal covariance matrix, of shape ``(..., N, N)``.
        channels: List of ``M`` channel indices to compute sensitivities for. If
            None, computes sensitivities for all channels.

    Returns:
        An array of sensitivities for the specified channels, of shape ``(...,
        M)``.

    Raises:
        ValueError: If the noise power spectral densities are not of shape
            ``(..., N)`` or if the signal covariance matrix is not of shape
            ``(..., N, N)``.
        ValueError: If the number of channels specified in ``channels`` is
            greater than the number of channels in the noise power spectral
            densities.
        ValueError: If not all elements in ``noise_psds`` are positive.
    """
    # Check the shape of the input matrices
    _check_signal_covariance_shape(signal_cov)
    try:
        np.broadcast_arrays(noise_psds[..., None], signal_cov)
    except ValueError as e:
        raise ValueError("noise_psds and signal_cov have incompatible shapes.") from e

    # If channels is None, use all channels
    if channels is None:
        channels = range(noise_psds.shape[-1])

    # Compute the sensitivities for the specified channels
    return noise_psds[..., channels] / signal_cov[..., channels, channels]  # (..., M)
