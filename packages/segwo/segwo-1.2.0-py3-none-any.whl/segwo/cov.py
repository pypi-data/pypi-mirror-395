r"""
Covariance matrices
===================

SEGWO provides a set of convenient functions to define frequency-domain
covariance matrices. Covariance matrices capture statistical properties of (at
least locally) stationary, potentially correlated processes.

Mixing matrices define the linear transformation between a set of observables
to another set of observables. They are used to project measurements or
covariance matrices from one set of observables to another.

Building covariance matrices
----------------------------

In our case, these processes are often noises, but they can also be
gravitational-wave signals. A covariance matrix :math:`\mathbf{C}` then
describes how theses noises (or signals) appear in a given set of observables
(e.g., a set of measurements). For a set of :math:`N` observables :math:`y_i`,
the covariance matrix is a :math:`N \times N` matrix.

Entries :math:`\mathbf{C}_{ii}` on the diagonal of a covariance matrix
correspond to the real-valued power spectral density (PSD) of the process in
each observable :math:`i`. Off-diagonal entries :math:`\mathbf{C}_{ij}`
correspond to the complex-valued cross-spectral density (CSD) between
observables :math:`i` and :math:`j`. Note that covariance matrices are always
Hermitian and positive-definite, such that :math:`\mathbf{C}_{ij} =
\mathbf{C}_{ji}^*`.

As mentioned above, SEGWO works in the frequency domain, under the assumption of
local stationarity. That means that covariance matrices are time _and_ frequency
dependent. Users are expected to define a time grid (with :math:`N_t` time
steps) and a frequency grid (with :math:`N_f` frequency steps).

The resulting covariance matrix is then a 4D Numpy array of shape :math:`(N_t,
N_f, N, N)`, where the first two dimensions are used for time and frequency, and
the last two dimensions are used for the observables.

One way to build a covariance matrix for a set of uncorrelated observables is
to provide a list of PSD values for each observable. The covariance matrix can
be built by calling :func:`construct_covariance_from_psds`, and will be
a diagonal matrix with the PSD values on the diagonal.

.. code:: python

    import numpy as np
    from segwo.cov import construct_covariance_from_psds

    # Frequency grid
    f = np.logspace(...)  # [Hz]

    # Define a list of PSDs for each observable
    psd1 = 1e-20 * (1 + (2e-3 / f) ** 4)  # Example PSD
    psd2 = 1e-15 * 2 * np.pi * f * (1 + (f / 8e-3) ** 4)  # Example PSD
    psd3 = 1e-20 * (1 + (2e-3 / f) ** 4)  # Example PSD

    # Build the covariance matrix
    noise_cov = construct_covariance_from_psds([psd1, psd2, psd3])


You can also concatenate existing covariance matrices into a single covariance
matrix. This is useful when you have a set of covariance matrices for different,
uncorrelated observables, and you want to combine them as a block-diagonal
matrix. You can use the :func:`concatenate_covariances` function to do this.


.. autofunction:: construct_covariance_from_psds

.. autofunction:: construct_covariance_from_measurements

.. autofunction:: concatenate_covariances

Building mixing matrices
------------------------

Mixing matrices define the linear transformation between a set of :math:`M`
observables to another set of :math:`N` observables. They are defined in the
frequency domain as :math:`N \times M` complex-valued matrices under the
assumption of local stationarity.

As a consequence, they are also time- and frequency-dependent. The mixing
matrices are defined for each time step and frequency step, and the resulting
mixing matrix is a 4D Numpy array of shape :math:`(N_t, N_f, N, M)`, where the
first two dimensions are used for time and frequency, and the last two
dimensions are used for the observables.

One way to build a mixing matrix is to provide a list of TDI combinations
defining the transfer functions for each observable. The TDI combinations are
defined as a dictionary of the form ``{measurement: [(scaling_factor, [delays]),
...]}``, where the measurement is the input observable, the scaling factor is a
complex number, and the delays are lists of delays/advancements to be applied to
the measurement. The mixing matrix can be built by calling
:func:`construct_mixing_from_pytdi`.

.. code:: python

    from segwo.cov import construct_mixing_from_pytdi
    import numpy as np
    import pytdi

    # Frequency grid
    f = np.logspace(...)  # [Hz]

    # Define a list of TDI combinations for each observable
    tdi_combinations = [
        pytdi.TDICombination(
            "eta_31", [(-1, ["A_21", "D_13"]), (1, ["D_21", "D_13"])],
            "eta_13", [(-1, ["A_21"]), (1, ["D_21"])],
        ),
        pytdi.TDICombination(
            "eta_13", [(-1, ["A_21"]), (1, ["D_21"])],
            "eta_12", [(1, ["A_21"])],
            "eta_21", [(1, [])],
        ),
        pytdi.TDICombination(
            "eta_21", [(1, [])],
            "eta_12", [(1, ["A_21"])],
        ),
    ]

    # Define the list of ordered original measurements
    measurements = ["eta_31", "eta_13", "eta_21", "eta_12"]

    # Define a list of light travel times for each link at each time point
    ltts = np.array(...) #  shape (t, link)

    # Build the mixing matrix
    mixing = construct_mixing_from_pytdi(
        f, measurements, tdi_combinations, ltts
    )

You can also compose a sequence of mixing matrices into a single mixing matrix,
to represent a sequence of transformations, with :func:`compose_mixings`. This
is useful when you have a set of mixing matrices for different observables and
you want to represent them as a single transformation to go from the first set
of observables to the last set.

.. autofunction:: construct_mixing_from_pytdi

.. autofunction:: compose_mixings

.. autofunction:: concatenate_mixings

Projecting measurements
-----------------------

.. autofunction:: project_measurements

.. autofunction:: project_covariance

"""

