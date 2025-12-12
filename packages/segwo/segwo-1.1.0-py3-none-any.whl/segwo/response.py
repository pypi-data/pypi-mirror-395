"""
Response functions
==================

This module contains functions to compute the response to gravitational waves
of a detector with an arbitrary number of interferometric links. The response is
formalised as a mixing matrix that relates the gravitational wave strain to the
fractional frequency deviation (aka, Doppler shift) of the links.

.. note::

    The response for an arbitrary set of observables is not yet implemented.
    Only the response for the LISA case (a triangle of 6 links) is available.

Strain and polarization
-----------------------

We define here the conventions for the polarization basis, as well as
transformation matrices between the linear and circular polarization bases.

.. autodata:: LINEAR_POLARIZATION

.. autodata:: CIRCULAR_POLARIZATION

.. autodata:: LINEAR2CIRCULAR

.. autodata:: CIRCULAR2LINEAR

Link response function
----------------------

.. autofunction:: compute_strain2link

.. autofunction:: compute_source_basis

Sky-averaged response function
------------------------------

.. autofunction:: compute_isotropic_signal_cov

.. autofunction:: sky_average

"""

from typing import Callable

import healpy as hp
import numpy as np
from lisaconstants import c

from segwo.cov import project_covariance

LINEAR_POLARIZATION = ["+", "x"]
"""Convention for linear (plus and cross) polarization basis."""

CIRCULAR_POLARIZATION = ["left", "right"]
"""Convention for circular (left and right) polarization basis."""

LINEAR2CIRCULAR = np.array([[1, -1j], [1, 1j]]) / np.sqrt(2)
"""Mixing matrix going from linear to circular polarization.

Order for rows and columns are given by :attr:`LINEAR_POLARIZATION` and
:attr:`CIRCULAR_POLARIZATION`, respectively.

Use :func:`segwo.cov.project_covariance` with this mixing matrix to
convert a linear polarization covariance matrix to a circular polarization
covariance matrix.
"""

CIRCULAR2LINEAR = np.array([[1, 1], [1j, -1j]]) / np.sqrt(2)
"""Mixing matrix going from circular to linear polarization.

Order for rows and columns are given by :attr:`CIRCULAR_POLARIZATION` and
:attr:`LINEAR_POLARIZATION`, respectively.

Use :func:`segwo.cov.project_covariance` with this mixing matrix to
convert a circular polarization covariance matrix to a linear polarization
covariance matrix.
"""