from typing import TypeAlias

import numpy as np
import pytdi
from numpy.typing import DTypeLike


def compose_mixings(mixings: list[np.ndarray]) -> np.ndarray:
    r"""Compose a sequence of mixing matrices into a single mixing matrix.

    This function takes a sequence of N mixing matrices :math:`\mathbf{M}^i`
    and composes them into a single mixing matrix
    :math:`\mathbf{M}`, such that the first mixing matrix in the sequence is
    applied first. Ie., we construct the matrix product

    .. math::

        \mathbf{M} = \mathbf{M}^{N-1}
        \mathbf{M}^{N-2} \ldots \mathbf{M}^0.

    Args:
        mixings: List of N mixing matrices, of compatible successive shapes. The
            i-th mixing matrice should have shape ``(..., M[i+1], M[i])``.

    Returns:
        Composed mixing matrix, of shape ``(..., M[N], M[0])``.

        Units are the product of the units of the input mixing matrices.
    """
    # Check we have at least one mixing matrix
    if not mixings:
        raise ValueError("mixings must be a non-empty list.")

    # If we have only one mixing matrix, return it
    if len(mixings) == 1:
        return mixings[0]

    # Recursively compose the mixing matrices
    mixing_new = mixings[-1]  # (..., M[N], M[N-1))
    mixing_recursed = compose_mixings(mixings[:-1])  # (..., M[N-1], M[0])

    return np.einsum(
        "...ij, ...jk -> ...ik", mixing_new, mixing_recursed
    )  # (..., M[N], M[0])


def concatenate_mixings(
    mixings: list[np.ndarray], *, dtype: DTypeLike | None = None
) -> np.ndarray:
    r"""Concatenate a sequence of mixing matrices into a single mixing matrix.

    This function takes a sequence of N mixing matrices :math:`\mathbf{M}^i` and
    concatenates them along the last 2 axes into a single mixing matrix
    :math:`\mathbf{M}`. We assume the observables across mixing matrices are
    uncorrelated; therefore, we effectively form the block-diagonal mixing
    matrix

    .. math::

        \mathbf{M} = \begin{pmatrix}
            \mathbf{M}^{0} & & & \\
            & \mathbf{M}^{1} & & \\
            & & \ddots & \\
            & & & \mathbf{M}^{N-1}
        \end{pmatrix}.

    .. rubric:: Usage

    .. code:: python

        mixing1 = np.array(...)
        mixing2 = np.array(...)

        concatenated_mixing = concatenate_mixings([mixing1, mixing2])

    Args:
        mixings:
            List of N mixing matrices, of shapes ``(..., N[i], N[i])``, where
            ``N[i]`` is the number of observables in the i-th mixing matrix. The
            first dimensions are traditionally used for time and frequency, and
            should be broadcastable across the mixing matrices.
        dtype:
            Data type of the output mixing matrix. If not provided, the data
            type of the first mixing matrix is used.

    Returns:
        Concatenated mixing matrix, of shape ``(..., N, N)``, where ``N`` is the
        total number of observables across all mixing matrices. The first
        dimensions are traditionally used for time and frequency, and are kept
        in the output.

        Units of each mixing matrix remain the same.
    """
    # Check we have at least one mixing matrix
    if not mixings:
        return np.empty((0, 0), dtype=float)
    assert len(mixings) > 0

    # Use the data type of the first mixing matrix if not provided
    if dtype is None:
        dtype = mixings[0].dtype

    # Form the block-diagonal mixing matrix
    total_size = sum(mixing.shape[-1] for mixing in mixings)
    first_dimensions = [mixing.shape[:-2] for mixing in mixings]
    broadcasted_first_dimensions = np.broadcast_shapes(*first_dimensions)
    result = np.zeros(
        (*broadcasted_first_dimensions, total_size, total_size),
        dtype=dtype,
    )

    # Fill the block-diagonal mixing matrix
    current_index = 0
    for mixing in mixings:
        size = mixing.shape[-1]
        end_index = current_index + size
        result[..., current_index:end_index, current_index:end_index] = mixing
        current_index = end_index

    # Check that we filled the entire matrix
    if current_index != total_size:
        raise ValueError(
            "Not all mixing matrices were filled in the block-diagonal matrix."
        )

    return result  # (..., N, N)