def compute_source_basis(
    beta: np.ndarray, lamb: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute the source-localization basis vectors.

    Args:
        beta: Ecliptic latitude(s) [rad].
        lamb: Ecliptic longitude(s) [rad].

    Returns:
        A 3-tuple of vector basis ``(k, u, v)`` as defined by the LDC Manual
        (2018), of shape ``(len(beta), 3)``.

        First axis correspond to the common shape of the input arrays. Second
        axis is for the coordinates ``(x, y, z)``.

    Raises:
        ValueError: If ``beta`` and ``lamb`` are not scalars or 1D arrays of the
            same shape.
    """
    # Check shapes
    beta = np.atleast_1d(beta)
    lamb = np.atleast_1d(lamb)
    if beta.ndim > 1 or lamb.ndim > 1:
        raise ValueError("beta and lamb must be scalars or 1D arrays.")
    if beta.shape != lamb.shape:
        raise ValueError("beta and lamb must have the same shape.")

    k = np.array(
        [
            -np.cos(beta) * np.cos(lamb),
            -np.cos(beta) * np.sin(lamb),
            -np.sin(beta) * np.ones_like(lamb),
        ]
    )  # (xyz, loc)
    u = np.array(
        [
            np.ones_like(beta) * np.sin(lamb),
            np.ones_like(beta) * -np.cos(lamb),
            np.zeros_like(beta) * np.zeros_like(lamb),
        ]
    )  # (xyz, loc)
    v = np.array(
        [
            -np.sin(beta) * np.cos(lamb),
            -np.sin(beta) * np.sin(lamb),
            np.cos(beta) * np.ones_like(lamb),
        ]
    )  # (xyz, loc)

    return k.T, u.T, v.T  # (loc, xyz)


def compute_strain2link(
    f: np.ndarray,
    beta: np.ndarray,
    lamb: np.ndarray,
    ltts: np.ndarray,
    positions: np.ndarray,
    *,
    method: str = "baghi+23",
) -> np.ndarray:
    r"""Frequency-domain link response to a GW strain (mixing matrix).

    The response is computed for the linear (plus and cross) polarization basis.
    To use another polarization basis, multiply by the appropriate polarization
    basis transformation matrix.

    Here, ``beta`` and ``lamb`` should be scalars or arrays of the same shape.

    The response for the link :math:`ij` and for a polarization :math:`p` (plus
    or cross), is given by :cite:`Baghi:2023qnq` or :cite:`Hartwig:2023pft`. Use
    the ``method`` argument to select the method to use.

    .. rubric:: Method "baghi+23"

    From :cite:`Baghi:2023qnq`, the single link response is given in the time
    domain by

    .. math::

        y_{ij,p}(t, \vu{k}) = \frac{\xi_p(\vu{k})}{2(1 - \vu{n}_{ij}(t) \vdot
        \vu{k})} \qty[h_p\qty(t - \frac{L_{ij}(t)}{c} - \frac{\vu{k} \vdot
        \vb{x}_j(t)}{c}) - h_p\qty(t - \frac{\vu{k} \vdot \vb{x}_i(t)}{c})],

    where :math:`\vu{k}` is the unit vector pointing towards the source,
    :math:`\vu{n}_{ij}(t)` is the unit vector pointing from spacecraft :math:`j`
    to spacecraft :math:`i`, :math:`\vb{x}_i(t)` is the position of spacecraft
    :math:`i`, :math:`L_{ij}(t)` is the arm length, :math:`h_p` is the strain in
    polarization :math:`p` (plus or cross), at the Solar System Barycenter, and
    :math:`\xi_p(\vu{k})` is the antenna pattern function for polarization
    :math:`p`, given by

    .. math::

        \xi_+ = \qty(\vu{k} \vdot \vu{u})^2 - \qty(\vu{k} \vdot \vu{v})^2,
        \xi_\times = 2 \qty(\vu{k} \vdot \vu{u}) \qty(\vu{k} \vdot \vu{v}).

    Assuming a adiabatically static constellation, the response in the frequency
    domain is given by

    .. math::

        y_{ij,p}(t, f, \vu{k}) = h_p(t, f, \vu{k}) G_{ij,p}(t, f, \vu{k}),

    where :math:`G_{ij,p}(t, f, \vu{k})` is the single-link response kernel,
    which is what this function computes. It is given by

    .. math::

        G_{ij,p}(t, f, \vu{k}) = \frac{\xi_p(\vu{k})}{2(1 - \vu{n}_{ij}(t) \vdot
        \vu{k})} \qty[e^{-i 2\pi f \frac{L_{ij}(t) + \vu{k} \vdot
        \vb{x}_j(t)}{c}} - e^{-i 2\pi f \frac{\vu{k} \vdot \vb{x}_i(t)}{c}}].

    Note that we use here an equivalent factorized form of this kernel, in which
    a sinc function appears, in order to prevent any numerical issues when the
    denominator is close to zero.

    .. rubric:: Method "Hartwig+23"

    Taken from :cite:`Hartwig:2023pft`.

    The final equations 2.15, 2.16 are the sky average of the complex response
    covariance matrix. We compute here only the complex response, and take the
    scalar product and sky average in a second step.

    .. warning::

        There is a sign difference between the two methods, which has not been
        tracked down and corrected for. We therefore multiply the Hartwig+23
        response by -1 to match the Baghi+23 response.

    Args:
        f: Frequency grid [Hz].
        beta: Ecliptic latitude(s) [rad].
        lamb: Ecliptic longitude(s) [rad].
        ltts: Light travel times between the test masses [s], of shape
            ``(t, link)``.
        positions: Test-mass positions [m], of shape ``(t, tm, xyz)``.
        method: Computation method, either "baghi+23" or "hartwig+23".

    Returns:
        Mixing matrix, of shape ``(len(t), len(f), len(beta), 6, 2)``.

        First axis is for time. Second axis is for frequency. The third axis is
        for the source localization, in the order given by the input ``beta``
        and ``lamb``.

        Fourth axis corresponds to the links, in the order 12, 23, 31, 13, 32.
        Fifth axis is for the two polarizations, in the order given by
        :attr:`LINEAR_POLARIZATION`.

        The response is given in (dimensionless) fractional frequency
        deviations (i.e., :math:`\Delta \nu / \nu`).
    """
    if method == "baghi+23":
        return _link_response_baghi23(f, beta, lamb, ltts, positions)
    if method == "hartwig+23":
        return -1 * _link_response_hartwig23(f, beta, lamb, ltts, positions)
    raise ValueError("Method must be either 'baghi+23' or 'Hartwig+23'.")


def _link_response_baghi23(
    f: np.ndarray,
    beta: np.ndarray,
    lamb: np.ndarray,
    ltts: np.ndarray,
    positions: np.ndarray,
) -> np.ndarray:
    """Sky-dependent, frequency-domain link response.

    .. seealso:: :func:`link_response`
    """
    k, u, v = compute_source_basis(beta, lamb)  # (loc, xyz)

    # 6 links ordered as (12, 23, 31, 13, 32, 21)
    # (usual conventions, ij goes from j to i)
    index_emitter = np.array([1, 2, 0, 2, 1, 0])  # (link,)
    index_receiver = np.array([0, 1, 2, 0, 2, 1])  # (link,)
    n = positions[:, index_receiver] - positions[:, index_emitter]  # (t, link, xyz)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)  # (t, link, xyz)

    # Dot products
    delay_link = np.einsum("tij, kj -> tki", n, k)  # (t, loc, link)
    delay_receiver = np.einsum(
        "tij, kj -> tki", positions[:, index_receiver], k
    )  # (t, loc, link)

    # Broadcast delay_receiver over frequencies
    delay_link = delay_link[:, None, :, :]  # (t, f, loc, link)
    delay_receiver = delay_receiver[:, None, :, :]  # (t, f, loc, link)

    # Broadcast f over locations and links
    f = f[:, None, None]  # (f, loc, link)

    # Broadcast ltts over frequencies and locations
    ltts = ltts[:, None, None, :]  # (t, f, loc, link)

    # Compute complex factor
    sinc_arg = f * ltts * (1 - delay_link)  # (t, f, loc, link)
    g = (
        (-1j * np.pi * f * ltts)  # (t, f, loc, link)
        * np.exp(-2j * np.pi * f * delay_receiver / c)  # (t, f, loc, link)
        * np.exp(-1j * np.pi * sinc_arg)  # (t, f, loc, link)
        * np.sinc(sinc_arg)  # (t, f, loc, link)
    )

    # Antenna pattern functions
    xi_plus = (
        np.einsum("tij, kj -> tki", n, u) ** 2 - np.einsum("tij, kj -> tki", n, v) ** 2
    )  # (t, loc, link)
    xi_cross = (
        2 * np.einsum("tij, kj -> tki", n, u) * np.einsum("tij, kj -> tki", n, v)
    )  # (t, loc, link)
    xi = np.stack([xi_plus, xi_cross], axis=-1)  # (t, loc, link, pol)

    return g[..., None] * xi[:, None]  # (t, f, loc, link, pol)


def _link_response_hartwig23(
    f: np.ndarray,
    beta: np.ndarray,
    lamb: np.ndarray,
    ltts: np.ndarray,
    positions: np.ndarray,
) -> np.ndarray:
    """Sky-dependent, frequency-domain link response.

    .. seealso:: :func:`link_response`
    """
    # Define coordinate system
    k, u, v = compute_source_basis(beta, lamb)  # (loc, xyz)
    # Define polarization tensors, eq. 2.10
    e_plus = np.einsum("li, lj -> lij", u, u) - np.einsum(
        "li, lj -> lij", v, v
    )  # (loc, xyz, xyz)
    e_cross = np.einsum("li, lj -> lij", u, v) + np.einsum(
        "li, lj -> lij", v, u
    )  # (loc, xyz, xyz)

    # Spacecraft positions, expressed in seconds
    positions /= c  # (t, sc, xyz)

    # 6 links ordered as (12, 23, 31, 13, 32, 21)
    # (usual conventions, ij goes from j to i)
    index_emitter = np.array([1, 2, 0, 2, 1, 0])  # (link,)
    index_receiver = np.array([0, 1, 2, 0, 2, 1])  # (link,)
    # Define link vectors, below eq. 2.11
    l_ij = positions[:, index_emitter] - positions[:, index_receiver]  # (t, link, xyz)
    n = l_ij / np.linalg.norm(l_ij, axis=-1, keepdims=True)  # (t, link, xyz)

    # Geometric factor, eq. 2.14
    g_plus = np.einsum("tli, tlj, kij -> tkl", n, n, e_plus) / 2  # (t, loc, link)
    g_cross = np.einsum("tli, tlj, kij -> tkl", n, n, e_cross) / 2  # (t, loc, link)

    # Broadcast ltts over frequencies and locations
    ltts = ltts[:, None, None, :]  # (t, f, loc, link)

    # Compute M factor, eq. 2.14
    one_plus_kl = 1 + np.einsum("ki, tli -> tkl", k, n)  #  (t, loc, link)
    m_exp_factor = np.exp(
        np.pi * 1j * ltts * np.einsum("f, tkl -> tfkl", f, one_plus_kl)
    )  # (t, f, loc, link)
    m_sinc = np.sinc(
        ltts * np.einsum("f, tkl -> tfkl", f, one_plus_kl)
    )  # (t, f, loc, link)
    m_factor = m_exp_factor * m_sinc  # (t, f, loc, link)

    # Compute Xi, eq. 2.13
    xi_exp_factor = np.exp(
        -2j * np.pi * np.einsum("f, ki, tli -> tfkl", f, k, l_ij)
    )  # (t, f, loc, link)
    xi_plus = np.einsum(
        "tfkl, tfkl, tkl -> tfkl", xi_exp_factor, m_factor, g_plus
    )  # (t, f, loc, link)
    xi_cross = np.einsum(
        "tfkl, tfkl, tkl -> tfkl", xi_exp_factor, m_factor, g_cross
    )  # (t, f, loc, link)
    xi = np.stack([xi_plus, xi_cross], axis=-1)  # (t, f, loc, link, pol)

    # Broadcast f over locations and links
    f_broadcasted = f[:, None, None]  # (f, loc, link)

    # Add in final exponential factor in eq. 2.16
    # and f^2 pre-factor from eq. 2.15
    final_exp = (
        (2j * np.pi * f_broadcasted * ltts)  # (t, f, loc, link)
        * np.exp(-2j * np.pi * f_broadcasted * ltts)  # (t, f, loc, link)
        * np.exp(
            -2j
            * np.pi
            * np.einsum("f, kx, tlx -> tfkl", f, k, positions[:, index_receiver])
        )  # (t, f, loc, link)
    )  # (t, f, loc, link)

    return final_exp[..., None] * xi  # (t, f, loc, link, pol)


def sky_average(
    cov_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    *,
    nside: int = 12,
    axis: int = 2,
) -> np.ndarray:
    r"""Compute sky average of a covariance matrix.

    The ``cov_func`` argument can be any function that takes :math:`\beta` and
    :math:`\lambda` (sky localization angles, as latitude and longitude) as
    keyword arguments (with keywords `beta` and `lamb`) and returns an
    covariance matrix where ``axis`` corresponds to the sky pixels.

    This function calls ``cov_func`` for an array of pixels of a Healpix grid,
    and then the resulting covariance matrices will be averaged over the sky.

    .. rubric:: Usage

    .. code:: python

        from segwo.cov import project_covariance

        strain_cov = np.eye(2) / 2  # assumed unpolarized strain, shape (pol, pol)
        link2observables = np.array(...)  # shape (f, obs, link)

        def observable_cov(beta, lamb):
            strain2link = compute_strain2link(f, beta, lamb, ltts, positions)
            return project_covariance(strain_cov, [strain2link, link2observables])

        averaged_observable_cov = compute_sky_average(observable_cov)  # (t, f, obs)

    .. warning::

        Make sure to compute the covariance matrices before averaging them over
        the sky, as pixels should be incoherently summed.

    Args:
        cov_func: Callable that returns covariance matrices, taking ``beta`` and
            ``lamb`` as keyword arguments and returning an array.
        nside: Healpix nside parameter (sets sky resolution).
        axis: Axis of the covariance matrix that corresponds to the sky pixels.

    Returns:
        Sky-averaged covariance matrix, of shape matching the output of
        ``cov_func`` but with the ``axis`` dimension removed (averaged over).

        The resulting units are those of the ``cov_func`` output.
    """
    npix = hp.nside2npix(nside)
    thetas, phis = hp.pix2ang(nside, np.arange(npix))
    # Conversion from colatitude to latitude
    betas, lambs = np.pi / 2 - thetas, phis

    response = cov_func(betas, lambs)
    if response.shape[axis] != npix:
        raise ValueError("Covariance matrix does not have the expected shape.")

    return np.sum(response, axis=axis) / npix


def compute_isotropic_signal_cov(
    f: np.ndarray,
    ltts: np.ndarray,
    positions: np.ndarray,
    *,
    nside: int = 12,
    mixings: None | np.ndarray | list[np.ndarray] = None,
    method: str = "baghi+23",
    strain_cov: np.ndarray | None = None,
) -> np.ndarray:
    r"""Compute signal covariance from an isotropic background [1/Hz].

    This function returns the covariance matrix of a signal for a given set of
    observables computed from an isotropic stochastic gravitational-wave
    background in units of fractional frequency deviation (ie., :math:`\Delta
    \nu / \nu`) spectral power density.

    It is obtained by projecting the strain covariance matrix ``strain_cov``
    (expressed in the plus-cross polarization basis) onto the chosen observables
    (defined by the mixing matrices ``mixings`` going from single linkes to the
    chosen set of observables), using the sky position-dependent link responses;
    then, these covariance matrices are averaged over the sky using the Healpix
    pixelization of the sky.

    .. rubric:: Usage

    .. code:: python

        from segwo.response import compute_isotropic_signal_cov

        f = np.array(...)  # frequency grid [Hz]
        ltts = np.array(...)  # light travel times [s]
        positions = np.array(...)  # test-mass positions [m]

        mixing1 = np.array(...)  # mixing matrix 1
        mixing2 = np.array(...)  # mixing matrix 2

        response = compute_isotropic_signal_cov(
            f,
            ltts,
            positions,
            mixings=[mixing1, mixing2],
        )

    .. admonition:: Detector response

        By default, this function uses a normalized and unpolarized (i.e.,
        diagonal) strain covariance matrix. As a consequence, the covariance
        matrix returned by this function can be interpreted as the incoherent
        sum of the detector response for both polarizations. In this case, the
        units are fractional frequency deviation power spectral density (the
        signal) divided by the strain power spectral density (here equal to 1).

        The covariance matrix can be directly used as input to the sensitivity
        computation :func:`compute_sensitivity_from_covariances`.

    .. seealso:: :func:`segwo.response.strain2link`,
        :func:`segwo.response.sky_average`,
        :func:`segwo.sensitivity.compute_sensitivity_from_covariances`

    Parameters
    ----------
    f : Array of shape (Nf,)
        Frequency grid [Hz].
    ltts : Array of shape (Nt, link=6)
        Light travel times between the test masses [s].
    positions : Array of shape (Nt, sc=3, xyz=3)
        Test-mass positions [m].
    nside : int
        Healpix nside parameter (sets sky resolution).
    mixings : None, array, or list of arrays
        Mixing matrices transforming from single links to the desired set of
        observables.

        If None, the function will return the sky-averaged signal covariance at
        for single links.

        If a single array, it should be broadcastable to ``(Nt, Nf, Nobs,
        link=6)``, where ``Nobs`` is the number of observables. If a list of
        arrays, they should be of compatible shapes, such that the overall
        mixing matrix has the shape mentioned above (see
        :func:`segwo.cov.compose_mixings`).
    method : str
        Computation method, either "baghi+23" or "hartwig+23".

        See :func:`compute_strain2link` for more details.
    strain_cov : Array of shape (Npol=2, Npol=2)
        Strain covariance matrix.

        If None, the function will use a normalized and unpolarized strain
        (diagonal) covariance matrix.

    Returns
    -------
    np.ndarray of shape (Nt, Nf, Nobs, Nobs)
        Sky-averaged signal covariance matrix.

        Units are fractional frequency deviation power spectral density [1/Hz].
    """
    # By default, use a normalized, unpolarized strain covariance matrix
    if strain_cov is None:
        strain_cov = np.eye(2) / 2  # (pol, pol)

    # Make sure we have a list of mixings
    if mixings is None:
        mixings = []
    if isinstance(mixings, np.ndarray):
        mixings = [mixings]
    # Insert an extra dimansion in the mixing matrices for sky locations
    mixings = [mixing[..., None, :, :] for mixing in mixings]

    # Compute the response covariance for a specific sky location
    def obs_cov(beta, lamb) -> np.ndarray:
        strain2link = compute_strain2link(
            f, beta, lamb, ltts, positions, method=method
        )  # (t, f, loc, obs, obs)
        strain2obs = [strain2link] + mixings  # (t, f, loc, obs, obs)
        return project_covariance(strain_cov, strain2obs)  # (t, f, loc, obs, obs)

    # Average over the sky
    averaged_obs_cov = sky_average(obs_cov, nside=nside, axis=2)  # (t, f, obs, obs)
    return averaged_obs_cov  # (t, f, obs, obs)