def construct_mixing_from_pytdi(
    f: np.ndarray,
    measurements: list[str],
    tdi_combinations: (
        list[pytdi.TDICombination] | list[list[pytdi.TDICombination]]
    ),  # (tdi,) or (t, tdi)
    ltts: np.ndarray,
) -> np.ndarray:
    r"""Construct the mixing matrix from a list of TDI combinations.

    This function calls :func:`_construct_mixing_vector_from_pytdi_components`,
    but handles multiple TDI combinations at each time point. It also extracts
    the TDI components from the TDI combinations.

    Typical use case would be to pass a set of combinations, for example, X, Y,
    Z, at each time point.

    Args:
        f:
            Frequency array [Hz].
        measurements:
            Ordered list of measurements.
        tdi_combinations:
            List of TDI combinations for one time point, or list of lists of TDI
            combinations.
        ltts:
            Light travel times for each link at each time point, of shape
            ``(t, link)``.

    Returns:
        The constructed mixing matrix with shape ``(t, f, tdi, measurements)``.
    """
    # Check that `tdi_combinations` is an homogeneous list
    if not all(isinstance(tc, list) for tc in tdi_combinations) and not all(
        isinstance(tc, pytdi.TDICombination) for tc in tdi_combinations
    ):
        raise ValueError(
            "All elements of tdi_combinations must be lists "
            "or TDICombination objects."
        )
    # If this is a list of TDICombination objects, we need to convert it
    # to a list of lists
    if isinstance(tdi_combinations[0], pytdi.TDICombination):
        tdi_combinations = [tdi_combinations] * ltts.shape[0]
    # Else, check that every element is a list of TDICombination objects
    else:
        for tdi_combination in tdi_combinations:
            if not all(isinstance(tc, pytdi.TDICombination) for tc in tdi_combination):
                raise ValueError(
                    "All elements of tdi_combinations must be lists "
                    "of TDICombination objects."
                )

    # Extract components from TDI combinations
    components = [
        [combination.components for combination in timestep]
        for timestep in tdi_combinations
    ]

    # Stack the results to get a final shape (t, f, tdi, measurements)
    results = []
    for i in range(len(components[0])):
        # Extract the i-th slice of shape (t,)
        slice_input = [components[j][i] for j in range(len(components))]

        result = _construct_mixing_vector_from_pytdi_components(
            f, measurements, slice_input, ltts
        )

        # Store the result
        results.append(result)

    # Stack along the tdi axis
    return np.stack(results, axis=2)


# pylint: disable=invalid-name
PyTDIComponent: TypeAlias = dict[str, list[tuple[float, list[str]]]]
# pylint: enable=invalid-name


def _construct_mixing_vector_from_pytdi_components(
    f: np.ndarray,
    measurements: list[str],
    tdi_components: PyTDIComponent | list[PyTDIComponent],
    ltts: np.ndarray,
) -> np.ndarray:
    r"""Construct mixing vector for a single time-dependent TDI observable.

    PyTDI defines TDI combinations as a dictionary of the form

    .. code-block:: python

        {
            'eta_31': [(-1, ['A_21', 'D_13']), (1, ['D_21', 'D_13'])],
            'eta_13': [(-1, ['A_21']), (1, ['D_21'])],
            'eta_21': [(1, [])],
            'eta_12': [(1, ['A_21'])],
        }

    where the item labels denote the measurement to be delayed and the values
    are lists of touples of scaling factors and accompanying delays/advancements
    to be applied to the measurement.

    Assuming delays to be constant, we can convert the list of delays into
    Fourier domain exponential factors.

    Advancement operators satisfy ``D_ij A_ji = 1``, such that the value of each
    advancement is computed as ``a_ji = -d_ij``.

    The corresponding Fourier domain factors are then given as

    .. math::

        \mathrm{FT}[\mathbf{D}_{ij} x] &= e^{- 2 \pi f d_{ij}(t)} \mathrm{FT}[x],

        \mathrm{FT}[\mathbf{A}_{ij} x] &= e^{2 \pi f d_{ji}(t)} \mathrm{FT}[x].

    Parameters:
        f:
            Frequency array [Hz].
        measurements:
            Ordered list of measurements.
        tdi_components:
            Dictionary containing delays for measurement
            (e.g., 'eta_21': [(-1, ['D_12']), (1, ['D_13', 'D_31', 'D_12'])]),
            or list of such dictionaries for each time point in ``ltts``.
        ltts:
            Light travel times for each link at each time point, of shape
            ``(t, link)``.

    Returns:
        The constructed mixing vector with shape ``(t, f, measurements)``.
    """
    if ltts.ndim != 2:
        raise ValueError("ltts must be a 2D array of shape (t, link).")
    if ltts.shape[1] != 6:
        raise ValueError("ltts must have 6 columns, one for each link.")

    delays = ltts  # (t, link)
    links = [12, 23, 31, 13, 32, 21]  # (link,)
    # Index order is 12, 23, 31, 13, 32, 21,
    # ie., advancements simply flip the array
    advancements = np.flip(delays, axis=-1)  # (t, link)

    # Convert tdi_components to a list of dictionaries
    if not isinstance(tdi_components, list):
        tdi_components = [tdi_components] * delays.shape[0]
    if len(tdi_components) != delays.shape[0]:
        raise ValueError("Length of tdi_components must match length of delays.")

    def compute_exponentials(delay_list: list[str], t_index: int) -> np.ndarray:
        """Compute frequency domain factor corresponding to list of delays.

        Args:
            delay_list: List of delays and advancements for a specific
                measurement at a specific time point (index ``t_index``).
            t_index: Index of the time point.

        Returns:
            Frequency domain factor as a complex array of shape
            ``(len(f))``.
        """
        result = np.ones(len(f), dtype=complex)  # (f,)
        for item in delay_list:
            if item[0] == "A":
                result *= np.exp(
                    1j
                    * 2
                    * np.pi
                    * f  # (f,)
                    * advancements[t_index, links.index(int(item[2:]))]
                )
            elif item[0] == "D":
                result *= np.exp(
                    -1j
                    * 2
                    * np.pi
                    * f  # (f,)
                    * delays[t_index, links.index(int(item[2:]))]
                )
            else:
                raise ValueError(f"Invalid delay list entry: {item}")

        return result  # (f,)

    def build_factor_from_component(measurement: str, t_index: int) -> np.ndarray:
        """Computes frequency domain factor for given measurement.

        Args:
            measurement: Measurement label.
            t_index: Index of the time point.

        Returns:
            Frequency domain factor as a complex array of shape
            ``(len(f))``.
        """
        result = np.zeros(len(f), dtype=complex)  # (f,)
        for item in tdi_components[t_index][measurement]:
            result += item[0] * compute_exponentials(item[1], t_index)  # (f,)

        return result  # (f,)

    final = np.zeros((delays.shape[0], len(f), len(measurements)), dtype=complex)

    for t_index, t_tdi_components in enumerate(tdi_components):
        for meas_index, measurement in enumerate(measurements):
            if measurement in t_tdi_components:
                final[t_index, :, meas_index] = build_factor_from_component(
                    measurement, t_index
                )  # (f,)

    return final  # (t, f, measurements)


def project_measurements(x: np.ndarray, mixing: np.ndarray) -> np.ndarray:
    r"""Transform measurements to a new set of observables using a mixing matrix.

    This is a convenience function to apply a mixing matrix to a set of
    observables :math:`\mathbf{x}_j`, with shape ``(..., M)``. First axis are
    traditionally used for time and frequency, and are kept in the output.

    The mixing matrix :math:`\mathbf{M}` is always applied to the last
    dimension of the input array. The mixing matrix must be of shape ``(..., N,
    M)``.

    .. math::

        \mathbf{y}_{i} = \mathbf{M}_{ij} \mathbf{x}_{j}.

    Args:
        x: Array of observables, of shape ``(..., M)``.
        mixing: Mixing matrix, of shape ``(..., N, M)``.

    Returns:
        Projected observables, of shape ``(..., N)``.

        Units are the product of the units of ``x`` and ``mixing``.
    """
    # Number of dimensions for x and mixing
    if x.ndim < 1:
        raise ValueError("x must have at least 1 dimension.")
    if mixing.ndim < 2:
        raise ValueError("mixing must have at least 2 dimensions.")

    return np.einsum("...ij, ...j -> ...i", mixing, x)  # (..., meas)


def construct_covariance_from_measurements(x: np.ndarray) -> np.ndarray:
    r"""Compute covariance matrices from a vector of measurements.

    The input vector is an array of measurements :math:`\mathbf{x}_{i}`, with
    shape ``(..., N)``. The last dimension is reserved for the measurements, and
    additional first dimensions (traditionally for time and frequency) are kept
    in the output.

    The covariance matrix :math:`\mathbf{C}^{\mathbf{x}}_{ij}` is computed by
    taking the outer product of the measurement vector with its complex
    conjugate on the last dimension,

    .. math::

        \mathbf{C}^{\mathbf{x}}_{ij} = \mathbf{x}_{i}
        \mathbf{x}_{j}^{*}.

    .. warning::

        Adding covariance matrices is not equivalent to computing the covariance
        matrix of the summed measurement vectors. Only add covariance matrices
        for quantities that are statistically independent.

    Args:
        x: Array of measurements, of shape ``(..., N)``.

    Returns:
        Covariance matrix, of shape ``(..., N, N)``, with ``N`` the last
        dimension of ``x``. Additional dimensions are kept.

        Units are those of ``x``, squared.
    """
    # Check that x has at least 2 dimensions
    if x.ndim < 1:
        raise ValueError(f"x must have at least 1 dimensions, got {x.ndim}.")

    return np.einsum("...i, ...j -> ...ij", x, np.conj(x))  # (..., meas, meas)


def construct_covariance_from_psds(psds: list[np.ndarray]) -> np.ndarray:
    r"""Construct covariance matrix from a list of power spectral densities.

    This function takes a list of frequency-dependent PSDs :math:`S_i(f)` for
    each observable of interest :math:`i` and constructs the associated mixing
    matrix :math:`\mathbf{C}(f)`. The observables are assumed to be
    uncorrelated, such at the covariance matrix is diagonal.

    .. math::

        \mathbf{C}^{\mathbf{x}}_{ij}(f) = \mathbf{S}_i(f) \delta_{ij}.

    .. rubric:: Usage

    .. code:: python

        f = np.array(...)  # Frequency array [Hz]
        psd1 = 1e-20 * (1 + (2e-3 / f) ** 4) # Example PSD
        psd2 = 1e-15 * 2 * np.pi * f * (1 + (f / 8e-3) ** 4) # Example PSD

        noise_cov = construct_covariance_from_psds([psd1, psd2])

    Args:
        psds:
            List of N PSDs, each as an array of shape ``(..., f)``. The first
            dimensions are traditionally used for time and frequency, and are
            kept in the output. The last dimension is reserved for the

    Returns:
        Mixing matrix, of shape ``(t, f, obs, obs)``.

        Units are the product of the units of ``psds``.
    """
    # Turn PSD arrays into single-observable covariance matrices
    covs = [psd[..., None, None] for psd in psds]
    return concatenate_covariances(covs)


def concatenate_covariances(
    covs: list[np.ndarray], *, dtype: DTypeLike | None = None
) -> np.ndarray:
    r"""Concatenate covariance matrices into a single covariance matrix.

    This function takes a sequence of N covariance matrices :math:`\mathbf{C}^i` and
    concatenates them along the last 2 axes into a single covariance matrix
    :math:`\mathbf{C}`. We assume the observables across covariance matrices are
    uncorrelated; therefore, we effectively form the block-diagonal covariance
    matrix

    .. math::

        \mathbf{C} = \begin{pmatrix}
            \mathbf{C}^{0} & & & \\
            & \mathbf{C}^{1} & & \\
            & & \ddots & \\
            & & & \mathbf{C}^{N-1}
        \end{pmatrix}.

    .. rubric:: Usage

    .. code:: python

        cov1 = np.array(...)
        cov2 = np.array(...)

        concatenated_cov = concatenate_covariances([cov1, cov2])

    Args:
        covs:
            List of N covariance matrices, of shapes ``(..., N[i], N[i])``,
            where ``N[i]`` is the number of observables in the i-th covariance
            matrix. The first dimensions are traditionally used for time and
            frequency, and should be broadcastable across the covariance
            matrices.
        dtype:
            Data type of the output covariance matrix. If not provided, the data
            type of the first covariance matrix is used.

    Returns:
        Concatenated covariance matrix, of shape ``(..., N, N)``, where ``N`` is
        the total number of observables across all covariance matrices. The
        first dimensions are traditionally used for time and frequency, and are
        kept in the output.

        Units of each covariance matrix remain the same.
    """
    # Check we have at least one covariance matrix
    if not covs:
        return np.empty((0, 0), dtype=float)
    assert len(covs) > 0

    # Use the data type of the first covariance matrix if not provided
    if dtype is None:
        dtype = covs[0].dtype

    # Form the block-diagonal covariance matrix
    total_size = sum(mixing.shape[-1] for mixing in covs)
    first_dimensions = [mixing.shape[:-2] for mixing in covs]
    broadcasted_first_dimensions = np.broadcast_shapes(*first_dimensions)
    result = np.zeros(
        (*broadcasted_first_dimensions, total_size, total_size),
        dtype=dtype,
    )

    # Fill the block-diagonal covariance matrix
    current_index = 0
    for cov in covs:
        size = cov.shape[-1]
        end_index = current_index + size
        result[..., current_index:end_index, current_index:end_index] = cov
        current_index = end_index

    # Check that we filled the entire matrix
    if current_index != total_size:
        raise ValueError(
            "Not all covariance matrices were filled in the block-diagonal matrix."
        )

    return result  # (..., N, N)


def project_covariance(
    cov: np.ndarray, mixings: np.ndarray | list[np.ndarray]
) -> np.ndarray:
    r"""Transform covariance to a new set of observables using mixing matrices.

    This is a convenience function to apply a mixing matrix to a covariance
    :math:`\mathbf{C}^{\mathbf{x}}_{ij}`, associated with a set of observables
    :math:`\mathbf{x}` and of shape ``(..., M, M)``. The mixing matrix is
    applied to the 2 last dimensions of the input covariance matrix. Additional
    axes can be present (traditionally for time and frequency) and are kept in
    the output.

    The result is a new covariance matrix
    :math:`\mathbf{C}^{\mathbf{y}}_{ij}` for a new set of observables
    :math:`\mathbf{y}`, with shape ``(..., N, N)``,

    .. math::

        \mathbf{C}^{\mathbf{y}}_{ij} = \mathbf{M}_{ik}
        \mathbf{C}^{\mathbf{x}}_{kl} \mathbf{M}_{jl}^{*}.

    The mixing matrix :math:`\mathbf{M}` is defined by

    .. math::

        \mathbf{y}_{i} = \mathbf{M}_{ij} \mathbf{x}_{j}.

    The mixing matrix must be of shape ``(..., N, M)``.

    You can use a list of successive mixing matrices. In this case, this
    function first computes the overall mixing matrix by calling
    :func:`compose_mixings`, and then apply it to the covarance matrix.

    .. seealso:: :func:`compose_mixings`

    Args:
        cov: Input ovariance matrix, of shape ``(..., M, M)``.
        mixings: A single mixing matrix, or a list of N mixing matrices. If a
            single array, it should be of shape ``(..., N, M)``. If a
            list of arrays, they should be of compatible shapes, such that the
            overall mixing matrix has the shape mentioned above.

    Returns:
        Projected covariance matrix, of shape ``(..., N, N)``.

        Units are the product of the units of ``cov`` and square of ``mixing``.
    """
    # If no mixing matrix is given, return the input covariance matrix
    if isinstance(mixings, list) and not mixings:
        return cov

    # Compute overall mixing matrix in case of a list
    if isinstance(mixings, list):
        mixings = compose_mixings(mixings)
    assert isinstance(mixings, np.ndarray)

    # Number of dimensions for cov and mixing
    if cov.ndim < 2:
        raise ValueError("cov must have at least 2 dimensions.")
    if mixings.ndim < 2:
        raise ValueError("mixing must have at least 2 dimensions.")

    return np.einsum(
        "...ij, ...jk, ...lk -> ...il", mixings, cov, np.conj(mixings)
    )  # (..., meas, meas)
